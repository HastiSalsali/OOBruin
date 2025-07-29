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

#url = "http://192.168.0.113/1600x1200.jpg" #on bruin wifi
#url = "http://192.168.50.96/1600x1200.jpg"
url = "http://192.168.0.110/1600x1200.jpg"

# Function to download the image from esp32, given to you
def download_image():
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Image saved to: {filename}")
    else:
        print("Failed to download image. Status code:", response.status_code)


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


#AI PHOTO ANALYSIS FOR PICTURE:
response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Describe photo"},
            {
                "type": "input_image",
                "file_id": file_id,
            },
        ],
    }],
)

print(response.output_text)


#AI TEXT TO SPEECH:
speech_file_path = os.path.join(script_dir, "../frontend/public/image_to_speach.mp3") 
instruction = """Accent/Affect: heavy posh british accent; """

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="ash",
    input= response.output_text,
    instructions= instruction
) as response:
    response.stream_to_file(speech_file_path)

