#!/usr/bin/env python3
"""
Test client for people detection WebSocket server - 1 FPS stream
"""
import asyncio
import websockets
import json
import base64
from PIL import Image
import io

async def test_1fps_stream():
    """
    Test function that sends images at 1 FPS and displays people count
    """
    uri = "ws://localhost:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")
            
            # Wait for connection confirmation
            response = await websocket.recv()
            print(f"Server: {json.loads(response)['message']}")
            
            # Load the actual PNG images
            image_files = ['image1.png', 'image2.png', 'image3.png']
            images_data = []
            
            for img_file in image_files:
                try:
                    with open(img_file, 'rb') as f:
                        img_bytes = f.read()
                    base64_string = base64.b64encode(img_bytes).decode('utf-8')
                    data_url = f"data:image/png;base64,{base64_string}"
                    images_data.append(data_url)
                    print(f"Loaded {img_file}: {len(img_bytes)} bytes")
                except FileNotFoundError:
                    print(f"Warning: {img_file} not found")
            
            if not images_data:
                print("No images found, creating test image...")
                test_image = Image.new('RGB', (640, 480), color='red')
                img_buffer = io.BytesIO()
                test_image.save(img_buffer, format='JPEG')
                img_bytes = img_buffer.getvalue()
                base64_string = base64.b64encode(img_bytes).decode('utf-8')
                data_url = f"data:image/jpeg;base64,{base64_string}"
                images_data = [data_url]
            
            print(f"\nStarting 1 FPS people detection stream...")
            print("Press Ctrl+C to stop\n")
            
            # Send and receive concurrently at 1 FPS
            async def send_images_1fps():
                image_count = 0
                while True:
                    # Cycle through the available images
                    image_to_send = images_data[image_count % len(images_data)]
                    await websocket.send(image_to_send)
                    image_count += 1
                    await asyncio.sleep(1.0)  # Wait exactly 1 second
            
            async def receive_responses():
                while True:
                    response = await websocket.recv()
                    result = json.loads(response)
                    
                    if result['type'] == 'image_analysis':
                        people_count = result['data'].get('people_count', 0)
                        print(f"👥 People detected: {people_count}")
                    elif result['type'] == 'error':
                        print(f"❌ Error: {result['message']}")
            
            # Run sending and receiving concurrently
            try:
                await asyncio.gather(send_images_1fps(), receive_responses())
            except KeyboardInterrupt:
                print("\n🛑 Stopping people detection stream...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("People Detection WebSocket Test - 1 FPS Stream")
    print("Make sure the server is running on localhost:8000")
    asyncio.run(test_1fps_stream())
