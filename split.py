import os
import argparse
import random

parser = argparse.ArgumentParser()

parser.add_argument('--dataset', type=str, required=True,
                    help='Name of dataset')
parser.add_argument('--pattern', type=str, required=True,
                    help='Pattern we use')
parser.add_argument('--sample_s', type=int, default=1,
                    help='Number of head we sample')
parser.add_argument('--topk', type=int, default=5,
                    help='To select top K rules sorted by the number of assignments (which is k1 in our paper)')
parser.add_argument('--sample_split', type=int, default=2000,
                    help='Number of triples used for splitting (which is k2 in our paper)')

args = parser.parse_args()
DATASET = args.dataset
PATTERN = args.pattern
SAMPLE_FOR_S = args.sample_s
TOPK_RULE = args.topk

SAMPLE_FOR_SPLIT = args.sample_split
SPLIT_RATIO = [0.8, 0.1, 0.1]


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

def get_file_len(filename):
    with open(filename) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

def dictionary(input_list):
    
    """
    To generate a dictionary.
    Index: item in the array.
    Value: the index of this item.
    """
    
    return dict(zip(input_list, range(len(input_list))))

facts = []
fact_set = set()
f_data = open ("{}.ttl".format(DATASET))
count = 0
relations = set()
for line in f_data :
    count += 1
    if count < 3:
        continue
    triple = line.strip().split(' ')
    facts.append(triple)
    fact_set.add((triple[0], triple[1], triple[2])) 

f_relation_dic = open('relation_{}_{}.dict'.format(DATASET,PATTERN))
relations = []
for line in f_relation_dic:
    relation_new = line.strip()
    relations.append(relation_new)    
relation_dic = dictionary(relations)    
SPLIT_RATIO = [0.8, 0.1, 0.1]


#generate rules for symmetry/inversion/hierarchy
if PATTERN == 'symmetry' or PATTERN == 'inversion' or PATTERN == 'hierarchy':
    dict_relation_num_of_assignments = dict()
    for relation in relations:
        count = -1
        file_name = 'output_{}_{}/assignments_R={}.txt'.format(DATASET,PATTERN, relation_dic[relation])
        num_of_assignments = get_file_len(file_name) - 9
        #filter out relations with 0 assignments
        if num_of_assignments:
            if relation not in dict_relation_num_of_assignments:
                dict_relation_num_of_assignments[relation] = num_of_assignments
    dict_relation_num_of_assignments = sorted(dict_relation_num_of_assignments.items(), key=lambda x: x[1], reverse=True)
    #start to filter out those redundant rules
    derived_facts = set()
    #no need to check redundant rule for symmetry
    if PATTERN == 'symmetry':
        final_R = []
        rcount = 0
        for R, count in dict_relation_num_of_assignments:
            final_R.append(R)
            rcount += 1
            if rcount == TOPK_RULE:
                break
        f = open('final_rules_{}_{}.txt'.format(DATASET, PATTERN), 'w+')
        for r in final_R:
            f.write('{}\n'.format(r.replace('<','').replace('>','')))
        f.close()
    if PATTERN == 'inversion' or PATTERN == 'hierarchy':
        final_R_S = []
        rcount = 0
        flag = 1
        #check the redundant rules
        check_set = set() 
        for R, count in dict_relation_num_of_assignments:
            candidates_S = random.sample(relations, SAMPLE_FOR_S)
            for S in candidates_S:
                #to check if S(a,b) has already be contained in the derived facts
                if S not in check_set and S != R:
                    final_R_S.append([R,S])
                    rcount += 1
                    if rcount == TOPK_RULE:
                        flag = 0
                        break
            if flag == 0:
                break
                    
        print(len(final_R_S))
        f = open('final_rules_{}_{}.txt'.format(DATASET, PATTERN), 'w+')
        for r,s in final_R_S:
            f.write('{}\t{}\n'.format(r.replace('<','').replace('>',''), s.replace('<','').replace('>','')))
        f.close()


#generate rules for intersection/composition
if PATTERN == 'intersection' or PATTERN == 'composition':
    rs_set = set()
    dict_RS_num_of_assignments = dict()
    for R in relations:
        for S in relations:
            if (R,S) not in rs_set:
                rs_set.add((R,S))
                rs_set.add((S,R))
                if R != S:
                    count = -1
                    file_name = 'output_{}_{}/assignments_R={}_S={}.txt'.format(DATASET, PATTERN, relation_dic[R], relation_dic[S])
                    if True:
                        
                        num_of_assignments = get_file_len(file_name) - 9
                        #filter out relations with 0 assignments
                        if num_of_assignments:
                            if (R,S) not in dict_RS_num_of_assignments:
                                dict_RS_num_of_assignments[(R,S)] = num_of_assignments
    dict_RS_num_of_assignments = sorted(dict_RS_num_of_assignments.items(), key=lambda x: x[1], reverse=True)
    derived_facts = set()
    final_R_S_T = []
    rcount = 0
    #check the redundant rules
    check_set = set() 
    flag = 1
    for (R,S), count in dict_RS_num_of_assignments:
        while True:
            candidates_head = random.sample(relations, 1)
            head = candidates_head[0]
            if head not in check_set and head != R and head != S:
                break
            else:
                continue
            
        final_R_S_T.append([R,S,head])
        rcount += 1
        if rcount == TOPK_RULE:
            flag = 0
            break
    f = open('final_rules_{}_{}.txt'.format(DATASET, PATTERN), 'w+')
    for r,s,t in final_R_S_T:
        f.write('{}\t{}\t{}\n'.format(r.replace('<file://','').replace('>','').replace('<',''), s.replace('<file://','').replace('>','').replace('<',''), t.replace('<file://','').replace('>','').replace('<','')))
    f.close()
    

if PATTERN == 'triangle':
    rst_set = set()
    dict_RST_num_of_assignments = dict()
    for R in relations:
        for S in relations:
            for T in relations:
                if (R,S,T) not in rst_set:
                    rst_set.add((R,S,T))
                    if True:
                        count = -1
                        try:
                            file_name = 'output_{}_{}/assignments_R={}_S={}_T={}.txt'.format(DATASET, PATTERN, relation_dic[R], relation_dic[S], relation_dic[T])
                            num_of_assignments = get_file_len(file_name) - 9
                        except:
                            continue
                        #filter out relations with 0 assignments
                        if num_of_assignments:
                            if (R,S,T) not in dict_RST_num_of_assignments:
                                dict_RST_num_of_assignments[(R,S,T)] = num_of_assignments
    dict_RST_num_of_assignments = sorted(dict_RST_num_of_assignments.items(), key=lambda x: x[1], reverse=True)
    derived_facts = set()
    final_R_S_T_P = []
    rcount = 0
    #check the redundant rules
    check_set = set() 
    flag = 1
    for (R,S,T), count in dict_RST_num_of_assignments:
        while True:
            candidates_head = random.sample(relations, 1)
            head = candidates_head[0]
            if head not in check_set and head != R and head != S and head!=T:
                break
            else:
                continue
            
        final_R_S_T_P.append([R,S,T,head])
        rcount += 1
        if rcount == TOPK_RULE:
            flag = 0
            break
    f = open('final_rules_{}_{}.txt'.format(DATASET, PATTERN), 'w+')
    for r,s,t,p in final_R_S_T_P:
        f.write('{}\t{}\t{}\t{}\n'.format(r.replace('<file://','').replace('>',''), s.replace('<file://','').replace('>',''), t.replace('<file://','').replace('>',''), p.replace('<file://','').replace('>','')))
    f.close()    
    
rstp_set = set()
#generate rules for diamond
if PATTERN == 'diamond':

    rstp = []
    for r in relation_set1:
        for s in relation_set1:
            if (r,s) in rs:
                for t in relation_set1:
                    if (r,t) in rt:
                        for p in relation_set1:
                            if (t,p) in tp:
                                if (s,p) in sp:
                                    rstp.append([r,s,t,p])
    print(len(rstp))
    for R,S,T,P in rstp:
        count = -1
        try:
            file_name = 'output_{}_{}/assignments_R={}_S={}_T={}_P={}.txt'.format(DATASET, PATTERN, relation_dic[R], relation_dic[S], relation_dic[T], relation_dic[P])
            num_of_assignments = get_file_len(file_name) - 9
        except:
            continue
        #filter out relations with 0 assignments
        if num_of_assignments:
            if (R,S,T,P) not in dict_RSTP_num_of_assignments:
                dict_RSTP_num_of_assignments[(R,S,T,P)] = num_of_assignments
    dict_RSTP_num_of_assignments = sorted(dict_RSTP_num_of_assignments.items(), key=lambda x: x[1], reverse=True)
    derived_facts = set()
    final_R_S_T_P_Q = []
    rcount = 0
    #check the redundant rules
    check_set = set() 
    flag = 1
    for (R,S,T,P), count in dict_RSTP_num_of_assignments:
        while True:
            candidates_head = random.sample(relations, 1)
            head = candidates_head[0]
            if head not in check_set and head != R and head != S and head!=T and head!=P:
                break
            else:
                continue
            
        final_R_S_T_P_Q.append([R,S,T,P,head])
        rcount += 1
        if rcount == TOPK_RULE:
            flag = 0
            break
    f = open('final_rules_{}_{}.txt'.format(DATASET, PATTERN), 'w+')
    for r,s,t,p,q in final_R_S_T_P_Q:
        f.write('{}\t{}\t{}\t{}\t{}\n'.format(r.replace('<file://','').replace('>',''), s.replace('<file://','').replace('>',''), t.replace('<file://','').replace('>',''), p.replace('<file://','').replace('>',''), q.replace('<file://','').replace('>','')))
    f.close()  
'''
split train/valid/test for transductive setting
'''
  
trains = []
valids = []
tests = []
lens= []

candidate_entity_set = set()
candidate_relation_set = set()
if PATTERN == 'symmetry':
    for R in final_R:
        derived_facts = []
        candidate_relation_set.add(R.replace('file://','').replace('<','').replace('>',''))
        assignments = read_assignments('output_{}_{}/assignments_R={}.txt'.format(DATASET,PATTERN, relation_dic[R]))
        for assignment in assignments:
            candidate_entity_set.add(assignment[0].replace('file://','').replace('<','').replace('>',''))
            candidate_entity_set.add(assignment[1].replace('file://','').replace('<','').replace('>',''))
            if (assignment[1], R, assignment[0]) not in fact_set:
                derived_facts.append([assignment[1], R, assignment[0]])

        random.shuffle(derived_facts)
        if len(derived_facts) > SAMPLE_FOR_SPLIT:
            derived_facts = random.sample(derived_facts, SAMPLE_FOR_SPLIT)
        train_facts = derived_facts[:int(len(derived_facts)*SPLIT_RATIO[0])]
        valid_facts = derived_facts[int(len(derived_facts)*SPLIT_RATIO[0]):int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1]))]
        test_facts = derived_facts[int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1])):]
        for t in train_facts:
            trains.append(t)
        for t in valid_facts:
            valids.append(t)
        for t in test_facts:
            tests.append(t)
            
elif PATTERN == 'inversion' or PATTERN == 'hierarchy':
    for R, S in final_R_S:
        candidate_relation_set.add(S.replace('file://','').replace('<','').replace('>',''))
        derived_facts = []
        assignments = read_assignments('output_{}_{}/assignments_R={}.txt'.format(DATASET, PATTERN, relation_dic[R]))
        for assignment in assignments:
            candidate_entity_set.add(assignment[0].replace('file://','').replace('<','').replace('>',''))
            candidate_entity_set.add(assignment[1].replace('file://','').replace('<','').replace('>',''))            
            if PATTERN == 'inversion':
                if (assignment[1], S, assignment[0]) not in fact_set:
                    derived_facts.append([assignment[1], S, assignment[0]])
            elif PATTERN == 'hierarchy':
                if (assignment[0], S, assignment[1]) not in fact_set:
                    derived_facts.append([assignment[0], S, assignment[1]])  

        random.shuffle(derived_facts)
        if len(derived_facts) > SAMPLE_FOR_SPLIT:
            derived_facts = random.sample(derived_facts, SAMPLE_FOR_SPLIT)
        train_facts = derived_facts[:int(len(derived_facts)*SPLIT_RATIO[0])]
        valid_facts = derived_facts[int(len(derived_facts)*SPLIT_RATIO[0]):int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1]))]
        test_facts = derived_facts[int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1])):]
        for t in train_facts:
            trains.append(t)
        for t in valid_facts:
            valids.append(t)
        for t in test_facts:
            tests.append(t)
            
elif PATTERN =='intersection':
    for R, S, T in final_R_S_T:
        candidate_relation_set.add(T.replace('file://','').replace('<','').replace('>',''))
        derived_facts = []
        assignments = read_assignments('output_{}_{}/assignments_R={}_S={}.txt'.format(DATASET,PATTERN, relation_dic[R], relation_dic[S]))
        for assignment in assignments:
            candidate_entity_set.add(assignment[0].replace('file://','').replace('<','').replace('>',''))
            candidate_entity_set.add(assignment[1].replace('file://','').replace('<','').replace('>',''))
            
            if (assignment[0], T, assignment[1]) not in fact_set:
                derived_facts.append([assignment[0], T, assignment[1]])  

        random.shuffle(derived_facts)
        if len(derived_facts) > SAMPLE_FOR_SPLIT:
            derived_facts = random.sample(derived_facts, SAMPLE_FOR_SPLIT)
        train_facts = derived_facts[:int(len(derived_facts)*SPLIT_RATIO[0])]
        valid_facts = derived_facts[int(len(derived_facts)*SPLIT_RATIO[0]):int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1]))]
        test_facts = derived_facts[int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1])):]
        for t in train_facts:
            trains.append(t)
        for t in valid_facts:
            valids.append(t)
        for t in test_facts:
            tests.append(t)
            
elif PATTERN =='composition':
    for R, S, T in final_R_S_T:
        candidate_relation_set.add(T.replace('file://','').replace('<','').replace('>',''))
        derived_facts = []
        derived_fact_set = set()
        try:
            assignments = read_assignments2('output_{}_{}/assignments_R={}_S={}.txt'.format(DATASET, PATTERN, relation_dic[R], relation_dic[S]))
        except:
            continue
        
        for assignment in assignments:
            candidate_entity_set.add(assignment[0].replace('file://','').replace('<','').replace('>',''))
            candidate_entity_set.add(assignment[1].replace('file://','').replace('<','').replace('>',''))
            candidate_entity_set.add(assignment[2].replace('file://','').replace('<','').replace('>',''))
            if (assignment[0], T, assignment[2]) not in fact_set and (assignment[0], T, assignment[2]) not in derived_fact_set:
                derived_facts.append([assignment[0], T, assignment[2]])  
                derived_fact_set.add((assignment[0], T, assignment[2]))
        random.shuffle(derived_facts)
        if len(derived_facts) > SAMPLE_FOR_SPLIT:
            derived_facts = random.sample(derived_facts, SAMPLE_FOR_SPLIT)
        train_facts = derived_facts[:int(len(derived_facts)*SPLIT_RATIO[0])]
        valid_facts = derived_facts[int(len(derived_facts)*SPLIT_RATIO[0]):int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1]))]
        test_facts = derived_facts[int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1])):]
        for t in train_facts:
            trains.append(t)
        for t in valid_facts:
            valids.append(t)
        for t in test_facts:
            tests.append(t)

            
elif PATTERN =='triangle':
    for R, S, T, P in final_R_S_T_P:
        candidate_relation_set.add(P.replace('file://','').replace('<','').replace('>',''))
        derived_facts = []
        derived_fact_set = set()
        assignments = read_assignments('output_{}_{}/assignments_R={}_S={}_T={}.txt'.format(DATASET,PATTERN, relation_dic[R], relation_dic[S], relation_dic[T]))
        for assignment in assignments:
            candidate_entity_set.add(assignment[0].replace('file://','').replace('<','').replace('>',''))
            candidate_entity_set.add(assignment[1].replace('file://','').replace('<','').replace('>',''))
            if (assignment[0], P, assignment[1]) not in fact_set and (assignment[0], P, assignment[1]) not in derived_fact_set:
                derived_facts.append([assignment[0], P, assignment[1]])  
                derived_fact_set.add((assignment[0], P, assignment[1])) 
        random.shuffle(derived_facts)
        if len(derived_facts) > SAMPLE_FOR_SPLIT:
            derived_facts = random.sample(derived_facts, SAMPLE_FOR_SPLIT)
        train_facts = derived_facts[:int(len(derived_facts)*SPLIT_RATIO[0])]
        valid_facts = derived_facts[int(len(derived_facts)*SPLIT_RATIO[0]):int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1]))]
        test_facts = derived_facts[int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1])):]
        for t in train_facts:
            trains.append(t)
        for t in valid_facts:
            valids.append(t)
        for t in test_facts:
            tests.append(t)
            
elif PATTERN =='diamond':
    for R, S, T, P, Q in final_R_S_T_P_Q:
        candidate_relation_set.add(Q.replace('file://','').replace('<','').replace('>',''))
        derived_facts = []
        derived_fact_set = set()
        assignments = read_assignments('output_{}_{}/assignments_R={}_S={}_T={}_P={}.txt'.format(DATASET,PATTERN, relation_dic[R], relation_dic[S], relation_dic[T], relation_dic[P]))
        for assignment in assignments:
            candidate_entity_set.add(assignment[0].replace('file://','').replace('<','').replace('>',''))
            candidate_entity_set.add(assignment[1].replace('file://','').replace('<','').replace('>',''))
            if (assignment[0], Q, assignment[1]) not in fact_set and (assignment[0], Q, assignment[1]) not in derived_fact_set:
                derived_facts.append([assignment[0], Q, assignment[1]])  
                derived_fact_set.add((assignment[0], Q, assignment[1])) 
        random.shuffle(derived_facts)
        if len(derived_facts) > SAMPLE_FOR_SPLIT:
            derived_facts = random.sample(derived_facts, SAMPLE_FOR_SPLIT)
        train_facts = derived_facts[:int(len(derived_facts)*SPLIT_RATIO[0])]
        valid_facts = derived_facts[int(len(derived_facts)*SPLIT_RATIO[0]):int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1]))]
        test_facts = derived_facts[int(len(derived_facts)*(SPLIT_RATIO[0]+SPLIT_RATIO[1])):]
        for t in train_facts:
            trains.append(t)
        for t in valid_facts:
            valids.append(t)
        for t in test_facts:
            tests.append(t)
            
print('Num of triples in T_train:', len(trains)) 
print('Num of triples in T_valid:', len(valids))
print('Num of triples in T_test:', len(tests))

map_dic={'symmetry':'sym', 'inversion':'inver', 'hierarchy':'hier', 'composition':'comp', 'intersection':'inter', 'triangle':'trian', 'diamond':'diam'}

path = 'benchmarks/LogInfer-{}-{}'.format(DATASET, map_dic[PATTERN])
if not os.path.exists(path):
    os.makedirs(path)
f_train = open('{}/train.txt'.format(path),'w+')

f_ori1 = open('{}_ori/train.txt'.format(DATASET))
f_ori2 = open('{}_ori/valid.txt'.format(DATASET))
f_ori3 = open('{}_ori/test.txt'.format(DATASET))
for line in f_ori1:
    f_train.write(line)

for line in f_ori2:
    f_train.write(line)

for line in f_ori3:
    f_train.write(line)
all_set = set()
for t in trains: 
    all_set.add((t[0],t[1], t[2]))
    f_train.write('{}\t{}\t{}\n'.format(t[0].replace('file://','').replace('<','').replace('>',''),t[1].replace('file://','').replace('<','').replace('>',''),t[2].replace('file://','').replace('<','').replace('>','')))
f_train.close()
f_valid = open('{}/valid.txt'.format(path),'w+')
for t in valids:
    if (t[0],t[1], t[2]) not in all_set:
                f_valid.write('{}\t{}\t{}\n'.format(t[0].replace('file://','').replace('<','').replace('>',''),t[1].replace('file://','').replace('<','').replace('>',''),t[2].replace('file://','').replace('<','').replace('>','')))
    all_set.add((t[0],t[1], t[2]))
f_valid.close()
f_test = open('{}/test.txt'.format(path),'w+')
for t in tests:
    if (t[0],t[1], t[2]) not in all_set:
                f_test.write('{}\t{}\t{}\n'.format(t[0].replace('file://','').replace('<','').replace('>',''),t[1].replace('file://','').replace('<','').replace('>',''),t[2].replace('file://','').replace('<','').replace('>','')))
f_test.close()

f_entity = open('{}/candidate_entities.txt'.format(path),'w+')  
for entity in candidate_entity_set:
    f_entity.write(entity)
    f_entity.write('\n')
f_entity.close()

f_relation = open('{}/candidate_relations.txt'.format(path),'w+')  
for relation in candidate_relation_set:
    f_relation.write(entity)
    f_relation.write('\n')
f_relation.close()