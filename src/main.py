import pytesseract
from PIL import Image
import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract text from images or directories of images.")
    parser.add_argument("--input", required=True, help="Path to an image or directory of images.")
    parser.add_argument("--output", required=False, help="Path to save the extracted text. If omitted, text is printed.")
    return parser.parse_args()


def save_text_to_file(text, output_path):
    with open(output_path, "w") as file:
        file.write(text)
        print(f"Text saved to {output_path}")

def process_image_directory(directory_path, output_directory=None):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path): 
            print(f"Processing file: {filename}")
            extracted_text = extract_text_from_image(file_path)
            if extracted_text:
                if output_directory:
                    os.makedirs(output_directory, exist_ok=True) 
                    output_path = os.path.join(output_directory, f"{filename}_text.txt")
                else:
                    output_path = f"./output/{filename}_text.txt"
                save_text_to_file(extracted_text, output_path)

def preprocess_image(image):
    grayscale_image = image.convert("L")  
    return grayscale_image

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


import os
import argparse

def main():
    args = parse_arguments()

    if os.path.isdir(args.input):
        print(f"Processing directory: {args.input}")
        process_image_directory(args.input, args.output)
    elif os.path.isfile(args.input):
        print(f"Processing single file: {args.input}")
        extracted_text = extract_text_from_image(args.input)
        if args.output:
            save_text_to_file(extracted_text, args.output)
        else:
            print("Extracted Text:\n", extracted_text)
    else:
        print(f"Error: {args.input} is neither a valid file nor a directory.")

if __name__ == "__main__":
    main()