import os
import requests
from PIL import Image

def download_chapter_as_pdf(base_url, chapter_start, chapter_end, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for chapter in range(chapter_start, chapter_end + 1):
        chapter_images = []
        chapter_folder = os.path.join(output_dir, f"Chapter_{chapter}")
        os.makedirs(chapter_folder, exist_ok=True)
        
        print(f"Processing Chapter {chapter}")
        page = 1  # Start with the first page
        
        while True:
            img_url = base_url.replace("xxx", str(chapter)).replace("00.jpg", f"{page}.jpg")
            img_filename = os.path.join(chapter_folder, f"Page_{page:02d}.jpg")
            
            try:
                # Attempt to download the image
                response = requests.get(img_url, stream=True)
                
                if response.status_code == 404:
                    print(f"Reached end of Chapter {chapter} at Page {page - 1}")
                    break  # Stop when there are no more pages
                
                response.raise_for_status()
                
                with open(img_filename, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                
                chapter_images.append(img_filename)
                print(f"Downloaded: {img_filename}")
                page += 1  # Move to the next page
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")
                break  # Exit on unexpected errors

        # Combine downloaded images into a PDF
        if chapter_images:
            pdf_path = os.path.join(output_dir, f"Dandadan_Chapter_{chapter}.pdf")
            images = [Image.open(img).convert('RGB') for img in chapter_images]
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
            print(f"Chapter {chapter} saved as PDF: {pdf_path}")
        else:
            print(f"No valid images for Chapter {chapter}")

if __name__ == "__main__":
    BASE_URL = "https://cdn.black-clover.org/file/sugois/Dandadan/Chapter-xxx/00.jpg"
    CHAPTER_START = 176
    CHAPTER_END = 177
    OUTPUT_DIR = "/Users/adil/Downloads/DanDaDanChapter"

    download_chapter_as_pdf(BASE_URL, CHAPTER_START, CHAPTER_END, OUTPUT_DIR)