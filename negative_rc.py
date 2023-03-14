"""
This is the script for generating negative examples with the conventional random corruption strategy

"""



import os
import argparse
import random

parser = argparse.ArgumentParser()

parser.add_argument('--dataset', type=str, required=True,
                    help='Name of dataset')


args = parser.parse_args()
dataset = args.dataset



f_train = open('benchmarks/{}/train.txt'.format(dataset))
f_valid = open('benchmarks/{}/valid.txt'.format(dataset))
f_test = open('benchmarks/{}/test.txt'.format(dataset))



all_true = set()
train_triples = []
valid_triples = []
test_triples = []
all_entities = set()
for line in f_train:
    t = line.strip().split('\t')
    train_triples.append(t)
    all_true.add((t[0], t[1], t[2]))
    all_entities.add(t[0])
    all_entities.add(t[2])
for line in f_valid:
    t = line.strip().split('\t')
    valid_triples.append(t)
    all_true.add((t[0], t[1], t[2]))
    all_entities.add(t[0])
    all_entities.add(t[2])
for line in f_test:
    t = line.strip().split('\t')
    all_true.add((t[0], t[1], t[2]))
    test_triples.append(t)
    all_entities.add(t[0])
    all_entities.add(t[2])

    
"""
generating negative examples for training

"""


import random
i = -1

f = open('benchmarks/{}/train_neg_rc.txt'.format(dataset), 'w+')
train_negative_triples = []

i = 0
for t in train_triples:
    i += 1

    sub = t[0]
    rel = t[1]
    obj = t[2]
    while True:
        can_obj = random.choice(list(all_entities))
        if (sub, rel, can_obj) not in all_true:
            train_negative_triples.append([sub, rel, can_obj])
            all_true.add((t[0], t[1], t[2]))
            break
            

for t in train_negative_triples:
    f.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f.close()  


"""
generating negative examples for validation

"""


f = open('benchmarks/{}/valid_neg_rc.txt'.format(dataset), 'w+')
valid_negative_triples = []

i = 0
for t in valid_triples:
    i += 1

    sub = t[0]
    rel = t[1]
    obj = t[2]
    while True:
        can_obj = random.choice(list(all_entities))
        if (sub, rel, can_obj) not in all_true:
            valid_negative_triples.append([sub, rel, can_obj])
            all_true.add((t[0], t[1], t[2]))
            break
            

for t in valid_negative_triples:
    f.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f.close()   

"""
generating negative examples for testing

"""


f = open('benchmarks/{}/test_neg_rc.txt'.format(dataset), 'w+')
test_negative_triples = []

i = 0
for t in test_triples:
    i += 1
    sub = t[0]
    rel = t[1]
    obj = t[2]
    while True:
        can_obj = random.choice(list(all_entities))
        if (sub, rel, can_obj) not in all_true:
            test_negative_triples.append([sub, rel, can_obj])
            all_true.add((t[0], t[1], t[2]))
            break
            

for t in test_negative_triples:
    f.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f.close()   