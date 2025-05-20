import pandas as pd

# Load the dataset
df = pd.read_csv('maize_references_labeled_train.csv')

# Ensure 'pubmed' is numeric
df['pubmed'] = pd.to_numeric(df['pubmed'], errors='coerce')

# Drop rows with missing 'pubmed'
df = df.dropna(subset=['pubmed'])

# Drop duplicate pubmed IDs, keeping the first occurrence
df_unique = df.drop_duplicates(subset='pubmed')

# Sort by 'pubmed' and select the first 100 unique ones
df_sorted = df_unique.sort_values(by='pubmed').head(100)

# Select only the relevant columns
df_subset = df_sorted[['pubmed', 'title', 'abstract']]

# Save to Excel
df_subset.to_excel('maize_100pmid.xlsx', index=False)

print("Saved first 100 unique pubmed IDs with titles and abstracts to maize_100pmid.xlsx")
