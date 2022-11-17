
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