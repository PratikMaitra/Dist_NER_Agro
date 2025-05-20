import pandas as pd
import re

# Load the CSV file
file_path = "maize_traits_references_test.csv"
df = pd.read_csv(file_path)

# Open a file to write the output
with open("test.txt", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        title = str(row['reference title']) if pd.notnull(row['reference title']) else ""
        abstract = str(row['abstract']) if pd.notnull(row['abstract']) else ""
        traits = ""

        # Write title
        for word in title.strip().split():
            f.write(f"{word} O 0\n")
        f.write("\n")  # newline after title

        # Write abstract sentence by sentence
        sentences = re.split(r'(?<=[.])\s+', abstract.strip())
        for sentence in sentences:
            for word in sentence.strip().split():
                f.write(f"{word} O 0\n")
            f.write("\n")

        # Write traits at the end
        for word in traits.strip().split():
            f.write(f"{word} O 0\n")
        f.write("\n")

print("Finished writing to test.txt")
