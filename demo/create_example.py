"""
Example image generator for documentation
"""
import numpy as np
import matplotlib.pyplot as plt

def create_gradient_image(size=512):
    """Create test image with alpha gradient"""
    gradient = np.linspace(0, 1, size)
    image = np.zeros((size, size, 4))
    
    # RGB values (purple example)
    image[..., 0] = 0.5  # Red channel
    image[..., 1] = 0.2  # Green channel
    image[..., 2] = 0.7  # Blue channel
    image[..., 3] = np.tile(gradient, (size, 1))  # Alpha gradient
    
    return image

if __name__ == "__main__":
    img = create_gradient_image()
    plt.imsave("./gradient_example.png", img)
    print("Example image created at: ./gradient_example.png")