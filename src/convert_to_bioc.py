import bioc
import re
import os
import argparse
from datetime import datetime

def clean_xml_text(s):
    return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', s)

def create_annotation(text, start):
    ann = bioc.BioCAnnotation()
    ann.text = text
    ann.add_location(bioc.BioCLocation(offset=start, length=len(text.strip())))
    ann.id = f"T{start}"
    ann.infons['type'] = 'Trait'
    return ann

def process_block_with_annotations(block, base_offset):
    text = ""
    annotations = []
    current_entity = ""
    start_offset = None
    offset = base_offset

    for line in block.strip().split('\n'):
        line = line.strip()
        if not line:
            if current_entity:
                annotations.append(create_annotation(current_entity.strip(), start_offset))
                current_entity = ""
            text += "\n"
            offset += 1
            continue

        parts = line.split()
        if len(parts) != 3:
            continue

        word, tag, pred = parts
        if text and not text.endswith((' ', '\n')):
            text += " "
            offset += 1

        if pred == '1':
            if not current_entity:
                start_offset = offset
            current_entity += word + " "
        else:
            if current_entity:
                annotations.append(create_annotation(current_entity.strip(), start_offset))
                current_entity = ""
            start_offset = None

        text += word
        offset += len(word)

    if current_entity:
        annotations.append(create_annotation(current_entity.strip(), start_offset))

    return text, annotations

def convert_to_bioc(input_file, output_file, pmid, source_name="TraitNER"):
    collection = bioc.BioCCollection()
    collection.source = source_name
    collection.key = "TraitsBatch"
    collection.version = "2.0"
    collection.date = datetime.today().strftime('%Y-%m-%d')

    document = bioc.BioCDocument()
    document.id = pmid
    document.infons['source'] = source_name
    document.infons['pmid'] = pmid

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.strip().split('\n\n', 1)
    title_block = blocks[0]
    abstract_block = blocks[1] if len(blocks) > 1 else ""

    title_passage = bioc.BioCPassage()
    title_passage.offset = 0
    title_passage.infons['type'] = 'title'
    title_text, title_annotations = process_block_with_annotations(title_block, base_offset=0)
    title_passage.text = clean_xml_text(title_text if title_text else "No title available.")
    title_passage.annotations.extend(title_annotations)

    abstract_passage = bioc.BioCPassage()
    abstract_passage.offset = len(title_passage.text) + 1
    abstract_passage.infons['type'] = 'abstract'
    abstract_text, abstract_annotations = process_block_with_annotations(abstract_block, base_offset=abstract_passage.offset)
    abstract_passage.text = clean_xml_text(abstract_text if abstract_text.strip() else "No abstract available.")
    abstract_passage.annotations.extend(abstract_annotations)

    document.passages.extend([title_passage, abstract_passage])
    collection.documents.append(document)

    with open(output_file, 'w', encoding='utf-8') as fp:
        bioc.dump(collection, fp)

    print(f"✅ Saved BioC XML: {output_file} (PMID: {pmid})")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True, help='Directory of prediction .txt files')
    parser.add_argument('--output_dir', required=True, help='Directory to save BioC XML files')
    parser.add_argument('--source', default='TraitNER', help='Source tag for BioC metadata')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for file in os.listdir(args.input_dir):
        if file.endswith('.txt'):
            match = re.search(r'pred_(?:maize_|grain_|soy_)?(\d+)\.txt', file)
            if match:
                pmid = match.group(1)
                input_file = os.path.join(args.input_dir, file)
                output_file = os.path.join(args.output_dir, f'{args.source}_{pmid}.xml')
                convert_to_bioc(input_file, output_file, pmid, args.source)
            else:
                print(f"⚠️ Skipped file (no PMID found): {file}")

    print(f"\n🎉 Conversion complete. BioC files saved in: {args.output_dir}")

if __name__ == "__main__":
    main()
