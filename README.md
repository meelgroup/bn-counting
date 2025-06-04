# Content
- `approxasp`: ApproxASP binary
- `ganak`: GANAK and ApproxMC binary
    
# Run ApproxASP
__We run our experiments in a linux environment__

__Please make sure that approxasp, t1_244.fix.lp, IS_t1_244.fix.lp are present in the current directory__

__Please make sure that approxasp is executable (execute: chmod +x approxasp)__

Run Approxasp for `t1_244.fix.lp` with independent support `IS_t1_244.fix.lp`
```
./approxasp --conf 0.35 --sparse --useind IS_t1_244.fix.lp --asp t1_244.fix.lp
```
The command runs approxasp for `tolerance = 0.8` and `confidence = 0.2`

# Run GANAK & ApproxMC
__We run our experiments in a linux environment__

__Install biodivine_aeon and sympy package using command `pip install biodivine_aeon sympy`, [related link](https://github.com/sybila/biodivine-aeon-py)__

__Please make sure that ganak, test_to_cnf.py, test_to_cnf_approx.py, t1_244.bnet are present in the current directory__

__Please make sure that ganak is executable (execute: chmod +x ganak)__

Run GANAK for `t1_244.bnet`
```
python test_to_cnf.py t1_244.bnet
```

Run ApproxMC for `t1_244.bnet`
```
python test_to_cnf_approx.py t1_244.bnet
```
The `ganak` is taken from the latest model counting competition.

# Benchmark:
Benchmark of the experiment is available at [https://zenodo.org/records/15141045](https://zenodo.org/records/15141045). 

# Sources of other counters:
- `tsconj`: [https://github.com/daemontus/tsconj](https://github.com/daemontus/tsconj)
- `fASP`: [https://github.com/giang-trinh/fASP](https://github.com/giang-trinh/fASP)
- `k++ADF`: [https://www.cs.helsinki.fi/group/coreo/k++adf/](https://www.cs.helsinki.fi/group/coreo/k++adf/)
- `AEON`: [https://github.com/sybila/biodivine-aeon-py](https://github.com/sybila/biodivine-aeon-py)

# How to cite
TBA
