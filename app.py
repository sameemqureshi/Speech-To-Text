import os
import requests
from pypdf import PdfReader
from tqdm import tqdm
import yt_dlp
from web_scraper_script import get_all_transcripts_urls , get_all_lectre_urls
# Ensure the required folders exist
os.makedirs("pdfs", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

def download_pdf(drive_url, save_path):
    """
    Downloads a PDF file from a Google Drive URL.
    """
    try:
        file_id = drive_url.split("/d/")[1].split("/view")[0]
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as pdf_file:
                for chunk in response.iter_content(1024):
                    pdf_file.write(chunk)
            print(f"✅ Downloaded PDF: {save_path}")
        else:
            print(f"❌ Failed to download PDF: {drive_url}")
    except Exception as e:
        print(f"⚠ Error downloading {drive_url}: {e}")

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file using pypdf.
    """
    try:
        reader = PdfReader(pdf_path)
        extracted_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        return extracted_text.strip()
    except Exception as e:
        print(f"⚠ Error extracting text from {pdf_path}: {e}")
        return ""

def save_text_to_file(text, text_file_path):
    """
    Saves extracted text to a .txt file.
    """
    try:
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)
        print(f"✅ Saved extracted text: {text_file_path}")
    except Exception as e:
        print(f"⚠ Error saving text file {text_file_path}: {e}")



os.makedirs("lectures", exist_ok=True)
def download_lecture(video_url, output_folder="lectures"):
    """
    Downloads a YouTube video using yt-dlp.
    """
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",  # Best quality available
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),  # Save as title.mp4
        "merge_output_format": "mp4",  # Ensure MP4 format
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"✅ Downloaded: {video_url}")
    except Exception as e:
        print(f"❌ Failed to download {video_url}: {e}")



def main():
    """
    Main function to download and process both transcripts and lectures
    """
    print("Starting downloads...")

    # Part 1: Download transcripts
    transcripts_urls = get_all_transcripts_urls()
    print(f"Found {len(transcripts_urls)} transcripts to process")

    for idx, url in enumerate(tqdm(transcripts_urls, desc="Processing PDFs")):
        pdf_filename = f"pdfs/lecture_{idx+1}.pdf"
        text_filename = f"transcripts/lecture_{idx+1}.txt"

        download_pdf(url, pdf_filename)
        extracted_text = extract_text_from_pdf(pdf_filename)
        save_text_to_file(extracted_text, text_filename)

    # Part 2: Download lectures
    lectures_urls = get_all_lectre_urls()
    print(f"Found {len(lectures_urls)} lectures to download")

    os.makedirs("lectures", exist_ok=True)
    for url in tqdm(lectures_urls, desc="Downloading lectures"):
        download_lecture(url)

    print("✅ All downloads completed!")

if __name__ == "__main__":
    main()

