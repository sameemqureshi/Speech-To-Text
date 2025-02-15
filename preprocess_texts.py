import os
import re
import string
from num2words import num2words
print('hi')
# Input and output directories
import os

# Using os.path.join for cross-platform compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "transcripts")
OUTPUT_FOLDER = os.path.join(BASE_DIR,"preprocessed_data","preprocessed_transcripts")
#  Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def preprocess_text(text):
    """
    Preprocess the transcript:
    1. Convert to lowercase
    2. Remove punctuations
    3. Convert digits to words
    """
    text = text.lower()  # Convert to lowercase
    
    # Convert digits to words
    text = re.sub(r'\d+', lambda x: num2words(int(x.group())), text)

    # Remove punctuations (keeping basic ones like periods if needed)
    text = text.translate(str.maketrans("", "", string.punctuation))

    return text

def process_transcripts():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".txt"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename)

            with open(input_path, "r", encoding="utf-8") as infile:
                text = infile.read()

            processed_text = preprocess_text(text)

            with open(output_path, "w", encoding="utf-8") as outfile:
                outfile.write(processed_text)

            print(f"✅ Processed: {filename}")

if __name__ == "__main__":
    process_transcripts()
