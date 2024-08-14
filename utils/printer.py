from io import BytesIO
import matplotlib.pyplot as plt
import requests
from PIL import Image


class Printer:
    """
    A class to print messages with style.

    Attributes:
        COLORS (dict): A dictionary with the color codes.
    """
    COLORS = {
        'red': 91,
        'green': 92,
        'yellow': 93,
        'blue': 94,
        'purple': 95,
        'cyan': 96,
        'light_gray': 97,
        'black': 98,
    }

    @staticmethod
    def print_with_style(message, color=None):
        """
        Print a message with style.
        
        Args:
            message (str): The message to print.
            color (str): The color of the message.
            
        Returns:
            None
        """
        color_code = Printer.COLORS.get(color, "")
        print(f"\033[{color_code}m{message}\033[0m")

    @staticmethod
    def print_image_from_url(url):
        """
        Print an image from a URL.
        
        Args:
            url (str): The URL of the image.
        
        Returns:
            None
        """
        response = requests.get(url, stream=True, verify=False, timeout=10)
        img = Image.open(BytesIO(response.content))

        plt.imshow(img)
        plt.axis('off')  # Hide the axes
        plt.show()
