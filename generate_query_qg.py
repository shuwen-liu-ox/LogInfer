"""
This is the script for generating querys to search assignments for body-subset rules 

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


f_command = open('search_{}_negative.rdfox'.format(dataset),'w+')
f_command.write('endpoint start\ndstore create {}\nactive {}\nimport {}.ttl\n'.format(DATASET, DATASET, DATASET))

if 'trian' in dataset:
    for rule in rules:
        r,s,t,p = rule
        R=r
        S=s
        T=t
        P=p
        path = 'negative_assignments_{}'.format(dataset)
        if not os.path.exists(path):
            os.makedirs(path)
        f_command.write("set output {}/assignments_R={}_notS={}_T={}.txt\n".format(path, relation_dic['<file://'+R+'>'], relation_dic['<file://'+S+'>'], relation_dic['<file://'+T+'>']))
        f_command.write('SELECT ?x  ?y  ?z WHERE {?x <file://'+R+'> ?y . FILTER( !EXISTS {?x <file://'+S+'> ?z})}\n')
        f_command.write("set output {}/assignments_R={}_S={}_notT={}.txt\n".format(path, relation_dic['<file://'+R+'>'], relation_dic['<file://'+S+'>'], relation_dic['<file://'+T+'>']))
        f_command.write('SELECT ?x  ?y  ?z WHERE {?x <file://'+R+'> ?y . FILTER( !EXISTS {?y <file://'+T+'> ?z})}\n')
        f_command.write("set output {}/assignments_notR={}_S={}_T={}.txt\n".format(path, relation_dic['<file://'+R+'>'], relation_dic['<file://'+S+'>'], relation_dic['<file://'+T+'>']))
        f_command.write('SELECT ?x  ?y  ?z WHERE {?x <file://'+S+'> ?y . FILTER( !EXISTS {?y <file://'+T+'> ?z})}\n')

elif 'inter' in dataset:
    for rule in rules:
        r,s,t = rule
        R=r
        S=s
        path = 'negative_assignments_{}'.format(dataset)
        if not os.path.exists(path):
            os.makedirs(path)
        f_command.write("set output {}/assignments_R={}_notS={}.txt\n".format(path, relation_dic['<'+R+'>'], relation_dic['<'+S+'>']))
        f_command.write('SELECT ?x  ?y WHERE {?x <file://'+R+'> ?y . FILTER( !EXISTS {?x <file://'+S+'> ?y})}\n')
        f_command.write("set output {}/assignments_notR={}_S={}.txt\n".format(path, relation_dic['<'+R+'>'], relation_dic['<'+S+'>']))
        f_command.write('SELECT ?x  ?y WHERE {?x <file://'+S+'> ?y . FILTER( !EXISTS {?x <file://'+R+'> ?y})}\n')

    
elif 'diam' in dataset:
    for rule in rules:
    r,s,t,p,q = rule
    R=r
    S=s
    T=t
    P=p
    Q=q
    path = 'negative_assignments_{}_{}'.format(DATASET,PATTERN)
    if not os.path.exists(path):
        os.makedirs(path)
    f_command.write("set output {}/assignments_R={}_notS={}_T={}_P={}_Q={}.txt\n".format(path, relation_dic['<'+R+'>'], relation_dic['<'+S+'>'], relation_dic['<'+T+'>'], relation_dic['<'+P+'>'], relation_dic['<'+Q+'>']))
    f_command.write('SELECT ?x  ?y  ?z ?w WHERE {?x <file://'+R+'> ?y . FILTER( !EXISTS {?x <file://'+S+'> ?z})}\n')
    f_command.write("set output {}/assignments_R={}_S={}_notT={}_P={}_Q={}.txt\n".format(path, relation_dic['<'+R+'>'], relation_dic['<'+S+'>'], relation_dic['<'+T+'>'], relation_dic['<'+P+'>'], relation_dic['<'+Q+'>']))
    f_command.write('SELECT ?x  ?y  ?z ?w WHERE {?x <file://'+R+'> ?y . FILTER( !EXISTS {?y <file://'+T+'> ?w})}\n')
    f_command.write("set output {}/assignments_notR={}_S={}_T={}_P={}_Q={}.txt\n".format(path, relation_dic['<'+R+'>'], relation_dic['<'+S+'>'], relation_dic['<'+T+'>'], relation_dic['<'+P+'>'], relation_dic['<'+Q+'>']))
    f_command.write('SELECT ?x  ?y  ?z ?w WHERE {?x <file://'+S+'> ?y . ?x <file://'+T+'> ?y . FILTER( !EXISTS {?y <file://'+R+'> ?w})}\n')
f_command.close()