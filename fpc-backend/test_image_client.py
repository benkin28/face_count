#!/usr/bin/env python3
"""
Test client for the image stream WebSocket server
"""
import asyncio
import websockets
import json
import base64
from PIL import Image
import io
import numpy as np

async def test_image_stream():
    uri = "ws://localhost:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")
            
            # Wait for connection confirmation
            response = await websocket.recv()
            print(f"Server response: {response}")
            
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
            
            print(f"Loaded {len(images_data)} images for streaming")

            # Send and receive concurrently
            async def send_images():
                for i in range(10):
                    # Cycle through the available images
                    image_to_send = images_data[i % len(images_data)]
                    await websocket.send(image_to_send)
                    print(f"Sent image {i+1}/10 (using image{(i % len(images_data)) + 1}.png)")
                    await asyncio.sleep(0.1)  # Small delay between sends
            
            async def receive_responses():
                for i in range(10):
                    response = await websocket.recv()
                    result = json.loads(response)
                    print(f"Response {i+1}: {json.dumps(result, indent=2)}")
            
            # Run sending and receiving concurrently
            await asyncio.gather(send_images(), receive_responses())
            
    except Exception as e:
        print(f"Error: {e}")

async def test_1fps_stream():
    """
    Test function that sends images at 1 FPS (one image per second)
    """
    uri = "ws://localhost:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server for 1 FPS test")
            
            # Wait for connection confirmation
            response = await websocket.recv()
            print(f"Server response: {response}")
            
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
            
            print(f"Starting 1 FPS stream with {len(images_data)} images...")
            print("Press Ctrl+C to stop")
            
            # Send and receive concurrently at 1 FPS
            async def send_images_1fps():
                image_count = 0
                while True:
                    # Cycle through the available images
                    image_to_send = images_data[image_count % len(images_data)]
                    await websocket.send(image_to_send)
                    print(f"Sent image {image_count + 1} at {image_count + 1}s (using image{(image_count % len(images_data)) + 1}.png)")
                    image_count += 1
                    await asyncio.sleep(1.0)  # Wait exactly 1 second
            
            async def receive_responses():
                response_count = 0
                while True:
                    response = await websocket.recv()
                    result = json.loads(response)
                    response_count += 1
                    print(f"Response {response_count}: {result['data']['success']} - {result['data'].get('width', 'N/A')}x{result['data'].get('height', 'N/A')}")
            
            # Run sending and receiving concurrently
            try:
                await asyncio.gather(send_images_1fps(), receive_responses())
            except KeyboardInterrupt:
                print("\nStopping 1 FPS stream...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Burst test (10 images quickly)")
    print("2. 1 FPS stream test")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        print("Starting 1 FPS stream test...")
        print("Make sure the server is running on localhost:8000")
        asyncio.run(test_1fps_stream())
    else:
        print("Testing image stream WebSocket...")
        print("Make sure the server is running on localhost:8000")
        asyncio.run(test_image_stream())
