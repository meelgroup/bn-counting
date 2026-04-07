from sympy import symbols, Or, And, Not, Implies, Equivalent, to_cnf, parse_expr
from sympy.logic.boolalg import is_cnf
import sys, time
import subprocess as sp
from biodivine_aeon import *


def run(cmd, timeout, ttl = 3, silent = False):
    if not silent:
        print("Executing:", cmd)
    proc = sp.Popen([cmd], stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    try:
        (out, err) = proc.communicate(timeout = int(timeout * 1.1) + 1)
        out = out.decode("utf-8")
    except sp.TimeoutExpired:
        proc.kill()
        try:
            (out, err) = proc.communicate()
            out = out.decode("utf-8")
        except ValueError:
            if ttl > 0:
                return run(cmd, timeout, ttl - 1)
            out = ""
    return out

def convert_to_dimacs(formula, symbol_list, projection_var):
    """Converts a symbolic formula to CNF and then to DIMACS format."""
    
    # Convert to CNF using sympy
    cnf_formula = to_cnf(formula)
    
    # Check if it's actually in CNF
    if not is_cnf(cnf_formula):
        raise ValueError("Formula conversion to CNF failed!")

    # Create a mapping from symbols to integers
    symbol_map = {symbol: i + 1 for i, symbol in enumerate(symbol_list)}
    
    # Extract clauses
    clauses = []
    if cnf_formula != True:
        if isinstance(cnf_formula, And):
            clause_list = cnf_formula.args
        else:
            clause_list = [cnf_formula]  # Single clause case

        for clause in clause_list:
            if isinstance(clause, Or):
                literals = clause.args
            else:
                literals = [clause]  # Single literal case
            
            clause_nums = []
            for lit in literals:
                if isinstance(lit, Not):  # Handle negation
                    clause_nums.append(-symbol_map[lit.args[0]])
                else:
                    clause_nums.append(symbol_map[lit])

            clauses.append(clause_nums)

    # Generate DIMACS CNF output
    num_vars = len(symbol_map)
    num_clauses = len(clauses)
    proj_lit = []
    for var in projection_var:
        proj_lit.append(symbol_map[symbols(var)])

    dimacs = [f"p cnf {num_vars} {num_clauses}"]
    if len(proj_lit) > 0:
        # if there is any projection variable
        dimacs.append("c ind " + " ".join(map(str, proj_lit)) + " 0")
    for clause in clauses:
        dimacs.append(" ".join(map(str, clause)) + " 0")

    return "\n".join(dimacs)

# read .bnet file and get the DIMACS CNF
if len(sys.argv) < 2:
    print("Input Boolean network is not given !!!")
    exit(1)

aeon_file = None
phenotype = dict()
perturbation_variables = dict()
if len(sys.argv) > 2:
    # aeon file present 
    bn = BooleanNetwork.from_file(sys.argv[2])

    annotation = ModelAnnotation.from_file(sys.argv[2])
    if annotation["phenotype"].value:
        phenotype = eval(annotation["phenotype"].value)
    if annotation["perturbation-variables"].value:
        perturbation_variables = eval(annotation["perturbation-variables"].value)

    print(f"This network has {len(phenotype)} phenotype variables.")
    print(f"This network has {len(perturbation_variables)} perturbable variables.")

fileobj = open(sys.argv[1], "r", encoding="utf-8")
list_vars = []
formula = True
total_time = 3600
start_time = time.time()
for line in fileobj.readlines():
    if line.startswith("#") or line.startswith("targets, factors") or line.startswith("targets,factors"):
        continue
    line = line.split("#")[0]
    try:
        x, fx = line.replace(" ", "").replace("!", "~").split(",", maxsplit=1)
    except ValueError: # not enough values to unpack
        continue
    
    list_vars.append(x)
    x = parse_expr(x)
    fx = parse_expr(fx)

    formula = And(formula, Equivalent(x, fx))

list_symbols = symbols(" ".join(list_vars))

# adding phenotype 
for var in phenotype:
    if phenotype[var] == 0:
        fx = parse_expr("~" + var)
        formula = And(formula, fx)
    else:
        fx = parse_expr(var)
        formula = And(formula, fx)

proj_set = set()
for var in perturbation_variables:
    proj_set = proj_set.union(perturbation_variables[var])


# Convert and print DIMACS CNF format
dimacs_output = convert_to_dimacs(formula, list_symbols, proj_set)
output_cnf = open(sys.argv[1] + ".cnf", 'w')
output_cnf.write(dimacs_output)
output_cnf.close()
print("### Done {}".format(sys.argv[1] + ".cnf"))
# remaining time 
remaining_time = 3600 - (time.time() - start_time)
print("#SAT timeout: {}".format(remaining_time))

assert(remaining_time > 0)
cmd = "timeout {} ./ganak -v 0 --appmct 0.1 {}".format(int(remaining_time), sys.argv[1] + ".cnf")

out = run(cmd, int(remaining_time))

for line in out.splitlines():
    if line.startswith("c s exact arb int") or line.startswith("c s approx arb int"):
        l = line.strip().split()
        count = int(l[-1])
        print("#SAT (ApproxMC) count: {0}".format(count))
    
