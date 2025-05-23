## Re-Examine Distantly Supervised NER: A New Benchmark and a Simple Approach



### Performance of DS-NER Methods on QTL 


### Environment

Python 3.10

### How to run

For example, on CoNLL2003

```python
python train.py --do_train --do_eval --dataset_name CoNLL2003_KB \
        --train_epochs 2 --train_lr 2e-5 --drop_other 0.5  \
        --curriculum_train_sub_epochs 1 --curriculum_train_lr 5e-5  \ 
        --curriculum_train_epochs 5  \ 
        --self_train_epochs 5 --self_train_lr 5e-7 --m 50  --max_seq_length 150 
```

on QTL dataset,


```python
python train.py --do_train --do_eval --dataset_name QTL \ 
        --loss_type MAE --m 20     \
        --train_epochs 1 --train_lr 5e-7 --drop_other 0.5  \
        --curriculum_train_sub_epochs 1 --curriculum_train_lr 2e-7  \ 
        --curriculum_train_epochs 5 --self_train_lr 5e-7 --self_train_epochs 5  \
        --max_seq_length 300
```

Parameters are tuned from validation set, and all hyper-parameters show in Appendix D, Table 5. 

### Citation

```
@inproceedings{li-etal-2025-examine,
    title = "Re-Examine Distantly Supervised {NER}: A New Benchmark and a Simple Approach",
    author = "Li, Yuepei  and
      Zhou, Kang  and
      Qiao, Qiao  and
      Wang, Qing  and
      Li, Qi",
    editor = "Rambow, Owen  and
      Wanner, Leo  and
      Apidianaki, Marianna  and
      Al-Khalifa, Hend  and
      Eugenio, Barbara Di  and
      Schockaert, Steven",
    booktitle = "Proceedings of the 31st International Conference on Computational Linguistics",
    month = jan,
    year = "2025",
    address = "Abu Dhabi, UAE",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.coling-main.727/",
    pages = "10940--10959",
    abstract = ""
}
```
