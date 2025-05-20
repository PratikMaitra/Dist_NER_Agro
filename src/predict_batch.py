import os
import shutil
import subprocess
import argparse

def clean_up(data_dir, global_data_dir):
    global_pt_file = os.path.join(global_data_dir, 'Allcrops_test.pt')
    if os.path.exists(global_pt_file):
        os.remove(global_pt_file)
        print("🗑️ Removed global Allcrops_test.pt")

    temp_dir = os.path.join(data_dir, 'temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print("🗑️ Cleared temp folder")
    os.makedirs(temp_dir, exist_ok=True)

    pycache_dir = os.path.join(data_dir, '__pycache__')
    if os.path.exists(pycache_dir):
        shutil.rmtree(pycache_dir)
        print("🗑️ Removed __pycache__")

def run_prediction(args, input_file, pmid, data_dir, output_dir):
    # Copy file as test.txt
    shutil.copy(input_file, os.path.join(data_dir, 'test.txt'))

    # Run prediction
    subprocess.run([
        "python", "predict.py",
        "--dataset_name", args.dataset_name,
        "--loss_type", args.loss_type,
        "--m", str(args.m),
        "--train_epochs", str(args.train_epochs),
        "--train_lr", str(args.train_lr),
        "--drop_other", str(args.drop_other),
        "--curriculum_train_sub_epochs", str(args.curriculum_train_sub_epochs),
        "--curriculum_train_lr", str(args.curriculum_train_lr),
        "--curriculum_train_epochs", str(args.curriculum_train_epochs),
        "--self_train_lr", str(args.self_train_lr),
        "--self_train_epochs", str(args.self_train_epochs),
        "--max_seq_length", str(args.max_seq_length)
    ])

    # Rename prediction output
    pred_output = os.path.join(data_dir, 'pred_test.txt')
    if os.path.exists(pred_output):
        dest_file = os.path.join(output_dir, f'pred_{pmid}.txt')
        shutil.move(pred_output, dest_file)
        print(f"✅ Prediction saved for {pmid}")
    else:
        print(f"❗ No prediction output for {pmid}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True, help='Path to folder with test_*.txt files')
    parser.add_argument('--output_dir', required=True, help='Path to save prediction outputs')
    parser.add_argument('--dataset_name', default='Allcrops')
    parser.add_argument('--loss_type', default='MAE')
    parser.add_argument('--m', type=int, default=20)
    parser.add_argument('--train_epochs', type=int, default=1)
    parser.add_argument('--train_lr', type=float, default=5e-7)
    parser.add_argument('--drop_other', type=float, default=0.5)
    parser.add_argument('--curriculum_train_sub_epochs', type=int, default=1)
    parser.add_argument('--curriculum_train_lr', type=float, default=2e-7)
    parser.add_argument('--curriculum_train_epochs', type=int, default=5)
    parser.add_argument('--self_train_lr', type=float, default=5e-7)
    parser.add_argument('--self_train_epochs', type=int, default=5)
    parser.add_argument('--max_seq_length', type=int, default=300)

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    data_dir = '../data/Allcrops'
    global_data_dir = '../data'

    for filename in os.listdir(args.input_dir):
        if filename.endswith('.txt'):
            pmid = filename.replace('test_maize_', '').replace('.txt', '')
            input_path = os.path.join(args.input_dir, filename)

            clean_up(data_dir, global_data_dir)
            run_prediction(args, input_path, pmid, data_dir, args.output_dir)

    print("\n🎉 All predictions completed.")

if __name__ == "__main__":
    main()
