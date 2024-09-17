
import re
from common.info_class import InfoClass


class PatternExtract:

    @staticmethod
    def miblist_pattern_search(content: str) -> InfoClass:
        '''
        查找miblist的rssi和crc信息
        :param content:
        :return:
        '''
        info_calss = InfoClass()
        # 提取mibrssi
        rssis = re.findall(r'rssi=-\d+\((-?\d+)', content)
        rssi = int(rssis[0]) if rssis else -999999

        # 提取 mibcrc
        mibcrcs = re.findall(r'crc=(\d+)', content)
        mibcrc = int(mibcrcs[0]) if mibcrcs else -999999

        info_calss.ul_dl_type = "dl"
        info_calss.burst_type = 'MIB_LIST'
        info_calss.sub_chan = 'MIB_LIST'
        info_calss.rssi = rssi
        info_calss.crc = mibcrc
        return info_calss

    @staticmethod
    def miblist_info_pattern_search(content: str) -> InfoClass:
        '''
        查找并提取miblist对应的波束号和卫星id信息
        :param content:
        :return:
        '''
        info_calss = InfoClass()
        # 提取mib卫星ID，并转换为十进制数
        mib_statellite_hex = content.split(" ")[3]
        mib_statellite = int(mib_statellite_hex, 16)

        # 提取mib的波束，并转为10进制
        mib_frameoff_hex = content.split(" ")[4]
        # 将16进制字符串转换为二进制
        # decimal_number = int(mib_frameoff_hex, 16)
        binary_string = bytes.fromhex(mib_frameoff_hex)
        mib_frameoff_binary_str = ''.join('{:08b}'.format(byte) for byte in binary_string)
        # 取二进制字符串前6位,并转为10进制
        mib_frameoff = int(mib_frameoff_binary_str[:6], 2)  # 转换为十进制数

        info_calss.satellite = mib_statellite
        info_calss.frameoff = mib_frameoff
        return info_calss

    @staticmethod
    def dl_schedule_patten_search(content: str) -> InfoClass:
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

    @staticmethod
    def ul_schedule_patten_search(content: str) -> InfoClass:
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

    @staticmethod
    def l1c_l1a_rx_data_ind_patten_search(content: str) -> InfoClass:
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

    @staticmethod
    def l1c_l1a_beam_meas_ind_patten_search(content: str) -> InfoClass:
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

        # 提取 V1.0早期的rssi
        # rssi_match = re.findall(r'rssi=-\d+\((-?\d+)', content)
        # 提取 V1.2的早期版本rssi
        # rssi_match = re.findall(r'rssi=(-?\d+)', content)
        #V1.0和V1.2最新版本realRssi（20240802以后的版本）
        rssi_match = re.findall(r'realRssi=(-?\d+)', content)
        rssi = int(rssi_match[0]) if rssi_match else -999999  # 如果未找到，赋值-999999的异常值
        # 提取 sinr
        sinr_match = re.findall(r'SINR=(-?\d+)', content)
        # sinr = int(int(sinr_match[0])/256+0.5) if sinr_match else -999999  # 加0.5四舍五入
        sinr = int(sinr_match[0]) if sinr_match else -999999
        info_calss.ul_dl_type = "dl"
        info_calss.frameoff = frameoff
        info_calss.fn = fn
        info_calss.tsn = tsn
        info_calss.rssi = rssi
        info_calss.sinr = sinr
        return info_calss

    @staticmethod
    def l1a_mac_tx_data_ind_patten_search(content: str) -> InfoClass:
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

    @staticmethod
    def handover_success_pattern_search(handover_number: int,handover_type: str) -> InfoClass:
        '''
        波束切换成功，信息提取
        :param handover_number:
        :return:
        '''
        info_calss = InfoClass()
        info_calss.ul_dl_type = '第'+str(handover_number)+'次切换成功'
        info_calss.burst_type = handover_type
        return info_calss

    @staticmethod
    def handover_faile_pattern_search(handover_number: int,handover_type: str) -> InfoClass:
        '''
        波束切换失败，信息提取
        :param handover_number:
        :return:
        '''
        info_calss = InfoClass()
        info_calss.ul_dl_type = '第'+str(handover_number)+'次切换失败'
        info_calss.burst_type = handover_type
        return info_calss

    @staticmethod
    def satellite_pattern_search(content: str) -> int:
        '''
        卫星id信息提取函数
        :param content:
        :return:
        '''
        satelliteid_match = re.findall(r'satelliteId=(\d+)', content)
        satelliteid = int(satelliteid_match[0]) if satelliteid_match else -999999  # 如果未找到，赋值-999999的异常值
        return satelliteid

    @staticmethod
    def ul_dl_schedule_bandid_pattern_search(content: str):
        '''
        set DL schedule[1]: band 和 set UL schedule[1]: band中的bandid提取函数
        :param content:
        :return:
        '''
        bandid_match = re.findall(r'band\s+(\d+)', content)
        bandid = int(bandid_match[0]) if bandid_match else -999999
        return bandid

    @staticmethod
    def mac_l1a_adjust_t_f_offset_ind_pattern_search(content: str):
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

    @staticmethod
    def ssrinfoxw_pattern_search(content: str):
        '''
        导航电文数据提取函数
        :param content:
        :return:
        '''
        info_calss = InfoClass()
        ssrinfo_match = re.findall(r'SSRINFOXW: 1824,(.+)', content)
        ssrinfo = ssrinfo_match[0] if ssrinfo_match else -999999  # 如果未找到，赋值-999999的异常值
        info_calss.ul_dl_type = "dl"
        info_calss.burst_type = "PMBCH"
        info_calss.sub_chan = "PMBCH_DH"
        info_calss.ssrinfo = ssrinfo
        return info_calss

