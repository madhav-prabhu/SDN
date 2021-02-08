# SDN on Mininet

## Part 1: Implementing a FatTree topology on Mininet

A two-stage fat-tree network is created as shown in the diagram below where N is a variable provided by the user.

<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part1/fattree_topo.PNG" width='700' title="Topology1">
</p>

To create the network on mininet, use the following command with N=4, 
```bash
sudo mn --custom ~/../p1_fattree_topology.py --topo fattree,4
```

## Part 2: Implementing a Custom topology on Mininet with RYU controller
<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part2/ryu_topo.PNG" width='700' title="Topology2">
</p>
