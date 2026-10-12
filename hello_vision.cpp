#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // 1. Read the image from file
    cv::Mat image = cv::imread("
        +6");

    // Check if the image loaded successfully
    if (image.empty()) {
        std::cerr << "Error: Could not open or find the image!" << std::endl;
        return -1;
    }

    // 2. Create a display window
    cv::namedWindow("Hello Vision", cv::WINDOW_AUTOSIZE);

    // 3. Display the image
    cv::imshow("Hello Vision", image);

    // 4. Wait for a keystroke in the window before exiting
    cv::waitKey(0);

    return 0;
}