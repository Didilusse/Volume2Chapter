import os
import requests
from PIL import Image
from fpdf import FPDF
from PyPDF2 import PdfMerger

BASE_URL = "https://cdn.readkakegurui.com/file/cdnpog/mashle-manga/chapter-{}/{}.webp"
CHAPTERS = list(range(75, 163))  # Chapters 75 to 162
PAGES_PER_CHAPTER = 20  # Estimated max pages per chapter

# Volume chapter mapping
VOLUMES = {
    "Volume_09": list(range(75, 83)),
    "Volume_10": list(range(83, 92)),
    "Volume_11": list(range(92, 101)),
    "Volume_12": list(range(101, 110)),
    "Volume_13": list(range(110, 119)),
    "Volume_14": list(range(119, 128)),
    "Volume_15": list(range(128, 137)),
    "Volume_16": list(range(137, 146)),
    "Volume_17": list(range(146, 155)),
    "Volume_18": list(range(155, 163)),
}

SAVE_DIR = "Mashle_Manga"
CHAPTERS_DIR = os.path.join(SAVE_DIR, "Chapters")
VOLUMES_DIR = os.path.join(SAVE_DIR, "Volumes")

# Ensure directories exist
os.makedirs(CHAPTERS_DIR, exist_ok=True)
os.makedirs(VOLUMES_DIR, exist_ok=True)

def download_image(url, path):
    """Downloads an image and saves it."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, "wb") as file:
            file.write(response.content)
        return True
    return False

def convert_webp_to_jpg(webp_path, jpg_path):
    """Converts .webp image to .jpg format."""
    with Image.open(webp_path) as img:
        img.convert("RGB").save(jpg_path, "JPEG")
    os.remove(webp_path)  # Delete the original .webp file

def create_pdf(images, pdf_path):
    """Creates a PDF from a list of images."""
    pdf = FPDF()
    for image in images:
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)  # A4 size
    pdf.output(pdf_path, "F")

def download_chapter(chapter):
    """Downloads all pages of a chapter and creates a PDF."""
    chapter_folder = os.path.join(CHAPTERS_DIR, f"Chapter_{chapter}")
    os.makedirs(chapter_folder, exist_ok=True)

    images = []
    for page in range(1, PAGES_PER_CHAPTER + 1):
        img_path = os.path.join(chapter_folder, f"{page}.webp")
        jpg_path = img_path.replace(".webp", ".jpg")

        url = BASE_URL.format(chapter, page)
        if not download_image(url, img_path):
            break  # Stop if the page does not exist

        convert_webp_to_jpg(img_path, jpg_path)
        images.append(jpg_path)

    if images:
        pdf_path = os.path.join(CHAPTERS_DIR, f"Chapter_{chapter}.pdf")
        create_pdf(images, pdf_path)
        print(f"Chapter {chapter} saved as PDF.")
    else:
        print(f"No images found for Chapter {chapter}.")

def create_volume_cover_pdf(volume_name):
    """Creates a PDF for the volume cover and returns its path."""
    cover_webp = os.path.join(SAVE_DIR, f"{volume_name}.webp")
    cover_jpg = cover_webp.replace(".webp", ".jpg")
    cover_pdf = os.path.join(VOLUMES_DIR, f"{volume_name}_cover.pdf")

    if not os.path.exists(cover_webp):
        print(f"⚠️ Warning: {volume_name} cover not found! Skipping cover.")
        return None

    # Convert .webp to .jpg
    convert_webp_to_jpg(cover_webp, cover_jpg)

    # Create PDF with the cover
    pdf = FPDF()
    pdf.add_page()
    pdf.image(cover_jpg, 0, 0, 210, 297)  # Full-page A4 size
    pdf.output(cover_pdf, "F")
    print(f"✅ {volume_name} cover saved as PDF.")

    return cover_pdf  # Return path to use in merging

def compile_volumes():
    """Merges chapter PDFs into their respective volumes using PyPDF2."""
    for volume, chapters in VOLUMES.items():
        volume_pdf_path = os.path.join(VOLUMES_DIR, f"{volume}.pdf")
        cover_jpg = os.path.join(SAVE_DIR, f"{volume}.jpg")
        cover_pdf = os.path.join(VOLUMES_DIR, f"{volume}_cover.pdf")

        # Check if the cover exists
        if not os.path.exists(cover_jpg):
            print(f"🚨 ERROR: Cover {cover_jpg} not found!")
        else:
            print(f"✅ Found cover: {cover_jpg}")

        # Convert JPG to PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.image(cover_jpg, 0, 0, 210, 297)  # A4 size
        pdf.output(cover_pdf, "F")

        merger = PdfMerger()
        merger.append(cover_pdf)

        # Add all chapters
        for chapter in chapters:
            chapter_pdf = os.path.join(CHAPTERS_DIR, f"Chapter_{chapter}.pdf")
            if os.path.exists(chapter_pdf):
                merger.append(chapter_pdf)
                print(f"✅ Added: {chapter_pdf}")
            else:
                print(f"🚨 ERROR: Missing {chapter_pdf}")

        # Save final volume PDF
        merger.write(volume_pdf_path)
        merger.close()
        print(f"📖 {volume} compiled successfully.\n")

def main():
    # Step 1: Download all chapters
    #for chapter in CHAPTERS:
        #download_chapter(chapter)

    # Step 2: Compile volumes
    compile_volumes()

if __name__ == "__main__":
    main()