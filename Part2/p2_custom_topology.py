#!/usr/bin/python

from mininet.topo import Topo

class MyTopo( Topo ):

    def build( self ):
        
        # Add hosts and switches
        host1 = self.addHost( 'h1' , ip='10.0.0.1/24' )
        host2 = self.addHost( 'h2', ip='10.0.0.2/24' )
        A = self.addSwitch( 's1' )
        B = self.addSwitch( 's2' )
        C = self.addSwitch( 's3' )
        D = self.addSwitch( 's4' )
        E = self.addSwitch( 's5' )

        self.addLink(host1, A,2,1)
        self.addLink(D, host2,4,2)
        self.addLink(A, B,2,1)
        self.addLink(A, C,3,1)
        self.addLink(B, E,3,1)
        self.addLink(B, D,2,2)
        self.addLink(C, E,3,3)
        self.addLink(C, D,2,3)
        self.addLink(E, D,2,1)
		

topos = { 'ctp': ( lambda: MyTopo() ) }