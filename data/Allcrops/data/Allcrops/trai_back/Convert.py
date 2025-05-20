import pandas as pd

# Load the line mapping file
mapping_df = pd.read_csv("allcrops_map_pmid_train.csv")

# Read the annotated CoNLL-style file
with open("train.ALL.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Strip newlines from lines
lines = [line.strip() for line in lines]

# Store results here
annotations = []

# Iterate over each entry in the mapping
for _, row in mapping_df.iterrows():
    pmid = row['pmid']
    start = int(row['start_line']) - 1  # convert to 0-based index
    end = int(row['end_line'])         # end is inclusive in slicing

    # Extract lines for this PMID
    section_lines = lines[start:end+1]

    # Extract tokens with label "1"
    annotated_words = []
    for line in section_lines:
        if line:  # skip empty lines
            parts = line.split()
            if len(parts) == 3 and parts[2] == '1':
                annotated_words.append(parts[0])

    # Combine annotations
    annotations.append({
        'pmid': pmid,
        'annotations': ', '.join(annotated_words)
    })

# Save to Excel
annotations_df = pd.DataFrame(annotations)
annotations_df.to_excel("train_pmid_dicitionary_annotate.xlsx", index=False)
annotations_df.to_csv("train_pmid_dicitionay_annotate.csv", index=False)

print("Saved per-pmid annotations to train_pmid_annotate.xlsx")
