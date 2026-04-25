import os, random, fASP, os.path, argparse, tempfile
import shutil
from biodivine_aeon import *
from pathlib import Path
from helper import parse_perturbation_variables, parse_phenotype, run_approxasp
from contextlib import contextmanager

parser = argparse.ArgumentParser()
parser.add_argument('-bn','--bn', help='input BN program', required=True)
parser.add_argument('-phen','--phen', help='phenotype', required=False)
parser.add_argument('-pert','--pert', help='perturbation', required=False)
parser.add_argument('-t','--t', help='task (e.g., 1 or 2 or 3)', default=1, required=False)


# First, prepare ASP programs for all "normal" networks without any special requirements.

@contextmanager
def pushd(path):
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def preprocess_bn(bn_path):
    # preprocess BN
    bn_path = Path(bn_path).resolve()

    file_path = str(bn_path)
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
    bn_path = Path(bn_path).resolve()

    with pushd(bn_path.parent):
        fASP.compute_fix_points(
            str(bn_path), 
            display=False,
            max_output=1,         
            method="conj",
            write_asp_file=True,
        )
        # the query file should be written
        query_file = bn_path.parent / "query.lp"
        out_file = bn_path.with_suffix(".t1.fix.lp")

        # os.replace("query.lp", f"{bn_path.replace('.bnet', '.t1.fix.lp')}")

        if not query_file.exists():
            raise FileNotFoundError(f"Expected file was not created: {query_file}")

        os.replace(query_file, out_file)


def second_task(bn_path, phenotype):
    bn_path = Path(bn_path).resolve()
    bn = BooleanNetwork.from_file(str(bn_path))
    
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

    print(f"[{bn_path.name}] Loaded {bn}.")

    PHENOTYPE_SIZE = len(phenotype.keys())
    # annotation = ModelAnnotation()
    # annotation["phenotype"].value = repr(phenotype)

    # Save the network with the phenotype annotation, embedding the size of the phenotype into the filename.
    # model_str = f"{str(annotation)}\n{bn_path.to_aeon()}"
    # Path(f'{bn_path.replace(".bnet", f".phen-{PHENOTYPE_SIZE}.aeon")}').write_text(model_str)
    # Path(f'{bn_path.replace(".bnet", f".phen-{PHENOTYPE_SIZE}.bnet")}').write_text(bn.to_bnet())
    phen_bn = bn_path.with_name(f"{bn_path.stem}.phen-{PHENOTYPE_SIZE}.bnet")
    print(f"[{bn_path.name}] Saved a network with phenotype annotation.")

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
    # base_asp_file = bn_path.replace(f".bnet", ".t1.fix.lp") # first task must be done

    base_asp_file = bn_path.with_suffix(".t1.fix.lp")
    query = base_asp_file.read_text(encoding="utf-8")
    query = f"{query}\n" + "\n".join(asp_commands)
    
    out_file = bn_path.with_suffix(".t2.fix.lp")
    out_file.write_text(query, encoding="utf-8")

def third_task(bn_path, phenotype, perturbable):
    bn_path = Path(bn_path).resolve()
    bn = BooleanNetwork.from_file(str(bn_path))
    
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

    print(f"[{bn_path.name}] Loaded {bn}.")

    PHENOTYPE_SIZE = len(phenotype.keys())
    PERTURBABLE_VARIABLES = len(perturbable)
    bn = BooleanNetwork.from_file(str(bn_path))
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

    print(f"[{bn_path.name}] Generated a network with {len(perturbation_variable_names)} new perturbation input variables.")
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

    # pert_bn = f'{bn_path.replace(".bnet", f".phen-{PHENOTYPE_SIZE}.pert-{PERTURBABLE_VARIABLES}.bnet")}' # name of pert bn
    # Path(pert_bn).write_text(p_bn.to_bnet())
    pert_bn = bn_path.with_name(
        f"{bn_path.stem}.phen-{PHENOTYPE_SIZE}.pert-{PERTURBABLE_VARIABLES}.bnet"
    )
    pert_bn.write_text(p_bn.to_bnet(), encoding="utf-8")

    old_cwd = os.getcwd()
    try:
        os.chdir(str(bn_path.parent))
        fASP.compute_fix_points(
            str(pert_bn), 
            display=False,
            max_output=1,         
            method="conj",
            write_asp_file=True,
        )

        # Only read the commands, not the show directives.
        query_file = bn_path.parent / "query.lp"

        # Only read the commands, not the show directives.
        asp_commands = [
            l for l in query_file.read_text(encoding="utf-8").splitlines()
            if not l.startswith("#")
        ]

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

        # print(f"[{bn_path.name}] Saved a perturbable network with phenotype annotation.")

        for var in new_variables:
            # fASP will add a p- and n- variant of the new variables, i.e. for each perturbable
            # variable, we have 4 ASP variables. We probably should modify this so that 2 are sufficient.
            asp_commands.append(f"#project p{var}.")
            asp_commands.append(f"#project n{var}.")
            asp_commands.append(f"#show p{var}/0.")
            asp_commands.append(f"#show n{var}/0.")

        # Merge and output ASP commands.
        out_file = bn_path.with_suffix(".t3.fix.lp")
        out_file.write_text("\n".join(asp_commands), encoding="utf-8")

        print(f"[{bn_path.name}] ASP file for fixed points with phenotype restriction and controlability computed.")
    finally:
        os.chdir(old_cwd)


# preprocess_bn(file_path)
args = parser.parse_args()

if int(args.t) == 2 and args.phen == None:
    print(f"Exit! task 2 requires a phenotype")
    exit(0)

if int(args.t) == 3 and (args.phen == None or args.pert == None):
    print(f"Exit! task 3 requires both phenotype and perturbation")
    exit(0)

with tempfile.NamedTemporaryFile(suffix=".bnet", delete=False) as f:
    temp_file = Path(f.name)

shutil.copy2(args.bn, temp_file)
input_bn = str(temp_file)

if int(args.t) == 1:
    first_task(input_bn)
    print(f"Executing first task")

    input_bn_path = Path(input_bn)
    asp_file = input_bn_path.with_suffix(".t1.fix.lp")

    # asp_file = input_bn.replace(".bnet", ".t1.fix.lp")
    if asp_file.exists():
        run_approxasp(str(asp_file), prefix="C-FIX-1")
    else:
        print("Error !!")

    base = input_bn_path.with_suffix("")
    for file in input_bn_path.parent.glob(f"{base.name}*"):
        if file.is_file():
            file.unlink()

    query_file = input_bn_path.parent / "query.lp"
    if query_file.exists():
        query_file.unlink()


elif int(args.t) == 2:
    phenotype = parse_phenotype(args.phen)
    print(f"phenotype: {phenotype}")
    first_task(input_bn)
    print(f"Executing second task")
    second_task(input_bn, phenotype)

    input_bn_path = Path(input_bn)
    asp_file = input_bn_path.with_suffix(".t2.fix.lp")

    if asp_file.exists():
        run_approxasp(str(asp_file), prefix="C-FIX-2")
    else:
        print(f"Error: expected file not found: {asp_file}")

    base = input_bn_path.with_suffix("")
    for file in input_bn_path.parent.glob(f"{base.name}*"):
        if file.is_file():
            file.unlink()

    query_file = input_bn_path.parent / "query.lp"
    if query_file.exists():
        query_file.unlink()

elif int(args.t) == 3:
    phenotype = parse_phenotype(args.phen)
    perturbable = parse_perturbation_variables(args.pert)
    print(f"Executing third task")
    print(f"phenotype: {phenotype}")
    print(f"perturbation : {len(perturbable)} variables")
    third_task(input_bn, phenotype, perturbable)

    input_bn_path = Path(input_bn)
    asp_file = input_bn_path.with_suffix(".t3.fix.lp")

    if asp_file.exists():
        run_approxasp(str(asp_file), prefix="C-FIX-3", projection=True)
    else:
        print(f"Error: expected file not found: {asp_file}")

    base = input_bn_path.with_suffix("")
    for file in input_bn_path.parent.glob(f"{base.name}*"):
        if file.is_file():
            file.unlink()

    query_file = input_bn_path.parent / "query.lp"
    if query_file.exists():
        query_file.unlink()

else:
    print(f"Exit!! task:{args.t} no such task")
    exit(0)

