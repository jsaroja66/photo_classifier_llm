import os
import requests
import base64

# Set API key and prompt
api_key = os.getenv('OPENAI_API_KEY')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# # Function to get the description of an image
def get_image_description(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 100
    }

    response = requests.post("https://llm-proxy.codio.com/api/providers/openai/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        if 'choices' in response_data:
            return response_data['choices'][0]['message']['content']
        else:
            print(f"Error: 'choices' not found in response for {image_path}")
            return "No description available"
    else:
        print(f"Error: Failed to get response for {image_path}, Status Code: {response.status_code}")
        return "No description available"

# # Function to store the description in a record file
def store_description(image_path, description):
    with open("record.txt", "a") as record_file:
        record_file.write(f"{os.path.basename(image_path)}: {description}\n")
        record_file.write("/////////\n")

# # Function to process all images in a folder
def process_images(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg', 'webp', 'gif'))]
    
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        description = get_image_description(image_path)
        store_description(image_path, description)
        print(f"Processed {image_file}")

folder_path = "images"
process_images(folder_path)

import json

def parse_categorized_output(output):
    # Clean up the output to ensure it is valid JSON
    output = output.replace("Categorized Images:\n", "").strip()
    output = output.replace("\'", "\"")  # Replace single quotes with double quotes for valid JSON
    output = output.replace("}{", "},{")  # Ensure proper separation between JSON objects
    output = f"[{output}]"  # Wrap in list brackets to form a valid JSON array

    try:
        categorized_data_list = json.loads(output)
        # Combine all dictionaries in the list into one
        categorized_data = {}
        for data in categorized_data_list:
            categorized_data.update(data)
        return categorized_data
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {}

import shutil

def organize_images(categorized_data, images_folder):
    for category, image_files in categorized_data.items():
        category_path = os.path.join(images_folder, category)
        os.makedirs(category_path, exist_ok=True)
        
        for image_file in image_files:
            src_path = os.path.join(images_folder, image_file)
            dst_path = os.path.join(category_path, image_file)
            if os.path.exists(src_path):
                shutil.move(src_path, dst_path)
                print(f"Moved {image_file} to {category_path}")
            else:
                print(f"File {image_file} not found in {images_folder}")

                import textsort


import textsort
# Step 1: Read descriptions from record.txt
file_path = "record.txt"
descriptions = textsort.read_descriptions(file_path)

# Step 2: Categorize the images based on their descriptions
categorized_output = textsort.categorize_images(descriptions)
print("Categorized Images:\n", categorized_output)

# Step 3: Parse the categorized output
categorized_data = parse_categorized_output(categorized_output)

# Step 4: Organize images into folders
images_folder = "images"
organize_images(categorized_data, images_folder)