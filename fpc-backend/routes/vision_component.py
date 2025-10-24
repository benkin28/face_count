from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging

from services.vision_service import analyze_image_from_data_url

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": "Connected to image stream server"
        }))
        
        while True:
            try:
                # Receive data URL (text format)
                data_url = await websocket.receive_text()
                logger.info(f"Received data URL: {len(data_url)} characters")
                
                # Analyze image using vision service
                result = await analyze_image_from_data_url(data_url)
                
                # Send back the analysis result
                await websocket.send_text(json.dumps({
                    "type": "image_analysis",
                    "data": result
                }))
                
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
                break
            except Exception as e:
                logger.error(f"Error in WebSocket loop: {str(e)}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Processing error: {str(e)}"
                }))
                
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
