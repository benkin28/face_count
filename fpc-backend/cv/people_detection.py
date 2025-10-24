from ultralytics import YOLO
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Initialize YOLO model (class 0 is 'person' in COCO dataset)
model = YOLO('yolov8n.pt')

async def detect_people(image: bytes) -> dict:
    """
    Detect people in an image and return count
    """
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image, np.uint8)
        
        # Decode image using OpenCV
        image_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image_cv is None:
            return {"people_count": 0, "error": "Failed to decode image"}
        
        # Run YOLO detection
        results = model(image_cv)
        
        # Count people (class 0 in COCO dataset)
        people_count = 0
        for result in results:
            if result.boxes is not None:
                # Filter for person class (class 0)
                person_boxes = result.boxes[result.boxes.cls == 0]
                people_count = len(person_boxes)
        
        logger.info(f"Detected {people_count} people in image")
        return {"people_count": people_count}
        
    except Exception as e:
        logger.error(f"Error detecting people: {str(e)}")
        return {"people_count": 0, "error": f"Detection failed: {str(e)}"}
    