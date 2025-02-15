# Speech-to-Text Data Pipeline

A comprehensive pipeline for processing, transcribing, and analyzing lecture video content into structured speech data.

---
## **Setup Instructions**

### **Prerequisites**
Before running the scraper, ensure you have the following installed:
- **Google Chrome** (latest version) → [Download Chrome](https://www.google.com/chrome/)
- **Chrome WebDriver** → [Installation Guide](https://developer.chrome.com/docs/chromedriver/downloads)
- **FFmpeg** for audio processing
- **GNU Parallel** for parallel processing

### **Development Setup**

#### **1. Create a Virtual Environment**
To manage dependencies, create and activate a virtual environment:

```bash
# Create virtual environment (Both Windows and Unix)
python -m venv .env

# Activate virtual environment (macOS/Linux)
source .env/bin/activate

# Activate virtual environment (Windows Command Prompt)
.env\Scripts\activate.bat

# Activate virtual environment (Windows PowerShell)
.env\Scripts\Activate.ps1
```

#### **2. Install Dependencies**
Once the virtual environment is activated, install the required packages:
```bash
pip install -r requirements.txt
```

### **3. Install System Dependencies**

#### **FFmpeg Installation**
```bash
# macOS
brew install ffmpeg

# Windows (using Chocolatey)
choco install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg
```

#### **GNU Parallel Installation**
```bash
# macOS
brew install parallel

# Linux (Ubuntu/Debian)
sudo apt-get install parallel

# Windows
# Install WSL (Windows Subsystem for Linux) first, then:
wsl sudo apt-get install parallel
```

#### **Chrome Browser and ChromeDriver Installation**
```bash
# macOS
brew install chromedriver
```
For Windows/Linux, follow [this guide](https://developer.chrome.com/docs/chromedriver/downloads).

### **Note for Windows Users**
- If you encounter permission issues in PowerShell, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Use backslashes (`\`) instead of forward slashes (`/`) for file paths.
- Run commands in Command Prompt or PowerShell as Administrator if needed.

---
## **Data Collection Process**

### **1. Web Scraping and Downloads**
Run the following command to start the data collection pipeline:
```bash
python app.py
```
This process:
- Scrapes **lecture content** from NPTEL course pages.
- Extracts **transcript URLs** and **YouTube video URLs**.
- Displays real-time progress for each unit and lesson.
- Downloads lectures and transcripts into the following structure:
  ```
  speech-to-text/
  ├── lectures/           # Downloaded video lectures
  │   ├── lecture_1.mp4
  │   ├── lecture_2.mp4
  │   └── ...
  └── transcripts/        # Downloaded transcripts
      ├── lecture_1.txt
      ├── lecture_2.txt
      └── ...
  ```

---
## **2. Audio Preprocessing**

The `preprocess_audio.sh` script optimizes lecture videos for speech recognition.

#### **Make the script executable:**
```bash
chmod +x preprocess_audio.sh
```

#### **Run the script:**
```bash
./preprocess_audio.sh <input_dir> <output_dir> <num_cpus>
```

#### **Processing Steps:**
1. Converts audio to **WAV format** (16kHz, mono)
2. Removes **intro (first 10s)** and **outro (last 20s)**
3. Normalizes **audio volume**
4. Skips files **shorter than 30 seconds**
5. Utilizes **parallel processing**

---
## **3. Text Preprocessing (Transcripts)**
The `preprocess_texts.py` script processes transcript files for speech-to-text.

#### **Features:**
- Converts text to **lowercase**
- Removes **punctuation**
- Converts **numbers to words**
- Processes all `.txt` files **in batch**

#### **Directory Structure:**
```
speech-to-text/
├── transcripts/             # Input folder with original transcripts
└── preprocessed_transcripts/# Output folder with processed texts
```

#### **Usage:**
```bash
python preprocess_texts.py
```
This will:
1. Read `.txt` files from `transcripts/`
2. Apply text preprocessing rules
3. Save output to `preprocessed_transcripts/`

---
## **4. Manifest Creation**
The `create_manifest.py` script pairs preprocessed audio files with transcripts.
This script generates a JSON Lines (JSONL) training manifest compatible with speech-to-text models like NVIDIA NeMo. This manifest is essential for training, as it pairs preprocessed audio files with their corresponding transcripts, ensuring proper alignment of speech data.

#### **Features:**
- Matches audio files with corresponding transcripts
- Calculates **audio duration** using `ffprobe`
- Generates a **JSONL manifest**

#### **Directory Structure:**
```
speech-to-text/
└── preprocessed_data/
    ├── preprocessed_audios/
    ├── preprocessed_transcripts/
    └── train_manifest.jsonl
```

#### **Usage:**
```bash
python create_manifest.py
```
This will:
1. Find WAV files in `preprocessed_data/preprocessed_audios/`
2. Match them with transcripts in `preprocessed_data/preprocessed_transcripts/`
3. Generate `train_manifest.jsonl` with structured data

#### **Output Format:**
```json
{
    "audio_filepath": "/absolute/path/to/audio.wav",
    "duration": 123.45,
    "text": "transcribed text content"
}
```

---
## **5. Dataset Statistics**
The `compute_stats.py` script analyzes the dataset and generates statistics.

#### **Features:**
- Computes **total utterances, duration, vocabulary size, and alphabet size**
- Analyzes **word and character counts**
- Outputs results in **JSON and CSV formats**

#### **Output Files:**
1. **Overall Statistics (`overall_stats.json`)**:
```json
{
    "total_utterances": 117,
    "total_duration_hours": 25.09,
    "vocabulary_size": 8091,
    "alphabet_size": 38,
    "complete_alphabet": "abcdefghijklmnopqrstuvwxyz..."
}
```

2. **Per-file Statistics (`per_file_stats.csv`)**:
   - Duration
   - Word count
   - Character count

#### **Usage:**
```bash
python compute_stats.py
```

#### **Notes:**
- The script **normalizes text** (lowercase, removes punctuation)
- **Excludes whitespace** in alphabet size calculation
- **Duration** is converted to **hours** for readability

---
## **Conclusion**
This pipeline efficiently **scrapes, processes, and analyzes** lecture video content, making it ready for speech-to-text applications.

If you encounter any issues, refer to the [ChromeDriver Installation Guide](https://developer.chrome.com/docs/chromedriver/downloads) or check system dependencies.



