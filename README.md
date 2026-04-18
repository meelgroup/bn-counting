# Tool and Benchmark of Scalable Counting of Minimal Trap Spaces and Fixed Points in Boolean Networks

The repository has the benchmark and tools of our [CP2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol340-cp2025/LIPIcs.CP.2025.17/LIPIcs.CP.2025.17.pdf) paper. 


### Clone the repo
```
git clone --recurse-submodules git@github.com:meelgroup/bn-counting.git
```

### Dependencies
You need to install cmake, g++, re2c, and bison.
```
sudo apt install build-essential bison re2c cmake gringo python3-pip
```

Install python packages
```
pip install networkx
pip install clingo
```

### ASP Counter: ApproxASP
Compile approxasp:
```
chmod +x build.sh
./build.sh
```

    
## Run ApproxASP
First cd to scripts: `cd scripts`


### Running first task
`Input`: 
- `Boolean network`: a Boolean network (.bnet file)

For counting minimal trap spaces:
```
python3 run_minimal_trap_space.py -t 1 -bn t1_244.bnet
```
it should print the count in line: `C-MTS-1:`

For counting fixed points:
```
python3 run_fixed_point.py -t 1 -bn t1_244.bnet
```
it should print the count in line: `C-FIX-1:`

### Running second task
`Input`: 
- `Boolean network`: a Boolean network (.bnet file)
- `phenotype`: a phenotype, we specify it in a file. You can see example in file `phen_244.txt`

For counting minimal trap spaces:
```
python3 run_minimal_trap_space.py -t 2 -bn t1_244.bnet -phen phen_244.txt
```
it should print the count in line: `C-MTS-2:`

For counting fixed points:
```
python3 run_fixed_point.py -t 2 -bn t1_244.bnet -phen phen_244.txt
```
it should print the count in line: `C-FIX-2:`

### Running third task
`Input`: 
- `Boolean network`: a Boolean network (.bnet file)
- `phenotype`: a phenotype, we specify it in a file. You can see example in file `phen_244.txt`
- `perturbation`: a perturbation, we specify it in a file. You can see example in file `pert_244.txt`

For counting minimal trap spaces:
```
python3 run_minimal_trap_space.py -t 3 -bn t1_244.bnet -phen phen_244.txt -pert pert_244.txt
```
it should print the count in line: `C-MTS-3:`

For counting fixed points:
```
python3 run_fixed_point.py -t 3 -bn t1_244.bnet -phen phen_244.txt -pert pert_244.txt
```
it should print the count in line: `C-FIX-3:`

## Preprocessing BNs
We used [tsconj](https://github.com/daemontus/tsconj) and [fASP](https://github.com/giang-trinh/fASP) to process BNs to ASP program, for minimal trap space and fixed points, respectively. 


## Benchmark:
The benchmark of our CP2025 experiments is available at [https://zenodo.org/records/19609732](https://zenodo.org/records/19609732). 


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
