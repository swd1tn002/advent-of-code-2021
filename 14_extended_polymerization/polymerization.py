from typing import Tuple, Dict, List

data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

data = """SCVHKHVSHPVCNBKBPVHV

SB -> B
HH -> P
VF -> N
BS -> S
NC -> C
BF -> H
BN -> H
SP -> H
BK -> H
FF -> N
VN -> B
FN -> C
FS -> S
PP -> F
ON -> H
FV -> F
KO -> F
PK -> H
VB -> S
HS -> B
NV -> O
PN -> S
VH -> B
OS -> P
BP -> H
OV -> B
HK -> S
NN -> K
SV -> C
PB -> F
SK -> F
FB -> S
NB -> K
HF -> P
FK -> K
KV -> P
PV -> F
BC -> S
FO -> N
HC -> F
CP -> B
KK -> F
PC -> S
HN -> O
SH -> H
CK -> P
CO -> F
HP -> K
PS -> C
KP -> F
OF -> K
KS -> F
NO -> V
CB -> K
NF -> N
SF -> F
SC -> P
FC -> V
BV -> B
SS -> O
KC -> K
FH -> C
OP -> C
CF -> K
VO -> V
VK -> H
KH -> O
NP -> V
NH -> O
NS -> V
BH -> C
CH -> S
CC -> F
CS -> P
SN -> F
BO -> S
NK -> S
OO -> P
VV -> F
FP -> V
OK -> C
SO -> H
KN -> P
HO -> O
PO -> H
VS -> N
PF -> N
CV -> F
BB -> H
VC -> H
HV -> B
CN -> S
OH -> K
KF -> K
HB -> S
OC -> H
KB -> P
OB -> C
VP -> C
PH -> K"""

lines = data.split('\n')
polymer_template = lines[0]


def line_to_tuple(line: str) -> Tuple:
    left, right = line.split(' -> ')
    return (left[0], left[1]), right


rules = dict((line_to_tuple(line)) for line in lines[2:])

print(rules)


def grow_polymer(poly_template: str, rules: Dict[Tuple, str]) -> str:
    pairs = zip(poly_template, poly_template[1:])
    insertions: List[str] = [char_pair[0] + rules[char_pair]
                             for char_pair in pairs] + [poly_template[-1]]
    return ''.join(insertions)


for i in range(10):
    print(i)
    polymer_template = grow_polymer(polymer_template, rules)

print(polymer_template)

counts = {ch: polymer_template.count(ch) for ch in rules.values()}
print(max(counts.values()) - min(counts.values()))
