import os, argparse, tempfile, shutil
import subprocess as sp
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input ASP file', required=True)
args = parser.parse_args()
file_name = args.i

def run(cmd, timeout, ttl = 3, silent = False):
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

with tempfile.NamedTemporaryFile(dir=".", delete=False) as f:
    temp_file = f.name
    os.system("cp {0} {1}".format(args.i, temp_file))
    input_file = os.path.basename(temp_file)

if shutil.which("gringo"):
    # print("Gringo Installed")
    pass
else:
    print("gringo is not installed. Please install gringo")
    exit(1)

os.system('gringo {0} > grounded_{0}'.format(input_file))
cnt_time = 3600
is_time = 1200
# computing independet support using the grounded file
cmd = 'python compute_independent_support.py -g 1 -i grounded_{0}'.format(input_file)

out = run(cmd, int(is_time))

cmd = "timeout {0}s ./approxasp --conf 0.35 --sparse --useind IS_{1} --asp {1}".format(cnt_time, input_file)
out = run(cmd, int(cnt_time))

cnt = None
for line in out.splitlines():
    if line.startswith("final ApproxASP estimate"):
        cnt = line
        print("bn-counting: {0}".format(line))

if cnt is None:
    print("No estimate found in the ApproxASP.")

os.system(f'rm -f {input_file} IS_{input_file} grounded_{input_file}')