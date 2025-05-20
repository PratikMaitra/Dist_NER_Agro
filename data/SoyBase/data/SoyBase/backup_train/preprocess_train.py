import pandas as pd
import re

# Load the cleaned Excel file
file_path = "pmid_cleaned.xlsx"
df = pd.read_excel(file_path)

# Open a file to write the output
with open("train.txt", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        title = str(row['Title']) if pd.notnull(row['Title']) else ""
        abstract = str(row['Abstract']) if pd.notnull(row['Abstract']) else ""

        # Write the title, word by word
        for word in title.strip().split():
            f.write(f"{word} O 0\n")
        f.write("\n")  # Newline after title

        # Split abstract into sentences and then into words
        abstract_sentences = re.split(r'(?<=[.!?])\s+', abstract.strip())

        for sentence in abstract_sentences:
            for word in sentence.strip().split():
                f.write(f"{word} O 0\n")
            f.write("\n")  # Newline after each sentence

print("Finished writing to train.txt")
