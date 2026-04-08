## Computing Independent Support
We compute independent support of the ASP programs. The computational mechanism to compute independent support is similar to [Arjun](https://www.msoos.org/wordpress/wp-content/uploads/2022/08/arjun.pdf). 

Here we present a prototype implementation to compute independent support of ASP programs from BN benchmarks. The implementation _might not_ be worked for arbitrary ASP programs. 


## Dependencies
You need to install Clingo. The best way to install clingo is to install it from [potassco](https://github.com/potassco/clingo/releases/).

After successful installation, you should be able to import it from python

```
$ python -c "import clingo; print(clingo.__version__)"
5.6.2
```

**gringo**: you need grounder to process ASP programs. We used gringo and it will be installed with [potassco](https://github.com/potassco/clingo/releases/). You should be able to test it:
```
$ gringo --version
gringo version 5.5.2
```

**networkx**: install package `networkx` as follows: `pip install networkx`

## Compute independent support
First ground the ASP program using `gringo` as follows:
```
gringo t1_244.fix.lp > grounded_t1_244.fix.lp
```
We have a script `compute_independent_support.py`. Please run `compute_independent_support.py` with `grounded_t1_244.fix.lp` as follows:
```
python compute_independent_support.py -g 1 -i grounded_t1_244.fix.lp
```
The command should give the following output:
```
The timeout is set to 1000
The input file is: grounded_t1_244.fix.lp
=== We parse the file ===
The possible candidate for independent support: XXX
The size of atom set: XXX
The size of initial independent support: XXX
The size of final independent support: XXX
c ind XXX 0
```

After the command, `IS_t1_244.fix.lp` is the independent support file of ASP program `t1_244.fix.lp`.


