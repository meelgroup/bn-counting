import ast, re, shutil, os
import subprocess as sp
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parent
APPROXASP_BIN = SCRIPT_DIR / "approxasp"   # because build.sh currently copies it here
IS_SCRIPT = SCRIPT_DIR / "compute_independent_support.py"


def run(cmd, timeout, ttl = 3, silent = False):
    proc = sp.Popen([cmd], stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
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

def run_approxasp(input_asp_file, prefix="count: ", projection=False):
    input_asp_file = Path(input_asp_file).resolve()

    if not shutil.which("gringo"):
        raise RuntimeError("gringo is not installed")

    grounded_file = input_asp_file.parent / f"grounded_{input_asp_file.name}"
    is_file = input_asp_file.parent / f"IS_{input_asp_file.name}"

    with grounded_file.open("w", encoding="utf-8") as f:
        sp.run(["gringo", str(input_asp_file)], stdout=f, check=True)

    sp.run(
        ["python3", str(IS_SCRIPT), "-g", "1", "-i", str(grounded_file)],
        text=True,
        capture_output=True,
    )

    cmd = [
        "timeout", "3600s",
        str(APPROXASP_BIN),
        "--conf", "0.35",
        "--sparse",
        "--useind", str(is_file),
    ]
    if projection:
        cmd.append("--project=project")
    cmd += ["--asp", str(input_asp_file)]

    result = sp.run(cmd, text=True, capture_output=True)

    cnt = None
    for line in result.stdout.splitlines():
        if line.startswith("final ApproxASP estimate") or line.startswith("The exact number of solution:"):
            cnt = line
            print(f"{prefix}: {line}")

    if cnt is None:
        print("No estimate found in ApproxASP output.")

    grounded_file.unlink(missing_ok=True)
    is_file.unlink(missing_ok=True)