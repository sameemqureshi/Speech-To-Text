#!/bin/bash

# Get input arguments
INPUT_DIR="$1"
OUTPUT_DIR="$2"
N_CPUS="$3"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

convert_audio() {
    local input_file="$1"
    local output_file="$OUTPUT_DIR/$(basename "$input_file" | sed 's/\.[^.]*$/.wav/')"

    echo "Processing: $(basename "$input_file")"

    # Get total duration of the audio file
    total_duration=$(ffmpeg -i "$input_file" 2>&1 | grep "Duration" | awk '{print $2}' | tr -d ,)
    
    if [[ -z "$total_duration" ]]; then
        echo "❌ Error: Could not determine duration for $input_file"
        return
    fi

    # Convert duration to seconds
    IFS=: read -r h m s <<< "$total_duration"
    duration_in_seconds=$(echo "$h*3600 + $m*60 + $s" | bc)

    # Ensure the file is long enough for trimming
    if (( $(echo "$duration_in_seconds < 30" | bc -l) )); then
        echo "⚠️ Skipping: $(basename "$input_file") (Duration too short for trimming)"
        return
    fi

    # Calculate new duration excluding the last 30 seconds
    trim_duration=$(echo "$duration_in_seconds - 40" | bc)

    echo "Removing intro (first 10s) and outro (last 20s)..."

    # Convert, trim, normalize volume, and save as WAV
    ffmpeg -i "$input_file" -ac 1 -ar 16000 -ss 10 -t "$trim_duration" -af "volume=1.0" "$output_file" -y

    if [ -f "$output_file" ]; then
        echo "✅ Processed: $(basename "$output_file")"
    else
        echo "❌ Failed to process: $(basename "$input_file")"
    fi
}

export -f convert_audio
export OUTPUT_DIR

# Find all audio files and process them in parallel
find "$INPUT_DIR" -type f \( -name "*.mp4" -o -name "*.wav" -o -name "*.m4a" -o -name "*.aac" \) | parallel -j "$N_CPUS" convert_audio {}

echo "✅ All audio files processed successfully!"
