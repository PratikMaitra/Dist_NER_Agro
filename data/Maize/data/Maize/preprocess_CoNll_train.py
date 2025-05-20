import pandas as pd
import re

# Load the CSV file
file_path = "maize_references_labeled_train.csv"
df = pd.read_csv(file_path)

# Open a file to write the output
with open("train.txt", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        title = str(row['title']) if pd.notnull(row['title']) else ""
        abstract = str(row['abstract']) if pd.notnull(row['abstract']) else ""

        # Write the title
        for word in title.strip().split():
            f.write(f"{word} O 0\n")
        f.write("\n")  # Newline after title

        # Add newlines after sentence-ending punctuation in the abstract
        abstract_sentences = re.split(r'(?<=[.!?])\s+', abstract.strip())

        for sentence in abstract_sentences:
            for word in sentence.strip().split():
                f.write(f"{word} O 0\n")
            f.write("\n")  # Newline after each sentence

print("Finished writing to train.txt")
