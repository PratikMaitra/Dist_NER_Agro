import pandas as pd

# Load the Grain.xlsx file
df = pd.read_excel("Grain.xlsx")

# Extract and clean trait names
traits = df['traitname'].dropna().astype(str).str.strip().unique()

# Write to Trait.txt
with open("Trait.txt", "w", encoding="utf-8") as f:
    for trait in sorted(traits, key=str.lower):
        f.write(f"{trait}\n")

print("Trait.txt created successfully!")
