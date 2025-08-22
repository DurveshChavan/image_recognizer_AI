#pragma once

#include "image_processor.h"
#include "bounding_box.h"
#include "nms_processor.h"
#include <opencv2/opencv.hpp>
#include <vector>
#include <deque>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <functional>

namespace yolov10_cpp {

/**
 * @brief Video processing configuration
 */
struct VideoConfig {
    int frame_width = 640;
    int frame_height = 480;
    int fps = 30;
    int buffer_size = 10;
    bool enable_temporal_smoothing = true;
    float temporal_weight = 0.7f;
    bool enable_multi_threading = true;
    int num_threads = 4;
    bool enable_gpu_acceleration = false;
    std::string output_format = "mp4";
    int quality = 95;
};

/**
 * @brief Frame information structure
 */
struct FrameInfo {
    cv::Mat frame;
    int frame_number;
    double timestamp;
    std::vector<BoundingBox> detections;
    bool is_processed;
};

/**
 * @brief High-performance video processor for YOLOv10
 * 
 * This class provides optimized video processing capabilities including:
 * - Real-time frame processing
 * - Temporal consistency
 * - Multi-threaded processing
 * - GPU acceleration support
 * - Video streaming and recording
 */
class VideoProcessor {
public:
    VideoProcessor();
    explicit VideoProcessor(const VideoConfig& config);
    ~VideoProcessor();

    /**
     * @brief Set video processing configuration
     * @param config Video configuration
     */
    void set_config(const VideoConfig& config);

    /**
     * @brief Get current video configuration
     * @return Current configuration
     */
    VideoConfig get_config() const;

    /**
     * @brief Initialize video processor
     * @return True if initialization successful
     */
    bool initialize();

    /**
     * @brief Process video file
     * @param input_path Input video file path
     * @param output_path Output video file path (optional)
     * @param callback Callback function for processed frames
     * @return True if processing successful
     */
    bool process_video(const std::string& input_path,
                      const std::string& output_path = "",
                      std::function<void(const FrameInfo&)> callback = nullptr);

    /**
     * @brief Process video stream (camera)
     * @param camera_id Camera device ID
     * @param output_path Output video file path (optional)
     * @param callback Callback function for processed frames
     * @return True if processing successful
     */
    bool process_stream(int camera_id = 0,
                       const std::string& output_path = "",
                       std::function<void(const FrameInfo&)> callback = nullptr);

    /**
     * @brief Process single frame
     * @param frame Input frame
     * @param frame_number Frame number
     * @return Processed frame with detections
     */
    FrameInfo process_frame(const cv::Mat& frame, int frame_number = 0);

    /**
     * @brief Start real-time processing
     * @param callback Callback function for processed frames
     */
    void start_processing(std::function<void(const FrameInfo&)> callback);

    /**
     * @brief Stop real-time processing
     */
    void stop_processing();

    /**
     * @brief Check if processing is active
     * @return True if processing
     */
    bool is_processing() const;

    /**
     * @brief Get processing statistics
     * @return Processing statistics
     */
    struct ProcessingStats {
        int total_frames = 0;
        int processed_frames = 0;
        int dropped_frames = 0;
        double avg_fps = 0.0;
        double avg_processing_time_ms = 0.0;
        double total_processing_time = 0.0;
        std::map<int, int> detections_per_frame;
    };
    ProcessingStats get_stats() const;

    /**
     * @brief Reset processing statistics
     */
    void reset_stats();

    /**
     * @brief Set detection callback
     * @param callback Detection callback function
     */
    void set_detection_callback(std::function<std::vector<BoundingBox>(const cv::Mat&)> callback);

    /**
     * @brief Apply temporal smoothing to detections
     * @param current_detections Current frame detections
     * @param previous_detections Previous frame detections
     * @param weight Temporal smoothing weight
     * @return Smoothed detections
     */
    std::vector<BoundingBox> apply_temporal_smoothing(
        const std::vector<BoundingBox>& current_detections,
        const std::vector<BoundingBox>& previous_detections,
        float weight = 0.7f);

    /**
     * @brief Draw detections on frame
     * @param frame Input frame
     * @param detections Vector of detections
     * @param draw_labels Whether to draw labels
     * @param draw_confidence Whether to draw confidence scores
     * @return Frame with drawn detections
     */
    cv::Mat draw_detections(const cv::Mat& frame,
                           const std::vector<BoundingBox>& detections,
                           bool draw_labels = true,
                           bool draw_confidence = true);

    /**
     * @brief Save frame to file
     * @param frame Frame to save
     * @param filename Output filename
     * @return True if save successful
     */
    bool save_frame(const cv::Mat& frame, const std::string& filename);

    /**
     * @brief Extract frames from video
     * @param video_path Video file path
     * @param output_dir Output directory for frames
     * @param frame_interval Extract every Nth frame
     * @return Number of extracted frames
     */
    int extract_frames(const std::string& video_path,
                      const std::string& output_dir,
                      int frame_interval = 1);

    /**
     * @brief Create video from frames
     * @param frame_dir Directory containing frames
     * @param output_path Output video path
     * @param fps Frames per second
     * @return True if creation successful
     */
    bool create_video_from_frames(const std::string& frame_dir,
                                 const std::string& output_path,
                                 int fps = 30);

private:
    VideoConfig config_;
    ProcessingStats stats_;
    std::atomic<bool> is_processing_;
    std::atomic<bool> should_stop_;
    
    std::unique_ptr<ImageProcessor> image_processor_;
    std::unique_ptr<NMSProcessor> nms_processor_;
    
    std::deque<FrameInfo> frame_buffer_;
    std::mutex buffer_mutex_;
    std::condition_variable buffer_cv_;
    
    std::thread processing_thread_;
    std::vector<std::thread> worker_threads_;
    
    std::function<std::vector<BoundingBox>(const cv::Mat&)> detection_callback_;
    std::function<void(const FrameInfo&)> frame_callback_;
    
    cv::VideoWriter video_writer_;
    cv::VideoCapture video_capture_;
    
    std::vector<BoundingBox> previous_detections_;
    std::mutex detections_mutex_;

    /**
     * @brief Processing thread function
     */
    void processing_thread_func();

    /**
     * @brief Worker thread function
     * @param thread_id Thread ID
     */
    void worker_thread_func(int thread_id);

    /**
     * @brief Process frame buffer
     */
    void process_frame_buffer();

    /**
     * @brief Add frame to buffer
     * @param frame_info Frame information
     */
    void add_frame_to_buffer(const FrameInfo& frame_info);

    /**
     * @brief Get frame from buffer
     * @return Frame information
     */
    FrameInfo get_frame_from_buffer();

    /**
     * @brief Initialize video writer
     * @param output_path Output video path
     * @param frame_size Frame size
     * @return True if initialization successful
     */
    bool initialize_video_writer(const std::string& output_path, const cv::Size& frame_size);

    /**
     * @brief Initialize video capture
     * @param input_path Input video path or camera ID
     * @return True if initialization successful
     */
    bool initialize_video_capture(const std::string& input_path);

    /**
     * @brief Update processing statistics
     * @param processing_time Processing time in milliseconds
     */
    void update_stats(double processing_time);

    /**
     * @brief Calculate frame similarity
     * @param frame1 First frame
     * @param frame2 Second frame
     * @return Similarity score
     */
    double calculate_frame_similarity(const cv::Mat& frame1, const cv::Mat& frame2);

    /**
     * @brief Track objects across frames
     * @param current_detections Current frame detections
     * @param previous_detections Previous frame detections
     * @return Tracked detections
     */
    std::vector<BoundingBox> track_objects(
        const std::vector<BoundingBox>& current_detections,
        const std::vector<BoundingBox>& previous_detections);
};

} // namespace yolov10_cpp
