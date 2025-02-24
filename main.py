import os
from pathlib import Path
from PyPDF2 import PdfMerger
import re

# Define volumes and chapters
volumes = {
    18: range(162, 177)
}

# Directories
input_dir = Path("/Users/adil/Downloads/DanDaDanChapter")  # Path to your PDF chapter files
output_dir = Path("/Users/adil/Downloads/DanDaDanVolume")  # Path to save volumes
cover_dir = Path("/Users/adil/Downloads/DanDaDanChapter")  # Path to your cover images

# Ensure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

def find_chapter_files(chapter_number, files):
    """Find chapter files matching the chapter number."""
    chapter_number_str = f"{int(chapter_number):03d}"  # Zero-padded number
    pattern = re.compile(rf"Dandadan {chapter_number_str}\.pdf")
    matched_files = [file for file in files if pattern.match(file.name)]
    
    if not matched_files:
        print(f"Warning: No files found for Chapter {chapter_number_str}")
    return matched_files

def add_cover_to_pdf(merger, volume_number):
    """Add the cover image as the first page of the PDF."""
    cover_image_path = cover_dir / f"Volume_{volume_number}.jpeg"
    if cover_image_path.exists():
        print(f"Adding cover image for Volume {volume_number} to the PDF.")
        # Convert the image to a single-page PDF before merging
        from PIL import Image
        cover_pdf_path = cover_image_path.with_suffix(".pdf")
        image = Image.open(cover_image_path)
        image.convert("RGB").save(cover_pdf_path)
        merger.append(str(cover_pdf_path))
    else:
        print(f"Warning: Cover image for Volume {volume_number} not found.")

def create_volume(volume_number, chapters, all_files):
    """Combine chapter PDFs into a single volume PDF."""
    volume_filename = output_dir / f"Volume_{volume_number:02d}.pdf"
    merger = PdfMerger()

    # Add cover image as the first page
    add_cover_to_pdf(merger, volume_number)

    # Add chapters to volume
    for chapter in chapters:
        chapter_files = find_chapter_files(chapter, all_files)
        for chapter_file in chapter_files:
            print(f"Adding Chapter {chapter}: {chapter_file.name}")
            merger.append(str(chapter_file))
    
    # Write the combined volume PDF
    merger.write(str(volume_filename))
    merger.close()
    print(f"Created {volume_filename} with chapters {chapters}.")

def main():
    """Main function to combine manga chapters into volumes."""
    # Get all .pdf files in the input directory
    all_pdf_files = sorted(input_dir.glob("*.pdf"))
    
    # Create volumes
    for volume_num, chapters in volumes.items():
        create_volume(volume_num, chapters, all_pdf_files)

if __name__ == "__main__":
    main()