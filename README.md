![SibnetDL](SibnetDL.png)

# SibnetDL

## Overview

SibnetDL is a Python-based application offering a user-friendly interface for downloading videos from a list of URLs. This tool utilizes PyQt5 for its GUI and pySmartDL for downloading videos. The application allows users to manage video download tasks from sibnet.ru links provided in a text file. 

**Note:** _This app specifically get sibnet links from [cizgivedizi.com](https://www.cizgivedizi.com)_

### Features

- **URL List Creation**: Generate a list of URLs for video download.
- **Download Link Retrieval**: Obtain links for downloading videos.
- **Video Download**: Download videos from sibnet.ru links.
- **User-friendly Interface**: A clean and straightforward UI for a seamless user experience.

## Installation

1. Ensure you have Python installed.
2. Clone the repository to your local machine.
3. Install the required packages: `pip install -r requirements.txt`.
4. Run the application: `python sibnetDL.py`.

Or you can download lastest [Release](https://github.com/mickiemouse/SibnetDL/releases).

## Usage

1. **Creating a URL List**
    - Click on the "Create" tab and fill in the URL and the total number of video episodes.
    - Click "Generate Episode Links" to create a file containing the URLs.

2. **Retrieving Download Links**
    - Click on the "Retrieve" tab to extract download links from the generated URL list.
    - Select the desired file and destination folder.

3. **Downloading Videos**
    - Choose the text file with the URLs and the destination folder.
    - Click "Start" to initiate the download process.

## Contribution

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/AmazingFeature`.
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`.
4. Push to the branch: `git push origin feature/AmazingFeature`.
5. Open a pull request.

## License

Distributed under the GPLv3 License. See `LICENSE` for more information.
