import requests
import base64
import time
from PIL import Image

class OmniparserClient:
    def __init__(self, host='http://localhost', port=8000):
        self.base_url = f"{host}:{port}"

    def probe(self):
        response = requests.get(f"{self.base_url}/probe/")
        return response.json()

    def parse_image(self, base64_image):
        payload = {"base64_image": base64_image}
        start_time = time.time()
        response = requests.post(f"{self.base_url}/parse/", json=payload)
        duration = time.time() - start_time
        print(f"parse_image took {duration} seconds")
        return response.json()

class ImageConverter:
    @staticmethod
    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode('utf-8')
            print("data conversion to base64_image complete")
        return data

    @staticmethod
    def get_image_resolution(image_path):
        with Image.open(image_path) as img:
            return img.size

if __name__ == "__main__":
    client = OmniparserClient()
    print("Probing the service...")
    print(client.probe())
    
    # Example usage for parse_image
    image_path = r"C:\Users\herbe\Downloads\Screenshot.png"
    base64_image = ImageConverter.image_to_base64(image_path)
    resolution = ImageConverter.get_image_resolution(image_path)
    print(f"Image resolution: {resolution}")
    print(client.parse_image(base64_image)["parsed_content_list"])