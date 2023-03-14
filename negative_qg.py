"""
This is the script for generating negative examples with our query-guided negative sampling strategy

"""



import os
import argparse
import random

parser = argparse.ArgumentParser()

parser.add_argument('--dataset', type=str, required=True,
                    help='Name of dataset')

def dictionary(input_list):
    
    """
    To generate a dictionary.
    Index: item in the array.
    Value: the index of this item.
    """
    
    return dict(zip(input_list, range(len(input_list))))

def read_assignments(file_name):    
    assignments = []
    line_count = 0
    for line in open(file_name):
        line_count += 1
        if line_count < 10:
            continue
        assignment = [line.split(' ')[0].replace('file://',''), line.split(' ')[1].replace('file://','')]        
        assignments.append(assignment)
    return assignments

def read_assignments2(file_name):    
    assignments = []
    line_count = 0
    for line in open(file_name):
        line_count += 1
        if line_count < 10:
            continue
        assignment = [line.split(' ')[0].replace('file://',''), line.split(' ')[1].replace('file://',''), line.split(' ')[2].replace('file://','')]        
        assignments.append(assignment)
    return assignments

def read_assignments3(file_name):    
    assignments = []
    line_count = 0
    for line in open(file_name):
        line_count += 1
        if line_count < 10:
            continue
        assignment = [line.split(' ')[0].replace('file://',''), line.split(' ')[1].replace('file://',''), line.split(' ')[2].replace('file://',''), line.split(' ')[3].replace('file://','')]        
        assignments.append(assignment)
    return assignments

args = parser.parse_args()
dataset = args.dataset



f_train = open('benchmarks/{}/train.txt'.format(dataset))
f_valid = open('benchmarks/{}/valid.txt'.format(dataset))
f_test = open('benchmarks/{}/test.txt'.format(dataset))

if 'inter' in dataset:
    if 'FB' in dataset:
        f_rule = open('final_rules_FB_intersection.txt')
    if 'WN' in dataset:

        f_rule = open('final_rules_WN_intersection.txt')

    rules = []
    for line in f_rule:
        r,s,t = line.strip().split('\t')
        r = r.replace('<','')
        s = s.replace('<','')
        t = t.replace('<','')
        rules.append([r,s,t])

if 'trian' in dataset:
    if 'FB' in dataset:
        f_rule = open('final_rules_FB_trian.txt')
    if 'WN' in dataset:

        f_rule = open('final_rules_WN_trian.txt')

    rules = []
    for line in f_rule:
        r,s,t,p = line.strip().split('\t')
        r = r.replace('<','')
        s = s.replace('<','')
        t = t.replace('<','')
        p = p.replace('<','')
        rules.append([r,s,t])
        
if 'diam' in dataset:
    if 'FB' in dataset:
        f_rule = open('final_rules_FB_diam.txt')
    if 'WN' in dataset:

        f_rule = open('final_rules_WN_diam.txt')

    rules = []
    for line in f_rule:
        r,s,t,p = line.strip().split('\t')
        r = r.replace('<','')
        s = s.replace('<','')
        t = t.replace('<','')
        p = p.replace('<','')
        rules.append([r,s,t])
        
relations = set()
count = 0
if 'FB' in dataset:
    if 'inter' in dataset:
        f_relation_dic = open('relation_FB_intersection.dict'.format(dataset))
elif 'WN' in dataset:
    if 'inter' in dataset:
        f_relation_dic = open('relation_WN_intersection.dict'.format(dataset))
if 'FB' in dataset:
    if 'trian' in dataset:
        f_relation_dic = open('relation_FB_triangle.dict'.format(dataset))
elif 'WN' in dataset:
    if 'trian' in dataset:
        f_relation_dic = open('relation_WN_triangle.dict'.format(dataset))
if 'FB' in dataset:
    if 'diam' in dataset:
        f_relation_dic = open('relation_FB_diamond.dict'.format(dataset))
elif 'WN' in dataset:
    if 'diam' in dataset:
        f_relation_dic = open('relation_WN_diamond.dict'.format(dataset))
relations = []

for line in f_relation_dic:
    relation_new = line.strip()
    relations.append(relation_new)

relation_dic = dictionary(relations)



all_true = set()
positive_train_triples = []
positive_valid_triples = []
positive_test_triples = []
all_entities = set()
for line in f_train:
    t = line.strip().split('\t')
    positive_train_triples.append(t)
    all_true.add((t[0], t[1], t[2]))
    all_entities.add(t[0])
    all_entities.add(t[2])
for line in f_valid:
    t = line.strip().split('\t')
    positive_valid_triples.append(t)
    all_true.add((t[0], t[1], t[2]))
    all_entities.add(t[0])
    all_entities.add(t[2])
for line in f_test:
    t = line.strip().split('\t')
    all_true.add((t[0], t[1], t[2]))
    positive_test_triples.append(t)
    all_entities.add(t[0])
    all_entities.add(t[2])
    
if 'inter' in dataset:   
    rule_assignment1_dict = dict()
    rule_assignment2_dict = dict()
    candidate_neg_triples1 = []

    candidate_neg_triples2 = []
    candidate_neg_set = set()
    for rule in rules:
        r,s,t = rule
        path = 'negative_assignments_{}_{}'.format(dataset)

        assignments_miss1 =  read_assignments('{}/assignments_R={}_notS={}.txt'.format(path, relation_dic['<'+r+'>'], relation_dic['<'+s+'>']))
        assignments_miss2 =  read_assignments('{}/assignments_notR={}_S={}.txt'.format(path, relation_dic['<'+r+'>'], relation_dic['<'+s+'>']))
        rule_assignment1_dict[(r,s,t)] = assignments_miss1
        rule_assignment2_dict[(r,s,t)] = assignments_miss2

    for rule in rules:
        r,s,t = rule
        ass1 = rule_assignment1_dict[(r,s,t)]
        ass2 = rule_assignment2_dict[(r,s,t)]

        for sub, obj in ass1:
            rel = t
            candidate_neg_triples1.append([sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')])
            candidate_neg_set.add((sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')))

        for sub, obj in ass2:
            rel = t
            candidate_neg_triples2.append([sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')])
            candidate_neg_set.add((sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')))

if 'trian' in dataset:
    rule_assignment1_dict = dict()
    rule_assignment2_dict = dict()
    rule_assignment3_dict = dict()
    candidate_neg_triples1 = []

    candidate_neg_triples2 = []
    candidate_neg_triples3 = []
    candidate_neg_set = set()   
    for rule in rules:
        r,s,t,p = rule
        path = 'negative_assignments_{}_{}'.format(DATASET,PATTERN)

        assignments_miss1 =  read_assignments2('{}/assignments_R={}_notS={}_T={}.txt'.format(path, relation_dic['<'+r+'>'], relation_dic['<'+s+'>'], relation_dic['<'+t+'>']))
        assignments_miss2 =  read_assignments2('{}/assignments_R={}_S={}_notT={}.txt'.format(path, relation_dic['<'+r+'>'], relation_dic['<'+s+'>'], relation_dic['<'+t+'>']))
        assignments_miss3 =  read_assignments2('{}/assignments_notR={}_S={}_T={}.txt'.format(path, relation_dic['<'+r+'>'], relation_dic['<'+s+'>'], relation_dic['<'+t+'>']))
        rule_assignment1_dict[(r,s,t,p)] = assignments_miss1
        rule_assignment2_dict[(r,s,t,p)] = assignments_miss2
        rule_assignment3_dict[(r,s,t,p)] = assignments_miss3
    for rule in rules:
        r,s,t,p = rule
        ass1 = rule_assignment1_dict[(r,s,t,p)]
        ass2 = rule_assignment2_dict[(r,s,t,p)]
        ass2 = rule_assignment3_dict[(r,s,t,p)]
        for sub, obj, z in ass1:
            rel = p
            candidate_neg_triples1.append([sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')])
            candidate_neg_set.add((sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')))
        for sub, obj, z in ass2:
            rel = p
            candidate_neg_triples2.append([sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')])
            candidate_neg_set.add((sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')))
        for sub, obj, z in ass3:
            rel = p
            candidate_neg_triples3.append([sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')])
            candidate_neg_set.add((sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')))
            
if 'diam' in dataset:
    rule_assignment1_dict = dict()
    rule_assignment2_dict = dict()
    rule_assignment3_dict = dict()
    candidate_neg_triples1 = []
    candidate_neg_triples_sub_rel_dic1 = dict()
    candidate_neg_triples_rel_obj_dic1 = dict()
    candidate_neg_triples_rel_dic1 = dict()
    candidate_neg_triples2 = []
    candidate_neg_set = set()
    for rule in rules:
        r,s,t,p,q = rule
        path = 'negative_assignments_{}_{}'.format(DATASET,PATTERN)
# we did check for removing the equality, but it returns no facts
        assignments_miss1 =  read_assignments3('{}/assignments_R={}_notS={}_T={}_P={}_Q={}.txt'.format(path, relation_dic['<'+r+'>'], relation_dic['<'+s+'>'], relation_dic['<'+t+'>'], relation_dic['<'+p+'>'], relation_dic['<'+q+'>']))
        assignments_miss2 =  read_assignments3('{}/assignments_R={}_S={}_notT={}_P={}_Q={}.txt'.format(path, relation_dic['<'+r+'>'], relation_dic['<'+s+'>'], relation_dic['<'+t+'>'], relation_dic['<'+p+'>'], relation_dic['<'+q+'>']))
        assignments_miss3 =  read_assignments3('{}/assignments_notR={}_S={}_T={}_P={}_Q={}.txt'.format(path, relation_dic['<'+r+'>'], relation_dic['<'+s+'>'], relation_dic['<'+t+'>'], relation_dic['<'+p+'>'], relation_dic['<'+q+'>']))
        rule_assignment1_dict[(r,s,t,p,q)] = assignments_miss1
        rule_assignment2_dict[(r,s,t,p,q)] = assignments_miss2
        rule_assignment3_dict[(r,s,t,p,q)] = assignments_miss3

    for rule in rules:
        r,s,t,p,q = rule
        ass1 = rule_assignment1_dict[(r,s,t,p,q)]
        ass2 = rule_assignment2_dict[(r,s,t,p,q)]
        ass3 = rule_assignment3_dict[(r,s,t,p,q)]
        for sub, obj, z, w in ass1:
            rel = q
            candidate_neg_triples1.append([sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')])
            candidate_neg_set.add((sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')))

        for sub, obj, z, w in ass2:
            rel = q
            candidate_neg_triples2.append([sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')])
            candidate_neg_set.add((sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')))
        for sub, obj, z, w in ass3:
            rel = q
            candidate_neg_triples3.append([sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')])
            candidate_neg_set.add((sub.replace('<','').replace('>',''),rel,obj.replace('<','').replace('>','')))    
            
final_candidate_set = set()
for (sub,rel,obj) in candidate_neg_set:
    if (sub,rel,obj) not in all_true:
        final_candidate_set.add((sub,rel,obj))
        
        
import random
SPLIT_RATIO = [0.8,0.1,0.1]
derived_facts = list(final_candidate_set)

train_neg_facts = derived_facts[:int(len(derived_facts)*SPLIT_RATIO[0])]
if len(train_neg_facts) > len(positive_train_triples):
    train_neg_facts = random.sample(train_neg_facts, len(positive_train_triples))
valid_neg_facts = derived_facts[int(len(derived_facts)*SPLIT_RATIO[0]):int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1]))]
if len(valid_neg_facts) > len(positive_valid_triples):
    valid_neg_facts = random.sample(valid_neg_facts, len(positive_valid_triples))
test_neg_facts = derived_facts[int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1])):]
if len(test_neg_facts) > len(positive_test_triples):
    test_neg_facts = random.sample(test_neg_facts, len(positive_test_triples))

f_train = open('benchmarks/{}/train_neg_qg.txt'.format(dataset), 'w+')
f_valid = open('benchmarks/{}/valid_neg_qg.txt'.format(dataset), 'w+')
f_test = open('benchmarks/{}/test_neg_qg.txt'.format(dataset), 'w+')

for t in train_neg_facts:
    f_train.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f_train.close()     
for t in valid_neg_facts:
    f_valid.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f_valid.close()     
for t in test_neg_facts:
    f_test.write('{}\t{}\t{}\n'.format(t[0], t[1], t[2]))
f_test.close()   