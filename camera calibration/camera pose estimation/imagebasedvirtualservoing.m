% =========================================================================
% Image-Based Visual Servoing (IBVS) Simulation in MATLAB
% =========================================================================
clear; clc; close all;

% 1. Camera Intrinsic Parameters (Pinhole Camera Model)
cameraParams = cameraIntrinsics([500, 500], [320, 240], [640, 480]);

% 2. Define Target Points in 3D Space (e.g., 4 corners of a square)
% World coordinates (X, Y, Z) in meters
target_XYZ = [
    -0.1, -0.1, 1.0;
     0.1, -0.1, 1.0;
     0.1,  0.1, 1.0;
    -0.1,  0.1, 1.0
];

% 3. Define Desired Feature Points in the Image Plane (Desired Pixels [u, v])
desired_uv = [
    270, 190;
    370, 190;
    370, 290;
    270, 290
];

% 4. Initial Camera Pose (Transformation from World to Camera Frame)
cameraPose = rigidtform3d(eul2rotm([0, 0, 0]), [0.05, 0.05, 0.2]);

% Control Parameters
lambda = 0.5;      % Gain parameter for control loop
dt = 0.05;         % Time step
max_iterations = 150;

figure('Name', 'Visual Servoing Simulation', 'Position', [100, 100, 800, 400]);

for i = 1:max_iterations
    % --- Step A: Project 3D points onto the current camera image plane ---
    current_uv = worldToImage(cameraParams, cameraPose, target_XYZ);
    
    % --- Step B: Compute Error ---
    error_pixels = desired_uv - current_uv;
    error_vector = error_pixels(:); % Vectorize error (8x1 for 4 points)
    
    % Check convergence
    if norm(error_vector) < 1.0
        fprintf('Visual servoing converged at iteration %d.\n', i);
        break;
    end
    
    % --- Step C: Compute Interaction Matrix (Image Jacobian) for each point ---
    num_points = size(target_XYZ, 1);
    L = zeros(2 * num_points, 6);
    
    fx = cameraParams.FocalLength(1);
    fy = cameraParams.FocalLength(2);
    cx = cameraParams.PrincipalPoint(1);
    cy = cameraParams.PrincipalPoint(2);
    
    for j = 1:num_points
        % Get current pixel coordinates
        u = current_uv(j, 1);
        v = current_uv(j, 2);
        
        % Estimate depth Z in camera frame for point j
        pt_cam = transformPointsInverse(cameraPose, target_XYZ(j, :));
        Z = pt_cam(3);
        
        % Normalize pixel coordinates manually using intrinsics
        x = (u - cx) / fx;
        y = (v - cy) / fy;
        
        % Interaction matrix block for a single point (2x6)
        L(2*j-1:2*j, :) = [
            -1/Z,  0,    x/Z,   x*y,     -(1 + x^2),  y;
             0,   -1/Z,  y/Z,   1 + y^2, -x*y,       -x
        ];
    end
    
    % --- Step D: Compute Camera Velocity Control Law ---
    v_camera = -lambda * pinv(L) * error_vector;
    
    % --- Step E: Update Camera Pose ---
    linear_vel = v_camera(1:3);
    angular_vel = v_camera(4:6);
    
    delta_trans = linear_vel * dt;
    delta_rot = axang2rotm([angular_vel'/norm(angular_vel), norm(angular_vel)*dt]);
    
    delta_pose = rigidtform3d(delta_rot, delta_trans');
    
    % Compose transformation using the .A property matrices
    cameraPose = rigidtform3d(cameraPose.A * delta_pose.A);
    
    % --- Step F: Visualization ---
    subplot(1, 2, 1);
    plot(current_uv(:,1), current_uv(:,2), 'ro', 'MarkerSize', 8, 'LineWidth', 2);
    hold on;
    plot(desired_uv(:,1), desired_uv(:,2), 'gx', 'MarkerSize', 8, 'LineWidth', 2);
    xlim([0, cameraParams.ImageSize(2)]);
    ylim([0, cameraParams.ImageSize(1)]);
    set(gca, 'YDir', 'reverse');
    legend('Current Features', 'Desired Features', 'Location', 'southeast');
    title(sprintf('Image Plane (Iter: %d)', i));
    xlabel('u (pixels)'); ylabel('v (pixels)');
    grid on; hold off;
    
    subplot(1, 2, 2);
    plot(i, norm(error_vector), 'bo', 'MarkerSize', 4);
    hold on;
    title('Feature Error Norm');
    xlabel('Iteration'); ylabel('Norm of Error');
    grid on;
    
    drawnow;
end