import os
import argparse
import random

"""""""""
This is the script of our simple baseline
"""""""""


parser = argparse.ArgumentParser()

parser.add_argument('--dataset', type=str, required=True,
                    help='Name of dataset')
parser.add_argument('--neg', type=str, required=True,
                    help='type of negative sampling strategy we use')

args = parser.parse_args()
from sklearn.metrics import average_precision_score, roc_auc_score, accuracy_score, f1_score, precision_score, recall_score
import numpy as np


dataset = args.dataset
neg = args.neg

ents = set()
ftrain = open('benchmarks/{}/train.txt'.format(dataset))
fvalid = open('benchmarks/{}/valid.txt'.format(dataset))
ftest = open('benchmarks/{}/test.txt'.format(dataset))
ftest_neg = open('benchmarks/{}/test_neg_{}.txt'.format(dataset, neg))
trains = []
valids = []
tests = []
facts = set()
test_negs = []
rel_dic_sub = dict()
rel_dic_obj = dict()
ent_dic = dict()
for line in ftrain:
    t = line.strip().split('\t')
    trains.append(t)
    ents.add(t[0])
    ents.add(t[2])
    facts.add((t[0], t[1], t[2]))
    if t[1] not in rel_dic_sub:
        rel_dic_sub[t[1]] = set()
        rel_dic_sub[t[1]].add(t[0])
    else:
        rel_dic_sub[t[1]].add(t[0])
    if t[1] not in rel_dic_obj:
        rel_dic_obj[t[1]] = set()
        rel_dic_obj[t[1]].add(t[2])
    else:
        rel_dic_obj[t[1]].add(t[2])
    if t[0] not in ent_dic:
        ent_dic[t[0]] = set()
        ent_dic[t[0]].add(t[1])
    else:
        ent_dic[t[0]].add(t[1])
    if t[2] not in ent_dic:
        ent_dic[t[2]] = set()
        ent_dic[t[2]].add(t[1])
    else:
        ent_dic[t[2]].add(t[1])

for line in fvalid:
    ents.add(t[0])
    ents.add(t[2])
    facts.add((t[0], t[1], t[2]))
    t = line.strip().split('\t')
    valids.append(t)
    if t[1] not in rel_dic_sub:
        rel_dic_sub[t[1]] = set()
        rel_dic_sub[t[1]].add(t[0])
    else:
        rel_dic_sub[t[1]].add(t[0])
    if t[1] not in rel_dic_obj:
        rel_dic_obj[t[1]] = set()
        rel_dic_obj[t[1]].add(t[2])
    else:
        rel_dic_obj[t[1]].add(t[2])
    if t[0] not in ent_dic:
        ent_dic[t[0]] = set()
        ent_dic[t[0]].add(t[1])
    else:
        ent_dic[t[0]].add(t[1])
    if t[2] not in ent_dic:
        ent_dic[t[2]] = set()
        ent_dic[t[2]].add(t[1])
    else:
        ent_dic[t[2]].add(t[1])
        
labels = []
preds = []
neg_num = 0
for line in ftest:
    t = line.strip().split('\t')
    tests.append(t)
    labels.append(1)

    if t[1] in ent_dic[t[0]] and t[1] in ent_dic[t[2]]:
        preds.append(1)
    else:
        preds.append(0)           

neg_preds = []
for line in ftest_neg:
    t = line.strip().split('\t')
    test_negs.append(t)

    labels.append(0)
    if t[1] in ent_dic[t[0]] and t[1] in ent_dic[t[2]]:
        preds.append(1)
    else:
        preds.append(0) 

num_neg = 0
num_neg_true = 0
for i in range(len(preds)):
    if labels[i] == 0:
        num_neg += 1
        if preds[i] == 0:
            num_neg_true += 1

recall_negative = num_neg_true / num_neg

auc_pr = average_precision_score(labels, preds)
roc_auc = roc_auc_score(labels, preds)
accuracy = accuracy_score(labels, preds)
f1 = f1_score(labels, preds)
precision = precision_score(labels, preds)
recall = recall_score(labels, preds)

print(" {} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}".format(args.dataset, round(auc_pr,3), round(roc_auc,3), round(accuracy,3), round(f1,3), round(precision,3), round(recall,3)))