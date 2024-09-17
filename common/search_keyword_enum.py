#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from enum import Enum

'''
@Project ：hand_tti
@File    ：ps_search_keyword_enum_class
@Author  ：lzc
@Date    ：2024/9/7
@Description :
'''


class SearchKeyword(Enum):
    # mib list查找
    MIBLIST = '[L1A_Rx] MIB list'
    # _MIBLIST_INFO = 'L1aLog_printfL1aRecvL1cBeamSearchInd:1047 0a'
    MIBLIST_INFO = 'L1aLog_printfL1aRecvL1cBeamSearchInd:1324 0a'

    # 下行相关提取关键字
    SATELLITE = 'Beam: satelliteId'
    DL_SCHEDULE = 'set DL schedule[1]: BURST_TYPE'
    DL_SCHEDULE_BAND = 'set DL schedule[1]: band'
    L1C_L1A_RX_DATA_IND = 'L1C_L1A_RX_DATA_IND'
    L1C_L1A_BEAM_MEAS_IND = 'L1C_L1A_BEAM_MEAS_IND'
    MAC_L1A_ADJUST_T_F_OFFSET_IND = 'MAC_L1A_ADJUST_T_F_OFFSET_IND'

    # 上行相关提取关键字
    L1A_MAC_TX_DATA_IND = 'L1A_MAC_TX_DATA_IND'
    UL_SCHEDULE = 'set UL schedule[1]: BURST_TYPE'
    UL_SCHEDULE_BAND = 'set UL schedule[1]: band'

    # 波速切换提取关键字
    # HANDOVER_START = 'RRC_L1A_HO_CONFIG_REQ'
    HANDOVER_START = 'Send ConnReConfig Complete For Handover'
    HANDOVER_SUCCESS = '[RLC] ACK'

    # 导航电文关键词
    SSRINFO = 'SSRINFOXW: 1824,'

    # 物理层日志查找关键词
    PHY_DL_BURST_SCHE = "dl burst sche"
    PHY_DLBURSTAGCAVE = "dlBurstAgcAve"

    @staticmethod
    def get_ps_search_keywords():
        return [member.value for member in SearchKeyword.__members__.values() if not member.name.startswith('PHY_')]

    @staticmethod
    def get_dsp_search_keywords():
        return [member.value for member in SearchKeyword.__members__.values() if member.name.startswith('PHY_')]

