import sys
sys.path.append("..")
import numpy as np
from collections import defaultdict
import data_processor
import copy
from tqdm import tqdm
import multiprocessing as mp
from rapidfuzz import fuzz

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    if s in [ordinal(n) for n in range(1,999)]:
        return True
    if s in ["first", "second", "third", "forth", "fifth", "eigth", "ninth", "tenth",
             "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth",
             "seventeenth", "eighteenth", "nineteenth", "twentieth"]:
        return True
    return False

def convert(words_):
    words = []
    for w in words_:
        if is_number(w):
            words.append("DIGIT")
        elif w in ["percent", "%", "year", "years", "month", "Mos", "mos", "mo", "months",
                   "week", "weeks", "wks", "wk", "day", "days", "d", "hour", "hours", "hr", "hrs",
                   "minute", "minutes", "mi", "kg"]:
            words.append("UNIT")
        else:
            words.append(w)
    return words

def lookup_in_Dic(tag2idx, dicFile, sentences, tag, windowSize):
    tagIdx = tag2idx[tag]
    dic = []
    labeled_word = set()
    count = 0
    with open(dicFile, "r", encoding='utf-8') as fw:
        dic = [line.strip() for line in fw if line.strip()]
    if not dic:
        return sentences, 0, 0

    for sentence in tqdm(sentences, desc="looking up: "):
        wordList = [word for word, label, dicFlags in sentence]
        wordList = convert(wordList)
        isFlag = np.zeros(len(sentence))
        j = 0
        while j < len(wordList):
            max_window = min(windowSize, len(wordList) - j)
            matched = False
            for k in range(max_window, 0, -1):
                window_words = wordList[j:j + k]
                phrase = " ".join(window_words)
                if phrase in dic:
                    isFlag[j:j+k] = 1
                    j += k
                    matched = True
                    break
                first_word = window_words[0]
                candidates = [entry for entry in dic if entry.split()[0] == first_word]
                for candidate in candidates:
                    
                    ## CHANGE THIS FOR METHOD ###
                    #score = fuzz.token_set_ratio(phrase, candidate)
                    
                    score = fuzz.ratio(phrase, candidate)
                    #score = fuzz.WRatio(phrase, candidate)

                    ## CHANGE THIS FOR THRESHOLD ###
                    #if score >= 90:
                    
                    if score >= 90:
                        isFlag[j:j+k] = 1
                        j += k
                        matched = True
                        break
                if matched:
                    break
            if not matched:
                j += 1

        for m, flag in enumerate(isFlag):
            if flag == 1:
                count += 1
                labeled_word.add(sentence[m][0])
                sentence[m][2][tagIdx] = 1
    return sentences, len(labeled_word), count


def readFile(trainFile, classNum):
    with open(trainFile, "r", encoding='utf-8') as fw:
        sentences = []
        sentence = []
        for line in fw:
            if len(line.strip()) == 0 or line.startswith('-DOCSTART') or line[0] == '\n':
                if len(sentence) > 0:
                    sentences.append(sentence)
                    sentence = []
                continue
            splits = line.split(' ')
            sentence.append([splits[0].strip(), splits[1].strip(), np.zeros(classNum)])
        if len(sentence) > 0:
            sentences.append(sentence)
    return sentences

def writeFile(fileName, sentences):
    with open(fileName, 'w', encoding='utf-8') as fw:
        for sentence in sentences:
            for word, truth, labels in sentence:
                label = labels.argmax() + 1 if labels.sum() == 1 else 0
                fw.write(word + " " + truth + " " + str(label) + "\n")
            fw.write("\n")

def getLabelsAndPreds(sentences):
    labels, preds = [], []
    for sent in sentences:
        for word, label, pred in sent:
            label = label.split('-')[-1] if '-' in label else label
            labels.append(label)
            preds.append(pred)
    return labels, preds

def generate_single_from_all(tag, dataset, tag2idx):
    with open("../data/" + dataset + "/train.ALL.txt", 'r', encoding='utf-8') as ALL, \
         open("../data/" + dataset + "/train." + tag + ".txt", 'w', encoding='utf-8') as SIN:
        for line in ALL:
            if line.strip():
                token = line.strip().split(' ')
                label = 1 if int(token[2]) == tag2idx[tag] else 0
                SIN.write(f"{token[0]} {token[1]} {label}\n")
            else:
                SIN.write(line)

def dict_match(dictNames, file, tag2idx, dataset, suffix=''):
    tag2idx_copy = copy.deepcopy(tag2idx)
    tag2idx_copy.pop('O')
    new_tag2idx = {tag: idx for idx, tag in enumerate(tag2idx_copy)}
    classNum = len(new_tag2idx)
    sentences = readFile(file, classNum)
    maxLen = 10
    for tag in new_tag2idx:
        dic_file = f"dictionaries/{dataset}/{dictNames[tag]}" + (f".{suffix}" if suffix else "")
        sentences, _, _ = lookup_in_Dic(new_tag2idx, dic_file, sentences, tag, maxLen)
    output_file = f"data/{dataset}/{'train.ALL.txt' if 'train' in file else 'test_distant_labeling.txt'}"
    writeFile(output_file, sentences)

def entityIDGeneration(sentences):
    sent_id = 0
    true_entities, pred_entities = [], []
    for sentence in sentences:
        sent_true, sent_pred = [], []
        pre_label, pre_pred = "O", 0
        for i, (word, label, pred) in enumerate(sentence):
            if label == "O":
                if pre_label != "O":
                    sent_true.append(f"{sent_id}_{label_start_id}_{i-1}_{entity_type}")
            else:
                if "B-" in label:
                    label = label.split("-")[-1]
                    if pre_label != "O":
                        sent_true.append(f"{sent_id}_{label_start_id}_{i-1}_{entity_type}")
                    label_start_id, entity_type = i, label
            pre_label = label
        if pre_label != "O":
            sent_true.append(f"{sent_id}_{label_start_id}_{len(sentence)-1}_{entity_type}")

        for i, (word, label, pred) in enumerate(sentence):
            if pred == 0:
                if pre_pred != 0:
                    sent_pred.append(f"{sent_id}_{pred_start_id}_{i-1}_{pre_pred}")
            else:
                if pre_pred != pred:
                    if pre_pred != 0:
                        sent_pred.append(f"{sent_id}_{pred_start_id}_{i-1}_{pre_pred}")
                    pred_start_id = i
            pre_pred = pred
        if pre_pred != 0:
            sent_pred.append(f"{sent_id}_{pred_start_id}_{len(sentence)-1}_{pre_pred}")
        sent_id += 1
        true_entities.append(sent_true)
        pred_entities.append(sent_pred)
    return true_entities, pred_entities

def compute_overall_precision_recall_f1(tag2Idx, true_entities, pred_entities):
    tp = sum(
        any(e.replace(flag, str(tag2Idx[flag])) in sent_pred
            for flag in tag2Idx if flag in e)
        for sent_true, sent_pred in zip(true_entities, pred_entities)
        for e in sent_true
    )
    np_, pp = sum(map(len, true_entities)), sum(map(len, pred_entities))
    p = tp / pp if pp else 0
    r = tp / np_ if np_ else 0
    f1 = 2 * p * r / (p + r) if p and r else 0
    return p, r, f1

def matching_f1(File, tag2idx):
    with open(File, 'r', encoding='utf-8') as T:
        sentences, sentence = [], []
        for line in T:
            if line.strip():
                token = line.strip().split(' ')
                sentence.append([token[0], token[1], int(token[2])])
            else:
                sentences.append(sentence)
                sentence = []
        if sentence:
            sentences.append(sentence)
    true_entities, pred_entities = entityIDGeneration(sentences)
    p, r, f1 = compute_overall_precision_recall_f1(tag2idx, true_entities, pred_entities)
    print(f"OVERALL: Precision: {p}, Recall: {r}, F1: {f1}")

def generate_entity_data(dataset):
    with open(f'../data/{dataset}/train.ALL.txt', 'r', encoding='utf-8') as ALL, \
         open(f'../data/{dataset}/train.Entity.txt', 'w', encoding='utf-8') as Entity:
        for line in ALL:
            if line.strip():
                line_info = line.strip().split(' ')
                label = '1' if int(line_info[2]) > 0 else line_info[2]
                Entity.write(f"{line_info[0]} {line_info[1]} {label}\n")
            else:
                Entity.write(line)

def main():
    dataset = 'Maize'
    tag2idx = {"O": 0, "Trait": 1}
    dict_names = {"Trait": "Trait.txt"}
    trainFile = f'./data/{dataset}/train.txt'
    dict_match(dict_names, trainFile, tag2idx, dataset)

if __name__ == '__main__':
    main()
