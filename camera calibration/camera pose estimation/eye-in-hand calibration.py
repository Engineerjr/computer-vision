import numpy as np
import cv2

from scipy.spatial.transform import Rotation


# ==========================================
# 1. Transformation Utilities
# ==========================================

def create_transform(R, t):

    T = np.eye(4)

    T[:3, :3] = R
    T[:3, 3] = t.reshape(3)

    return T


def invert_transform(T):

    R = T[:3, :3]
    t = T[:3, 3]

    T_inv = np.eye(4)

    T_inv[:3, :3] = R.T
    T_inv[:3, 3] = -R.T @ t

    return T_inv


# ==========================================
# 2. Generate Random Robot Motions
# ==========================================

def generate_random_transform():

    rot = Rotation.random()

    R = rot.as_matrix()

    t = np.random.uniform(-0.3, 0.3, 3)

    return create_transform(R, t)


# ==========================================
# 3. Ground Truth Camera-to-Gripper
# ==========================================

np.random.seed(42)

R_true = Rotation.from_euler(
    'xyz', [20, 10, 30], degrees=True
).as_matrix()

t_true = np.array([0.08, 0.04, 0.12])

X_true = create_transform(R_true, t_true)


# ==========================================
# 4. Generate Robot and Camera Poses
# ==========================================

N = 15

robot_poses = []

camera_poses = []

# Fixed calibration target relative to robot base
T_base_target = generate_random_transform()

for i in range(N):

    # Robot gripper pose relative to robot base
    T_base_gripper = generate_random_transform()

    # Camera pose relative to calibration target
    #
    # T_gripper_camera = X_true
    #
    # T_base_target * T_target_camera
    # = T_base_gripper * X_true

    T_target_camera = (
        invert_transform(T_base_target)
        @ T_base_gripper
        @ X_true
    )

    robot_poses.append(T_base_gripper)

    camera_poses.append(T_target_camera)


# ==========================================
# 5. Convert Poses into OpenCV Inputs
# ==========================================

R_gripper2base = []
t_gripper2base = []

R_target2cam = []
t_target2cam = []

for Tg, Tc in zip(robot_poses, camera_poses):

    R_gripper2base.append(Tg[:3, :3])
    t_gripper2base.append(Tg[:3, 3].reshape(3, 1))

    R_target2cam.append(Tc[:3, :3])
    t_target2cam.append(Tc[:3, 3].reshape(3, 1))


# ==========================================
# 6. Solve Hand-Eye Calibration
# ==========================================

R_est, t_est = cv2.calibrateHandEye(

    R_gripper2base,
    t_gripper2base,

    R_target2cam,
    t_target2cam,

    method=cv2.CALIB_HAND_EYE_PARK

)


X_est = create_transform(R_est, t_est)


# ==========================================
# 7. Display Results
# ==========================================

print("\nGround Truth Transformation X:")
print(X_true)

print("\nEstimated Transformation X:")
print(X_est)


# ==========================================
# 8. Calculate Calibration Errors
# ==========================================

R_error = R_true.T @ R_est

rotation_error = np.degrees(
    Rotation.from_matrix(R_error).magnitude()
)

translation_error = np.linalg.norm(
    t_true - t_est.flatten()
)

print("\n========== CALIBRATION ERRORS ==========")

print("Rotation Error:", rotation_error, "degrees")

print("Translation Error:", translation_error, "meters")