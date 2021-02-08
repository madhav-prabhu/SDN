from mininet.topo import Topo
import os

class FatTree( Topo ):

    #maintaining lists of core switches, edge switches and hosts

    core_sw = []
    edge_sw = []
    end_hosts = []

    def __init__(self, N):

        self.coreswitch = N/2       #no of core switches
        self.edgeswitch = N         #no of edge switches
        self.host = 2*((N/2)**2)    #no of hosts

        Topo.__init__(self)

        self.makeTopo()
        self.makeLink()

    #forming switches
    def makeswitch(self, m, l, switchtype):
        for i in range(1, m+1):
            switchtype.append(self.addSwitch('s' + str(l) + str(i)))


    #forming core switches using the makeswitch function
    def makecore(self, m):
        self.makeswitch(m, 1, self.core_sw)


    #forming edge switches using the makeswitch function
    def makeedge(self, m):
        self.makeswitch(m, 2, self.edge_sw)


    #forming hosts
    def makehost(self, m):
        for i in range(1, m+1):
            self.end_hosts.append(self.addHost('h'+ str(i)))


    #forming links
    def makeLink(self):
        p = self.coreswitch
        for i in range(0, self.edgeswitch):
            for j in range(0, p):
                self.addLink(self.core_sw[j], self.edge_sw[i])

        for i in range(0, self.edgeswitch):
            for j in range(0, p):
                self.addLink(self.edge_sw[i], self.end_hosts[p * i + j])

    #forming the topology
    def makeTopo(self):
        self.makecore(self.coreswitch)
        self.makeedge(self.edgeswitch)
        self.makehost(self.host)


topos = { 'fattree' : (lambda N : FatTree(N)) }