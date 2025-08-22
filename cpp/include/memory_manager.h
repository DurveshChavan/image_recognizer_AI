#pragma once

#include <opencv2/opencv.hpp>
#include <vector>
#include <memory>
#include <mutex>
#include <unordered_map>
#include <cstddef>

namespace yolov10_cpp {

/**
 * @brief Memory pool configuration
 */
struct MemoryPoolConfig {
    size_t initial_size = 1024 * 1024 * 100;  // 100MB initial pool
    size_t max_size = 1024 * 1024 * 1024;     // 1GB max pool
    size_t block_size = 1024 * 1024;          // 1MB block size
    bool enable_growth = true;
    bool enable_shrink = true;
    float growth_factor = 2.0f;
    float shrink_threshold = 0.25f;
};

/**
 * @brief Memory allocation statistics
 */
struct MemoryStats {
    size_t total_allocated = 0;
    size_t total_used = 0;
    size_t total_free = 0;
    size_t peak_usage = 0;
    size_t allocation_count = 0;
    size_t deallocation_count = 0;
    size_t fragmentation_count = 0;
    double fragmentation_ratio = 0.0;
};

/**
 * @brief Memory block information
 */
struct MemoryBlock {
    void* ptr = nullptr;
    size_t size = 0;
    bool is_used = false;
    size_t alignment = 0;
    std::chrono::steady_clock::time_point last_access;
};

/**
 * @brief High-performance memory manager for YOLOv10
 * 
 * This class provides optimized memory management including:
 * - Memory pooling for efficient allocation
 * - GPU memory management
 * - Memory alignment optimization
 * - Garbage collection and defragmentation
 * - Memory usage statistics and monitoring
 */
class MemoryManager {
public:
    MemoryManager();
    explicit MemoryManager(const MemoryPoolConfig& config);
    ~MemoryManager();

    /**
     * @brief Set memory pool configuration
     * @param config Memory pool configuration
     */
    void set_config(const MemoryPoolConfig& config);

    /**
     * @brief Get current memory pool configuration
     * @return Current configuration
     */
    MemoryPoolConfig get_config() const;

    /**
     * @brief Initialize memory manager
     * @return True if initialization successful
     */
    bool initialize();

    /**
     * @brief Allocate memory block
     * @param size Size in bytes
     * @param alignment Memory alignment requirement
     * @return Pointer to allocated memory
     */
    void* allocate(size_t size, size_t alignment = 16);

    /**
     * @brief Deallocate memory block
     * @param ptr Pointer to memory block
     */
    void deallocate(void* ptr);

    /**
     * @brief Allocate memory for OpenCV Mat
     * @param rows Number of rows
     * @param cols Number of columns
     * @param type Mat type
     * @return Allocated cv::Mat
     */
    cv::Mat allocate_mat(int rows, int cols, int type);

    /**
     * @brief Allocate memory for vector of Mats
     * @param count Number of matrices
     * @param rows Number of rows
     * @param cols Number of columns
     * @param type Mat type
     * @return Vector of allocated cv::Mat
     */
    std::vector<cv::Mat> allocate_mat_vector(int count, int rows, int cols, int type);

    /**
     * @brief Allocate aligned memory for image data
     * @param width Image width
     * @param height Image height
     * @param channels Number of channels
     * @param bytes_per_pixel Bytes per pixel
     * @return Pointer to allocated memory
     */
    void* allocate_image_data(int width, int height, int channels, int bytes_per_pixel);

    /**
     * @brief Deallocate image data
     * @param ptr Pointer to image data
     */
    void deallocate_image_data(void* ptr);

    /**
     * @brief Allocate memory for bounding box data
     * @param count Number of bounding boxes
     * @return Pointer to allocated memory
     */
    void* allocate_bbox_data(size_t count);

    /**
     * @brief Deallocate bounding box data
     * @param ptr Pointer to bounding box data
     */
    void deallocate_bbox_data(void* ptr);

    /**
     * @brief Get memory usage statistics
     * @return Memory statistics
     */
    MemoryStats get_stats() const;

    /**
     * @brief Reset memory statistics
     */
    void reset_stats();

    /**
     * @brief Perform garbage collection
     * @return Number of freed blocks
     */
    size_t garbage_collect();

    /**
     * @brief Defragment memory pool
     * @return True if defragmentation successful
     */
    bool defragment();

    /**
     * @brief Shrink memory pool
     * @return Amount of memory freed
     */
    size_t shrink_pool();

    /**
     * @brief Expand memory pool
     * @param additional_size Additional size to allocate
     * @return True if expansion successful
     */
    bool expand_pool(size_t additional_size);

    /**
     * @brief Preallocate memory for expected usage
     * @param expected_size Expected memory usage
     * @return True if preallocation successful
     */
    bool preallocate(size_t expected_size);

    /**
     * @brief Get memory pool status
     * @return Status information
     */
    struct PoolStatus {
        size_t total_blocks = 0;
        size_t used_blocks = 0;
        size_t free_blocks = 0;
        size_t largest_free_block = 0;
        double utilization_ratio = 0.0;
        bool is_fragmented = false;
    };
    PoolStatus get_pool_status() const;

    /**
     * @brief Set memory usage limits
     * @param soft_limit Soft memory limit
     * @param hard_limit Hard memory limit
     */
    void set_memory_limits(size_t soft_limit, size_t hard_limit);

    /**
     * @brief Check if memory usage is within limits
     * @return True if within limits
     */
    bool is_within_limits() const;

    /**
     * @brief Get memory usage warning level
     * @return Warning level (0-100)
     */
    int get_warning_level() const;

    /**
     * @brief Register memory callback
     * @param callback Callback function for memory events
     */
    void register_callback(std::function<void(const MemoryStats&)> callback);

    /**
     * @brief Unregister memory callback
     */
    void unregister_callback();

private:
    MemoryPoolConfig config_;
    MemoryStats stats_;
    std::mutex mutex_;
    
    std::vector<MemoryBlock> memory_blocks_;
    std::unordered_map<void*, MemoryBlock*> block_map_;
    
    size_t soft_limit_;
    size_t hard_limit_;
    std::function<void(const MemoryStats&)> callback_;

    /**
     * @brief Find suitable memory block
     * @param size Required size
     * @param alignment Required alignment
     * @return Pointer to suitable block or nullptr
     */
    MemoryBlock* find_suitable_block(size_t size, size_t alignment);

    /**
     * @brief Split memory block
     * @param block Block to split
     * @param size Size for first part
     */
    void split_block(MemoryBlock* block, size_t size);

    /**
     * @brief Merge adjacent free blocks
     */
    void merge_free_blocks();

    /**
     * @brief Update memory statistics
     * @param allocated Whether this is an allocation
     * @param size Size of operation
     */
    void update_stats(bool allocated, size_t size);

    /**
     * @brief Calculate fragmentation ratio
     * @return Fragmentation ratio
     */
    double calculate_fragmentation_ratio() const;

    /**
     * @brief Check if memory pool needs expansion
     * @return True if expansion needed
     */
    bool needs_expansion() const;

    /**
     * @brief Check if memory pool needs shrinking
     * @return True if shrinking needed
     */
    bool needs_shrinking() const;

    /**
     * @brief Allocate new memory block from system
     * @param size Size to allocate
     * @return New memory block
     */
    MemoryBlock* allocate_system_block(size_t size);

    /**
     * @brief Free memory block to system
     * @param block Block to free
     */
    void free_system_block(MemoryBlock* block);

    /**
     * @brief Validate memory block
     * @param block Block to validate
     * @return True if valid
     */
    bool validate_block(const MemoryBlock* block) const;

    /**
     * @brief Notify callback of memory event
     */
    void notify_callback();
};

} // namespace yolov10_cpp
