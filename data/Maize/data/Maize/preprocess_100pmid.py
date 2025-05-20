import pandas as pd
import re

# Load the Excel file
file_path = "maize_100pmid.xlsx"
df = pd.read_excel(file_path)

# Open a file to write the output
with open("train_maize100.txt", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        title = str(row['title']) if pd.notnull(row['title']) else ""
        abstract = str(row['abstract']) if pd.notnull(row['abstract']) else ""

        # Write the title
        for word in title.strip().split():
            f.write(f"{word} O 0\n")
        f.write("\n")  # Newline after title

        # Split abstract into sentences using punctuation
        abstract_sentences = re.split(r'(?<=[.!?])\s+', abstract.strip())

        for sentence in abstract_sentences:
            for word in sentence.strip().split():
                f.write(f"{word} O 0\n")
            f.write("\n")  # Newline after each sentence

print("Finished writing to train.txt")
