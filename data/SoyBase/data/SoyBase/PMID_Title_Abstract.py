# import time
# import pandas as pd
# from Bio import Entrez

# # Configure your email (required by NCBI)
# Entrez.email = "pratikmaitraus93@gmail.com"  # replace with your email

# # Read PMIDs from the file
# with open("legume_pmid.txt", "r") as f:
#     pmids = [line.strip() for line in f if line.strip().isdigit()]

# # Function to fetch title and abstract for a single PMID
# def fetch_details(pmid):
#     try:
#         handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="xml")
#         records = Entrez.read(handle)
#         handle.close()
#         article = records['PubmedArticle'][0]['MedlineCitation']['Article']
#         title = article.get('ArticleTitle', '')
#         abstract = ''
#         if 'Abstract' in article and 'AbstractText' in article['Abstract']:
#             abstract = ' '.join(str(x) for x in article['Abstract']['AbstractText'])
#         return (pmid, title, abstract)
#     except Exception as e:
#         return (pmid, "Error", f"Failed to fetch: {e}")

# # Collect details
# data = []
# for i, pmid in enumerate(pmids):
#     data.append(fetch_details(pmid))
#     time.sleep(0.4)  # respectful delay to avoid hammering NCBI

# # Save to Excel
# df = pd.DataFrame(data, columns=["PMID", "Title", "Abstract"])
# df.to_excel("pmid_results.xlsx", index=False)


import pandas as pd
import re

# Load the Excel file
df = pd.read_excel("pmid_results.xlsx")

# Function to remove HTML-like tags
def clean_text(text):
    if pd.isna(text):
        return ""
    return re.sub(r"</?(i|sub|sup|b|u|em|strong)[^>]*>", "", str(text))

# Apply cleaning
df["Title"] = df["Title"].apply(clean_text)
df["Abstract"] = df["Abstract"].apply(clean_text)

# Save to new Excel file
df.to_excel("pmid_cleaned.xlsx", index=False)
