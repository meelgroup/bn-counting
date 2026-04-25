import argparse
# import platform
# print(platform.python_version())
import networkx as nx
from networkx.algorithms.approximation import vertex_cover
from clingo import Control
from clingo import Function
from pathlib import Path
import time, os

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
parser.add_argument('-t','--t', help='timeout', required=False)
parser.add_argument('-c','--c', help='do the independent support test', required=False)
parser.add_argument('-k','--k', help='keep intermediate files', default=False, required=False)
parser.add_argument('-g','--g', help='use the given independent support', default=False, required=False)
args = parser.parse_args()

# default time for IS
max_time = 1000
if args.t != None:
    max_time = args.t
small_time = 50

print("The timeout is set to {0}".format(max_time))
# the graph
grph = nx.Graph() 

def parse_rule_string(line: str):
    lst = line.strip().split()
    choice = int(lst[1]) == 1

    size_of_head = int(lst[2])
    head_atom_start = 3
    head_atoms = []
    body_atoms = []
    # first parsing the head of the rule
    for index in range(head_atom_start, head_atom_start + size_of_head):
        head_atoms.append(int(lst[index]))

    assert(lst[head_atom_start + size_of_head] == '0') ## end of head of the rule
    size_of_body = int(lst[head_atom_start + size_of_head + 1])
    body_atom_start = head_atom_start + size_of_head + 2
    # second parsing the head of the rule
    for index in range(body_atom_start, len(lst)):
        body_atoms.append(int(lst[index]))

    return choice, head_atoms, body_atoms

print("The input file is: {0}".format(args.i))
print("=== We parse the file ===")
mapping_of_origin_atom = dict()
all_rules = []
given_independent_support = set()
for line in open(args.i, 'r'):
    if line.startswith("asp "):
        continue
    elif line.startswith("0"):
        # end of input file 
        continue
    elif line.startswith("4 "):
        lst = line.strip().split()
        if int(lst[3]) > 0:
            mapping_of_origin_atom[int(lst[4])] = lst[2]
            if args.g:
                given_independent_support.add(int(lst[4]))
    elif line.startswith("1 "):
        choice, head, body = parse_rule_string(line)
        all_rules.append((choice, head, body))

initial_independent_support = set()
given_atom_set = set()
input_file = Path(args.i).resolve()
copy_program = input_file.parent / ("copy_" + input_file.name.replace("grounded_", ""))

copy_program_writer = open(copy_program, "w", encoding="utf-8")
# copy_program = "copy_" + args.i.replace("grounded_", "")
# copy_program_writer = open(copy_program, 'w')
if args.c:
    check_program = "check_" + args.i.replace("grounded_", "")
    check_program_writer = open(check_program, 'w')
for rule in all_rules:
    choice, head, body = rule
    rule_str_x = ""
    rule_str_y = ""
    for index, head_atom in enumerate(head):
        if index == 0 or index == len(head):
            rule_str_x += "x{0}".format(head_atom)
            rule_str_y += "y{0}".format(head_atom)
        else:
            rule_str_x += " ; x{0}".format(head_atom)
            rule_str_y += " ; y{0}".format(head_atom)

    # if len(head) > 1:
    for i1 in range(0, len(head)):
        initial_independent_support.add(head[i1]) 
        given_atom_set.add(head[i1])
        for i2 in range(0, len(body)):
            if body[i2] > 0 and head[i1] != body[i2]:
                grph.add_edge(head[i1], body[i2])

    if choice:
        rule_str_x = "{ " + rule_str_x + " }"
        rule_str_y = "{ " + rule_str_y + " }"

    rule_str_x += ":-"
    rule_str_y += ":-"

    for index, body_atom in enumerate(body):
        if index == 0 or index == len(body):
            if body_atom > 0:
                rule_str_x += "x{0} ".format(body_atom)
                rule_str_y += "y{0} ".format(body_atom)
            else:
                rule_str_x += "not x{0} ".format(abs(body_atom))
                rule_str_y += "not y{0} ".format(abs(body_atom))
        else:
            if body_atom > 0:
                rule_str_x += ", x{0}".format(body_atom)
                rule_str_y += ", y{0}".format(body_atom)
            else:
                rule_str_x += ", not x{0}".format(abs(body_atom))
                rule_str_y += ", not y{0}".format(abs(body_atom))

    rule_str_x += "."
    rule_str_y += "."

    copy_program_writer.write(rule_str_x + "\n")
    copy_program_writer.write(rule_str_y + "\n")
    if args.c:
        check_program_writer.write(rule_str_x + "\n")
        check_program_writer.write(rule_str_y + "\n")

    # construct the underlying graph
    # for i1 in range(0, len(head)):
    #     initial_independent_support.add(head[i1])
    #     for i2 in range(0, len(body)):
    #         if head[i1] != body[i2]:
    #             grph.add_edge(head[i1], body[i2])
if args.g:
    #print("Using the initial independent support ")
    initial_independent_support = given_independent_support
print("The possible candidate for independent support: {0}".format(len(initial_independent_support)))
print("The size of atom set: {0}".format(len(given_atom_set)))
for atom in list(initial_independent_support):
    copy_program_writer.write("{ " + "z{0}".format(atom) + " }.\n") # z_i is a free variable
    constraint1 = ":- x{0}, not y{0}, z{0}.\n".format(atom) 
    copy_program_writer.write(constraint1)
    constraint2 = ":- not x{0}, y{0}, z{0}.\n".format(atom)
    copy_program_writer.write(constraint2)

copy_program_writer.close()

# new computing the priority or degree of each atom
priority = dict()
for atom in list(initial_independent_support):
    if atom in grph.nodes:
        priority[atom] = grph.degree[atom]
    else:
        priority[atom] = 0




# print("=============== We create copy program ===============")

# copy_program = "copy_" + args.i.replace("dlp_", "")
# copy_program_writer = open(copy_program, 'w')

# initial_independent_support = set()
# for line in open(args.i, 'r'):
#     if not line.startswith("%"):
#         line1 = line.replace("v", "x")
#         line2 = line.replace("v", "y")

#         copy_program_writer.write(line1)
#         copy_program_writer.write(line2)

#         head_atoms = list()
#         head_str = None
#         if ":-" not in line:
#             head_str = line.replace(".", "").strip()
#         else:
#             head_str = line[:line.find(":-")]
#         # parse the head 
#         head_atoms = head_str.split(";")
#         # print("The number of head atoms: {0}".format(head_atoms))
#         if len(head_atoms) > 1:
#             for i1 in range(0, len(head_atoms)):
#                 initial_independent_support.add(head_atoms[i1])
#                 for i2 in range(i1 + 1, len(head_atoms)):
#                     if i1 != i2 and head_atoms[i1] != head_atoms[i2]:
#                         grph.add_edge(head_atoms[i1].strip(), head_atoms[i2].strip())


# print("The number of nodes: {0} and edges: {1}".format(grph.number_of_nodes(), grph.number_of_edges()))
# print("========== Computing the backdoor ========== ")
# vc = vertex_cover.min_weighted_vertex_cover(grph)
# print("The size of backdoor: {0}".format(len(vc)))
# priority = dict()
# for vc_nodes in vc:
#     new_var = vc_nodes.replace("v", "z")
#     x_var = vc_nodes.replace("v", "x")
#     y_var = vc_nodes.replace("v", "y")
#     copy_program_writer.write("{ " + new_var + " }.\n") # z_i is a free variable
#     constraint1 = ":- {0}, not {1}, {2}.\n".format(x_var, y_var, new_var) 
#     constraint2 = ":- not {0}, {1}, {2}.\n".format(x_var, y_var, new_var)
#     copy_program_writer.write(constraint1)
#     copy_program_writer.write(constraint2)
#     # it is useful to do sorting
#     priority[vc_nodes.replace("v", "")] = grph.degree[vc_nodes]

# copy_program_writer.close()
# # print(priority)

def get_index(element):
    return priority[element]
 
# # Sort the original list based on the sort order list using sorted() function and the custom function as the key

# print("========== Computing the independent support ========== ")
if True:
    ctl = Control(["0"])
    ctl.configuration.solve.models = 1 # check SAT or UNSAT
    ctl.load(str(copy_program))
    ctl.ground([("base", [])])

    unknown = []
    for _ in initial_independent_support:
        unknown.append(_)

    start_time = time.perf_counter()
    print("The size of initial independent support: {0}".format(len(unknown)))
    assumptions = list()
    unknown = sorted(unknown, key=get_index, reverse=False)
    mathcal_I = list()
    while len(unknown) > 0:
        assumptions.clear()
        index = unknown.pop()

        for j in mathcal_I:
            assumptions.append((Function("z{0}".format(j)), True))
        for j in unknown:
            assumptions.append((Function("z{0}".format(j)), True))
        

        assumptions.append((Function("x{0}".format(index)), True)) # x is the original set of variable
        assumptions.append((Function("y{0}".format(index)), False)) # y is the copy variable 
        # ret = ctl.solve(assumptions=assumptions)
        with ctl.solve(async_=True, assumptions=assumptions) as handle:
            handle.wait(small_time)
            handle.cancel()
            ret = handle.get()
            if not ret.unsatisfiable:
                mathcal_I.append(index)

        # run the script for a fixed time
        current_time = time.perf_counter()
        if current_time - start_time >= max_time:
            break

    print("The size of final independent support: {0}".format(len(mathcal_I) + len(unknown)))
    # printing the independent support 
    input_file = Path(args.i).resolve()
    is_file = input_file.parent / ("IS_" + input_file.name.replace("grounded_", ""))

    IS_file_pointer = open(is_file, "w", encoding="utf-8")
    # IS_file_pointer = open("IS_" + args.i.replace("grounded_", ""), 'w')
    independent_str = "c ind "
    independent_support = set()
    for is_atoms in mathcal_I:
        independent_str += "{0} ".format(mapping_of_origin_atom[is_atoms] if is_atoms in mapping_of_origin_atom else "aux")
        independent_support.add(is_atoms)
    for un_atoms in unknown:
        independent_str += "{0} ".format(mapping_of_origin_atom[un_atoms] if un_atoms in mapping_of_origin_atom else "aux")
        independent_support.add(un_atoms)
    independent_str += "0"
    # print(independent_str)
    IS_file_pointer.write(independent_str)
    IS_file_pointer.close()

if not args.k:
    os.remove(copy_program)

if args.c:
    max_time = 3600
    # check independent support atoms are in initial independent support
    for is_atoms in independent_support:
        assert(is_atoms in independent_support)

    # add clauses that the independent support atoms must be equal
    for is_atoms in list(independent_support):
        str1 = ":- x{0}, not y{0}.".format(is_atoms)
        check_program_writer.write(str1 + "\n")
        str2 = ":- not x{0}, y{0}.".format(is_atoms)
        check_program_writer.write(str2 + "\n")

    # add clauses for rest of the atoms, introduce a new atom `w1`
    w1_atom_seen = False
    aux_atom_added = 0
    for atom in list(given_atom_set):
        # it should be given_atom_set for param "-g"
        if atom not in independent_support:
            str1 = "w1 :- x{0}, not y{0}.".format(atom)
            check_program_writer.write(str1 + "\n")

            str2 = "w1 :- not x{0}, y{0}.".format(atom)
            check_program_writer.write(str2 + "\n")
            w1_atom_seen = True
            aux_atom_added += 1
    
    print("Auxiliary atoms added: {0}".format(aux_atom_added))
    if w1_atom_seen:
        check_program_writer.write(":- not w1. \n")
    check_program_writer.close()

    ctl_check = Control(["0"])
    ctl_check.configuration.solve.models = 1 # check SAT or UNSAT
    ctl_check.load(check_program)
    ctl_check.ground([("base", [])])

    with ctl_check.solve(async_=True) as handle:
        handle.wait(max_time)
        handle.cancel()
        ret = handle.get()
        if ret.unsatisfiable:
            print("INDEPENDENT SUPPORT VERIFIED !!!")
            if not args.k:
                os.remove(check_program)
        elif ret.satisfiable:
            print("INDEPENDENT SUPPORT INCORRECT !!!")
        else:
            print("INDEPENDENT SUPPORT NOT VERIFIED !!!")

    