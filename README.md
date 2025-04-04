Project Title
Image2Text Converter

Description

A Python-powered tool that extracts text from images using Optical Character Recognition (OCR). This application leverages the Tesseract OCR engine and the Pillow library for preprocessing to provide accurate text extraction from a variety of image formats.

Features

-Extract text from a single image file or an entire directory of images.
-Supports various image formats, including JPG, PNG, GIF, and more.
-Includes preprocessing for grayscale conversion and binarization to enhance OCR accuracy.
-Saves extracted text to .txt files in a specified directory or prints it directly to the terminal.
-Command-line interface for easy input/output customization.

Getting Started

Follow these steps to set up and run the application.

Prerequisites

-Python3.13 or higher
-Tesseract OCR installed on your system and added to the PATH.

Installation

Clone the repository:
git clone https://https://github.com/Nicholas671/Image2Text
cd Image2Text

Create abd activate a virtual environment:
python -m venv venv
source venv/Scripts/activate # On Windows
source venv/bin/activate # On Mac/Linux

Install dependencies:
pip install -r requirements.txt

Usage

Single Image:
Extract text from a single image and print it:
python src/main.py --input ./sample_images/test_image1.jpg

Save extracted text to a file:
python src/main.py --input ./sample_images/test_image1.jpg --output ./output

Directory of Images:
Process all images in a directory and save the text files:
python src/main.py --input ./sample_images --output ./output

Example Output
Sample image (test_image1.jpg):
Extracted Text:
SHAME ON YOU!

How It Works:

Preprocessing:
Converts images to grayscale and applies binarization to improve text readability.

Text Extraction:
Utilizes Tesseract OCR to extract text from preprocessed images.

Output:
Saves text to files or prints it in the terminal, based on user preferences.

Directory Structure

image2text/
├── src/
│ ├── main.py # Main script
│ ├── utils.py # Supporting utilities (e.g., saving text)
│ ├── preprocessing.py # Image preprocessing functions
├── sample_images/ # Test images
├── output/ # Directory for extracted text files
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── tests/ # Unit tests for validation
