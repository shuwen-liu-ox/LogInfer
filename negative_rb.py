"""
This is the script for generating negative examples with our relevance-based random sampling strategy

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
relevant_entities = set()
relevant_relations = set()


#these two files are generated when running split.py

f_relevant_entities = open('benchmarks/{}/candidate_entities.txt'.format(dataset))
for line in f_relevant_entities:
    relevant_entities.add(line.strip())
    
f_relevant_relations = open('benchmarks/{}/candidate_relations.txt'.format(dataset))
for line in f_relevant_relations:
    relevant_relations.add(line.strip())


candidate_negtives = set()
for sub in relevant_entities:
    for rel in relevant_relations:
        for obj in relevant_entities:
            if (sub, rel, obj) not in all_true:
                candidate_negtives.add((sub,rel,obj))


all_sampled = random.sample(list(candidate_negtives), len(train_triples)+len(valid_triples)+len(test_triples))
train_negative_triples = all_sampled[:len(train_triples)]
valid_negative_triples = all_sampled[len(train_triples):len(train_triples)+len(valid_triples)]
test_negative_triples = all_sampled[len(train_triples)+len(valid_triples):]


f_train = open('benchmarks/{}/train_neg_rb.txt'.format(dataset), 'w+')
f_valid = open('benchmarks/{}/valid_neg_rb.txt'.format(dataset), 'w+')
f_test = open('benchmarks/{}/test_neg_rb.txt'.format(dataset), 'w+')

for t in train_negative_triples:
    f_train.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f_train.close()     
for t in valid_negative_triples:
    f_valid.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f_valid.close()     
for t in test_negative_triples:
    f_test.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f_test.close()     