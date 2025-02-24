import os
from pathlib import Path
from PyPDF2 import PdfMerger
from PIL import Image

# Explicitly define the chapters to verify they are unique
volumes = {
    16: list(range(134, 144)),  # Volume 16
    17: list(range(144, 154)),
    18: list(range(154, 165)),
    19: list(range(165, 176)),
    20: list(range(176, 188)),  # Volume 20
}

# Directories
chapter_dir = Path("/Users/adil/Downloads/ChainsawManChapters")
output_dir = Path("/Users/adil/Downloads/ChainsawManVolume")
cover_dir = Path("/Users/adil/Downloads/ChainsawManVolume")
temp_dir = Path("/Users/adil/Downloads/ChainsawTemp")

# Ensure output and temp directories exist
output_dir.mkdir(parents=True, exist_ok=True)
temp_dir.mkdir(parents=True, exist_ok=True)

def create_chapter_pdf(chapter_folder, chapter_number):
    """Convert chapter images into a single PDF."""
    chapter_number_str = f"{int(chapter_number):03d}"  # Zero-padded chapter number
    pdf_path = temp_dir / f"ChainsawMan_{chapter_number_str}.pdf"
    
    # Skip if the chapter PDF already exists
    if pdf_path.exists():
        print(f"Chapter PDF already exists: {pdf_path}")
        return pdf_path

    image_files = sorted(chapter_folder.glob("*.jpg"), key=lambda x: x.stem)
    if not image_files:
        print(f"Warning: No images found in {chapter_folder}")
        return None

    # Convert images to a PDF
    image_list = []
    for image_file in image_files:
        try:
            img = Image.open(image_file).convert("RGB")
            image_list.append(img)
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
    
    if image_list:
        # Save as PDF
        image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
        print(f"Created chapter PDF: {pdf_path}")
        return pdf_path
    else:
        print(f"Warning: No valid images in {chapter_folder}")
        return None

def add_cover_to_pdf(merger, volume_number):
    """Add the cover image as the first page of the PDF."""
    cover_image_path = cover_dir / f"Volume_{volume_number}.jpeg"
    if cover_image_path.exists():
        print(f"Adding cover image for Volume {volume_number} to the PDF.")
        # Convert the image to a single-page PDF before merging
        cover_pdf_path = temp_dir / f"Volume_{volume_number}_cover.pdf"
        if not cover_pdf_path.exists():
            image = Image.open(cover_image_path)
            image.convert("RGB").save(cover_pdf_path)
        merger.append(str(cover_pdf_path))
    else:
        print(f"Warning: Cover image for Volume {volume_number} not found.")

def create_volume(volume_number, chapters):
    """Combine chapter PDFs into a single volume PDF."""
    volume_filename = output_dir / f"ChainsawMan_Volume_{volume_number:02d}.pdf"
    
    # If the final volume already exists, skip
    if volume_filename.exists():
        print(f"Volume {volume_number} already exists. Skipping creation.")
        return

    merger = PdfMerger()

    # Add cover image as the first page
    add_cover_to_pdf(merger, volume_number)

    seen_chapters = set()  # To track chapters that have already been added
    processed_chapters = []  # For debugging duplicates

    # Add chapters to volume
    for chapter in chapters:
        chapter_folder = chapter_dir / f"Chapter_{chapter}"
        chapter_pdf = create_chapter_pdf(chapter_folder, chapter)
        
        if chapter_pdf:
            if chapter in seen_chapters:
                print(f"Skipping duplicate Chapter {chapter} within Volume {volume_number}")
                continue  # Skip adding this chapter as it's already added
            print(f"Adding Chapter {chapter} to Volume {volume_number}")
            merger.append(str(chapter_pdf))
            seen_chapters.add(chapter)  # Mark chapter as added
            processed_chapters.append(chapter)
        else:
            print(f"Chapter {chapter} could not be added.")

    # Debug: Print processed chapters for the volume
    print(f"Volume {volume_number} processed chapters: {processed_chapters}")

    # Write the combined volume PDF
    merger.write(str(volume_filename))
    
    # Now, close the merger after writing
    merger.close()
    print(f"Created {volume_filename} with chapters {chapters}.")

def main():
    """Main function to combine manga chapters into volumes."""
    # Check for duplicates in chapter ranges
    all_chapters = []
    for volume_num, chapters in volumes.items():
        all_chapters.extend(chapters)
        print(f"Volume {volume_num}: {chapters}")

    # Detect and warn if duplicate chapters exist across volumes
    duplicates = {chapter for chapter in all_chapters if all_chapters.count(chapter) > 1}
    if duplicates:
        print(f"Warning: Duplicate chapters detected across volumes: {duplicates}")

    # Create volumes
    for volume_num, chapters in volumes.items():
        create_volume(volume_num, chapters)

if __name__ == "__main__":
    main()