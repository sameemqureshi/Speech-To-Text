import os
import json
import pandas as pd
import string

# Path to your manifest file
manifest_file = os.path.join(os.getcwd(), "preprocessed_data", "train_manifest.jsonl")

# Read the manifest file into a DataFrame
records = []
with open(manifest_file, "r", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))
df = pd.DataFrame(records)

# Total number of utterances
total_utterances = len(df)

# Total duration in hours
total_duration_hours = df['duration'].sum() / 3600

# Preprocess transcripts: lower case and remove punctuation
def preprocess_text(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.lower().translate(translator)

df['processed_text'] = df['text'].apply(preprocess_text)

# Vocabulary: unique words (split by whitespace)
all_words = []
for text in df['processed_text']:
    all_words.extend(text.split())
vocabulary = set(all_words)
vocab_size = len(vocabulary)

# Alphabet: unique characters (we can remove whitespace)
all_chars = set("".join(df['processed_text']).replace(" ", ""))
alphabet_size = len(all_chars)
complete_alphabet = sorted(all_chars)

# Compute words and characters per file
df['num_words'] = df['processed_text'].apply(lambda x: len(x.split()))
df['num_chars'] = df['processed_text'].apply(lambda x: len(x.replace(" ", "")))

# Print overall stats
print(f"Total number of utterances: {total_utterances}")
print(f"Total number of hours: {total_duration_hours:.2f}")
print(f"Vocabulary size: {vocab_size}")
print(f"Alphabet size: {alphabet_size}")
print("Complete Alphabet:", complete_alphabet)

# Save overall statistics to a CSV (or JSON) file
overall_stats = {
    "total_utterances": total_utterances,
    "total_duration_hours": total_duration_hours,
    "vocabulary_size": vocab_size,
    "alphabet_size": alphabet_size,
    "complete_alphabet": "".join(complete_alphabet)
}
with open("overall_stats.json", "w", encoding="utf-8") as f:
    json.dump(overall_stats, f, indent=2)

# Save per-file distributions for histograms
df[['duration', 'num_words', 'num_chars']].to_csv("per_file_stats.csv", index=False)

# Optionally, you can also save overall stats as CSV:
pd.DataFrame([overall_stats]).to_csv("overall_stats.csv", index=False)
