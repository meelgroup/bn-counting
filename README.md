# Tool and Benchmark of Scalable Counting of Minimal Trap Spaces and Fixed Points in Boolean Networks

The repository has the benchmark and tools of our [CP2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol340-cp2025/LIPIcs.CP.2025.17/LIPIcs.CP.2025.17.pdf) paper. 


### Clone the repo
```
git clone --recurse-submodules git@github.com:meelgroup/bn-counting.git
```

### Dependencies
You need to install cmake, g++, re2c, and bison.
```
sudo apt-get install bison
sudo apt-get install re2c
sudo apt install build-essential cmake
```

### ASP Counter: ApproxASP
Compile approxasp:
```
chmod +x build.sh
./build.sh
```

    
## Run ApproxASP
cd to scripts: `cd scripts`
run on `t1_244.fix.lp` as follows:
```
python run_counting_bn.py -i t1_244.fix.lp
```

run on `t1_244.mts.lp` as follows:
```
python run_counting_bn.py -i t1_244.mts.lp
```

## Preprocessing BNs
We used [tsconj](https://github.com/daemontus/tsconj) and [fASP](https://github.com/giang-trinh/fASP) to process BNs to ASP program, for minimal trap space and fixed points, respectively. 

- [tsconj](https://github.com/daemontus/tsconj), related paper: [AAAI2024](https://ojs.aaai.org/index.php/AAAI/article/view/28943)
- [fASP](https://github.com/giang-trinh/fASP), related paper: [CP2023](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2023.35)


## Benchmark:
The benchmark of our CP2025 experiments is available at [https://zenodo.org/records/19473442](https://zenodo.org/records/19473442). 


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
