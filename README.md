# Tool of Scalable Counting of Minimal Trap Spaces and Fixed Points in Boolean Networks

The repository is the tool of our [CP2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol340-cp2025/LIPIcs.CP.2025.17/LIPIcs.CP.2025.17.pdf) paper. 

The tool counts the number of minimal trap spaces and fixed points of a Boolean network. The detailed can be found here: [CP2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol340-cp2025/LIPIcs.CP.2025.17/LIPIcs.CP.2025.17.pdf).


### Clone the repo
```
git clone --recurse-submodules https://github.com/meelgroup/bn-counting.git
```

### Dependencies
You need to install cmake, g++, re2c, and bison.
```
sudo apt install build-essential bison re2c cmake gringo clasp python3-pip
```

Install python packages
```
pip install networkx
pip install clingo
pip install biodivine-aeon
```

### Compilation and install
You need to compile approxasp and install python package `fASP` and `tsconj`. The following command to do that:
```
chmod +x build.sh
./build.sh
```


### Running first task: C-MTS-1 and C-FIX-1
`Input`: 
- `Boolean Network`: a Boolean network (.bnet file)

For counting minimal trap spaces:
```
python3 script/run_minimal_trap_space.py -t 1 -bn tests/t1_244.bnet
```
it should print the count in line: `C-MTS-1:`

For counting fixed points:
```
python3 script/run_fixed_point.py -t 1 -bn tests/t1_244.bnet
```
it should print the count in line: `C-FIX-1:`

### Running second task: C-MTS-2 and C-FIX-2
`Input`: 
- `Boolean network`: a Boolean network (.bnet file)
- `phenotype`: a phenotype, we specify it in a file. You can see example in file `phen_244.txt`

For counting minimal trap spaces:
```
python3 script/run_minimal_trap_space.py -t 2 -bn tests/t1_244.bnet -phen tests/phen_244.txt
```
it should print the count in line: `C-MTS-2:`

For counting fixed points:
```
python3 script/run_fixed_point.py -t 2 -bn tests/t1_244.bnet -phen tests/phen_244.txt
```
it should print the count in line: `C-FIX-2:`

### Running third task: C-MTS-3 and C-FIX-3
`Input`: 
- `Boolean network`: a Boolean network (.bnet file)
- `phenotype`: a phenotype, we specify it in a file. You can see example in file `phen_244.txt`
- `perturbation`: a perturbation, we specify it in a file. You can see example in file `pert_244.txt`

For counting minimal trap spaces:
```
python3 script/run_minimal_trap_space.py -t 3 -bn tests/t1_244.bnet -phen tests/phen_244.txt -pert tests/pert_244.txt
```
it should print the count in line: `C-MTS-3:`

For counting fixed points:
```
python3 script/run_fixed_point.py -t 3 -bn tests/t1_244.bnet -phen tests/phen_244.txt -pert tests/pert_244.txt
```
it should print the count in line: `C-FIX-3:`

## Preprocessing BNs
We used [tsconj](https://github.com/daemontus/tsconj) and [fASP](https://github.com/giang-trinh/fASP) to encode BNs to ASP program, for minimal trap space and fixed points, respectively. The original implementation is modified for our usage. 


## Benchmark:
The benchmark of our CP2025 experiments is available at [https://zenodo.org/records/19665913](https://zenodo.org/records/19665913). 


## How to cite
If you use it, please cite our work:
```
@article{KTPM2025,
  title={Scalable counting of minimal trap spaces and fixed points in boolean networks},
  author={Kabir, Mohimenul and Trinh, Van-Giang and Pastva, Samuel and Meel, Kuldeep S},
  booktitle={CP},
  year={2025}
}
```

## Contributors
- [Mohimenul Kabir](https://mahi045.github.io/)
- [Van-Giang Trinh](https://dblp.org/pid/152/4760.html)
- [Samuel Pastva](https://dblp.org/pid/167/4487.html)
- [Kuldeep S Meel](https://scs.gatech.edu/people/kuldeep-s-meel)
