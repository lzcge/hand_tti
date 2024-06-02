from typing import Union, Tuple, Any


class InfoClass:

    def __init__(self):
        self._id = ""
        self._ul_dl_type = ""
        self._burst_type = ""
        self._sub_chan = ""
        self._fn = ""
        self._tsn = ""
        self._rssi = ""
        self._sinr = ""
        self._caridx = ""
        self._frameoff = ""
        self._bandid = ""
        self._crc = ""
        self._satellite = ""
        self._ta = ""
        self._fa = ""
        self._pa = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def ul_dl_type(self):
        return self._ul_dl_type

    @ul_dl_type.setter
    def ul_dl_type(self, value):
        self._ul_dl_type = value

    @property
    def burst_type(self):
        return self._burst_type

    @burst_type.setter
    def burst_type(self, value):
        self._burst_type = value


    @property
    def sub_chan(self):
        return self._sub_chan

    @sub_chan.setter
    def sub_chan(self, value):
        self._sub_chan = value

    @property
    def fn(self):
        return self._fn

    @fn.setter
    def fn(self, value):
        self._fn = value

    @property
    def tsn(self):
        return self._tsn

    @tsn.setter
    def tsn(self, value):
        self._tsn = value

    @property
    def rssi(self):
        return self._rssi

    @rssi.setter
    def rssi(self, value):
        self._rssi = value


    @property
    def sinr(self):
        return self._sinr

    @sinr.setter
    def sinr(self, value):
        self._sinr = value


    @property
    def caridx(self):
        return self._caridx

    @caridx.setter
    def caridx(self, value):
        self._caridx = value

    @property
    def frameoff(self):
        return self._frameoff

    @frameoff.setter
    def frameoff(self, value):
        self._frameoff = value

    @property
    def bandid(self):
        return self._bandid

    @bandid.setter
    def bandid(self, value):
        self._bandid = value

    @property
    def crc(self):
        return self._crc

    @crc.setter
    def crc(self, value):
        self._crc = value

    @property
    def satellite(self):
        return self._satellite

    @satellite.setter
    def satellite(self, value):
        self._satellite = value

    @property
    def ta(self):
        return self._ta

    @ta.setter
    def ta(self, value):
        self._ta = value

    @property
    def fa(self):
        return self._fa

    @fa.setter
    def fa(self, value):
        self._fa = value

    @property
    def pa(self):
        return self._pa

    @pa.setter
    def pa(self, value):
        self._pa = value


    def __eq__(self, other):
        return self._id == other.id

    def get_all_info(self):
        return [self.ul_dl_type,self.burst_type,self.sub_chan,self.fn,self.tsn,self.rssi,self.sinr,self.caridx,self.frameoff,self.bandid,self.crc,self.satellite,self.ta,self.fa,self.pa]

    def get_title_info(self):
        return ["ul_dl_type","burst_type","sub_chan","fn","tsn","rssi","sinr","caridx","frameoff","bandid","crc","satellite","ta","fa","pa"]


    def update_info(self,infoclass):
        if infoclass.ul_dl_type != "":
            self.ul_dl_type = infoclass.ul_dl_type
        if infoclass.burst_type != "":
            self.burst_type = infoclass.burst_type
        if infoclass.sub_chan != "":
            self.sub_chan = infoclass.sub_chan
        if infoclass.fn != "":
            self.fn = infoclass.fn
        if infoclass.tsn != "":
            self.tsn = infoclass.tsn
        if infoclass.rssi != "":
            self.rssi = infoclass.rssi
        if infoclass.sinr != "":
            self.sinr = infoclass.sinr
        if infoclass.caridx != "":
            self.caridx = infoclass.caridx
        if infoclass.frameoff != "":
            self.frameoff = infoclass.frameoff
        if infoclass.bandid != "":
            self.bandid = infoclass.bandid
        if infoclass.crc != "":
            self.crc = infoclass.crc
        self.satellite = infoclass.satellite
        if infoclass.ta != "":
            self.ta = infoclass.ta
        if infoclass.fa != "":
            self.fa = infoclass.fa
        if infoclass.pa != "":
            self.pa = infoclass.pa
