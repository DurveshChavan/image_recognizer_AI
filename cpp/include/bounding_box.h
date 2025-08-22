#pragma once

#include <opencv2/opencv.hpp>
#include <vector>
#include <algorithm>
#include <cmath>

namespace yolov10_cpp {

/**
 * @brief Optimized bounding box structure and operations
 * 
 * This class provides high-performance bounding box operations including:
 * - Intersection over Union (IoU) calculations
 * - Coordinate transformations
 * - Area calculations
 * - Bounding box merging and splitting
 */
class BoundingBox {
public:
    float x1, y1, x2, y2;  // Top-left and bottom-right coordinates
    float confidence;
    int class_id;
    std::string label;

    BoundingBox();
    BoundingBox(float x1, float y1, float x2, float y2, 
                float conf = 0.0f, int cls_id = 0, const std::string& lbl = "");
    BoundingBox(const cv::Rect& rect, float conf = 0.0f, 
                int cls_id = 0, const std::string& lbl = "");

    /**
     * @brief Calculate area of the bounding box
     * @return Area as float
     */
    float area() const;

    /**
     * @brief Calculate width of the bounding box
     * @return Width as float
     */
    float width() const;

    /**
     * @brief Calculate height of the bounding box
     * @return Height as float
     */
    float height() const;

    /**
     * @brief Get center point of the bounding box
     * @return Center point as cv::Point2f
     */
    cv::Point2f center() const;

    /**
     * @brief Convert to OpenCV Rect
     * @return cv::Rect representation
     */
    cv::Rect to_rect() const;

    /**
     * @brief Check if bounding box is valid
     * @return True if valid
     */
    bool is_valid() const;

    /**
     * @brief Scale bounding box by given factors
     * @param scale_x X-axis scale factor
     * @param scale_y Y-axis scale factor
     * @return Scaled bounding box
     */
    BoundingBox scale(float scale_x, float scale_y) const;

    /**
     * @brief Translate bounding box by given offset
     * @param offset_x X-axis offset
     * @param offset_y Y-axis offset
     * @return Translated bounding box
     */
    BoundingBox translate(float offset_x, float offset_y) const;

    /**
     * @brief Clip bounding box to image boundaries
     * @param img_width Image width
     * @param img_height Image height
     * @return Clipped bounding box
     */
    BoundingBox clip(int img_width, int img_height) const;
};

/**
 * @brief Optimized bounding box operations
 */
class BoundingBoxOps {
public:
    /**
     * @brief Calculate Intersection over Union (IoU) between two bounding boxes
     * @param box1 First bounding box
     * @param box2 Second bounding box
     * @return IoU value
     */
    static float calculate_iou(const BoundingBox& box1, const BoundingBox& box2);

    /**
     * @brief Calculate intersection area between two bounding boxes
     * @param box1 First bounding box
     * @param box2 Second bounding box
     * @return Intersection area
     */
    static float intersection_area(const BoundingBox& box1, const BoundingBox& box2);

    /**
     * @brief Calculate union area between two bounding boxes
     * @param box1 First bounding box
     * @param box2 Second bounding box
     * @return Union area
     */
    static float union_area(const BoundingBox& box1, const BoundingBox& box2);

    /**
     * @brief Check if two bounding boxes overlap
     * @param box1 First bounding box
     * @param box2 Second bounding box
     * @param threshold IoU threshold for overlap
     * @return True if overlapping
     */
    static bool is_overlapping(const BoundingBox& box1, const BoundingBox& box2, 
                              float threshold = 0.0f);

    /**
     * @brief Merge two bounding boxes
     * @param box1 First bounding box
     * @param box2 Second bounding box
     * @return Merged bounding box
     */
    static BoundingBox merge(const BoundingBox& box1, const BoundingBox& box2);

    /**
     * @brief Calculate distance between centers of two bounding boxes
     * @param box1 First bounding box
     * @param box2 Second bounding box
     * @return Euclidean distance
     */
    static float center_distance(const BoundingBox& box1, const BoundingBox& box2);

    /**
     * @brief Transform bounding box coordinates from one coordinate system to another
     * @param box Input bounding box
     * @param src_size Source image size
     * @param dst_size Destination image size
     * @param transform_matrix Transformation matrix
     * @return Transformed bounding box
     */
    static BoundingBox transform_coordinates(const BoundingBox& box,
                                           const cv::Size& src_size,
                                           const cv::Size& dst_size,
                                           const cv::Mat& transform_matrix = cv::Mat());

    /**
     * @brief Convert relative coordinates (0-1) to absolute coordinates
     * @param box Bounding box with relative coordinates
     * @param img_width Image width
     * @param img_height Image height
     * @return Bounding box with absolute coordinates
     */
    static BoundingBox relative_to_absolute(const BoundingBox& box,
                                          int img_width, int img_height);

    /**
     * @brief Convert absolute coordinates to relative coordinates (0-1)
     * @param box Bounding box with absolute coordinates
     * @param img_width Image width
     * @param img_height Image height
     * @return Bounding box with relative coordinates
     */
    static BoundingBox absolute_to_relative(const BoundingBox& box,
                                          int img_width, int img_height);

    /**
     * @brief Sort bounding boxes by confidence score (descending)
     * @param boxes Vector of bounding boxes
     */
    static void sort_by_confidence(std::vector<BoundingBox>& boxes);

    /**
     * @brief Sort bounding boxes by area (descending)
     * @param boxes Vector of bounding boxes
     */
    static void sort_by_area(std::vector<BoundingBox>& boxes);

    /**
     * @brief Filter bounding boxes by confidence threshold
     * @param boxes Input vector of bounding boxes
     * @param threshold Confidence threshold
     * @return Filtered vector of bounding boxes
     */
    static std::vector<BoundingBox> filter_by_confidence(const std::vector<BoundingBox>& boxes,
                                                        float threshold);

    /**
     * @brief Filter bounding boxes by area range
     * @param boxes Input vector of bounding boxes
     * @param min_area Minimum area
     * @param max_area Maximum area
     * @return Filtered vector of bounding boxes
     */
    static std::vector<BoundingBox> filter_by_area(const std::vector<BoundingBox>& boxes,
                                                  float min_area, float max_area);
};

} // namespace yolov10_cpp
