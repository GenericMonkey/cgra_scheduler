# CGRA Scheduler

## Requirements
This was built on Python 3.6, and requires GraphViz to run the visualization.

## Example Usage
```
python cfgGenerator.py
```
This runs the visualization on `output.ll`, which is an output of the pass in `/HW1` run on either `simple_bf.c` or `vec_mult.c`.

```
python scheduler.py --size 3
```
This runs the scheduler that outputs a rolled and unrolled scheduler for a CGRA of size 3.
```
python scheduler.py --size 3 --debug --verbose
```
This prints a lot more things, and allows you to step through the scheduling process instruction by instruction.
