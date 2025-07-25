
# TODO: import your module
from openai import OpenAI
import requests
import os
import sys
from secrets import API_KEY

# Get the folder where the script is located, done for you
script_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_dir, "../frontend/src/downloaded_image.jpg")

url = "http://172.20.10.6/1024x768.jpg"             # You will have to change the IP Address

# Function to download the image from esp32, given to you
def download_image():
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Image saved to: {filename}")
    else:
        print("Failed to download image. Status code:", response.status_code)

# TODO: Download the image and get a response from openai

# TODO: How to control when to take photo?


client = OpenAI(api_key = API_KEY)

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {
                "type": "input_image",
                "image_url": "",
            },
        ],
    }],
)

print(response.output_text)