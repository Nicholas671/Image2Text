import pytesseract
from PIL import Image
from multiprocessing import Pool
import os
import argparse
import logging
from googletrans import Translator
from functools import lru_cache
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

DEFAULT_OUTPUT_DIR = "./output"

logging.basicConfig(level=logging.INFO)

def add_task(description):
    # Input validation
    if not description.strip():
        logging.error("Error: Task description cannot be empty.")
        return None
    if len(description) > 50:
        logging.error("Error: Task description is too long. Max 50 characters.")
        return None

    # Task creation
    task = {"description": description, "status": "Not Completed"}
    logging.info(f"Task added: {description}")
    return task

def toggle_task_status(task):
    if task["status"] == "Not Completed":
        task["status"] = "Completed"
    else:
        task["status"] = "Not Completed"
        logging.info(f"Task status updated to: {task['status']}")
    return task

task = {"description": "Learn Python logging", "status": "Not Completed"}
toggle_task_status(task)  

add_task("Learn Python logging")
add_task("Extract text from images or directories of images.")
add_task("Preprocess images to grayscale before text extraction.")
add_task("")  
add_task("A very long task description that exceeds the fifty-character limit.")  # Should log an error about length
add_task("Complete the Python project")  # Should log the task addition

def test_add_task():
    assert add_task("") is None
    assert add_task("A valid task") == {"description": "A vaild task", "status": "Not Completed"}
    assert add_task("Too long task description that exceeds fifty characters") is None

test_add_task()




def translate_text(text, target_language="en"):
    translator = Translator()
    try: 
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return text 

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract text from images or directories of images.")
    parser.add_argument("--input", required=True, help="Path to an image or directory of images.")
    parser.add_argument("--output", required=False, help="Path to save the extracted text. If omitted, text is printed.")
    parser.add_argument("--language", required=False, help="Target language for translation (e.g., 'en' for English, 'es' for Spanish).")
    return parser.parse_args()

def save_text_to_file(text, output_path):
    with open(output_path, "w") as file:
        file.write(text)
        print(f"Text saved to {output_path}")

@lru_cache(maxsize=128)
def tokenize_text(text: str):
    tokens = word_tokenize(text)
    return tokens

def process_single_image(args):
    file_path, output_directory, target_language = args
    try:
        print(f"Processing file: {os.path.basename(file_path)}")
        extracted_text = extract_text_from_image(file_path)

        if extracted_text and extracted_text.strip():
            if target_language:
                extracted_text = translate_text(extracted_text, target_language)
            tokens = tokenize_text(extracted_text)
            print(f"Tokenized {len(tokens)} words: {tokens}")
            output_directory = output_directory if output_directory else DEFAULT_OUTPUT_DIR

            os.makedirs(output_directory, exist_ok=True)
            output_path = os.path.join(output_directory, f"{os.path.basename(file_path)}_text.txt")
            save_text_to_file(" ".join(tokens), output_path)

    except FileNotFoundError as e:
        print(f"File not found: {file_path} - {e}")
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error processing {file_path}: {e}")


def process_image_directory(directory_path, output_directory=None, target_language=None):
    tasks = [
        (os.path.join(directory_path, filename), output_directory, target_language)
        for filename in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, filename))
    ]
    with Pool() as pool:
        pool.map(process_single_image, tasks)

def preprocess_image(image):
    grayscale_image = image.convert("L")
    
    scale_factor = 1.5

    resized_image = grayscale_image.resize((grayscale_image.width * scale_factor, grayscale_image.height * scale_factor), Image.ANTIALIAS)
    
    threshold = grayscale_image.histogram().index(max(grayscale_image.histogram()))
    
    return resized_image.point(lambda p: p > threshold and 255)

def extract_text_from_image(image_path):
    try:
        print(f"Opening image: {image_path}")
        image = Image.open(image_path)
        preprocessed_image = preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed_image)
        return text
    except FileNotFoundError:
        print(f"Error: File not found: {image_path}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def main():
    args = parse_arguments()

    if os.path.isdir(args.input):
        print(f"Processing directory: {args.input}")
        process_image_directory(args.input, args.output, args.language)
    elif os.path.isfile(args.input):
        print(f"Processing single file: {args.input}")
        extracted_text = extract_text_from_image(args.input)
        if args.language:
            extracted_text = translate_text(extracted_text, args.language)
        if args.output:
            save_text_to_file(extracted_text, args.output)
        else:
            print("Extracted Text:\n", extracted_text)
    else:
        print(f"Error: {args.input} is neither a valid file nor a directory.")

if __name__ == "__main__":
    main()