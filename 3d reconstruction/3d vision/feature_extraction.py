#%% SECTION 1: Natural Feature Extraction
import cv2
import numpy as np
import matplotlib.pyplot as plt

def extract_features(image_path, feature_method='sift', max_features=2000):
    """
    Extract features from an image using different methods.
    """

    # Read the image in color and convert to grayscale
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #using SIFT, SURF, or ORB for feature extraction allows for robust feature detection and description, 
    # which is crucial for tasks like image matching, 3D reconstruction, and object recognition.
    # Initialize feature detector based on method
    if feature_method.lower() == 'sift':
        detector = cv2.SIFT_create(nfeatures=max_features)
    elif feature_method.lower() == 'surf':
        # Note: SURF is patented and may not be available in all OpenCV distributions
        detector = cv2.xfeatures2d.SURF_create(400)  # Adjust threshold as needed
    elif feature_method.lower() == 'orb':
        detector = cv2.ORB_create(nfeatures=max_features)
    else:
        raise ValueError(f"Unsupported feature method: {feature_method}")
    
    # Detect and compute keypoints and descriptors
    keypoints, descriptors = detector.detectAndCompute(gray, None)
    
    # Create visualization
    img_with_features = cv2.drawKeypoints(
        img, keypoints, None, 
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )
    
    print(f"Extracted {len(keypoints)} {feature_method.upper()} features")
    
    return keypoints, descriptors, img_with_features

image_path = "/home/jr/Documents/engineering/computer-vision/3d reconstruction/3d vision/Neuralangelo.png"  # Replace with your image path

# Extract features with different methods
kp_sift, desc_sift, vis_sift = extract_features(image_path, 'sift')
kp_orb, desc_orb, vis_orb = extract_features(image_path, 'orb')

# Display results
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(vis_sift, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.savefig("vis_sift_matplotlib.png", bbox_inches='tight')
plt.close() # Close the figure to free up memory
# Save the visualization results to disk
cv2.imwrite("vis_sift.jpg", vis_sift)
cv2.imwrite("vis_orb.jpg", vis_orb)
print("Saved feature visualizations to disk!")