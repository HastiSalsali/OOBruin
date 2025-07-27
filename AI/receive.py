#
# TODO: import your module
from openai import OpenAI
from pathlib import Path
import requests
import os
import sys
from my_secrets import API_KEY

# Get the folder where the script is located, done for you
script_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_dir, "../frontend/public/downloaded_image.jpg")

#url = "https://canto-wp-media.s3.amazonaws.com/app/uploads/2019/08/19194139/image-url.jpg" 
url = "https://www.movies4kids.co.uk/wp-content/uploads/sites/15/2019/04/spycat.jpg"
#url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
#url = "http://192.168.50.72/1600x1200.jpg" #(1)

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

download_image()
client = OpenAI(api_key = API_KEY)


# Function to create a file with the Files API
def create_file(file_path):
  with open(file_path, "rb") as file_content:
    result = client.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id

# Getting the file ID
file_id = create_file("../frontend/public/downloaded_image.jpg")


#AI PHOTO ANALYSIS FOR FILE IN FRONTEND (1):
# response = client.responses.create(
#     model="gpt-4.1-mini",
#     input=[{
#         "role": "user",
#         "content": [
#             {"type": "input_text", "text": "what's in this image?"},
#             {
#                 "type": "input_image",
#                 "file_id": file_id,
#             },
#         ],
#     }],
# )
#___________________________________(1)


#AI PHOTO ANALYSIS FOR PHOTO IN WEB (2):
response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {
                "type": "input_image",
                "image_url": url,
            },
        ],
    }],
)
#___________________________________(2)


print(response.output_text)


speech_file_path = os.path.join(script_dir, "../frontend/public/image_to_speach.mp3") 

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="ash",
    input= response.output_text,
    instructions="Speak like a spy like james bond. have a british accent",
) as response:
    response.stream_to_file(speech_file_path)