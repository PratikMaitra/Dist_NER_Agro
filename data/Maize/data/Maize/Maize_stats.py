import pandas as pd

def count_sentences_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Sentences are separated by double newlines
    sentences = content.strip().split("\n\n")
    num_sentences = len(sentences)

    # Tokens are on non-empty lines
    tokens = [line for line in content.splitlines() if line.strip()]
    num_tokens = len(tokens)

    return num_sentences, num_tokens

# File paths
train_path = "train.txt"
test_path = "test.txt"

# Count stats
train_sentences, train_tokens = count_sentences_tokens(train_path)
test_sentences, test_tokens = count_sentences_tokens(test_path)

# Create DataFrame
stats_df = pd.DataFrame([
    {"Set": "Train", "# Sentences": train_sentences, "# Tokens": train_tokens},
    {"Set": "Test", "# Sentences": test_sentences, "# Tokens": test_tokens}
])

# Save to Excel
output_file = "Maize_stats.xlsx"
stats_df.to_excel(output_file, index=False)

print(f"Saved statistics to {output_file}")
