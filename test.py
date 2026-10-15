import pyrealsense2 as rs
import numpy as np
import cv2
import sys

def main():
    # ------------------------------------------------------------
    # 1. Print a welcome message and start initializing
    # ------------------------------------------------------------
    print("[INFO] Starting RealSense D435 depth camera test...")

    # Create a pipeline object. This is the main interface to the camera.
    pipeline = rs.pipeline()
    config = rs.config()

    # ------------------------------------------------------------
    # 2. Check if the camera is physically connected
    # ------------------------------------------------------------
    ctx = rs.context()
    devices = ctx.query_devices()
    print(f"[INFO] Found {len(devices)} RealSense device(s) connected.")
    if len(devices) == 0:
        print("[ERROR] No RealSense device detected. Please check the USB connection.")
        sys.exit(1)

    # Print the name of the connected device (should be Intel RealSense D435)
    for dev in devices:
        print(f"[INFO] Device: {dev.get_info(rs.camera_info.name)}")
        print(f"[INFO] Serial Number: {dev.get_info(rs.camera_info.serial_number)}")
        print(f"[INFO] Firmware Version: {dev.get_info(rs.camera_info.firmware_version)}")

    # ------------------------------------------------------------
    # 3. Configure the depth stream
    # ------------------------------------------------------------
    # D435 supports depth at 640x480, 30 FPS, Z16 format.
    # If your camera does not support this exact configuration,
    # an error will be printed below.
    try:
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        print("[INFO] Depth stream configured: 640x480, Z16, 30 FPS.")
    except RuntimeError as e:
        print(f"[ERROR] Failed to configure depth stream: {e}")
        sys.exit(1)

    # ------------------------------------------------------------
    # 4. Start the pipeline
    # ------------------------------------------------------------
    try:
        profile = pipeline.start(config)
        print("[INFO] Pipeline started successfully.")
    except RuntimeError as e:
        print(f"[ERROR] Could not start pipeline: {e}")
        print("[ERROR] The camera may be in use by another program, or the")
        print("        requested stream configuration is not supported.")
        sys.exit(1)

    # ------------------------------------------------------------
    # 5. Optional: Get the depth sensor and its scale
    # ------------------------------------------------------------
    # The depth scale converts raw uint16 values to meters.
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    print(f"[INFO] Depth scale: {depth_scale} meters per unit.")
    print("[INFO] Press 'q' in the image window to quit.")

    # ------------------------------------------------------------
    # 6. Main loop: Capture and display depth frames
    # ------------------------------------------------------------
    try:
        frame_count = 0
        while True:
            # Wait for a coherent set of frames (blocks until available)
            frames = pipeline.wait_for_frames()
            frame_count += 1

            # Get the depth frame
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                print("[WARN] Depth frame not available in this set. Skipping.")
                continue

            # ----------------------------------------------------
            # 7. Print a status message every 30 frames to show it's working
            # ----------------------------------------------------
            if frame_count % 30 == 0:
                print(f"[INFO] Frame {frame_count}: depth frame received "
                      f"(width={depth_frame.get_width()}, "
                      f"height={depth_frame.get_height()}).")

            # ----------------------------------------------------
            # 8. Convert the depth frame to a NumPy array
            # ----------------------------------------------------
            depth_image = np.asanyarray(depth_frame.get_data())

            # ----------------------------------------------------
            # 9. Apply a color map for visualization
            # ----------------------------------------------------
            # Normalize the depth image for display (0–255 range).
            depth_colormap = cv2.applyColorMap(
                cv2.convertScaleAbs(depth_image, alpha=0.03),
                cv2.COLORMAP_JET
            )

            # Show the depth image in a window
            cv2.imshow('RealSense D435 Depth', depth_colormap)

            # ----------------------------------------------------
            # 10. Check for a key press to quit
            # ----------------------------------------------------
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("[INFO] 'q' pressed. Exiting...")
                break

    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
    finally:
        # --------------------------------------------------------
        # 11. Stop the pipeline and close windows
        # --------------------------------------------------------
        pipeline.stop()
        cv2.destroyAllWindows()
        print("[INFO] Pipeline stopped. Program ended.")

if __name__ == "__main__":
    main()