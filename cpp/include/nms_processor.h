#pragma once

#include "bounding_box.h"
#include <vector>
#include <algorithm>
#include <queue>
#include <unordered_set>

namespace yolov10_cpp {

/**
 * @brief Optimized Non-Maximum Suppression (NMS) processor
 * 
 * This class provides high-performance NMS algorithms including:
 * - Standard NMS
 * - Soft NMS
 * - Weighted NMS
 * - Class-agnostic NMS
 * - Multi-class NMS
 */
class NMSProcessor {
public:
    /**
     * @brief NMS algorithm types
     */
    enum class NMSType {
        STANDARD,    // Standard greedy NMS
        SOFT,        // Soft NMS with score decay
        WEIGHTED,    // Weighted NMS
        ADAPTIVE     // Adaptive NMS
    };

    /**
     * @brief Configuration for NMS processing
     */
    struct NMSConfig {
        float iou_threshold = 0.45f;
        float confidence_threshold = 0.5f;
        NMSType nms_type = NMSType::STANDARD;
        bool class_agnostic = false;
        float soft_nms_sigma = 0.5f;
        int max_detections = 300;
        float adaptive_threshold = 0.5f;
    };

    NMSProcessor();
    explicit NMSProcessor(const NMSConfig& config);
    ~NMSProcessor();

    /**
     * @brief Set NMS configuration
     * @param config NMS configuration
     */
    void set_config(const NMSConfig& config);

    /**
     * @brief Get current NMS configuration
     * @return Current configuration
     */
    NMSConfig get_config() const;

    /**
     * @brief Apply Non-Maximum Suppression to bounding boxes
     * @param boxes Input vector of bounding boxes
     * @return Filtered vector of bounding boxes after NMS
     */
    std::vector<BoundingBox> apply_nms(const std::vector<BoundingBox>& boxes);

    /**
     * @brief Apply standard greedy NMS
     * @param boxes Input vector of bounding boxes
     * @param iou_threshold IoU threshold
     * @return Filtered vector of bounding boxes
     */
    std::vector<BoundingBox> apply_standard_nms(const std::vector<BoundingBox>& boxes,
                                               float iou_threshold);

    /**
     * @brief Apply soft NMS with score decay
     * @param boxes Input vector of bounding boxes
     * @param iou_threshold IoU threshold
     * @param sigma Soft NMS sigma parameter
     * @return Filtered vector of bounding boxes
     */
    std::vector<BoundingBox> apply_soft_nms(const std::vector<BoundingBox>& boxes,
                                           float iou_threshold,
                                           float sigma);

    /**
     * @brief Apply weighted NMS
     * @param boxes Input vector of bounding boxes
     * @param iou_threshold IoU threshold
     * @return Filtered vector of bounding boxes
     */
    std::vector<BoundingBox> apply_weighted_nms(const std::vector<BoundingBox>& boxes,
                                               float iou_threshold);

    /**
     * @brief Apply adaptive NMS
     * @param boxes Input vector of bounding boxes
     * @param base_threshold Base IoU threshold
     * @return Filtered vector of bounding boxes
     */
    std::vector<BoundingBox> apply_adaptive_nms(const std::vector<BoundingBox>& boxes,
                                               float base_threshold);

    /**
     * @brief Apply class-agnostic NMS
     * @param boxes Input vector of bounding boxes
     * @param iou_threshold IoU threshold
     * @return Filtered vector of bounding boxes
     */
    std::vector<BoundingBox> apply_class_agnostic_nms(const std::vector<BoundingBox>& boxes,
                                                     float iou_threshold);

    /**
     * @brief Apply multi-class NMS
     * @param boxes Input vector of bounding boxes
     * @param iou_threshold IoU threshold
     * @return Filtered vector of bounding boxes
     */
    std::vector<BoundingBox> apply_multi_class_nms(const std::vector<BoundingBox>& boxes,
                                                  float iou_threshold);

    /**
     * @brief Apply NMS per class
     * @param boxes Input vector of bounding boxes
     * @param iou_threshold IoU threshold
     * @return Filtered vector of bounding boxes
     */
    std::vector<BoundingBox> apply_per_class_nms(const std::vector<BoundingBox>& boxes,
                                                float iou_threshold);

    /**
     * @brief Apply NMS with different thresholds per class
     * @param boxes Input vector of bounding boxes
     * @param class_thresholds Map of class ID to IoU threshold
     * @return Filtered vector of bounding boxes
     */
    std::vector<BoundingBox> apply_class_specific_nms(
        const std::vector<BoundingBox>& boxes,
        const std::map<int, float>& class_thresholds);

    /**
     * @brief Apply NMS with temporal consistency (for video)
     * @param current_boxes Current frame bounding boxes
     * @param previous_boxes Previous frame bounding boxes
     * @param iou_threshold IoU threshold
     * @param temporal_weight Weight for temporal consistency
     * @return Filtered vector of bounding boxes
     */
    std::vector<BoundingBox> apply_temporal_nms(
        const std::vector<BoundingBox>& current_boxes,
        const std::vector<BoundingBox>& previous_boxes,
        float iou_threshold,
        float temporal_weight = 0.7f);

    /**
     * @brief Get NMS statistics
     * @return Statistics about the last NMS operation
     */
    struct NMSStats {
        int input_boxes = 0;
        int output_boxes = 0;
        int suppressed_boxes = 0;
        float processing_time_ms = 0.0f;
        std::map<int, int> boxes_per_class;
    };
    NMSStats get_stats() const;

    /**
     * @brief Reset NMS statistics
     */
    void reset_stats();

private:
    NMSConfig config_;
    NMSStats stats_;

    /**
     * @brief Calculate soft NMS score decay
     * @param iou IoU value
     * @param sigma Soft NMS sigma
     * @return Decay factor
     */
    float calculate_soft_nms_decay(float iou, float sigma);

    /**
     * @brief Calculate adaptive threshold based on box density
     * @param boxes Vector of bounding boxes
     * @param base_threshold Base threshold
     * @return Adaptive threshold
     */
    float calculate_adaptive_threshold(const std::vector<BoundingBox>& boxes,
                                     float base_threshold);

    /**
     * @brief Group boxes by class
     * @param boxes Input vector of bounding boxes
     * @return Map of class ID to vector of boxes
     */
    std::map<int, std::vector<BoundingBox>> group_by_class(
        const std::vector<BoundingBox>& boxes);

    /**
     * @brief Merge overlapping boxes with weighted averaging
     * @param boxes Vector of overlapping boxes
     * @return Merged bounding box
     */
    BoundingBox merge_overlapping_boxes(const std::vector<BoundingBox>& boxes);

    /**
     * @brief Find overlapping boxes for a given box
     * @param target_box Target bounding box
     * @param boxes Vector of all boxes
     * @param iou_threshold IoU threshold
     * @return Vector of overlapping boxes
     */
    std::vector<BoundingBox> find_overlapping_boxes(
        const BoundingBox& target_box,
        const std::vector<BoundingBox>& boxes,
        float iou_threshold);
};

} // namespace yolov10_cpp
