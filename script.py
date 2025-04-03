"""
Image Alpha Channel Processor

Processes images by applying a threshold to the alpha channel to create a binary transparency mask.
"""

import argparse
import logging
from pathlib import Path
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def has_translucent_pixels(alpha_channel: np.ndarray) -> bool:
    """
    Check if an image contains translucent pixels (alpha values between 0 and 1).
    
    Args:
        alpha_channel: Numpy array representing the alpha channel of an image
    
    Returns:
        bool: True if translucent pixels exist, False otherwise
    """
    return ((alpha_channel > 0) & (alpha_channel < 1)).any()


def process_image(
    input_path: Path,
    output_suffix: str = "_processed",
    threshold: float = 0.5
) -> Tuple[bool, bool]:
    """
    Process image alpha channel using specified threshold.
    
    Args:
        input_path: Path to input image file
        output_suffix: Suffix for output filename
        threshold: Alpha threshold value (0-1)
    
    Returns:
        Tuple containing pre/post processing translucent status
    
    Raises:
        ValueError: If image has no alpha channel or invalid threshold
    """
    if not 0 <= threshold <= 1:
        raise ValueError(f"Threshold {threshold} must be between 0 and 1")

    try:
        img = plt.imread(input_path)
    except Exception as e:
        logger.error(f"Failed to read image: {e}")
        raise

    if img.shape[-1] != 4:
        raise ValueError("Input image must have an alpha channel (RGBA format)")

    alpha_channel = img[..., 3]
    initial_status = has_translucent_pixels(alpha_channel)
    logger.info(f"Translucent pixels present (pre-processing): {initial_status}")

    # Apply threshold to create binary alpha channel
    processed_alpha = np.where(alpha_channel > threshold, 1, 0)
    img[..., 3] = processed_alpha
    final_status = has_translucent_pixels(img[..., 3])
    logger.info(f"Translucent pixels present (post-processing): {final_status}")

    # Prepare output path
    output_path = input_path.parent / f"{input_path.stem}{output_suffix}{input_path.suffix}"
    
    try:
        plt.imsave(
            output_path,
            img,
            dpi=300,
            format='png'
        )
        logger.info(f"Processed image saved to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save image: {e}")
        raise

    return initial_status, final_status


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process image alpha channel using thresholding"
    )
    parser.add_argument(
        "input_path",
        type=str,
        help="Path to input image file"
    )
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=0.5,
        help="Alpha threshold value (0-1, default: 0.5)"
    )
    parser.add_argument(
        "-s", "--suffix",
        type=str,
        default="_processed",
        help="Output filename suffix (default: '_processed')"
    )
    
    args = parser.parse_args()
    
    try:
        process_image(
            input_path=Path(args.input_path),
            output_suffix=args.suffix,
            threshold=args.threshold
        )
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        exit(1)