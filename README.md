# Manga Volume2Chapter

**Volume2Chapter** is a Python program designed to automate the process of combining individual manga chapters (in `.cbz` format) into organized volumes. It supports adding a cover image for each volume and ensures chapters are grouped in the correct order based on predefined ranges.

## Features
- Automatically combines manga chapters into volumes.
- Adds a cover image for each volume (named `Volume_x.jpeg`).
- Handles `.cbz` files (zip-compressed CBZ manga chapters).
- Customizable volume and chapter ranges for any manga series.

## Installation

### Prerequisites
Ensure that you have the following installed on your system:
- Python 3.x
- `zipfile` module (included with Python's standard library)
- `pathlib` (included with Python's standard library)

### Steps to Install

1. Clone or download the repository:
    ```bash
    git clone https://github.com/Didilusse/Volume2Chapter.git
    ```
    or download the ZIP and extract it.

2. Install the necessary dependencies (if any):
    - This script uses Python's standard libraries, so there are no additional dependencies to install.

## Usage
### How to Run the Script

1. Prepare the directory with all your `.cbz` files and cover images. Place the `Volume_x.jpeg` cover image files for each volume in the same directory.

2. Update the `input_dir` and `output_dir` variables in the script to reflect the correct paths for your manga chapter files and where you'd like the combined volumes to be saved:
    ```python
    input_dir = Path("/path/to/your/manga")
    output_dir = Path("/path/to/save/combined/volumes")
    ```

3. Run the script:
    ```bash
    python main.py
    ```

The script will combine the chapters for each volume, add the respective cover image (if available), and create a new `.cbz` file for each volume in the output directory.

### Example

Given the chapters and volumes defined in the script:

- Volume 10: Chapters 77-85
- Volume 11: Chapters 86-93
- ...

The program will create `.cbz` files like:

- `Volume_10.cbz` (with chapters 77 to 85)
- `Volume_11.cbz` (with chapters 86 to 93)
- ...

If the cover image `Volume_10.jpeg` exists, it will be included as `!cover.jpg` inside the `Volume_10.cbz` file.

## Contributing

Feel free to fork the repository, submit issues, and make pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

