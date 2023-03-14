import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--dataset', type=str, required=True,
                    help='Name of dataset')
parser.add_argument('--pattern', type=str, required=True,
                    help='Pattern we use')

args = parser.parse_args()
DATASET = args.dataset
PATTERN = args.pattern
path = 'benchmarks'
if not os.path.exists(path):
	os.makedirs(path)
def dictionary(input_list):
    
    """
    To generate a dictionary.
    Index: item in the array.
    Value: the index of this item.
    """
    
    return dict(zip(input_list, range(len(input_list))))

f_data = open ("{}.ttl".format(DATASET))

relations = set()
count = 0
try:
    f_relation_dic = open('relation_{}_{}.dict'.format(DATASET,PATTERN))
    relations = []
    for line in f_relation_dic:
        relation_new = line.strip()
        relations.append(relation_new)
except:
    for line in f_data:
        count += 1
        if count < 3:
            continue
        t = line.strip().split(' ')
        relations.add(t[1])
    relations = list(relations)
    f = open('relation_{}_{}.dict'.format(DATASET,PATTERN),'w+')
    for i in range(len(relations)):
        f.write('{}\n'.format(relations[i]))
    f.close()

relation_dic = dictionary(relations)
count = 0
f_command = open('start_{}_{}.rdfox'.format(DATASET, PATTERN),'w+')
f_command.write('endpoint start\ndstore create {}\nactive {}\nimport {}.ttl\n'.format(DATASET, DATASET, DATASET))

print('yes')
#generate RDFox command for searching the assignments-------------symmetry/inversion/hierarchy
if PATTERN == 'symmetry' or PATTERN == 'inversion' or PATTERN == 'hierarchy':
    for R in relations:    
        path = 'output_{}_{}'.format(DATASET,PATTERN)
        if not os.path.exists(path):
            os.makedirs(path)
        f_command.write("set output {}/assignments_R={}.txt\n".format(path, relation_dic[R]))
        if DATASET == 'WN':
            f_command.write('SELECT ?p  ?c WHERE {{ ?p <{} ?c}}\n'.format(R[1:]))
        else:
            f_command.write('SELECT ?p  ?c WHERE {{ ?p <file://{} ?c}}\n'.format(R[1:]))
        count+=1
    f_command.write('quit\n')
    f_command.close()
rs_set = set()

    
#generate RDFox command for searching the assignments-------------intersection/composition    
if PATTERN == 'intersection' or PATTERN == 'composition':
    for R in relations:
        for S in relations:
            if (R,S) not in rs_set and (S,R) not in rs_set:
                rs_set.add((R,S))
                if R != S:
                    path = 'output_{}_{}'.format(DATASET,PATTERN)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    f_command.write("set output {}/assignments_R={}_S={}.txt\n".format(path, relation_dic[R], relation_dic[S]))
                    if DATASET == 'WN':
                        if PATTERN == 'intersection':
                            f_command.write('SELECT ?p  ?c WHERE {?p <'+R[1:]+' ?c . ?p <'+S[1:]+' ?c}\n')
                        elif PATTERN == 'composition':
                            f_command.write('SELECT ?p ?x ?c WHERE {?p <'+R[1:]+' ?x . ?x <'+S[1:]+' ?c}\n')
                    else:
                        if PATTERN == 'intersection':
                            f_command.write('SELECT ?p  ?c WHERE {?p <file://'+R[1:]+' ?c . ?p <file://'+S[1:]+' ?c}\n')
                        elif PATTERN == 'composition':
                            f_command.write('SELECT ?p ?x ?c WHERE {?p <file://'+R[1:]+' ?x . ?x <file://'+S[1:]+' ?c}\n')
    f_command.write('quit\n')
    f_command.close() 

#generate RDFox command for searching the assignments-------------triangle

if PATTERN == 'triangle':
    rst_set = set()
    count = 0
    f_command = open('commands_triangle/start_{}_{}.rdfox'.format(PATTERN, count),'w+')
    f_command.write('endpoint start\ndstore create {}\nactive {}\nimport {}.ttl\n'.format(DATASET, DATASET, DATASET))
    for R in relations:
        for S in relations:
            for T in relations:                
                if (R,S,T) not in rst_set:
                    count+= 1
                    
                    rst_set.add((R,S,T))
                    path = 'output_{}_{}'.format(DATASET, PATTERN)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    f_command.write("set output {}/assignments_R={}_S={}_T={}.txt\n".format(path, relation_dic[R], relation_dic[S], relation_dic[T]))
                    if DATASET == 'WN':
                        f_command.write('SELECT ?x ?y ?z WHERE {?x <'+R[1:]+' ?y . ?x <'+S[1:]+' ?z . ?y <'+T[1:]+' ?z . FILTER(?x != ?y) . FILTER(?x != ?z) . FILTER(?z != ?y)}\n')
                    else:
                        f_command.write('SELECT ?x ?y ?z WHERE {?x <file://'+R[1:]+' ?y . ?x <file://'+S[1:]+' ?z . ?y <file://'+T[1:]+' ?z . FILTER(?x != ?y) . FILTER(?x != ?z) . FILTER(?z != ?y)}\n')
                        
                        f_command.write('quit\n')
                        f_command.close()
                        f_command = open('commands_triangle/start_{}_{}.rdfox'.format(PATTERN, count),'w+')
                        f_command.write('endpoint start\ndstore create {}\nactive {}\nimport {}.ttl\n'.format(DATASET, DATASET, DATASET))
    f_command.write('quit\n')
    f_command.close()

#generate RDFox command for searching the assignments-------------diamond

if PATTERN == 'diamond':
    rstp_set = set()
    for R in relations:
        for S in relations:
            for T in relations:   
                for P in relations:
                    if (R,S,T,P) not in rstp_set:
                        rstp_set.add((R,S,T,P))
                        path = 'output_{}_{}'.format(DATASET, PATTERN)
                        if not os.path.exists(path):
                            os.makedirs(path)
                        f_command.write("set output {}/assignments_R={}_S={}_T={}_P={}.txt\n".format(path, relation_dic[R], relation_dic[S], relation_dic[T], relation_dic[P]))
                        if DATASET == 'WN':
                            f_command.write('SELECT ?x ?y ?z WHERE {?x <'+R[1:]+' ?y . ?x <'+S[1:]+' ?z . ?y <'+T[1:]+' ?w . ?z <'+P[1:]+' ?w . FILTER(?x != ?y) . FILTER(?x != ?z) . FILTER(?x != ?w) . FILTER(?y != ?z) . FILTER(?y != ?w) . FILTER(?z != ?w)}\n')
                        else:
                            f_command.write('SELECT ?x ?y ?z WHERE {?x <file://'+R[1:]+' ?y . ?x <file://'+S[1:]+' ?z . ?y <file://'+T[1:]+' ?w . ?z <file://'+P[1:]+' ?w . FILTER(?x != ?y) . FILTER(?x != ?z) . FILTER(?x != ?w) . FILTER(?y != ?z) . FILTER(?y != ?w) . FILTER(?z != ?w)}\n')
    f_command.write('quit\n')
    f_command.close()  


