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
We used [ApproxASP](https://github.com/meelgroup/ApproxASP) as the underlying ASP counter. It is added as a submodule. 

## Compile ApproxASP
First you need to compile ApproxASP. cd to ApproxASP and see the readme present in `ApproxASP` directory to compile ApproxASP. After sucessful compilation, mv approxasp binary to `script` directory.

    
## Run ApproxASP
cd to script. It has necessary input BN files.

Run Approxasp for `t1_244.fix.lp` with independent support `IS_t1_244.fix.lp`
```
./approxasp --conf 0.35 --sparse --useind IS_t1_244.fix.lp --asp t1_244.fix.lp
```
The command runs approxasp for `tolerance = 0.8` and `confidence = 0.2`

## Preprocessing BNs
We used [tsconj](https://github.com/daemontus/tsconj) and [fASP](https://github.com/giang-trinh/fASP) to process BNs to ASP program, for minimal trap space and fixed points, respectively. 

## Benchmark:
Benchmark of our CP2025 experiment is available at [https://zenodo.org/records/15141045](https://zenodo.org/records/15141045). 


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
