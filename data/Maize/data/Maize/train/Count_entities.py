import pandas as pd

def count_entities_and_words(file_path, output_excel):
    num_entities = 0
    num_words = 0
    inside_entity = False

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                inside_entity = False
                continue
            parts = line.split()
            if len(parts) != 3:
                continue
            word, tag, pred = parts
            if pred == '1':
                num_words += 1
                if not inside_entity:
                    num_entities += 1
                    inside_entity = True
            else:
                inside_entity = False

    df = pd.DataFrame([{
        'File': file_path,
        'Total Entities': num_entities,
        'Total Words in Entities': num_words
    }])

    df.to_excel(output_excel, index=False)
    print(f"Saved results to {output_excel}")

# Example usage
count_entities_and_words("train.txt", "entity_count_train.xlsx")

