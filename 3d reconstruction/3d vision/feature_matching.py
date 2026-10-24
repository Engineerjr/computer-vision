#%% SECTION 2: Feature Matching
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the directory to path if needed, or import directly if they are in the same folder
from feature_extraction import extract_features  # (Make sure to rename your file with an underscore instead of a space if needed)
def match_features(descriptors1, descriptors2, method='flann', ratio_thresh=0.75):
    """
    Match features between two images using different methods.
    """

    # Convert descriptors to appropriate type if needed
    if descriptors1 is None or descriptors2 is None:
        return []
    
    if method.lower() == 'flann':
        # FLANN parameters
        if descriptors1.dtype != np.float32:
            descriptors1 = np.float32(descriptors1)
        if descriptors2.dtype != np.float32:
            descriptors2 = np.float32(descriptors2)
            
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # Higher values = more accurate but slower
        
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(descriptors1, descriptors2, k=2)
    else:  # Brute Force
        # For ORB descriptors
        if descriptors1.dtype == np.uint8:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        else:  # For SIFT and SURF descriptors
            bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
        
        matches = bf.knnMatch(descriptors1, descriptors2, k=2)
    
    # Apply Lowe's ratio test
    good_matches = []
    for match in matches:
        if len(match) == 2:  # Sometimes fewer than 2 matches are returned
            m, n = match
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)
    
    return good_matches

def visualize_matches(img1, kp1, img2, kp2, matches, max_display=100):
    """
    Create a visualization of feature matches between two images.
    """

    # Limit the number of matches to display
    matches_to_draw = matches[:min(max_display, len(matches))]
    
    # Create match visualization
    match_img = cv2.drawMatches(
        img1, kp1, img2, kp2, matches_to_draw, None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    return match_img

# Load two images
img1_path = "/home/jr/Documents/engineering/computer-vision/3d reconstruction/3d vision/liege4.jpg"  # Replace with your image paths
img2_path = "/home/jr/Documents/engineering/computer-vision/3d reconstruction/3d vision/Neuralangelo.png"
    
# Extract features using SIFT (or your preferred method)
kp1, desc1, _ = extract_features(img1_path, 'sift')
kp2, desc2, _ = extract_features(img2_path, 'sift')
    
# Match features
good_matches = match_features(desc1, desc2, method='flann')
    
print(f"Found {len(good_matches)} good matches")