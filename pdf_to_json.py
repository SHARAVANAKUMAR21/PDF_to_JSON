import os
import pdfplumber
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import json
import base64
import io
from PIL import Image

class Table(BaseModel):
    headers: List[str]
    rows: List[List[str]]

class TextBlock(BaseModel):
    text: str

class ImageBlock(BaseModel):
    page_number: int
    image_index: int
    bbox: List[float]
    image_data: str  
    url: Optional[str] = None  

class PDFData(BaseModel):
    title: Optional[str]
    text_blocks: List[TextBlock]
    tables: List[Table]
    images: List[ImageBlock]

def read_pdf(pdf_path: str):
    try:
        pdf = pdfplumber.open(pdf_path)
        return pdf
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def extract_data_from_pdf(pdf, output_dir: str):
    title = None
    text_blocks = []
    tables = []
    images = []

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, page in enumerate(pdf.pages):
        if i == 0:
            title = page.extract_text().split('\n')[0] if page.extract_text() else None

        text = page.extract_text()
        if text:
            text_blocks.extend([TextBlock(text=block) for block in text.split('\n') if block.strip()])

        table_data = page.extract_tables()
        for table in table_data:
            headers = table[0]
            rows = table[1:]
            tables.append(Table(headers=headers, rows=rows))

        images_found = page.images
        if images_found:
            print(f"Found {len(images_found)} images on page {i + 1}.")
            for idx, image in enumerate(images_found):
                print(f"Image {idx}: {image}")
                bbox = image.get('bbox')
                if bbox:
                    try:
                        im = page.within_bbox(bbox).to_image()
                        img_bytes = io.BytesIO()
                        im.original.save(img_bytes, format='PNG')
                        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

                        # Save the image as a file and create a URL
                        image_filename = f"page_{i + 1}_image_{idx}.png"
                        image_path = os.path.join(output_dir, image_filename)
                        with open(image_path, 'wb') as img_file:
                            img_file.write(img_bytes.getvalue())
                        
                        image_url = f"file:///{os.path.abspath(image_path)}"  # Local file URL
                        images.append(ImageBlock(page_number=i + 1, image_index=idx, bbox=bbox, image_data=img_base64, url=image_url))
                    except Exception as e:
                        print(f"Error processing image {idx} on page {i + 1}: {e}")
                else:
                    print(f"Bounding box not found for image {idx} on page {i + 1}.")
        else:
            print(f"No images found on page {i + 1}.")

    return PDFData(title=title, text_blocks=text_blocks, tables=tables, images=images)

def serialize_data_to_json(pdf_data: PDFData, output_path: str):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(pdf_data.dict(), f, ensure_ascii=False, indent=4)
        print(f"Data successfully serialized to {output_path}")
    except Exception as e:
        print(f"Error serializing data to JSON: {e}")

def main():
    pdf_path = r"C:\Users\shara\OneDrive\Desktop\ansrsource\Biology2e-WEB_Excerpt.pdf"
    json_output_path = r"C:\Users\shara\OneDrive\Desktop\ansrsource\output.json"
    output_dir = r"C:\Users\shara\OneDrive\Desktop\ansrsource\images"  # Directory to save images

    pdf = read_pdf(pdf_path)
    if not pdf:
        return

    try:
        pdf_data = extract_data_from_pdf(pdf, output_dir)
    except ValidationError as e:
        print(f"Data validation error: {e.json()}")
        return

    serialize_data_to_json(pdf_data, json_output_path)

if __name__ == "__main__":
    main()
