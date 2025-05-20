import pandas as pd
import re
import time
import requests
from Bio import Entrez

# Set your email for NCBI
Entrez.email = "pratikmaitraus93@example.com"  # Replace with your real email

# Load the Excel file
df = pd.read_excel("GrainGenes_traits_references_20250409.xlsx")

# Function to clean formatting tags
def clean_text(text):
    if pd.isna(text):
        return ""
    return re.sub(r"</?(i|sub|sup|b|u|em|strong)[^>]*>", "", str(text))

# Function to fetch data from PubMed using PMID
def fetch_from_pubmed(pmid):
    try:
        handle = Entrez.efetch(db="pubmed", id=str(int(pmid)), rettype="abstract", retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        article = records['PubmedArticle'][0]['MedlineCitation']['Article']
        title = article.get('ArticleTitle', '')
        abstract = ''
        if 'Abstract' in article and 'AbstractText' in article['Abstract']:
            abstract = ' '.join(str(x) for x in article['Abstract']['AbstractText'])
        return clean_text(title), clean_text(abstract)
    except Exception as e:
        return "Error", f"Failed to fetch PMID {pmid}: {e}"

# Function to fetch data from CrossRef using DOI
def fetch_from_doi(doi):
    try:
        headers = {"Accept": "application/vnd.citationstyles.csl+json"}
        url = f"https://doi.org/{doi}"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()

            raw_title = data.get('title', '')
            if isinstance(raw_title, list):
                title = raw_title[0] if raw_title else ""
            else:
                title = raw_title

            abstract = data.get('abstract', '')
            abstract = re.sub(r"<[^>]+>", "", abstract)  # remove HTML tags
            return clean_text(title), clean_text(abstract)
        else:
            return "Error", f"Failed to fetch DOI {doi}: HTTP {response.status_code}"
    except Exception as e:
        return "Error", f"Failed to fetch DOI {doi}: {e}"


# Process each row
titles = []
abstracts = []

for idx, row in df.iterrows():
    pmid = row.get('Pubmed id', None)
    doi = row.get('DOI', None)

    if pd.notna(pmid):
        title, abstract = fetch_from_pubmed(pmid)
    elif pd.notna(doi):
        title, abstract = fetch_from_doi(doi)
    else:
        title, abstract = "", ""

    titles.append(title)
    abstracts.append(abstract)
    time.sleep(0.4)  # polite delay

# Add results and save
df['Title'] = titles
df['Abstract'] = abstracts
df.to_excel("Grain.xlsx", index=False)

print("Grain.xlsx saved successfully!")
