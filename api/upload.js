const formidable = require('formidable');
const fs = require('fs');
const path = require('path');

// Mock YOLO detection for Vercel (since we can't run heavy ML models on serverless)
// In production, you'd want to use a separate ML service or API
function mockYoloDetection(imageBuffer) {
  // Simulate YOLO detection with mock data
  const mockDetections = [
    {
      label: 'person',
      bbox: [100, 100, 300, 400],
      confidence: 0.95
    },
    {
      label: 'car',
      bbox: [400, 200, 600, 350],
      confidence: 0.87
    }
  ];
  
  return mockDetections;
}

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const form = formidable({
      maxFileSize: 16 * 1024 * 1024, // 16MB
      keepExtensions: true,
      uploadDir: '/tmp', // Use Vercel's temp directory
    });

    const [fields, files] = await new Promise((resolve, reject) => {
      form.parse(req, (err, fields, files) => {
        if (err) reject(err);
        else resolve([fields, files]);
      });
    });

    if (!files.file) {
      return res.status(400).json({ error: 'No file provided' });
    }

    const file = files.file[0];
    
    // Check file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp'];
    if (!allowedTypes.includes(file.mimetype)) {
      return res.status(400).json({ error: 'Invalid file type' });
    }

    // Read file buffer
    const imageBuffer = fs.readFileSync(file.filepath);
    
    // Process with mock YOLO (replace with actual ML service in production)
    const detections = mockYoloDetection(imageBuffer);
    
    // Convert image to base64 for response
    const base64Image = imageBuffer.toString('base64');
    
    // Clean up temp file
    fs.unlinkSync(file.filepath);

    // Prepare response
    const response = {
      success: true,
      filename: file.originalFilename,
      original_image: `data:${file.mimetype};base64,${base64Image}`,
      annotated_image: `data:${file.mimetype};base64,${base64Image}`, // In real app, this would be the annotated version
      detections: detections,
      summary: {
        total_objects: detections.length,
        image_size: `${file.size} bytes`,
        processing_time: '~1-2 seconds'
      }
    };

    res.status(200).json(response);

  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ error: 'Processing error: ' + error.message });
  }
}
