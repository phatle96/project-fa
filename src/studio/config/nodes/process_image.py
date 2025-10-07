"""
Image Processing Node for Fresh Alert Agent

This module handles image processing to reduce token usage when users send images.

TOKEN REDUCTION STRATEGY:
=========================
When users send images with their questions, token usage can be extremely high 
(1000-2000+ tokens per image). This node implements several strategies to reduce costs:

1. **Text Extraction (Default - 70-90% reduction)**
   - Extracts key information from images using a vision model
   - Replaces images with concise text descriptions
   - Focuses on food-relevant information (items, dates, barcodes, condition)
   - Main conversation uses text only, dramatically reducing token usage

2. **Image Optimization (Optional - 30-50% reduction)**
   - Set `optimize_before_processing=True` to compress images
   - Resizes to 512px max dimension
   - Converts to JPEG with quality=80
   - Useful if you want to keep images in the conversation flow

3. **Cost-Efficient Model Usage**
   - Uses Claude Haiku for vision analysis (lowest cost vision model)
   - Focused extraction prompt limits response tokens

CONFIGURATION:
==============
Adjust IMAGE_PROCESSING_CONFIG below to control behavior:
- max_dimension: Image resize dimension (smaller = fewer tokens)
- jpeg_quality: Compression quality 1-100 (lower = smaller file)
- extract_text_only: Convert images to text descriptions
- optimize_before_processing: Compress images before vision analysis
- detail_level: Vision model detail level ("low", "high", "auto")

USAGE:
======
This node runs automatically when users send messages with images.
The workflow routes to this node via the `has_image` conditional edge.
"""

import sys, io, base64, httpx, os, asyncio
from typing import Optional
from PIL import Image

from langchain_core.messages import HumanMessage

from ..states import MainState
from ..models import get_model

IMAGE_PROCESSING_CONFIG = {
    "max_dimension": 512,  # Smaller = fewer tokens (512 is good balance)
    "jpeg_quality": 80,  # Lower = smaller file, but may lose detail
    "enable_caching": True,  # Cache processed images in state
    "extract_text_only": True,  # Convert image -> text description (RECOMMENDED)
    "detail_level": "low",  # "low" uses fewer tokens than "high"
    "optimize_before_processing": True,  # Compress before vision analysis (optional additional savings)
}


def optimize_image(
    image_data: bytes,
    max_size: tuple = (IMAGE_PROCESSING_CONFIG["max_dimension"], IMAGE_PROCESSING_CONFIG["max_dimension"]),
    quality: int = IMAGE_PROCESSING_CONFIG["jpeg_quality"],
) -> str:
    """
    Compress and resize image to reduce token usage.

    Args:
        image_data: Raw image bytes
        max_size: Maximum dimensions (width, height)
        quality: JPEG quality (1-100)

    Returns:
        Base64 encoded optimized image
    """
    img = Image.open(io.BytesIO(image_data))

    # Convert to RGB if necessary
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize maintaining aspect ratio
    img.thumbnail(max_size, Image.Resampling.LANCZOS)

    # Compress
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)

    # Encode to base64
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


async def get_image_bytes(image_content: dict) -> Optional[bytes]:
    """
    Extract image bytes from various image content formats.
    
    Args:
        image_content: Image content block (can be base64, URL, or file path)
        
    Returns:
        Raw image bytes or None if extraction fails
    """
    try:
        # Handle image_url type
        if image_content.get("type") == "image_url":
            image_url = image_content.get("image_url", {})
            if isinstance(image_url, dict):
                url = image_url.get("url", "")
            else:
                url = image_url
                
            # Handle base64 data URLs
            if url.startswith("data:image"):
                # Extract base64 data
                base64_data = url.split(",", 1)[1] if "," in url else url
                return base64.b64decode(base64_data)
            
            # Handle HTTP URLs
            elif url.startswith("http"):
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)
                    return response.content
        
        # Handle direct image type with source
        elif image_content.get("type") == "image":
            # source = image_content.get("source", {})
            
            # Handle base64 in source
            if image_content.get("source_type") == "base64":
                data = image_content.get("data", "")
                return base64.b64decode(data)
            
            # Handle URL in source
            elif image_content.get("source_type") == "url":
                url = image_content.get("url", "")
                if url.startswith("http"):
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url)
                        return response.content
        
        return None
    except Exception as e:
        print(f"Error extracting image bytes: {e}")
        return None


def create_optimized_image_content(optimized_base64: str, detail: str = "low") -> dict:
    """
    Create an image content block with optimized image.
    
    Args:
        optimized_base64: Base64 encoded optimized image
        detail: Detail level for the image ("low", "high", "auto")
        
    Returns:
        Image content block dictionary
    """
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{optimized_base64}",
            "detail": detail
        }
    }

async def get_image_description(image_content: dict, original_text: str = "") -> str:
    """
    Call vision model with specific extraction prompt to get concise description.
    
    Args:
        image_content: The image content block from the message
        original_text: Any accompanying text from the user
        
    Returns:
        Concise text description of the image focusing on food items
    """
    extraction_prompt = f"""Analyze this image and extract ONLY the following information:
        1. Food items visible (name, quantity if visible)
        2. Product barcode/QR-code if visible
        3. Expiration dates, best before dates, or manufacture dates if visible
        4. Packaging condition (sealed/opened/damaged)
        5. Any visible text on packaging (brand, product name)

        Be concise and factual. Format as a bulleted list. Maximum 100 words.

        User's question: {original_text if original_text else "Please analyze this food image."}"""

    # Optionally optimize image before sending to reduce tokens
    processed_image_content = image_content
    
    if IMAGE_PROCESSING_CONFIG["optimize_before_processing"]:
        try:
            # Get image bytes
            image_bytes = await get_image_bytes(image_content)
            if image_bytes:
                # Optimize the image in a separate thread to avoid blocking the event loop
                optimized_base64 = await asyncio.to_thread(optimize_image, image_bytes)
                # Create new content with optimized image
                processed_image_content = create_optimized_image_content(
                    optimized_base64,
                    detail=IMAGE_PROCESSING_CONFIG["detail_level"]
                )
                print(f"✓ Image optimized: {len(optimized_base64)} characters")
            else:
                print("⚠ Could not extract image bytes, using original")
        except Exception as e:
            print(f"Warning: Could not optimize image, using original: {e}")
            # Fall back to original image
            
    print(f"✓ Final processed_image_content: {len(processed_image_content)} characters")
    
    # Create a focused message for vision analysis
    vision_message = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": extraction_prompt},
                processed_image_content  # Pass the (possibly optimized) image content
            ]
        }
    ]
    
    vision_model = get_model(model_config={"provider": "openai", "model_name": "gpt-5-mini"})
    
    # Make focused API call with the vision model
    response = await vision_model.ainvoke(vision_message)
    
    return response.content


async def process_image_node(state: MainState):
    """
    Extract key information from images and store descriptions in state.
    This keeps the original message intact while allowing the conversation node
    to use text descriptions instead of images.
    
    This node:
    1. Finds all images in the last message
    2. Extracts concise descriptions using vision model
    3. Stores descriptions in state (keyed by message ID)
    4. Keeps original message unchanged
    
    Token Reduction Strategy:
    - Converts images to text descriptions (70-90% token reduction)
    - Uses cost-efficient model for vision analysis
    - Optionally optimizes images before processing (set optimize_before_processing=True)
    """
    messages = state.get("messages", [])
    
    if not messages:
        return state
    
    # Get the last message (should be HumanMessage with images)
    last_message = messages[-1]
    message_id = last_message.id if hasattr(last_message, 'id') and last_message.id else str(id(last_message))

    # Initialize state fields if needed
    if "processed_images" not in state or state["processed_images"] is None:
        state["processed_images"] = []
    if "image_descriptions" not in state or state["image_descriptions"] is None:
        state["image_descriptions"] = {}
    
    # Extract text content if any
    original_text = ""
    if isinstance(last_message.content, str):
        original_text = last_message.content
    elif isinstance(last_message.content, list):
        for block in last_message.content:
            if isinstance(block, dict) and block.get("type") == "text":
                original_text = block.get("text", "")
                break
            elif isinstance(block, str):
                original_text = block
                break
    
    # Process images and collect descriptions
    image_descriptions = []
    images_processed = 0
    
    if isinstance(last_message.content, list):
        for i, content_block in enumerate(last_message.content):
            if isinstance(content_block, dict):
                block_type = content_block.get("type")
                
                # Handle image content
                if block_type in ["image_url", "image"]:
                    try:
                        # Get description from vision model
                        description = await get_image_description(content_block, original_text)
                        
                        # Format the description
                        image_number = images_processed + 1
                        formatted_description = f"[Image {image_number} Analysis]:\n{description}"
                        image_descriptions.append(formatted_description)
                        
                        # Store the image ID for potential future reference
                        image_id = f"img_{len(state['processed_images'])}_{image_number}"
                        state["processed_images"].append(image_id)
                        
                        images_processed += 1
                        print(f"✓ Processed image {image_number}/{len([b for b in last_message.content if isinstance(b, dict) and b.get('type') in ['image_url', 'image']])}")
                        
                    except Exception as e:
                        print(f"✗ Error processing image {i+1}: {e}")
                        # Add error message instead of failing completely
                        image_descriptions.append(f"[Image {images_processed + 1}]: Could not process image - {str(e)[:100]}")
                        images_processed += 1
    
    # Store descriptions keyed by message ID without modifying the original message
    if image_descriptions:
        # Combine original text with image descriptions
        combined_text_parts = []
        
        if original_text:
            combined_text_parts.append(f"User's Question: {original_text}")
        
        combined_text_parts.extend(image_descriptions)
        
        # Add helpful context about the image analysis
        if images_processed > 1:
            combined_text_parts.append(
                f"\n(Note: {images_processed} images were analyzed. Use the extracted information above to help the user.)"
            )
        
        new_text_content = "\n\n".join(combined_text_parts)
        
        # Store the text description keyed by message ID
        state["image_descriptions"][message_id] = new_text_content
        
        print(f"✓ Image processing complete: Stored descriptions for {images_processed} images (message ID: {message_id})")
    
    # Return state without modifying the messages
    return state
    
    
PROCESS_IMAGE = sys.intern("process_image")
