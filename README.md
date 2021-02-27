# SDN on Mininet

## Part 1: Implementing a FatTree topology on Mininet

Pre-requisite:
+ Install Mininet using the given [steps](http://mininet.org/download/). Choose preferred installation option. 

A two-stage fat-tree network is created as shown in the diagram. Variable N is a parameter provided by the user representing number of ports in a switch.

<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part1/fattree_topo.PNG" width='700' title="Topology1">
</p>

To get started, clone the repository using the following command,
```bash
git clone https://github.com/madhav-prabhu/SDN.git
cd Part1
```

To simulate the network on Mininet, use the following command with e.g. N=4, 
```bash
sudo mn --custom ~/../Part1/p1_fattree_topology.py --topo fattree,4
```
Switches are named as s(level)(number), level:1 = core,2=edge

## Part 2: Implementing a Custom topology with manual flow-rule installation
<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part2/custom_topo.PNG" width='700' title="Topology3">
</p>

Pre-requisite:
+ Install Mininet using the given [steps](http://mininet.org/download/). Choose preferred installation option. 
+ Install default ovs controller using the following steps,
```bash
sudo apt-get install openvswitch-testcontroller
sudo cp /usr/bin/ovs-testcontroller /usr/bin/ovs-controller
```

The following flow-based rules are manually installed on the switches:
+ For Traffic from H1 -> H2
  + HTTP traffic with d_port=80 follows path Sw_A -> Sw_B -> Sw_D
  + All other traffic follows path Sw_A -> Sw_C -> Sw_E -> Sw_D
+ For Traffic from H2 -> H1
  +  HTTP traffic with s_port=80 follows path Sw_D -> Sw_C -> Sw_A
  +  All other traffic follows path Sw_D -> Sw_B -> Sw_E -> Sw_C -> Sw_A

Clone the repository using steps shown in Part1.
To simulate the network on Mininet, change directory to Part2 and run the following command
```bash
sudo mn --custom ~/../Part2/p2_custom_topology.py --topo=ctp --controller remote
```
The '--controller remote' option disables the default controller.

On a seperate terminal, run the flows.sh script to install the respective rules on the simulated switches,

## Part 3: Implementing a Custom topology with flow-rule installation using RYU controller
<p align="center">
  <img src="https://github.com/madhav-prabhu/SDN/blob/main/Part3/ryu_topo.PNG" width='700' title="Topology3">
</p>

Pre-requisite:
+ Install Mininet using the given [steps](http://mininet.org/download/). Choose preferred installation option.
+ Install RYU Controller using the following steps,
```bash
sudo apt install python3-ryu #for Ubuntu_20.04
```
or 
```bash
git clone git://github.com/osrg/ryu.git
cd ryu
python ./setup.py install
```
To verify the installation, run the following command,
```bash
ryu
```

The following flow-based rules are reactively installed on the switches by the RYU controller:
+ H2 & H4 cannot send HTTP traffic (d_port=80), i.e. the controller sends an RST-set packet to the host 
+ H1 & H4 cannot send UDP traffic
+ All other traffic follows the Shortest path
+ If two shortest paths are available,
  + ICMP & TCP take the clockwise path
  + UDP traffic takes the counter-clockwise path

Clone the repository using steps shown in Part1.
To simulate the network on Mininet, change directory to Part3 and run the following command
```bash
sudo mn --custom ~/../p3_custom_topology.py --topo=mytopo --controller remote
```
The '--controller remote' option disables the default controller.

To start the RYU-Controller, run the following command on a seperate terminal,
```bash
ryu-manager --verbose p3_ryu_manager.py
```
