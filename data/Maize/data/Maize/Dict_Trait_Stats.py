import pandas as pd

# File path to the dataset
file_path = "Trait.txt"

# Read the dataset
with open(file_path, "r", encoding="utf-8") as file:
    entities = [line.strip() for line in file if line.strip()]

# Compute statistics
num_entities = len(entities)
# Count words in each trait and calculate average
avg_entity_length = sum(len(entity.split()) for entity in entities) / num_entities
proper_noun_count = sum(
    1 for entity in entities if any(word[0].isupper() for word in entity.split() if word)
)
proper_noun_ratio = proper_noun_count / num_entities

# Create a DataFrame with the results
stats_df = pd.DataFrame([{
    "Entity Type": "Trait",
    "# Entity": num_entities,
    "Average Entity Length": avg_entity_length,
    "Proper Noun Ratio": proper_noun_ratio
}])

# Save to Excel
output_path = "Trait_stats.xlsx"
stats_df.to_excel(output_path, index=False)

print(f"Saved statistics to {output_path}")
