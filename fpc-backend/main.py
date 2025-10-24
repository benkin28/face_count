from fastapi import FastAPI
import logging

from routes.vision_component import router as vision_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Image Stream WebSocket Server"}

# Include the vision router
app.include_router(vision_router)