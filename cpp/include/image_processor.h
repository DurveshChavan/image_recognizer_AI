#pragma once

#ifdef OPENCV_AVAILABLE
#include <opencv2/opencv.hpp>
#else
// Fallback definitions for when OpenCV is not available
#include <vector>
#include <string>
#include <memory>
#include <cstring>

// Simple OpenCV-like structures for fallback
struct cv_Size {
    int width, height;
    cv_Size(int w = 0, int h = 0) : width(w), height(h) {}
};

struct cv_Scalar {
    double val[4];
    cv_Scalar(double v0 = 0, double v1 = 0, double v2 = 0, double v3 = 0) {
        val[0] = v0; val[1] = v1; val[2] = v2; val[3] = v3;
    }
};

struct cv_Point2f {
    float x, y;
    cv_Point2f(float x_ = 0, float y_ = 0) : x(x_), y(y_) {}
};

// Simple matrix class for fallback
class cv_Mat {
public:
    cv_Mat() : rows(0), cols(0), data(nullptr) {}
    cv_Mat(int r, int c) : rows(r), cols(c), data(new float[r * c]) {}
    ~cv_Mat() { delete[] data; }
    
    int rows, cols;
    float* data;
    
    // Simple accessor
    float& at(int r, int c) { return data[r * cols + c]; }
    const float& at(int r, int c) const { return data[r * cols + c]; }
};

// Use fallback types
namespace cv {
    using Size = cv_Size;
    using Scalar = cv_Scalar;
    using Point2f = cv_Point2f;
    using Mat = cv_Mat;
}
#endif

#include <vector>
#include <memory>
#include <string>
#include <map>

namespace yolov10_cpp {

/**
 * @brief High-performance image processor for YOLOv10
 * 
 * This class provides optimized image processing operations including:
 * - Image resizing and normalization
 * - Color space conversions
 * - Data augmentation
 * - Memory-efficient operations
 */
class ImageProcessor {
public:
    ImageProcessor();
    ~ImageProcessor();

    /**
     * @brief Load and preprocess image for YOLOv10 inference
     * @param image_path Path to the input image
     * @param target_size Target size for the model (width, height)
     * @param normalize Whether to normalize pixel values to [0,1]
     * @return Preprocessed image as cv::Mat
     */
    cv::Mat preprocess_image(const std::string& image_path, 
                           const cv::Size& target_size = cv::Size(640, 640),
                           bool normalize = true);

    /**
     * @brief Resize image while maintaining aspect ratio with padding
     * @param image Input image
     * @param target_size Target size
     * @param pad_color Padding color (default: black)
     * @return Resized image with padding
     */
    cv::Mat resize_with_padding(const cv::Mat& image, 
                               const cv::Size& target_size,
                               const cv::Scalar& pad_color = cv::Scalar(0, 0, 0));

    /**
     * @brief Apply data augmentation to image
     * @param image Input image
     * @param augmentations Vector of augmentation types to apply
     * @return Augmented image
     */
    cv::Mat apply_augmentation(const cv::Mat& image, 
                              const std::vector<std::string>& augmentations);

    /**
     * @brief Convert image to blob format for neural network input
     * @param image Input image
     * @param scale_factor Scale factor for normalization
     * @param mean Mean values for normalization
     * @param std Standard deviation values for normalization
     * @return Blob format image
     */
    cv::Mat image_to_blob(const cv::Mat& image,
                         double scale_factor = 1.0/255.0,
                         const cv::Scalar& mean = cv::Scalar(0, 0, 0),
                         const cv::Scalar& std = cv::Scalar(1, 1, 1));

    /**
     * @brief Extract image patches for sliding window detection
     * @param image Input image
     * @param patch_size Size of each patch
     * @param stride Stride between patches
     * @return Vector of image patches
     */
    std::vector<cv::Mat> extract_patches(const cv::Mat& image,
                                        const cv::Size& patch_size,
                                        const cv::Size& stride);

    /**
     * @brief Apply Gaussian blur with optimized kernel
     * @param image Input image
     * @param kernel_size Kernel size
     * @param sigma Gaussian sigma
     * @return Blurred image
     */
    cv::Mat apply_gaussian_blur(const cv::Mat& image, 
                               const cv::Size& kernel_size,
                               double sigma);

    /**
     * @brief Apply histogram equalization for better contrast
     * @param image Input image
     * @return Equalized image
     */
    cv::Mat apply_histogram_equalization(const cv::Mat& image);

    /**
     * @brief Convert image to different color spaces
     * @param image Input image
     * @param conversion_code OpenCV color conversion code
     * @return Converted image
     */
    cv::Mat convert_color_space(const cv::Mat& image, int conversion_code);

    /**
     * @brief Get image statistics (mean, std, min, max)
     * @param image Input image
     * @return Statistics as a map
     */
    std::map<std::string, double> get_image_statistics(const cv::Mat& image);

private:
    class Impl;
    std::unique_ptr<Impl> pImpl;

    /**
     * @brief Validate input image
     * @param image Input image
     * @return True if valid
     */
    bool validate_image(const cv::Mat& image);

    /**
     * @brief Calculate optimal resize parameters
     * @param original_size Original image size
     * @param target_size Target size
     * @return Resize parameters
     */
    struct ResizeParams {
        cv::Size new_size;
        cv::Point2f offset;
        double scale_x, scale_y;
    };
    ResizeParams calculate_resize_params(const cv::Size& original_size,
                                       const cv::Size& target_size);
};

} // namespace yolov10_cpp
