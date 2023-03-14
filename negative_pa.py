"""
This is the script for generating negative examples with our position-aware corruption strategy

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
for line in f_valid:
    t = line.strip().split('\t')
    valid_triples.append(t)
    all_true.add((t[0], t[1], t[2]))
for line in f_test:
    t = line.strip().split('\t')
    all_true.add((t[0], t[1], t[2]))
    test_triples.append(t)
    
dict_subs = dict()
dict_objs = dict()

for t in all_true:
    sub = t[0]
    rel = t[1]
    obj = t[2]
    all_entities.add(sub)
    all_entities.add(obj)
    if rel not in dict_subs:
        dict_subs[rel] = set()
    dict_subs[rel].add(sub)
    if rel not in dict_objs:
        dict_objs[rel] = set()
    dict_objs[rel].add(obj)
entities = list(all_entities)

ori_set = set()

if 'LUBM' in dataset:
    f = open('lubm1_0.ttl')
    for line in f:
        t = line.strip().split(' ')
        if len(t)>1:
            ori_set.add((t[0], t[1], t[2]))
elif 'FB' in dataset:
    f_ori1 = open('FB_ori/train.txt')
    f_ori2 = open('FB_ori/valid.txt')
    f_ori3 = open('FB_ori/test.txt')
    for line in f_ori1:
        t = line.strip().split('\t')
        ori_set.add((t[0],t[1], t[2]))
    for line in f_ori2:
        t = line.strip().split('\t')
        ori_set.add((t[0],t[1], t[2]))
    for line in f_ori3:
        t = line.strip().split('\t')
        ori_set.add((t[0],t[1], t[2]))
elif 'WN' in dataset:
    f_ori1 = open('WN_ori/train.txt')
    f_ori2 = open('WN_ori/valid.txt')
    f_ori3 = open('WN_ori/test.txt')
    for line in f_ori1:
        t = line.strip().split('\t')
        ori_set.add((t[0],t[1], t[2]))
    for line in f_ori2:
        t = line.strip().split('\t')
        ori_set.add((t[0],t[1], t[2]))
    for line in f_ori3:
        t = line.strip().split('\t')
        ori_set.add((t[0],t[1], t[2]))
        
"""
generating negative examples for testing

"""
        
test_negative_triples = []
import random


f = open('benchmarks/{}/test_neg_pa.txt'.format(dataset), 'w+')

candidate_negs_test = set()


for t in test_triples:
    sub = t[0]
    rel = t[1]
    obj = t[2]
    can_subs = dict_subs[rel]
    can_objs = dict_objs[rel]
    if rel != 'rdf:type':
        for can_sub in can_subs:
            if (can_sub, rel, obj) not in all_true:
                candidate_negs_test.add((can_sub, rel, obj))
        for can_obj in can_objs:
            if (sub, rel, can_obj) not in all_true:
                candidate_negs_test.add((sub, rel, can_obj))
    else:
        can_subs = dict_subs[rel]
        for can_sub in can_subs:
            if (can_sub, rel, obj) not in all_true:
                candidate_negs_test.add((can_sub, rel, obj))        
candidate = random.sample(list(candidate_negs_test), len(test_triples))

for t in candidate:
    all_true.add((t[0], t[1], t[2]))
    f.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f.close()     
        

"""
generating negative examples for validation

"""

    
    
valid_negative_triples = []
import random
i = -1
print(len(valid_triples))
f = open('benchmarks/{}/valid_neg_pa.txt'.format(dataset), 'w+')

candidate_negs_valid = set()


for t in valid_triples:
    sub = t[0]
    rel = t[1]
    obj = t[2]
    can_subs = dict_subs[rel]
    can_objs = dict_objs[rel]
    if rel != 'rdf:type':
        
        for can_sub in can_subs:
            if (can_sub, rel, obj) not in all_true:
                candidate_negs_valid.add((can_sub, rel, obj))
        for can_obj in can_objs:
            if (sub, rel, can_obj) not in all_true:
                candidate_negs_valid.add((sub, rel, can_obj))
    else:
        for can_sub in can_subs:
            if (can_sub, rel, obj) not in all_true:
                candidate_negs_valid.add((can_sub, rel, obj))        
print(len(candidate_negs_valid))            
candidate = random.sample(list(candidate_negs_valid), len(valid_triples))

for t in candidate:
    all_true.add((t[0], t[1], t[2]))
    f.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f.close()     
        
"""
generating negative examples for training

"""


train_negative_triples = []
import random

print(len(train_triples))
t_train = []
for t in train_triples:
    if (t[0], t[1], t[2]) not in ori_set:
        t_train.append(t)


train_negative_triples = []
import random

print(len(t_train))
f = open('benchmarks/{}/train_neg_pa.txt'.format(dataset), 'w+')

candidate_negs_train = set()

random.shuffle(t_train)
for t in t_train:
    sub = t[0]
    rel = t[1]
    obj = t[2]
    
    can_subs = dict_subs[rel]
    can_objs = dict_objs[rel]
    if rel != 'rdf:type':
        for can_sub in can_subs:
            if (can_sub, rel, obj) not in all_true:
                candidate_negs_train.add((can_sub, rel, obj))
        for can_obj in can_objs:
            if (sub, rel, can_obj) not in all_true:
                candidate_negs_train.add((sub, rel, can_obj))
    else:
        for can_sub in can_subs:
            if (can_sub, rel, obj) not in all_true:
                candidate_negs_train.add((can_sub, rel, obj))
    if len(candidate_negs_train) >= len(train_triples)*20:
        break
            
candidate = random.sample(list(candidate_negs_train), len(train_triples))

for t in candidate:
    f.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f.close()     
        
 