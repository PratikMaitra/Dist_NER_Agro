import pandas as pd
import re

# Load the Grain.xlsx file
df = pd.read_excel("Grain.xlsx")

# Use the full DataFrame for both train and test
train_df, test_df = df, df

def write_to_file(dataframe, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for _, row in dataframe.iterrows():
            title = str(row['Title']) if pd.notnull(row['Title']) else ""
            abstract = str(row['Abstract']) if pd.notnull(row['Abstract']) else ""

            # Write the title
            for word in title.strip().split():
                f.write(f"{word} O 0\n")
            f.write("\n")

            # Write the abstract with sentence-based newlines
            abstract_sentences = re.split(r'(?<=[.!?])\s+', abstract.strip())
            for sentence in abstract_sentences:
                for word in sentence.strip().split():
                    f.write(f"{word} O 0\n")
                f.write("\n")

# Write train and test files
write_to_file(train_df, "train.txt")
write_to_file(test_df, "test.txt")

print("Finished writing train.txt and test.txt from Grain.xlsx")
