import os
import requests
from PIL import Image
from fpdf import FPDF
from PyPDF2 import PdfMerger

# Updated base URL format
BASE_URL = "https://cdn.readkakegurui.com/file/cdnpogx/spy-x-family/chapter-{chapter}/{page}.webp"

SAVE_DIR = "SpyXFamily"
VOLUMES_DIR = os.path.join(SAVE_DIR, "Volumes")
CHAPTERS_DIR = os.path.join(SAVE_DIR, "Chapters")
COVERS_DIR = os.path.join(SAVE_DIR, "Covers")

VOLUMES = {
    "Volume_15": [100, 101, 102, 103, 104, 105, 105.5, 106, 107, 108, 109, 110, 111],
}

# Ensure directories exist
for folder in [SAVE_DIR, CHAPTERS_DIR, VOLUMES_DIR]:
    os.makedirs(folder, exist_ok=True)


def sanitize_filename(name):
    """Replace invalid filename characters."""
    return str(name).replace(".", "_")


def download_image(chapter, page):
    """Download a .webp image for a given chapter and page, then convert it to .jpg."""
    chapter_folder = os.path.join(CHAPTERS_DIR, f"Chapter_{sanitize_filename(chapter)}")
    os.makedirs(chapter_folder, exist_ok=True)

    img_url = BASE_URL.format(chapter=chapter, page=page)
    webp_path = os.path.join(chapter_folder, f"Page_{page}.webp")
    jpg_path = os.path.join(chapter_folder, f"Page_{page}.jpg")

    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        with open(webp_path, "wb") as file:
            file.write(response.content)
        print(f"📥 Downloaded: Chapter {chapter}, Page {page}")

        # Convert WebP to JPG
        try:
            with Image.open(webp_path) as img:
                img.convert("RGB").save(jpg_path, "JPEG")
            os.remove(webp_path)  # Remove WebP file
            return jpg_path
        except Exception as e:
            print(f"🚨 Failed to convert {webp_path} to JPG: {e}")
            return None
    else:
        print(f"🚨 Failed to download Chapter {chapter}, Page {page}")
        return None


def convert_images_to_pdf(chapter):
    """Convert all downloaded chapter images into a single PDF."""
    chapter_folder = os.path.join(CHAPTERS_DIR, f"Chapter_{sanitize_filename(chapter)}")
    pdf_path = os.path.join(chapter_folder, f"Chapter_{sanitize_filename(chapter)}.pdf")
    pdf = FPDF()

    page = 1
    while True:
        img_path = os.path.join(chapter_folder, f"Page_{page}.jpg")
        if not os.path.exists(img_path):
            break

        try:
            pdf.add_page()
            pdf.image(img_path, 0, 0, 210, 297)
        except Exception as e:
            print(f"🚨 Error adding {img_path} to PDF: {e}")

        page += 1

    if pdf.page_no() > 0:
        pdf.output(pdf_path, "F")
        print(f"📄 Created PDF: {pdf_path}")
    else:
        print(f"⚠️ No valid images for Chapter {chapter}, skipping PDF creation.")


def process_chapters():
    """Download and convert all chapters into PDFs."""
    all_chapters = [ch for volume in VOLUMES.values() for ch in volume]

    for chapter in all_chapters:
        page = 1
        while True:
            img_path = download_image(chapter, page)
            if not img_path:
                break  # Stop downloading when no more pages exist
            page += 1

        convert_images_to_pdf(chapter)



def create_cover_pdf(volume_name):
    """Convert the cover image from the Covers folder into a PDF file."""
    cover_img_path = os.path.join(COVERS_DIR, f"{volume_name}.jpeg")
    cover_pdf_path = os.path.join(COVERS_DIR, f"{volume_name}.pdf")

    print(f"Checking cover for {volume_name}: {cover_img_path}")  # Debugging line

    if not os.path.exists(cover_img_path):
        print(f"⚠️ Cover image missing: {cover_img_path}")
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.image(cover_img_path, 0, 0, 210, 297)
    pdf.output(cover_pdf_path, "F")
    return cover_pdf_path



def compile_volumes():
    """Merge chapter PDFs into their respective volume PDFs, including covers."""
    for volume_name, chapters in VOLUMES.items():
        volume_pdf_path = os.path.join(VOLUMES_DIR, f"{volume_name}.pdf")
        merger = PdfMerger()

        # Add cover first
        cover_pdf = create_cover_pdf(volume_name)
        if cover_pdf:
            merger.append(cover_pdf)
            print(f"📖 Added Cover for {volume_name}")

        for chapter in chapters:
            chapter_folder = os.path.join(CHAPTERS_DIR, f"Chapter_{sanitize_filename(chapter)}")
            chapter_pdf = os.path.join(chapter_folder, f"Chapter_{sanitize_filename(chapter)}.pdf")

            if os.path.exists(chapter_pdf):
                merger.append(chapter_pdf)
                print(f"📖 Added Chapter {chapter} to {volume_name}")
            else:
                print(f"⚠️ Missing Chapter {chapter}, skipping.")

        if len(merger.pages) > 0:
            merger.write(volume_pdf_path)
            merger.close()
            print(f"📚 {volume_name}.pdf compiled successfully.")
        else:
            print(f"⚠️ No chapters found for {volume_name}, skipping.")



# Run the script
process_chapters()
compile_volumes()