import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import requests

# Directory to save the PDFs
output_dir = "/Users/adil/Downloads/ChainsawManVolume"
os.makedirs(output_dir, exist_ok=True)

# Base URL for the manga chapters
base_url = "https://ww4.readchainsawman.com/chapter/"

# Mapping of site chapters to actual series chapters
site_to_actual_mapping = {
    37: 134, 38: 135, 39: 136, 40: 137, 41: 138, 42: 139,
    43: 140, 44: 141, 45: 142, 46: 143, 47: 144, 48: 145,
    49: 146, 50: 147, 51: 148, 52: 149, 53: 150, 54: 151,
    55: 152, 56: 153, 57: 154, 58: 155, 59: 156, 60: 157,
    61: 158, 62: 159, 63: 160, 64: 161, 65: 162, 66: 163,
    67: 164, 68: 165, 69: 166, 70: 167, 71: 168, 72: 169,
    73: 170, 74: 171, 75: 172, 76: 173, 77: 174, 78: 175,
    79: 176, 80: 177, 81: 178, 82: 179, 83: 180, 84: 181,
    85: 182, 86: 183, 87: 184, 88: 185, 89: 186, 90: 187
}

# Function to initialize the WebDriver
def initialize_driver():
    # Setup Chrome WebDriver (using webdriver_manager to automatically manage chromedriver)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

# Function to download images for a specific chapter
def download_chapter_images(driver, chapter_url, chapter_number):
    print(f"Accessing: {chapter_url}")
    driver.get(chapter_url)

    # Wait for the images to load
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.js-page")))
    except Exception as e:
        print(f"Error: Unable to load images for {chapter_url}: {e}")
        return None

    # Extract image URLs
    img_elements = driver.find_elements(By.CSS_SELECTOR, "img.js-page")
    if not img_elements:
        print(f"No images found for Chapter {chapter_number}.")
        return None

    chapter_folder = os.path.join(output_dir, f"chapter_{chapter_number}")
    os.makedirs(chapter_folder, exist_ok=True)

    img_count = 1
    for img_element in img_elements:
        img_url = img_element.get_attribute("src")
        if not img_url:
            continue

        try:
            # Save the images in sequential order
            img_filename = os.path.join(chapter_folder, f"{img_count:03d}.jpg")
            img_data = requests.get(img_url).content
            with open(img_filename, "wb") as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {img_filename}")
            img_count += 1
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")

    return chapter_folder

# Main function to download and compile all chapters into volumes
def compile_volumes():
    driver = initialize_driver()

    for site_chapter, actual_chapter in site_to_actual_mapping.items():
        chapter_url = f"{base_url}chainsaw-man-part-2-chapter-{site_chapter}/"
        print(f"Processing Chapter {actual_chapter} from {chapter_url}...")

        chapter_folder = download_chapter_images(driver, chapter_url, actual_chapter)
        time.sleep(1)  # Short delay between requests to avoid rate limiting

    driver.quit()  # Don't forget to close the driver once done!

if __name__ == "__main__":
    compile_volumes()