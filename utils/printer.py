class Printer:
    
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
        color_code = Printer.COLORS.get(color, "")

        print(f"\033[{color_code}m{message}\033[0m")
    
    @staticmethod
    def print_image_from_url(url):
        import matplotlib.pyplot as plt
        import requests
        from io import BytesIO
        from PIL import Image
        
        response = requests.get(url, stream=True, verify=False)
        img = Image.open(BytesIO(response.content))
        
        plt.imshow(img)
        plt.axis('off')  # Hide the axes
        plt.show()

