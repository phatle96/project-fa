from PIL import Image
import io
import base64

IMAGE_PROCESSING_CONFIG = {
    "max_dimension": 512,  # Smaller = fewer tokens
    "jpeg_quality": 80,
    "enable_caching": True,
    "extract_text_only": True,  # Convert image -> text description
    "detail_level": "low",  # "low" | "high" | "auto"
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
