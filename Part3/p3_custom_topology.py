from mininet.topo import Topo

class MyTopo( Topo ):
    '''Simple topology example.'''

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        h1 = self.addHost( 'h1' , ip='10.0.0.1', mac='10:00:00:00:00:01')
        h2 = self.addHost( 'h2' , ip='10.0.0.2', mac='10:00:00:00:00:02')
        h3 = self.addHost( 'h3' , ip='10.0.0.3', mac='10:00:00:00:00:03')
        h4 = self.addHost( 'h4' , ip='10.0.0.4', mac='10:00:00:00:00:04')
        S1 = self.addSwitch( 's1' )
        S2 = self.addSwitch( 's2' )
        S3 = self.addSwitch( 's3' )
        S4 = self.addSwitch( 's4' )
        

        # Add links
        self.addLink(h1,S1,1,1)
        self.addLink(h2,S2,1,1)
        self.addLink(h3,S3,1,1)
        self.addLink(h4,S4,1,1)
        self.addLink(S1,S2,2,2)
        self.addLink(S2,S3,3,3)
        self.addLink(S3,S4,2,2)
        self.addLink(S4,S1,3,3)


topos = { 'mytopo': ( lambda: MyTopo() ) }

