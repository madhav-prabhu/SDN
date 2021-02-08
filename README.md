# SDN on Mininet

## Part 1: Implementing a FatTree topology on Mininet

A two-stage fat-tree network is created as shown in the diagram below where N is a variable provided by the user.

<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part1/fattree_topo.PNG" width='700' title="Topology1">
</p>

To create the network on mininet, use the following command with e.g. N=4, 
```bash
sudo mn --custom ~/../p1_fattree_topology.py --topo fattree,4
```
Switches are named as s(level)(number), level:1 = core,2=edge

## Part 2: Implementing a Custom topology with manual flow-rule installation


## Part 3: Implementing a Custom topology with flow-rule installation using RYU controller
<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part2/ryu_topo.PNG" width='700' title="Topology2">
</p>
