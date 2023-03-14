# LogInfer

This repository is for reproducing the experiment results in the paper: "Revisiting Inferential Benchmarks for Knowledge Graph Completion"

----------------------------------

1. Benchmarks

1.1 Datasets

The original dataset of FB15K237 can be found at the folder FB_ori, which contains three files:
- positive training set: FB_ori/train.txt  
- positive validation set: FB_ori/validation.txt  
- positive test set: FB_ori/test.txt

The original dataset of WN18RR can be found at the folder WN_ori, which contains three files:
- positive training set: WN_ori/train.txt  
- positive validation set: WN_ori/validation.txt  
- positive test set: WN_ori/test.txt

We also generated a file FB.ttl and WN.ttl by merging all the three sets, which is used for RDFox.

The original dataset of LUBM can be found in the file LUBM1_0.ttl.

1.2 LogInfer

All 37 benchmarks used in the experiments are available at the folder LogicInfer-benchmark in this repository.

Each benchmark LogInferFB^Y_Z / LogInferWN^Y_Z / LogInferLUBM^Y_Z contains the following in the subfolder LogInferFB-Y / LogInferWN-Y / LogInferLUBM-Y:

- train.txt    --------positive training set
- valid.txt    --------positive validation set
- test.txt    --------positive training set
- candidate_entities.txt    --------Entities for generating negative examples using relevance-based random sampling
- candidate_relations.txt    --------Relations for generating negative examples using relevance-based random sampling
- train_neg_Z.txt    --------Negative training set
- valid_neg_Z.txt    --------Negative validation set
- test_neg_Z.txt    --------Negative test set

----------------------------------

2. System Requirement
- Python 3.6.9
- numpy
- random
- [RDFox](https://www.oxfordsemantic.tech/product)


----------------------------------


3. Benchmark Generation

3.1 Rule Generation, application, and splitting

Given a KG (FB/WN/LUBM) and the inference patterns, to generate the candidate rules \mathcal{R}_\text{cand}, and generate a command which is used for searching the support of the body with RDFox, run the following command at this folder:

``time python generate_command.py --dataset DATASET_NAME --pattern PATTERN_NAME``

where DATASET_NAME can be chosen from {FB, WN, LUBM}, and PATTERN_NAME can be chosen from {symmetry, hierarchy, inversion, composition, intersection, triangle, diamond}.


Then, to use RDFox for searching the support of the body of the rules, put the RDFox files and licenses in this folder, and run the following command:

``./RDFox sandbox . start_DATASET_NAME_PATTERN_NAME.rdfox``


Finally, to select rules, conduct rule application and distribute the application results, run the following command at this folder:

``time python split.py --dataset DATASET_NAME --pattern PATTERN_NAME --topk k1 --sample_split k2``

where DATASET_NAME can be chosen from {FB, WN, LUBM}, PATTERN_NAME can be chosen from {symmetry, hierarchy, inversion, composition, intersection, triangle, diamond}, and k1 and k2 are two numbers mentioned in the paper, which can be customised based on the expected size and rule diversity of the benchmark.

Finally, there will be 5 files in the folder:

- train.txt    --------positive training set
- valid.txt    --------positive validation set
- test.txt    --------positive test set
- candidate_entities.txt    ---------entities for generating negative examples using relevance-based random sampling
- candidate_relations.txt   ---------relations for generating negative examples using relevance-based random sampling:    


3.2 Negative Example Generation

3.2.1 Relevance-Based Negative Sampling

To conduct relevance-based negative sampling for a benchmark named as BENCHMARK_NAME, run the following command at this folder:

``time python negative_rb.py --dataset BENCHMARK_NAME``

This will result in 3 files in the folder benchmarks/BENCHMARK_NAME/:

- train_neg_rb.txt
- valid_neg_rb.txt
- test_neg_rb.txt


3.2.2 Position-Aware Corruption

To conduct position-aware corruption for a benchmark named as BENCHMARK_NAME, run the following command at this folder:

``time python negative_pa.py --dataset BENCHMARK_NAME``

This will result in 3 files in the folder benchmarks/BENCHMARK_NAME/:
- train_neg_pa.txt
- valid_neg_pa.txt
- test_neg_pa.txt


3.2.3 Query-Guided Negative Sampling

To conduct query-guided negative sampling for a benchmark named as BENCHMARK_NAME, firstly, run the following command at this folder:

``time python generate_query_qg.py --dataset BENCHMARK_NAME``


Then, run the following command to search for the assignments for the body of the rules \mathcal{R}^-:

``./RDFox sandbox . search_BENCHMARK_NAME_negative.rdfox``


Finally, to generate the negative examples for a benchmark named as BENCHMARK_NAME, run the following command at this folder:

``time python negative_qg.py --dataset BENCHMARK_NAME``

This will result in 3 files in the folder benchmarks/BENCHMARK_NAME/:
- train_neg_qg.txt
- valid_neg_qg.txt
- test_neg_qg.txt



----------------------------------

4. Additional Scripts for Experiments

4.1 Conventional Random Corruption

In our experiments, we also compared our negative sampling strategy with the conventional random corruption strategy. To generate negative examples using conventional random corruption for a benchmark named as BENCHMARK_NAME, run the following command at this folder:

``time python negative_rc.py --dataset BENCHMARK_NAME``

This will result in 3 files in the folder benchmarks/BENCHMARK_NAME/:
- train_neg_rc.txt
- valid_neg_rc.txt
- test_neg_rc.txt


4.2 Simple Baseline

To evaluate a simple baseline on the benchmark, run the following command at this folder:

``time python simple.py --dataset BENCHMARK_NAME --neg NEGATIVE_SAMPLING_STRATEGY``

where NEGATIVE_SAMPLING_STRATEGY can be chosen from {rb, pa, qg}.


----------------------------------

5. Rules Used for LUBM

The 107 rules used for LUBM can be found in the file LUBM_rule_all.dlog at this folder.


This repository is for our 37 benchmarks proposed in the paper "Revisiting Inferential Benchmarks for Knowledge Graph Completion"


