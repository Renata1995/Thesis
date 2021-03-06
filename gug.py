import re
import sys
from nltk import CFG, nonterminals, RecursiveDescentParser
from utils import helper_methods as helper

"""
python gug.py <grammar> <output>
<grammar> could be "RE" or "CFG"

"""
if len(sys.argv) <= 1:
    grammar = "RE"
else:
    if sys.argv[1] == "c":
        grammar = "CFG"
    else:
        grammar = "RE"


output = helper.get_gug_file(grammar)

# Two grammars
# re_grammar = "^((TP*T(X+VP)*(S|X+VS))|(VX*V(PX+V)*P{,1}S))$"
re_grammar = "^X*V((JTX*V)*J|T|XJ*|TVJ*)$"

S, X, T = nonterminals("S, X, T")
cfg = CFG.fromstring("""
S -> X S X | T S | X | T
X -> 'P'|'S'|'T'
T -> 'V'|'X'
""")
rd_parser = RecursiveDescentParser(cfg)

# Get all strings with letter_length from 4 to 7
all_str = helper.get_all_str(helper.short_length, helper.long_length + 1)

# Split items into three list with different CS
g_items = []
ug_items = []

for item in all_str:
    if grammar == "RE":
        if re.findall(re_grammar, item):
            g_items.append(item)
        else:
            ug_items.append(item)

    elif grammar == "CFG":
        tree = rd_parser.parse(item)
        if len(list(tree)) == 0:
            ug_items.append(item)
        else:
            g_items.append(item)

# write results to the output file
ofile = open(output, "w")
ofile.write(grammar + "\nG\n")
for item in g_items:
    ofile.write(item + "\n")

ofile.write("UG\n")
for item in ug_items:
    ofile.write(item + "\n")
