
import _netpacket

class Ppcap(_netpacket.ppcap):
    def __init__(self, device=None, snaplen=1514,
                 filter=None, promisc=0, ms=0):
        _netpacket.ppcap.__init__(self)
        if not device:
            device = self.lookupdev()
        self.open_live(device, snaplen, promisc, ms)
        if filter:
            self.compile(filter)
            self.setfilter()