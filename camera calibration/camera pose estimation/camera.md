# Camera Projection: From 3D World to 2D Image

A camera turns a 3D scene into a 2D image by tracing rays from the camera center through points in the world and intersecting them with the image plane.

## 1. Pinhole camera model

The simplest model is a pinhole camera:

- The camera center is a single point in space.
- Light passes through a tiny aperture (the pinhole).
- The image is formed on a plane in front of the camera.

If a 3D point is written as:

```text
X = [X, Y, Z]^T
```

and the camera focal length is `f`, then the projection onto the image plane is:

```text
x = f * X / Z
y = f * Y / Z
```

This means:

- objects farther away appear smaller,
- points with larger `Z` (distance from camera) project closer to the image center,
- depth information is lost in the projection.

## 2. Image coordinates

The image plane is usually represented in pixel coordinates rather than physical distances. Let:

```text
u = f_x * X / Z + c_x
v = f_y * Y / Z + c_y
```

where:

- `f_x`, `f_y` are focal lengths in pixel units,
- `c_x`, `c_y` are the principal point (image center),
- `(u, v)` is the projected pixel location.

So the camera does not just “look” at the scene—it converts 3D points into 2D pixel coordinates according to its optics and calibration.

## 3. Matrix form

The projection can be written compactly with homogeneous coordinates:

```text
s [u, v, 1]^T = K [R | t] [X_w, Y_w, Z_w, 1]^T
```

where:

- `X_w, Y_w, Z_w` are the 3D coordinates in the world frame,
- `R` is the rotation matrix,
- `t` is the translation vector,
- `K` is the camera intrinsic matrix:

```text
K = [ [f_x, 0,   c_x],
      [0,   f_y, c_y],
      [0,   0,   1] ]
```

This equation has two important parts:

1. Extrinsic parameters (`R`, `t`): describe where the camera is in the world.
2. Intrinsic parameters (`K`): describe the camera’s internal optical properties.

## 4. Why this matters

Projection is the foundation of:

- camera calibration,
- 3D reconstruction,
- visual odometry,
- object tracking,
- stereo vision,
- pose estimation.

A camera does not directly measure the real 3D world—it records a 2D projection of it. Recovering 3D information requires additional knowledge, such as multiple views, depth sensors, or known geometry.

## 5. Intuition

Think of each 3D point as a ray starting at the camera center and passing through the point. The image sensor records where that ray intersects the image plane. This process is what turns the 3D world into a flat 2D image.

In short:

> A camera projects a 3D point onto the image plane by perspective projection, using the camera’s position, orientation, and internal calibration.
