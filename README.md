# SDN on Mininet

## Part 1: Implementing a FatTree topology on Mininet

A two-stage fat-tree network is created as shown in the diagram. Variable N is a parameter provided by the user representing number of ports in a switch.

<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part1/fattree_topo.PNG" width='700' title="Topology1">
</p>

To simulate the network on Mininet, use the following command with e.g. N=4, 
```bash
sudo mn --custom ~/../p1_fattree_topology.py --topo fattree,4
```
Switches are named as s(level)(number), level:1 = core,2=edge

## Part 2: Implementing a Custom topology with manual flow-rule installation
<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part2/custom_topo.PNG" width='700' title="Topology3">
</p>

The following flow-based rules are manually installed on the switches:
+ For Traffic from H1 -> H2
  + HTTP traffic with d_port=80 follows path Sw_A -> Sw_B -> Sw_D
  + All other traffic follows path Sw_A -> Sw_C -> Sw_E -> Sw_D
+ For Traffic from H2 -> H1
  +  HTTP traffic with s_port=80 follows path Sw_D -> Sw_C -> Sw_A
  +  All other traffic follows path Sw_D -> Sw_B -> Sw_E -> Sw_C -> Sw_A

To simulate the network on Mininet, run the following command
```bash
sudo mn --custom ~/../p2_custom_topology.py --topo=ctp --controller remote
```
The '--controller remote' option disables the default controller.

On a seperate terminal, run the flows.sh script to install the respective rules on the simulated switches,

## Part 3: Implementing a Custom topology with flow-rule installation using RYU controller
<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part3/ryu_topo.PNG" width='700' title="Topology3">
</p>
