import ast, re, shutil, os
import subprocess as sp


def run(cmd, timeout, ttl = 3, silent = False):
    proc = sp.Popen([cmd], stdout=sp.PIPE, stderr=sp.PIPE, check=True, text=True)
    # print(cmd)
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


def parse_phenotype(filename):
    data = {}

    with open(filename, "r") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) != 2:
                raise ValueError(
                    f"Line {line_no}: expected exactly 2 fields "
                    f"(<variable> <0/1>), but got {len(parts)}: {line!r}"
                )

            var, val_str = parts

            if var in data:
                raise ValueError(
                    f"Line {line_no}: duplicate variable {var!r}"
                )

            if val_str not in {"0", "1"}:
                raise ValueError(
                    f"Line {line_no}: value for {var!r} must be 0 or 1, got {val_str!r}"
                )

            data[var] = int(val_str)

    return data


def parse_perturbation_variables(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            raise ValueError("File is empty")

        # Split on commas or whitespace
        items = [x for x in re.split(r"[,\s]+", content) if x]

        if not items:
            raise ValueError("No variables found in file")

        for i, item in enumerate(items, start=1):
            if not isinstance(item, str):
                raise ValueError(f"Item {i} is not a string: {item!r}")

        return items

    except OSError as e:
        raise ValueError(f"Could not read file {filename!r}: {e}") from e
    
def run_approxasp(input_asp_file, prefix = "count: ", projection = False):
    if shutil.which("gringo"):
    # print("Gringo Installed")
        pass
    else:
        print("gringo is not installed. Please install gringo")
        exit(1)

    os.system('gringo {0} > grounded_{0}'.format(input_asp_file))
    counting_time = 3600
    is_time = 1200
    # computing independet support using the grounded file
    cmd = 'python3 compute_independent_support.py -g 1 -i grounded_{0}'.format(input_asp_file)

    out = run(cmd, int(is_time))
    # print(out)

    if projection:
        cmd = "timeout {0}s ./approxasp --conf 0.35 --sparse --useind IS_{1} --project=project --asp {1}".format(counting_time, input_asp_file) 
    else:
        cmd = "timeout {0}s ./approxasp --conf 0.35 --sparse --useind IS_{1} --asp {1}".format(counting_time, input_asp_file)

    out = run(cmd, int(counting_time))
    cnt = None
    for line in out.splitlines():
        if line.startswith("final ApproxASP estimate") or line.startswith("The exact number of solution:"):
            cnt = line
            print(f"{prefix}: {line}")

    if cnt is None:
        print("No estimate found in the ApproxASP.")

    os.system(f'rm -f IS_{input_asp_file} grounded_{input_asp_file}')