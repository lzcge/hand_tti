
class InfoClass:

    def __init__(self):
        self.ul_dl_type = ""
        self.burst_type = ""
        self.sub_chan = ""
        self.fn = ""
        self.tsn = ""
        self.phy_agc1 = ""
        self.phy_agc2 = ""
        self.phy_filter_befor_rssi = ""
        self.rssi = ""
        self.sinr = ""
        self.caridx = ""
        self.frameoff = ""
        self.bandid = ""
        self.crc = ""
        self.satellite = ""
        self.ta = ""
        self.fa = ""
        self.pa = ""
        self.ssrinfo = ""

    def get_all_info(self):
        return [self.ul_dl_type,self.burst_type,self.sub_chan,self.fn,self.tsn,self.phy_agc1,self.phy_agc2,self.phy_filter_befor_rssi,self.rssi,self.sinr,self.caridx,self.frameoff,self.bandid,self.crc,self.satellite,self.ta,self.fa,self.pa,self.ssrinfo]

    @staticmethod
    def get_infoclass_all_attribute():
        return ["ul_dl_type","burst_type","sub_chan","fn","tsn","phy_agc1","phy_agc2","phy_filter_befor_rssi","rssi","sinr","caridx","frameoff","bandid","crc","satellite","ta","fa","pa","ssrinfo"]
