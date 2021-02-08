#!/bin/bash

echo "Adding flows for s1";
sudo ovs-ofctl add-flow s1 priority=1000,in_port=1,dl_type=0x0800,nw_proto=6,tcp_dst=80,nw_src=10.0.0.1/24,nw_dst=10.0.0.2/24,actions=output:2;

sudo ovs-ofctl add-flow s1 priority=500,in_port=1,nw_src=10.0.0.1/24,nw_dst=10.0.0.2/24,actions=output:3;

sudo ovs-ofctl add-flow s1 priority=1000,in_port=3,dl_type=0x0800,nw_proto=6,tcp_src=80,nw_src=10.0.0.2/24,nw_dst=10.0.0.1/24,actions=output:1;

sudo ovs-ofctl add-flow s1 priority=500,in_port=3,nw_src=10.0.0.2/24,nw_dst=10.0.0.1/24,actions=output:1;

echo "Adding flows for s2";

sudo ovs-ofctl add-flow s2 priority=1000,in_port=1,dl_type=0x0800,nw_proto=6,tcp_dst=80,nw_src=10.0.0.1/24,nw_dst=10.0.0.2/24,actions=output:2;

sudo ovs-ofctl add-flow s2 priority=500,in_port=2,nw_src=10.0.0.2/24,nw_dst=10.0.0.1/24,actions=output:3;

echo "Adding flows for s3";

sudo ovs-ofctl add-flow s3 priority=500,in_port=1,nw_src=10.0.0.1/24,nw_dst=10.0.0.2/24,actions=output:3;

sudo ovs-ofctl add-flow s3 priority=1000,in_port=2,dl_type=0x0800,nw_proto=6,tcp_src=80,nw_src=10.0.0.2/24,nw_dst=10.0.0.1/24,actions=output:1;

sudo ovs-ofctl add-flow s3 priority=500,in_port=3,nw_src=10.0.0.2/24,nw_dst=10.0.0.1/24,actions=output:1;

echo "Adding flows for s4";

sudo ovs-ofctl add-flow s4 priority=1000,in_port=2,dl_type=0x0800,nw_proto=6,tcp_dst=80,nw_src=10.0.0.1/24,nw_dst=10.0.0.2/24,actions=output:4;

sudo ovs-ofctl add-flow s4 priority=500,in_port=1,nw_src=10.0.0.1/24,nw_dst=10.0.0.2/24,actions=output:4;

sudo ovs-ofctl add-flow s4 priority=1000,in_port=4,dl_type=0x0800,nw_proto=6,tcp_src=80,nw_src=10.0.0.2/24,nw_dst=10.0.0.1/24,actions=output:3;

sudo ovs-ofctl add-flow s4 priority=500,in_port=4,nw_src=10.0.0.2/24,nw_dst=10.0.0.1/24,actions=output:2;

echo "Adding flows for s5";

sudo ovs-ofctl add-flow s5 priority=500,in_port=3,nw_src=10.0.0.1/24,nw_dst=10.0.0.2/24,actions=output:2;

sudo ovs-ofctl add-flow s5 priority=500,in_port=1,nw_src=10.0.0.2/24,nw_dst=10.0.0.1/24,actions=output:3;
