import cv2
import numpy as np
from PIL import Image
import base64
import logging
import asyncio

from cv.people_detection import detect_people

logger = logging.getLogger(__name__)

def receive_image_data(data_url: str) -> bytes:
    """
    Extract image bytes from data URL format
    """
    try:
        if data_url.startswith('data:image/'):
            # Split the data URL to get the base64 part
            header, base64_data = data_url.split(',', 1)
            # Decode base64 to bytes
            image_bytes = base64.b64decode(base64_data)
            logger.info(f"Decoded image data: {len(image_bytes)} bytes")
        else:
            # Fallback: treat as base64 string directly
            image_bytes = base64.b64decode(data_url)
            logger.info(f"Decoded base64 data: {len(image_bytes)} bytes")
        
        return image_bytes
    except Exception as e:
        logger.error(f"Error parsing image data: {str(e)}")
        raise

async def process_image(image_data: bytes) -> dict:
    """
    Process the received image data and return people count
    """
    try:
        # Use people detection function
        result = await detect_people(image_data)
        return result
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return {"people_count": 0, "error": f"Image processing failed: {str(e)}"}

async def analyze_image_from_data_url(data_url: str) -> dict:
    """
    Complete image analysis pipeline from data URL
    """
    try:
        # Extract image data
        image_bytes = receive_image_data(data_url)
        
        # Process the image
        result = await process_image(image_bytes)
        
        return result
    except Exception as e:
        logger.error(f"Error in image analysis pipeline: {str(e)}")
        return {"people_count": 0, "error": f"Image analysis failed: {str(e)}"}
