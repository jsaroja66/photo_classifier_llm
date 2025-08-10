# WRITE YOUR CODE HERE
import openai


# Initialize the OpenAI client

client = openai.OpenAI()

# Function to read descriptions from record.txt
def read_descriptions(file_path):
    with open(file_path, "r") as file:
        descriptions = file.read().strip().split("/////////\n")
    return descriptions

# Function to categorize images using ChatGPT
def categorize_images(descriptions):
    prompt = "Here are some image descriptions. Please categorize them into a few distinct categories and list the image file names under each category in a python dictionary format: [category: img1, img2, ...].add  a `miscaleneous` folder for outliers. In your response only provide the categories without extra text. \n\n"
    for desc in descriptions:
        prompt += desc + "\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that categorizes images based on their descriptions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    
    return response.choices[0].message.content

# Example usage
file_path = "record.txt"
descriptions = read_descriptions(file_path)
categorized_output = categorize_images(descriptions)
print("Categorized Images:\n", categorized_output)