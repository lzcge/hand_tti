
import re
from info_class import InfoClass


class PatternRule:

    def __init__(self):
        # 下行相关提取关键字
        self._satellite_pattern = 'Beam: satelliteId'
        self._dl_schedule_pattern = 'set DL schedule[1]: BURST_TYPE'
        self._dl_schedule_band_pattern = 'set DL schedule[1]: band'
        self._l1c_l1a_rx_data_ind_pattern = 'L1C_L1A_RX_DATA_IND'
        self._l1c_l1a_beam_meas_ind_pattern = 'L1C_L1A_BEAM_MEAS_IND'
        self._mac_l1a_adjust_t_f_offset_ind_pattern = 'MAC_L1A_ADJUST_T_F_OFFSET_IND'

        # 上行相关提取关键字
        self._l1a_mac_tx_data_ind_pattern = 'L1A_MAC_TX_DATA_IND'
        self._ul_schedule_pattern = 'set UL schedule[1]: BURST_TYPE'
        self._ul_schedule_band_pattern = 'set UL schedule[1]: band'

        # 波速切换提取关键字
        self._handover_start_pattern = 'RRC_L1A_HO_CONFIG_REQ'
        self._handover_success_pattern = '[RLC] ACK(0) for Rb_Id(1)'

    @property
    def satellite_pattern(self):
        return self._satellite_pattern

    @satellite_pattern.setter
    def satellite_pattern(self, value):
        self._satellite_pattern = value

    @property
    def dl_schedule_pattern(self):
        return self._dl_schedule_pattern

    @dl_schedule_pattern.setter
    def dl_schedule_pattern(self, value):
        self._dl_schedule_pattern = value

    @property
    def dl_schedule_band_pattern(self):
        return self._dl_schedule_band_pattern

    @dl_schedule_band_pattern.setter
    def dl_schedule_band_pattern(self, value):
        self._dl_schedule_band_pattern = value

    @property
    def l1c_l1a_rx_data_ind_pattern(self):
        return self._l1c_l1a_rx_data_ind_pattern

    @l1c_l1a_rx_data_ind_pattern.setter
    def l1c_l1a_rx_data_ind_pattern(self, value):
        self._l1c_l1a_rx_data_ind_pattern = value

    @property
    def l1c_l1a_beam_meas_ind_pattern(self):
        return self._l1c_l1a_beam_meas_ind_pattern

    @l1c_l1a_beam_meas_ind_pattern.setter
    def l1c_l1a_beam_meas_ind_pattern(self, value):
        self._l1c_l1a_beam_meas_ind_pattern = value

    @property
    def mac_l1a_adjust_t_f_offset_ind_pattern(self):
        return self._mac_l1a_adjust_t_f_offset_ind_pattern

    @mac_l1a_adjust_t_f_offset_ind_pattern.setter
    def mac_l1a_adjust_t_f_offset_ind_pattern(self, value):
        self._mac_l1a_adjust_t_f_offset_ind_pattern = value

    @property
    def l1a_mac_tx_data_ind_pattern(self):
        return self._l1a_mac_tx_data_ind_pattern

    @l1a_mac_tx_data_ind_pattern.setter
    def l1a_mac_tx_data_ind_pattern(self, value):
        self._l1a_mac_tx_data_ind_pattern = value

    @property
    def ul_schedule_pattern(self):
        return self._ul_schedule_pattern

    @ul_schedule_pattern.setter
    def ul_schedule_pattern(self, value):
        self._ul_schedule_pattern = value

    @property
    def ul_schedule_band_pattern(self):
        return self._ul_schedule_band_pattern

    @ul_schedule_band_pattern.setter
    def ul_schedule_band_pattern(self, value):
        self._ul_schedule_band_pattern = value

    @property
    def handover_start_pattern(self):
        return self._handover_start_pattern

    @handover_start_pattern.setter
    def handover_start_pattern(self, value):
        self._handover_start_pattern = value

    @property
    def handover_success_pattern(self):
        return self._handover_success_pattern

    @handover_success_pattern.setter
    def handover_success_pattern(self, value):
        self._handover_success_pattern = value

    def get_all_info(self):
        return [self.satellite_pattern, self.dl_schedule_pattern, self.dl_schedule_band_pattern,self.l1c_l1a_rx_data_ind_pattern, self.l1c_l1a_beam_meas_ind_pattern, self.mac_l1a_adjust_t_f_offset_ind_pattern, self.l1a_mac_tx_data_ind_pattern, self.ul_schedule_pattern,self.ul_schedule_band_pattern, self.handover_start_pattern, self.handover_success_pattern]

    def dl_schedule_patten_search(self,content: str) -> InfoClass:
        '''
        set DL schedule[1]: BURST_TYPE数据提取函数
        :param content:
        :return:
        '''
        info_calss = InfoClass()
        # 提取BURST_TYPE
        burst_type_match = re.findall(r'BURST_TYPE_(\w+)', content)
        burst_type = burst_type_match[0] if burst_type_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取SUB_CHAN
        sub_chan_match = re.findall(r'SUB_CHAN_(\w+)', content)
        sub_chan = sub_chan_match[0] if sub_chan_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取fn
        fn_match = re.findall(r'time\[(\d+)', content)
        fn = int(fn_match[0]) if fn_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取tsn
        tsn_match = re.findall(r'time\[\d+,(\d+)', content)
        tsn = int(tsn_match[0]) if tsn_match else -999999

        # 提取 carIdx
        caridx_match = re.findall(r'carIdx\((\d+)', content)
        caridx = int(caridx_match[0]) if caridx_match else -999999
        info_calss.ul_dl_type = "dl"
        info_calss.burst_type = burst_type
        info_calss.sub_chan = sub_chan
        info_calss.fn = fn
        info_calss.tsn = tsn
        info_calss.caridx = caridx
        return info_calss

    def ul_schedule_patten_search(self,content: str) -> InfoClass:
        '''
        set UL schedule[1]: BURST_TYPE数据提取函数
        :param content:
        :return:
        '''
        info_calss = InfoClass()
        # 提取BURST_TYPE
        burst_type_match = re.findall(r'BURST_TYPE_(\w+)', content)
        burst_type = burst_type_match[0] if burst_type_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取SUB_CHAN
        sub_chan_match = re.findall(r'SUB_CHAN_(\w+)', content)
        sub_chan = sub_chan_match[0] if sub_chan_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取fn
        fn_match = re.findall(r'ulTime\[(\d+)', content)
        fn = int(fn_match[0]) if fn_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取tsn
        tsn_match = re.findall(r'ulTime\[\d+,(\d+)', content)
        tsn = int(tsn_match[0]) if tsn_match else -999999

        # 提取 carIdx
        caridx_match = re.findall(r'carIdx\((\d+)', content)
        caridx = int(caridx_match[0]) if caridx_match else -999999

        info_calss.ul_dl_type = "ul"
        info_calss.burst_type = burst_type
        info_calss.sub_chan = sub_chan
        info_calss.fn = fn
        info_calss.tsn = tsn
        info_calss.caridx = caridx
        info_calss.crc = 0
        info_calss.rssi = 0
        info_calss.sinr = 0
        return info_calss

    def l1c_l1a_rx_data_ind_patten_search(self,content: str) -> InfoClass:
        '''
        l1c_l1a_rx_data_ind 数据提取函数
        :param content:
        :return:
        '''
        info_calss = InfoClass()
        # 提取BURST_TYPE
        burst_type_match = re.findall(r'BURST_TYPE_(\w+)', content)
        burst_type = burst_type_match[0] if burst_type_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取SUB_CHAN
        sub_chan_match = re.findall(r'SUB_CHAN_(\w+)', content)
        sub_chan = sub_chan_match[0] if sub_chan_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取fn
        fn_match = re.findall(r'fn=(\d+)', content)
        fn = int(fn_match[0]) if fn_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取tsn
        tsn_match = re.findall(r'tsn=(\d+)', content)
        tsn = int(tsn_match[0]) if tsn_match else -999999

        # 提取 frameOff
        frameoff_match = re.findall(r'beamId=(\d+)', content)
        frameoff = int(frameoff_match[0]) if frameoff_match else -999999  # 加0.5四舍五入

        # 提取 bandid
        bandid_match = re.findall(r'bandId=(\d+)', content)
        bandid = int(bandid_match[0]) if bandid_match else -999999

        # 提取 crc
        crc_match = re.findall(r'crc=(\d+)', content)
        crc = int(crc_match[0]) if crc_match else -999999

        info_calss.ul_dl_type = "dl"
        info_calss.burst_type = burst_type
        info_calss.sub_chan = sub_chan
        info_calss.fn = fn
        info_calss.tsn = tsn
        info_calss.frameoff = frameoff
        info_calss.bandid = bandid
        info_calss.crc = crc
        return info_calss

    def l1c_l1a_beam_meas_ind_patten_search(self,content: str) -> InfoClass:
        '''
        l1c_l1a_beam_meas_ind数据提取函数
        :param content:
        :return:
        '''
        info_calss = InfoClass()

        # frameOff
        frameoffs = re.findall("(\d+)\(BURST_TYPE", content, re.S)
        frameoff = int(frameoffs[0]) if frameoffs else -999999

        # 提取fn
        fn_match = re.findall(r'fn=(\d+)', content)
        fn = int(fn_match[0]) if fn_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取tsn
        tsn_match = re.findall(r'tsn=(\d+)', content)
        tsn = int(tsn_match[0]) if tsn_match else -999999

        # 提取 rssi
        rssi_match = re.findall(r'rssi=-\d+\((-?\d+)', content)
        rssi = int(rssi_match[0]) if rssi_match else -999999  # 如果未找到，赋值-999999的异常值
        # 提取 sinr
        sinr_match = re.findall(r'SINR=(-?\d+)', content)
        sinr = int(int(sinr_match[0])/256+0.5) if sinr_match else -999999  # 加0.5四舍五入
        info_calss.ul_dl_type = "dl"
        info_calss.frameoff = frameoff
        info_calss.fn = fn
        info_calss.tsn = tsn
        info_calss.rssi = rssi
        info_calss.sinr = sinr
        return info_calss

    def l1a_mac_tx_data_ind_patten_search(self,content: str) -> InfoClass:
        '''
        l1a_mac_tx_data_ind数据提取函数
        :param content:
        :return:
        '''
        info_calss = InfoClass()
        # 提取BURST_TYPE
        burst_type_match = re.findall(r'DATA_TYPE_DCCH_(\w+)', content)
        burst_type = burst_type_match[0] if burst_type_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取fn
        fn_match = re.findall(r'fn=(\d+)', content)
        fn = int(fn_match[0]) if fn_match else -999999  # 如果未找到，赋值-999999的异常值

        # 提取tsn
        tsn_match = re.findall(r'tsn=(\d+)', content)
        tsn = int(tsn_match[0]) if tsn_match else -999999

        # 提取bandId
        bandid_match = re.findall(r'bandId=(\d+)', content)
        bandid = int(bandid_match[0]) if bandid_match else -999999

        # 提取 frameOff
        frameoff_match = re.findall(r'beamId=(\d+)', content)
        frameoff = int(frameoff_match[0]) if frameoff_match else -999999

        info_calss.ul_dl_type = "ul"
        info_calss.burst_type = burst_type
        info_calss.fn = fn
        info_calss.tsn = tsn
        info_calss.bandid = bandid
        info_calss.frameoff = frameoff
        info_calss.rssi = 0
        info_calss.sinr = 0
        info_calss.ta = 0
        info_calss.fa = 0
        info_calss.pa = 0
        return info_calss

    def handover_success_pattern_search(self,handover_number: int) -> InfoClass:
        '''
        波束切换成功，信息提取
        :param handover_number:
        :return:
        '''
        info_calss = InfoClass()
        info_calss.ul_dl_type = '第'+str(handover_number)+'次切换成功'
        info_calss.burst_type = '切换'
        return info_calss

    def handover_faile_pattern_search(self,handover_number: int) -> InfoClass:
        '''
        波束切换失败，信息提取
        :param handover_number:
        :return:
        '''
        info_calss = InfoClass()
        info_calss.ul_dl_type = '第'+str(handover_number)+'次切换失败'
        info_calss.burst_type = '切换'
        return info_calss

    def satellite_pattern_search(self,content: str) -> int:
        '''
        卫星id信息提取函数
        :param content:
        :return:
        '''
        satelliteid_match = re.findall(r'satelliteId=(\d+)', content)
        satelliteid = int(satelliteid_match[0]) if satelliteid_match else -999999  # 如果未找到，赋值-999999的异常值
        return satelliteid

    def ul_dl_schedule_bandid_pattern_search(self,content: str):
        '''
        set DL schedule[1]: band 和 set UL schedule[1]: band中的bandid提取函数
        :param content:
        :return:
        '''
        bandid_match = re.findall(r'band\s+(\d+)', content)
        bandid = int(bandid_match[0]) if bandid_match else -999999
        return bandid

    def mac_l1a_adjust_t_f_offset_ind_pattern_search(self,content: str):
        '''
        ta,fa,pa数据提取函数
        :param content:
        :return:
        '''
        info_calss = InfoClass()
        ta_match = re.findall(r'TA=(-?\d+)', content)
        ta = int(ta_match[0]) if ta_match else -999999

        fa_match = re.findall(r'FA=(-?\d+)', content)
        fa = int(fa_match[0]) if fa_match else -999999

        pa_match = re.findall(r'PA=(-?\d+)', content)
        pa = int(pa_match[0]) if pa_match else -999999
        info_calss.ta = ta
        info_calss.fa = fa
        info_calss.pa = pa
        return info_calss



