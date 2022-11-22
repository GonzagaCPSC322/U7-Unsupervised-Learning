import itertools

header = ["level", "lang", "tweets", "phd", "interviewed_well"]
table = [
        ["Senior", "Java", "no", "no", "False"],
        ["Senior", "Java", "no", "yes", "False"],
        ["Mid", "Python", "no", "no", "True"],
        ["Junior", "Python", "no", "no", "True"],
        ["Junior", "R", "yes", "no", "True"],
        ["Junior", "R", "yes", "yes", "False"],
        ["Mid", "R", "yes", "yes", "True"],
        ["Senior", "Python", "no", "no", "False"],
        ["Senior", "R", "yes", "no", "True"],
        ["Junior", "Python", "yes", "no", "True"],
        ["Senior", "Python", "yes", "yes", "True"],
        ["Mid", "Python", "no", "yes", "True"],
        ["Mid", "Java", "yes", "no", "True"],
        ["Junior", "Python", "no", "yes", "False"]
    ]

# warmup
def prepend_attribute_label(table, header):
    for row in table:
        for i in range(len(row)):
            row[i] = header[i] + "=" + str(row[i])

prepend_attribute_label(table, header)
for row in table:
    print(row)
# why do this? if we represent each row as a set, we can't distinguish
# between tweets and phd because they have overlapping domains

# unsupervised learning notes
# with unsupervised learning there is no special attribute (class)
# we are interested in predicting
# instead, we are looking for patterns, trends, groups, associations, etc.
# we are going to cover association rule mining (ARM) for PA8
# and clustering for BONUS PA9

# ARM notes
# recall: decision trees give us classification rules
# example: IF att1=val1 AND att2=val2 AND .... THEN class=label1
# let all the terms (att/value pair) to the left of the THEN be
# called the left hand side (LHS)
# let all the terms (att/value pair) to the right of the THEN be
# called the right hand side (RHS)
# with classification rules, there is at least one term in the LHS
# there is exactly one term in the RHS
# association rules relax this RHS constraint
# association rules: at least one term in the LHS and at least one term in the RHS
# example: IF att1=val1 AND att2=val2 AND .... THEN att10=val10 AND att11=val11 AND ...

# how to generate rules?
# brute force generate rules based on all possible term combinations
# VERY computationally expensive
# instead we will use the apriori algorithm
# some notes on apriori
# 1. even with tricks, still computationally expensive
# 2. generates lots of rules... some are "weak" and some are "rare"
# we will need to new metrics for evalutating association rules
# "rule interestingness measures"
# 3. association does not imply causality

# our game plan for learning ARM/apriori
# 1. Intro to ARM lab (today): given rules, interpret/evaluate them
# 2. Apriori lab (next classes): trace the algorithm to generate rules
# 3. PA8 starter code
# 4. Finish PA8 (last one!!)

# ARM lab task #2
# but first!! how to represent rules in python?
# use dictionaries!
# rule #1 IF interviewed_well=False THEN tweets=no
rule1 = {"lhs": ["interviewed_well=False"], "rhs": ["tweets=no"]}
# rule #5 IF phd=no AND tweets=yes THEN interviewed_well=True
rule5 = {"lhs": ["phd=no", "tweets=yes"], "rhs": ["interviewed_well=True"]}

def check_row_match(terms, row):
    # return 1 if all the terms are in the row (match)
    # return 0 otherwise
    for term in terms:
        if term not in row:
            return 0
    return 1

def compute_rule_counts(rule, table):
    Nleft = Nright = Nboth = 0
    Ntotal = len(table)
    for row in table:
        Nleft += check_row_match(rule["lhs"], row)
        Nright += check_row_match(rule["rhs"], row)
        Nboth += check_row_match(rule["lhs"] + rule["rhs"], row)

    return Nleft, Nright, Nboth, Ntotal

def compute_rule_interestingness(rule, table):
    Nleft, Nright, Nboth, Ntotal = compute_rule_counts(rule, table)
    print(Nleft, Nright, Nboth, Ntotal)
    rule["confidence"] = Nboth / Nleft
    rule["support"] = Nboth / Ntotal
    rule["completeness"] = Nboth / Nright

for rule in [rule1, rule5]:
    compute_rule_interestingness(rule, table)
    print(rule)

# set theory basics and implementation in python
# set: an unordered collection with no duplicates
# there is a built in set type
transaction = ["chocolate", "grahams", "chocolate", "marshmallows"]
transaction_set = set(transaction)
print("set:", transaction_set)
# note: duplicate is gone and order is lost
# note: there is a part of apriori that requires order

# A union B: the set of all items in A or B or both
# A intersect B: the of all items in both A and B
# apriori needs union()
# transaction_set.union()
# or...
# with lists
# example: we have a set (list) LHS and a set (list) RHS of a rule
# union is sorted(LHS + RHS)
# LHS intersect RHS = 0 (empty set)
# there won't be any duplicates with this union

# A is a subset of B if all elements in A are also in B
# set has issubset()
# or...
# with lists
# check_row_match(A, B) returns 1 if A is a subset of B, 0 otherwise

# powerset of A: the set of all possible subsets of A including
# 0 (empty set) and A itself
# how could we calculate the powerset of transaction?
transaction = sorted(list(transaction_set))
print("list:", transaction)
# lets use the combinations() function from itertools
powerset = []
for i in range(len(transaction) + 1):
    powerset.extend(itertools.combinations(transaction, i))
print("powerset:", powerset)

# intro to market basket analysis (MBA)
# associations between products purchased together
# example
# IF {"chocolate=true", "grahams=true"} THEN {"marshmallows=true"}
# we are only interested in products bought together
# not products not bought
# e.g. =true, not the =false
# shorthand... drop =true
# IF {"chocolate", "grahams"} THEN {"marshmallows"}
# {"chocolate", "grahams"} -> {"marshmallows"}
# terminology
# each row in our dataset is a "transaction" (AKA "itemset")
# apriori lab time!

# PA8 starter code
transactions = [
 ["b", "c", "m"],
 ["b", "c", "e", "m", "s"],
 ["b"],
 ["c", "e", "s"],
 ["c"],
 ["b", "c", "s"],
 ["c", "e", "s"],
 ["c", "e"]
]

# NOTE: apriori lab task #1: find the set I
def compute_unique_values(table):
    unique = set()
    for row in table:
        for value in row: 
            unique.add(value)
    return sorted(list(unique))

transactions_I = compute_unique_values(transactions)
print(transactions_I)
interview_I = compute_unique_values(table)
print(interview_I)

# NOTE: apriori algorithm step 4 prune step: exame all susbets of c with k - 1 elements
def compute_k_minus_1_subsets(itemset):
    # or use itertools.combinations()
    subsets = []
    for i in range(len(itemset)):
        subsets.append(itemset[:i] + itemset[i + 1:])
    return subsets

# NOTE: apriori lab task #4/5: generate confidenet rules using supported itemsets
def generate_apriori_rules(supported_itemsets, table, minconf):
    rules = []
    # for each itemset S in supported_itemsets
    # generate the 1 term RHSs and the corresponding LHSs
    # check confidence >= minconf => append to rules
    # move on to the 2 term RHS... len(S)-1 term RHS...
    return rules 

# NOTE: apriori lab task #3: find supported itemsets
def apriori(table, minsup, minconf):
    # goal is to generate and return supported and confident rules
    supported_itemsets = []
    # TODO: finish apriori...
    # step 1. generate L1 supported itemsets of cardinality 1
    # to do this, use I
    I = compute_unique_values(table)
    # TODO: check support of singletons in L1!!
    # step 2. k = 2
    k = 2
    # TODO: step 3. while loop... while(Lkminus1 is not empty)
    # TODO: steps 4., 5., 6., ...

    rules = generate_apriori_rules(supported_itemsets, table, minconf)
    return rules 

k2_subsets = compute_k_minus_1_subsets(["c", "e", "s"])
print(k2_subsets) # [[c, e], [c, s], [e, s]]

rules = apriori(transactions, 0.25, 0.8)
print(rules) # TODO: check against your hand trace from apriori lab tasks #4/5