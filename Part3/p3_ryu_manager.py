from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ether
from ryu.ofproto import inet
import json
from ryu.lib.packet import packet, ethernet, arp, ipv4, tcp, udp, icmp

global sw_tcp
sw_tcp = []
global sw_udp
sw_udp = []

class ryulab(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
     
    def __init__(self, *args, **kwargs):
        super(ryulab, self).__init__(*args, **kwargs)
        self.arp_table={}
        self.arp_table = {'10.0.0.1': '10:00:00:00:00:01','10.0.0.2': '10:00:00:00:00:02','10.0.0.3': '10:00:00:00:00:03','10.0.0.4': '10:00:00:00:00:04'}
    

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath
        dpid = dp.id
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser
        match = ofp_parser.OFPMatch()
        action = ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,[ofp_parser.OFPActionOutput(ofp.OFPP_CONTROLLER)])
        inst = [action]
        self.flow_mod(dp=dp,match=match, inst=inst, table=0, priority=0)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        dpid = dp.id
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        dst = eth.dst
        src = eth.src
        in_port = msg.match['in_port']
        pkt_icmp = pkt.get_protocol(icmp.icmp)
        tcp_pkt = pkt.get_protocol(tcp.tcp)
        arp_pkt = pkt.get_protocol(arp.arp)
        udp_pkt = pkt.get_protocol(udp.udp)
        
        if arp_pkt != None:
            self.arp_request(dp, in_port, pkt)
        
        if tcp_pkt != None:
            self.tcp_request(dp, in_port, pkt)
            
        
        if pkt_icmp:
            if (dpid == 1):
                self.shortest_path_flow(dp, '10.0.0.2', inet.IPPROTO_ICMP, 2)   
                self.shortest_path_flow(dp, '10.0.0.4', inet.IPPROTO_ICMP, 3)       
                self.shortest_path_flow(dp, '10.0.0.1', inet.IPPROTO_ICMP, 1)
                self.l4_flows(dp, '10.0.0.3', inet.IPPROTO_ICMP, 2)
                        
            elif (dpid == 2):
                self.shortest_path_flow(dp, '10.0.0.1', inet.IPPROTO_ICMP, 2)
                self.shortest_path_flow(dp, '10.0.0.2', inet.IPPROTO_ICMP, 1)
                self.shortest_path_flow(dp, '10.0.0.3', inet.IPPROTO_ICMP, 3)
                self.l4_flows(dp, '10.0.0.4', inet.IPPROTO_ICMP, 3)
                        
            elif (dpid == 3): 
                self.shortest_path_flow(dp, '10.0.0.2', inet.IPPROTO_ICMP, 3)
                self.shortest_path_flow(dp, '10.0.0.4', inet.IPPROTO_ICMP, 2)
                self.shortest_path_flow(dp, '10.0.0.3', inet.IPPROTO_ICMP, 1)
                self.l4_flows(dp, '10.0.0.1', inet.IPPROTO_ICMP, 2)

            elif (dpid == 4):
                self.shortest_path_flow(dp, '10.0.0.4', inet.IPPROTO_ICMP, 1)
                self.shortest_path_flow(dp, '10.0.0.1', inet.IPPROTO_ICMP, 3)
                self.shortest_path_flow(dp, '10.0.0.3', inet.IPPROTO_ICMP, 2)
                self.l4_flows(dp, '10.0.0.2', inet.IPPROTO_ICMP, 3)
        
        if (tcp_pkt != None) and (dpid not in sw_tcp):

            if (dpid == 1):
                self.l4_flows(dp, '10.0.0.1', inet.IPPROTO_TCP, 1)
                self.l4_flows(dp, '10.0.0.2', inet.IPPROTO_TCP, 2)
                self.l4_flows(dp, '10.0.0.3', inet.IPPROTO_TCP, 2)
                self.l4_flows(dp, '10.0.0.4', inet.IPPROTO_TCP, 3)
                sw_tcp.append(dpid)
                        
            elif (dpid == 2):
                self.l4_flows(dp, '10.0.0.2', inet.IPPROTO_TCP, 1)
                self.l4_flows(dp, '10.0.0.4', inet.IPPROTO_TCP, 3)
                self.l4_flows(dp, '10.0.0.3', inet.IPPROTO_TCP, 3)
                self.l4_flows(dp, '10.0.0.1', inet.IPPROTO_TCP, 2)
                self.http_flow(dp, '10.0.0.2', inet.IPPROTO_TCP, 80)
                sw_tcp.append(dpid)

            elif (dpid == 3): 
                self.l4_flows(dp, '10.0.0.1', inet.IPPROTO_TCP, 2)
                self.l4_flows(dp, '10.0.0.2', inet.IPPROTO_TCP, 3)
                self.l4_flows(dp, '10.0.0.3', inet.IPPROTO_TCP, 1)
                self.l4_flows(dp, '10.0.0.4', inet.IPPROTO_TCP, 2)
                sw_tcp.append(dpid)

            elif (dpid == 4):
                self.l4_flows(dp, '10.0.0.2', inet.IPPROTO_TCP, 3)
                self.l4_flows(dp, '10.0.0.1', inet.IPPROTO_TCP, 3)
                self.l4_flows(dp, '10.0.0.3', inet.IPPROTO_TCP, 2)
                self.l4_flows(dp, '10.0.0.3', inet.IPPROTO_TCP, 1)
                self.http_flow(dp, '10.0.0.4', inet.IPPROTO_TCP, 80)
                sw_tcp.append(dpid)

        if (udp_pkt != None) and (dpid not in sw_udp) and (udp_pkt.dst_port != 5353):

            if (dpid == 1):
               self.drop_udp(dp, '10.0.0.1', inet.IPPROTO_UDP, [])
               self.l4_flows(dp, '10.0.0.4', inet.IPPROTO_UDP, 3)
               sw_udp.append(dpid)
                        
            elif (dpid == 2):
               self.l4_flows(dp, '10.0.0.1', inet.IPPROTO_UDP, 2)
               self.l4_flows(dp, '10.0.0.3', inet.IPPROTO_UDP, 3)
               self.l4_flows(dp, '10.0.0.4', inet.IPPROTO_UDP, 2)
               sw_udp.append(dpid)
                
            elif (dpid == 3): 
               self.l4_flows(dp, '10.0.0.1', inet.IPPROTO_UDP, 3)
               self.l4_flows(dp, '10.0.0.4', inet.IPPROTO_UDP, 2)
               self.l4_flows(dp, '10.0.0.2', inet.IPPROTO_UDP, 3)
               sw_udp.append(dpid)

            elif (dpid == 4):
               self.drop_udp(dp, '10.0.0.4', inet.IPPROTO_UDP, [])
               self.l4_flows(dp, '10.0.0.4', inet.IPPROTO_UDP, 1)
               sw_udp.append(dpid)

        
            

    def http_flow(self,dp,ipv4_src,ip_proto,tcp_dst):
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser
        match = ofp_parser.OFPMatch(eth_type=ether.ETH_TYPE_IP, ipv4_src=ipv4_src,ip_proto=ip_proto,tcp_dst=tcp_dst)
        action = ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [ofp_parser.OFPActionOutput(ofp.OFPP_CONTROLLER)])
        inst = [action]
        self.flow_mod(dp, match, inst, 0, 500)
    
    def drop_udp(self, dp, ipv4_src,ip_proto,actions):
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser
        actions = actions
        match = ofp_parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,ipv4_src=ipv4_src,ip_proto=ip_proto)
        action = ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,actions)
        inst = [action]
        self.flow_mod(dp, match, inst, 0, 400)
    

    def shortest_path_flow(self,dp,ipv4_dst,proto,out_port):
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser
        match = ofp_parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,ipv4_dst=ipv4_dst,ip_proto=proto)
        action = ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [ofp_parser.OFPActionOutput(out_port)])
        inst = [action]
        self.flow_mod(dp, match, inst, 0, 10)

    def l4_flows(self,dp,ipv4_dst,proto,out_port):
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser
        match = ofp_parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,ipv4_dst=ipv4_dst,ip_proto=proto)
        action = ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [ofp_parser.OFPActionOutput(out_port)])
        inst = [action]
        self.flow_mod(dp, match, inst, 0, 50)

    def flow_mod(self, dp, match, inst, table, priority):
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser
        buffer_id = ofp.OFP_NO_BUFFER
        mod = ofp_parser.OFPFlowMod(datapath=dp, table_id=table, priority=priority, match=match, instructions=inst )
        dp.send_msg(mod)


    def send_packet(self, dp, port, pkt):
        ofproto = dp.ofproto
        parser = dp.ofproto_parser
        pkt.serialize()
        data = pkt.data
        action = [parser.OFPActionOutput(port=port)]
        out = parser.OFPPacketOut(datapath=dp, buffer_id=ofproto.OFP_NO_BUFFER, in_port=ofproto.OFPP_CONTROLLER, actions=action, data=data)
        dp.send_msg(out)

    
    def arp_request(self, dp, port, pkt):
        pkt_arp = pkt.get_protocol(arp.arp)
        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        
        if pkt_arp.opcode != arp.ARP_REQUEST:
            return
        if self.arp_table.get(pkt_arp.dst_ip) == None:
            return
        get_mac = self.arp_table[pkt_arp.dst_ip]
        pkt = packet.Packet()
        pkt.add_protocol(ethernet.ethernet( ethertype=ether.ETH_TYPE_ARP,
                                            dst=pkt_ethernet.src,
                                            src=get_mac ))
        pkt.add_protocol( arp.arp(opcode=arp.ARP_REPLY,
                                    src_mac=get_mac,
                                    src_ip=pkt_arp.dst_ip,
                                    dst_mac=pkt_arp.src_mac,
                                    dst_ip=pkt_arp.src_ip))
        self.send_packet(dp, port, pkt)


    def tcp_request(self, dp, port, pkt):
        eth = pkt.get_protocol(ethernet.ethernet)
        p_ipv4 = pkt.get_protocol(ipv4.ipv4)
        ip_src = p_ipv4.src
        ip_dst = p_ipv4.dst
        ip_proto = p_ipv4.proto
        p_tcp = pkt.get_protocol(tcp.tcp)
        dst_port = p_tcp.dst_port
        if (ip_src == "10.0.0.2" or ip_src == "10.0.0.4") and ip_proto == inet.IPPROTO_TCP and dst_port == 80:
            header_tcp = tcp.tcp(ack=p_tcp.seq + 1, src_port=p_tcp.dst_port, dst_port=p_tcp.src_port, bits=20)
            header_ip = ipv4.ipv4(dst=ip_src, src=ip_dst, proto=ip_proto)
            header_eth = ethernet.ethernet(ethertype=ether.ETH_TYPE_IP, dst=eth.src, src=eth.dst)
            reset = packet.Packet()
            reset.add_protocol(header_eth)
            reset.add_protocol(header_ip)
            reset.add_protocol(header_tcp)
            self.send_packet(dp, port, reset)