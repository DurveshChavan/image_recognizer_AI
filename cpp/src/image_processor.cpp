#include "image_processor.h"
#include <iostream>
#include <fstream>
#include <algorithm>
#include <cmath>

namespace yolov10_cpp {

class ImageProcessor::Impl {
public:
    Impl() = default;
    ~Impl() = default;
};

ImageProcessor::ImageProcessor() : pImpl(std::make_unique<Impl>()) {}

ImageProcessor::~ImageProcessor() = default;

cv::Mat ImageProcessor::preprocess_image(const std::string& image_path, 
                                       const cv::Size& target_size,
                                       bool normalize) {
    // Simple fallback implementation
    std::cout << "Processing image: " << image_path << std::endl;
    
    // Create a dummy matrix for demonstration
    cv::Mat result(target_size.height, target_size.width);
    
    // Fill with dummy data
    for (int i = 0; i < result.rows; ++i) {
        for (int j = 0; j < result.cols; ++j) {
            result.at(i, j) = (i + j) % 255; // Simple pattern
        }
    }
    
    if (normalize) {
        // Normalize to [0, 1]
        for (int i = 0; i < result.rows; ++i) {
            for (int j = 0; j < result.cols; ++j) {
                result.at(i, j) /= 255.0f;
            }
        }
    }
    
    return result;
}

cv::Mat ImageProcessor::resize_with_padding(const cv::Mat& image, 
                                          const cv::Size& target_size,
                                          const cv::Scalar& pad_color) {
    // Simple resize implementation
    cv::Mat result(target_size.height, target_size.width);
    
    // Fill with padding color
    for (int i = 0; i < result.rows; ++i) {
        for (int j = 0; j < result.cols; ++j) {
            result.at(i, j) = pad_color.val[0];
        }
    }
    
    // Copy image data (simplified)
    int min_rows = std::min(image.rows, result.rows);
    int min_cols = std::min(image.cols, result.cols);
    
    for (int i = 0; i < min_rows; ++i) {
        for (int j = 0; j < min_cols; ++j) {
            result.at(i, j) = image.at(i, j);
        }
    }
    
    return result;
}

cv::Mat ImageProcessor::apply_augmentation(const cv::Mat& image, 
                                         const std::vector<std::string>& augmentations) {
    cv::Mat result = image;
    
    for (const auto& aug : augmentations) {
        if (aug == "flip") {
            // Simple horizontal flip
            cv::Mat flipped(result.rows, result.cols);
            for (int i = 0; i < result.rows; ++i) {
                for (int j = 0; j < result.cols; ++j) {
                    flipped.at(i, j) = result.at(i, result.cols - 1 - j);
                }
            }
            result = flipped;
        }
    }
    
    return result;
}

cv::Mat ImageProcessor::image_to_blob(const cv::Mat& image,
                                     double scale_factor,
                                     const cv::Scalar& mean,
                                     const cv::Scalar& std) {
    cv::Mat result(image.rows, image.cols);
    
    for (int i = 0; i < image.rows; ++i) {
        for (int j = 0; j < image.cols; ++j) {
            float pixel = image.at(i, j);
            pixel = (pixel * scale_factor - mean.val[0]) / std.val[0];
            result.at(i, j) = pixel;
        }
    }
    
    return result;
}

std::vector<cv::Mat> ImageProcessor::extract_patches(const cv::Mat& image,
                                                    const cv::Size& patch_size,
                                                    const cv::Size& stride) {
    std::vector<cv::Mat> patches;
    
    for (int y = 0; y <= image.rows - patch_size.height; y += stride.height) {
        for (int x = 0; x <= image.cols - patch_size.width; x += stride.width) {
            cv::Mat patch(patch_size.height, patch_size.width);
            
            for (int i = 0; i < patch_size.height; ++i) {
                for (int j = 0; j < patch_size.width; ++j) {
                    if (y + i < image.rows && x + j < image.cols) {
                        patch.at(i, j) = image.at(y + i, x + j);
                    }
                }
            }
            
            patches.push_back(patch);
        }
    }
    
    return patches;
}

cv::Mat ImageProcessor::apply_gaussian_blur(const cv::Mat& image, 
                                           const cv::Size& kernel_size,
                                           double sigma) {
    // Simple blur implementation
    cv::Mat result(image.rows, image.cols);
    
    for (int i = 0; i < image.rows; ++i) {
        for (int j = 0; j < image.cols; ++j) {
            float sum = 0;
            int count = 0;
            
            // Simple 3x3 blur
            for (int di = -1; di <= 1; ++di) {
                for (int dj = -1; dj <= 1; ++dj) {
                    int ni = i + di;
                    int nj = j + dj;
                    if (ni >= 0 && ni < image.rows && nj >= 0 && nj < image.cols) {
                        sum += image.at(ni, nj);
                        count++;
                    }
                }
            }
            
            result.at(i, j) = sum / count;
        }
    }
    
    return result;
}

cv::Mat ImageProcessor::apply_histogram_equalization(const cv::Mat& image) {
    // Simple histogram equalization
    cv::Mat result(image.rows, image.cols);
    
    // Calculate histogram
    std::vector<int> histogram(256, 0);
    for (int i = 0; i < image.rows; ++i) {
        for (int j = 0; j < image.cols; ++j) {
            int pixel = static_cast<int>(image.at(i, j) * 255);
            if (pixel >= 0 && pixel < 256) {
                histogram[pixel]++;
            }
        }
    }
    
    // Calculate cumulative distribution
    std::vector<float> cdf(256, 0);
    cdf[0] = histogram[0];
    for (int i = 1; i < 256; ++i) {
        cdf[i] = cdf[i-1] + histogram[i];
    }
    
    // Normalize CDF
    float total_pixels = image.rows * image.cols;
    for (int i = 0; i < 256; ++i) {
        cdf[i] /= total_pixels;
    }
    
    // Apply equalization
    for (int i = 0; i < image.rows; ++i) {
        for (int j = 0; j < image.cols; ++j) {
            int pixel = static_cast<int>(image.at(i, j) * 255);
            if (pixel >= 0 && pixel < 256) {
                result.at(i, j) = cdf[pixel];
            } else {
                result.at(i, j) = image.at(i, j);
            }
        }
    }
    
    return result;
}

cv::Mat ImageProcessor::convert_color_space(const cv::Mat& image, int conversion_code) {
    // Simple color space conversion (just return the image for now)
    return image;
}

std::map<std::string, double> ImageProcessor::get_image_statistics(const cv::Mat& image) {
    std::map<std::string, double> stats;
    
    if (image.rows == 0 || image.cols == 0) {
        return stats;
    }
    
    double sum = 0, min_val = image.at(0, 0), max_val = image.at(0, 0);
    int total_pixels = image.rows * image.cols;
    
    for (int i = 0; i < image.rows; ++i) {
        for (int j = 0; j < image.cols; ++j) {
            float pixel = image.at(i, j);
            sum += pixel;
            min_val = std::min(min_val, static_cast<double>(pixel));
            max_val = std::max(max_val, static_cast<double>(pixel));
        }
    }
    
    double mean = sum / total_pixels;
    
    // Calculate standard deviation
    double variance = 0;
    for (int i = 0; i < image.rows; ++i) {
        for (int j = 0; j < image.cols; ++j) {
            float pixel = image.at(i, j);
            variance += (pixel - mean) * (pixel - mean);
        }
    }
    double std_dev = std::sqrt(variance / total_pixels);
    
    stats["mean"] = mean;
    stats["std"] = std_dev;
    stats["min"] = min_val;
    stats["max"] = max_val;
    
    return stats;
}

bool ImageProcessor::validate_image(const cv::Mat& image) {
    return image.rows > 0 && image.cols > 0 && image.data != nullptr;
}

ImageProcessor::ResizeParams ImageProcessor::calculate_resize_params(const cv::Size& original_size,
                                                                   const cv::Size& target_size) {
    ResizeParams params;
    
    double scale_x = static_cast<double>(target_size.width) / original_size.width;
    double scale_y = static_cast<double>(target_size.height) / original_size.height;
    double scale = std::min(scale_x, scale_y);
    
    params.scale_x = scale;
    params.scale_y = scale;
    params.new_size = cv::Size(static_cast<int>(original_size.width * scale),
                              static_cast<int>(original_size.height * scale));
    
    params.offset.x = (target_size.width - params.new_size.width) / 2.0f;
    params.offset.y = (target_size.height - params.new_size.height) / 2.0f;
    
    return params;
}

} // namespace yolov10_cpp
