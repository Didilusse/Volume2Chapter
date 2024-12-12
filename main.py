import os
import zipfile
from pathlib import Path
import re

# Define volumes and chapters
volumes = {
    10: range(77, 86),
    11: range(86, 94),
    12: range(94, 103),
    13: range(103, 112),
    14: range(112, 121),
    15: range(121, 130),
    16: range(130, 139),
    17: range(139, 148),
}

# Directories
input_dir = Path("/Users/adil/Downloads/DanDaDanChapter")  # Path to your CBZ chapter files
output_dir = Path("/Users/adil/Downloads/DanDaDanVolume")  # Path to save volumes
cover_dir = Path("/Users/adil/Downloads/DanDaDanChapter")    # Path to your cover images

# Ensure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

def find_chapter_files(chapter_number, files):
    """Find chapter files matching the chapter number."""
    chapter_number_str = f"{int(chapter_number):03d}"  # Zero-padded number
    pattern = re.compile(rf"Dandadan {chapter_number_str}\.cbz")
    matched_files = [file for file in files if pattern.match(file.name)]
    
    if not matched_files:
        print(f"Warning: No files found for Chapter {chapter_number_str}")
    return matched_files

def add_cover_to_volume(volume_number, volume_zip):
    """Add the cover image to the .cbz archive, renamed as !cover.jpg."""
    cover_image_path = cover_dir / f"Volume_{volume_number}.jpeg"
    if cover_image_path.exists():
        with open(cover_image_path, "rb") as cover_file:
            cover_data = cover_file.read()
            volume_zip.writestr("!cover.jpg", cover_data)  # Add as '!cover.jpg'
            print(f"Added cover image {cover_image_path.name} to volume.")
    else:
        print(f"Warning: Cover image for Volume {volume_number} not found.")

def create_volume(volume_number, chapters, all_files):
    """Combine chapter files into a single volume and add the cover image."""
    volume_filename = output_dir / f"Volume_{volume_number:02d}.cbz"
    
    with zipfile.ZipFile(volume_filename, 'w') as volume_zip:
        # Add chapters to volume
        for chapter in chapters:
            chapter_files = find_chapter_files(chapter, all_files)
            for chapter_file in chapter_files:
                with zipfile.ZipFile(chapter_file, 'r') as chapter_zip:
                    for file in chapter_zip.namelist():
                        # Write files from the chapter ZIP into the volume ZIP
                        content = chapter_zip.read(file)
                        volume_zip.writestr(f"Chapter_{chapter}/{file}", content)
        
        # Add cover image to volume
        add_cover_to_volume(volume_number, volume_zip)
        
        print(f"Created {volume_filename} with chapters {chapters}.")

def main():
    """Main function to combine manga chapters into volumes."""
    # Get all .cbz files in the input directory
    all_cbz_files = sorted(input_dir.glob("*.cbz"))
    
    # Create volumes
    for volume_num, chapters in volumes.items():
        create_volume(volume_num, chapters, all_cbz_files)

if __name__ == "__main__":
    main()