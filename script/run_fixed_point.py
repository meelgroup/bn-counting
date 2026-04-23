import os, random, fASP, os.path, argparse, tempfile
from biodivine_aeon import *
from pathlib import Path
from helper import parse_perturbation_variables, parse_phenotype, run_approxasp

parser = argparse.ArgumentParser()
parser.add_argument('-bn','--bn', help='input BN program', required=True)
parser.add_argument('-phen','--phen', help='phenotype', required=False)
parser.add_argument('-pert','--pert', help='perturbation', required=False)
parser.add_argument('-t','--t', help='task (e.g., 1 or 2 or 3)', default=1, required=False)


# First, prepare ASP programs for all "normal" networks without any special requirements.



def preprocess_bn(bn_path):
    # preprocess BN
    file_path = f"{bn_path}"
    bn = BooleanNetwork.from_file(file_path)
    
    # Once we remove irrelevant regulations, some models become disconnected
    # and these unused variables are then problematic in further steps.
    # Here, we thus ensure the network is always weakly connected.
    bn = bn.infer_valid_graph()
    wcc = sorted(bn.weakly_connected_components(), key=lambda x: -len(x))
    if len(wcc[0]) != bn.variable_count():        
        to_remove = set(bn.variables()) - set(wcc[0])
        print(f"[{file_path}] Removing variables {to_remove} since they are not connected to the rest of the graph (Weak components: {[len(x) for x in wcc]}).")
        bn = bn.drop(to_remove)
        # Replace the previous network file (otherwise it will not be used by tsconj)
        Path(file_path).write_text(bn.to_bnet())

    print(f"[{file_path}] Loaded {bn}.")

def first_task(bn_path):
    fASP.compute_fix_points(
        bn_path, 
        display=False,
        max_output=1,         
        method="conj",
        write_asp_file=True,
    )
    # the query file should be written
    os.replace("query.lp", f"{bn_path.replace('.bnet', '.t1.fix.lp')}")


def second_task(bn_path, phenotype):
    bn = BooleanNetwork.from_file(bn_path)
    
    # Once we remove irrelevant regulations, some models become disconnected
    # and these unused variables are then problematic in further steps.
    # Here, we thus ensure the network is always weakly connected.
    bn = bn.infer_valid_graph()
    wcc = sorted(bn.weakly_connected_components(), key=lambda x: -len(x))
    if len(wcc[0]) != bn.variable_count():        
        to_remove = set(bn.variables()) - set(wcc[0])
        print(f"[{bn_path}] Removing variables {to_remove} since they are not connected to the rest of the graph (Weak components: {[len(x) for x in wcc]}).")
        bn = bn.drop(to_remove)
        # Replace the previous network file (otherwise it will not be used by tsconj)
        Path(bn_path).write_text(bn.to_bnet())

    print(f"[{bn_path}] Loaded {bn}.")

    PHENOTYPE_SIZE = len(phenotype.keys())
    # annotation = ModelAnnotation()
    # annotation["phenotype"].value = repr(phenotype)

    # Save the network with the phenotype annotation, embedding the size of the phenotype into the filename.
    # model_str = f"{str(annotation)}\n{bn_path.to_aeon()}"
    # Path(f'{bn_path.replace(".bnet", f".phen-{PHENOTYPE_SIZE}.aeon")}').write_text(model_str)
    Path(f'{bn_path.replace(".bnet", f".phen-{PHENOTYPE_SIZE}.bnet")}').write_text(bn.to_bnet())
    print(f"[{bn_path}] Saved a network with phenotype annotation.")

    # file_path = f"{INPUT_PHENOTYPE_FOLDER}/{file}"
    # annotation = ModelAnnotation.from_file(file_path)
    # phenotype = eval(annotation["phenotype"].value)

    asp_commands = []
    # con_commands = []
    # the case is opposite from MTS
    for var, value in phenotype.items():
        if value:
            asp_commands.append(f":- n{var}.")
        else:
            asp_commands.append(f":- p{var}.")
            

    # Merge ASP commands into a single string.
    asp_suffix = "\n".join(asp_commands)

    # Append ASP commands to the ASP file.
    base_asp_file = bn_path.replace(f".bnet", ".t1.fix.lp") # first task must be done
    query = Path(f"{base_asp_file}").read_text()
    query = f"{query}\n{asp_suffix}"
    Path(bn_path.replace(".bnet", ".t2.fix.lp")).write_text(query)

def third_task(bn_path, phenotype, perturbable):
    bn = BooleanNetwork.from_file(bn_path)
    
    # Once we remove irrelevant regulations, some models become disconnected
    # and these unused variables are then problematic in further steps.
    # Here, we thus ensure the network is always weakly connected.
    bn = bn.infer_valid_graph()
    wcc = sorted(bn.weakly_connected_components(), key=lambda x: -len(x))
    if len(wcc[0]) != bn.variable_count():        
        to_remove = set(bn.variables()) - set(wcc[0])
        print(f"[{bn_path}] Removing variables {to_remove} since they are not connected to the rest of the graph (Weak components: {[len(x) for x in wcc]}).")
        bn = bn.drop(to_remove)
        # Replace the previous network file (otherwise it will not be used by tsconj)
        Path(bn_path).write_text(bn.to_bnet())

    print(f"[{bn_path}] Loaded {bn}.")

    PHENOTYPE_SIZE = len(phenotype.keys())
    PERTURBABLE_VARIABLES = len(perturbable)
    bn = BooleanNetwork.from_file(bn_path)
    perturbation_variables = { var: (f"pp_{var}", f"pn_{var}") for var in perturbable }
    perturbation_variable_names = sorted([ x[0] for x in perturbation_variables.values() ] + [ x[1] for x in perturbation_variables.values() ])

    p_bn = bn.extend(perturbation_variable_names)
    for (var, (p_var, n_var)) in perturbation_variables.items():
        # Add self-loops to var, p_var and n_var, plus a p_var -> var and n_var -> var regulations.
        for x in [p_var, n_var]:
            p_bn.ensure_regulation({
                'source': x,
                'target': var,
                'sign': None,
                'essential': False,
            })
        for x in [var, p_var, n_var]:
            p_bn.ensure_regulation({
                'source': x,
                'target': x,
                'sign': None,
                'essential': False,
            })
        
        current_update = p_bn.get_update_function(var)

        # These are the original functions that implement the perturbation effect:
        #new_update = UpdateFunction(p_bn, f"({p_var} => 1) & (!{p_var} => ({current_update}))").simplify_constants()
        #new_update = UpdateFunction(p_bn, f"({n_var} => 0) & (!{n_var} => ({new_update}))").simplify_constants()

        # This is a slimplified variant of the same function which is easier to process with tsconj:
        new_update = UpdateFunction(p_bn, f"!{n_var} & ({p_var} | {current_update})")

        p_bn.set_update_function(var, new_update)
        p_bn.set_update_function(p_var, p_var)
        p_bn.set_update_function(n_var, n_var)

    print(f"[{bn_path}] Generated a network with {len(perturbation_variable_names)} new perturbation input variables.")
    # For the .bnet file, we are going to use an update function which forbids knockout
    # and overexpression occuring together.
    # WARNING: This means the .bnet file is different.
    for (var, (p_var, n_var)) in perturbation_variables.items():
        p_bn.ensure_regulation({
            'source': n_var,
            'target': p_var,
            'sign': None,
            'essential': False,
        })

        p_bn.set_update_function(p_var, f'({p_var} & !{n_var})')

    pert_bn = f'{bn_path.replace(".bnet", f".phen-{PHENOTYPE_SIZE}.pert-{PERTURBABLE_VARIABLES}.bnet")}' # name of pert bn
    Path(pert_bn).write_text(p_bn.to_bnet())

    fASP.compute_fix_points(
        pert_bn, 
        display=False,
        max_output=1,         
        method="conj",
        write_asp_file=True,
    )

    # Only read the commands, not the show directives.
    asp_commands = [ l for l in Path("query.lp").read_text().splitlines() if not l.startswith("#") ]

    # the loop is also different from MTS
    for var, (p_var, n_var) in perturbation_variables.items():
        for i in range(len(asp_commands)):
            if asp_commands[i].startswith(f"p{p_var} :-"):
                asp_commands[i] = f"p{p_var} :- n{n_var}, p{p_var}."
                break # Should be just one rule of this type.
        asp_commands.append(f"n{p_var} :- p{n_var}.")

    # Add the phenotype restriction to the ASP query.
    for var, value in phenotype.items():
        if value:
            asp_commands.append(f":- n{var}.")
        else:
            asp_commands.append(f":- p{var}.")

    new_variables = sorted([ x[0] for x in perturbation_variables.values() ] + [ x[1] for x in perturbation_variables.values() ])

    print(f"[{bn_path}] Saved a perturbable network with phenotype annotation.")

    for var in new_variables:
        # Tsconj will add a p- and n- variant of the new variables, i.e. for each perturbable
        # variable, we have 4 ASP variables. We probably should modify this so that 2 are sufficient.
        asp_commands.append(f"#project p{var}.")
        asp_commands.append(f"#project n{var}.")
        asp_commands.append(f"#show p{var}/0.")
        asp_commands.append(f"#show n{var}/0.")

    # Merge and output ASP commands.
    Path(bn_path.replace(".bnet", ".t3.fix.lp")).write_text("\n".join(asp_commands))

    print(f"[{bn_path}] ASP file for trap spaces with phenotype restriction and controlability computed.")


# preprocess_bn(file_path)
args = parser.parse_args()

if int(args.t) == 2 and args.phen == None:
    print(f"Exit! task 2 requires a phenotype")
    exit(0)

if int(args.t) == 3 and (args.phen == None or args.pert == None):
    print(f"Exit! task 3 requires both phenotype and perturbation")
    exit(0)

with tempfile.NamedTemporaryFile(dir=".", delete=False) as f:
    temp_file = f.name + ".bnet"
    os.system("cp {0} {1}".format(args.bn, temp_file))
    input_bn = os.path.basename(temp_file)

if int(args.t) == 1:
    first_task(input_bn)
    print(f"Executing first task")

    asp_file = input_bn.replace(".bnet", ".t1.fix.lp")
    if os.path.exists(asp_file):
        run_approxasp(asp_file, prefix="C-FIX-1")
    else:
        print("Error !!")

    os.system(f'rm -f {input_bn.replace(".bnet", "")}* query.lp')

elif int(args.t) == 2:
    phenotype = parse_phenotype(args.phen)
    print(f"phenotype: {phenotype}")
    first_task(input_bn)
    print(f"Executing second task")
    second_task(input_bn, phenotype)

    asp_file = input_bn.replace(".bnet", ".t2.fix.lp")
    if os.path.exists(asp_file):
        run_approxasp(asp_file, prefix="C-FIX-2")
    else:
        print("Error !!")

    os.system(f'rm -f {input_bn.replace(".bnet", "")}* query.lp')

elif int(args.t) == 3:
    phenotype = parse_phenotype(args.phen)
    perturbable = parse_perturbation_variables(args.pert)
    print(f"Executing third task")
    print(f"phenotype: {phenotype}")
    print(f"perturbation : {len(perturbable)} variables")
    third_task(input_bn, phenotype, perturbable)

    asp_file = input_bn.replace(".bnet", ".t3.fix.lp")
    if os.path.exists(asp_file):
        run_approxasp(asp_file, prefix="C-FIX-3", projection=True)
    else:
        print("Error !!")

    os.system(f'rm -f {input_bn.replace(".bnet", "")}* query.lp')

else:
    print(f"Exit!! task:{args.t} no such task")
    exit(0)

