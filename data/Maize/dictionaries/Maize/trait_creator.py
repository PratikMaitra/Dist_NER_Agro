import os
import pandas as pd

# Set the path to the directory containing the Excel files
folder_path = os.path.dirname(os.path.abspath(__file__))

# List of Excel filenames
excel_files = [
    "merged_traits_unique_cleaned.xlsx"
]

# Output text file
output_file = os.path.join(folder_path, "Trait.txt")

# Open the output file for writing
with open(output_file, "w", encoding="utf-8") as outfile:
    for file in excel_files:
        file_path = os.path.join(folder_path, file)
        # Read the Excel file
        df = pd.read_excel(file_path, engine="openpyxl")

        # Flatten all values and write each non-empty string to file
        for value in df.values.flatten():
            if pd.notna(value) and str(value).strip():
                outfile.write(str(value).strip() + "\n")

print(f"Trait names have been written to {output_file}")
