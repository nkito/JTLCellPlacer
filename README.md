# JTLCellPlacer

under construction.

A PDF manual for the tool is available. Please contact me.

## Usage

Users need a file containing path information. The tool formulated the problem to tile JTL cells according to the given paths as an ILP problem.
Sample code "example.route" considers following JTLs.

![sample code](Example.png)

```
$ ./genlp.sh example.route
```
A formulated ILP problem is obtained as "wire2cell.lp". The next tool invokes an ILP solver and generates the resultant tiling information. 

```
$ ./runsolver.sh wire2cell.lp
```

wire2cell.skill is a generated output. It is a Cadence SKILL script to insert cell instances to a layout.


## Reference 

- "Automatic Cell Placement for Josephson Transmission Lines in Cell-Based Layout Design Environment for RSFQ Circuits", ISS2023, ED-8-3, Nov., 2023. 
