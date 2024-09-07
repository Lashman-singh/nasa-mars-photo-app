
#6kVdihE5jRgDkJgsw3aQrIkreW3HF4Zt7SN3UjUO


"""
Description: Fetches random dog pictures from Dog CEO's Dog API.
Author: MGA
Date: Sep/2024
"""
from requests import get
from PIL import Image
from io import BytesIO

# Base URL for the Dog API
url_random_dog = "https://dog.ceo/api/breeds/image/random"

def fetch_dog_picture() -> None:
    """Fetches a random dog picture and displays it."""
    response = get(url_random_dog)  # Make an API request to fetch a random dog image
    data = response.json()  # Parse the JSON response to get the image URL
    img_url = data["message"]

    # Display the fetched dog picture
    img_resp = get(img_url)  # Make another request to get the image content
    img = Image.open(BytesIO(img_resp.content))  # Open the image using PIL
    img.show()  # Display the image
    img.close()

if __name__ == "__main__":
    fetch_dog_picture()  # Call the function to fetch and show a dog picture
