import requests
from bs4 import BeautifulSoup
import os
import time
from PIL import Image
import glob


BASE_URL = "https://read-hxh.com/manga/hunter-x-hunter-chapter-"
VALID_IMAGE_SOURCES = ["laiond.com/images", "blogger.googleusercontent.com/img/b/"]

def get_image_urls(chapter_number):
    """Extracts all manga image URLs from a given chapter page."""
    chapter_url = f"{BASE_URL}{chapter_number}/"
    print(f"Fetching images from: {chapter_url}")
    
    response = requests.get(chapter_url)
    if response.status_code != 200:
        print(f"Failed to fetch Chapter {chapter_number}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    image_urls = [img.get('src') for img in soup.find_all('img') if img.get('src')]

    # Filter only valid image sources
    image_urls = [url for url in image_urls if any(source in url for source in VALID_IMAGE_SOURCES)]

    return image_urls



def create_pdf(output_pdf="HxH_383-410.pdf"):
    """Converts all downloaded images into a single PDF."""
    image_files = sorted(glob.glob("HxH/Chapter_*/[0-9]*.jpg"))  # Get all images in order
    
    if not image_files:
        print("No images found to create PDF!")
        return
    
    images = [Image.open(img).convert("RGB") for img in image_files]
    
    images[0].save(output_pdf, save_all=True, append_images=images[1:])
    print(f"PDF saved as {output_pdf}")



def download_images(image_urls, save_folder):
    """Downloads images from a list of URLs and saves them in the given folder."""
    os.makedirs(save_folder, exist_ok=True)

    for idx, img_url in enumerate(image_urls, start=1):
        try:
            img_data = requests.get(img_url).content
            file_path = os.path.join(save_folder, f"{idx}.jpg")
            with open(file_path, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded {img_url} -> {file_path}")
            #time.sleep(1)  # Avoid hitting rate limits
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

def main():
    for chapter in range(381, 411):  # From 383 to 410
        save_folder = f"HxH/Chapter_{chapter}"
        print(f"Processing Chapter {chapter}...")

        image_urls = get_image_urls(chapter)
        if not image_urls:
            print(f"No images found for Chapter {chapter}. Skipping...\n")
            continue

        download_images(image_urls, save_folder)
        print(f"Finished Chapter {chapter}!\n")
        
    create_pdf()

if __name__ == "__main__":
    main()