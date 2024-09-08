import time

from common.file_class import File
from common.pattern_extract_class import PatternExtract
from common.info_class import InfoClass
from common.search_keyword_enum import SearchKeyword
from common import file_operation


def find_miblist_info(i: int,ps_keywords_contents: list,infoclass_miblist: InfoClass):
    '''
    查找miblist的波束号和卫星id信息
    :param i:
    :param ps_pattern_contents:
    :param infoclass_miblist:
    :return:
    '''
    lines_length = len(ps_keywords_contents)
    # 在后面提取miblist的卫星id和波束号
    k = i + 1
    while k < lines_length and SearchKeyword.MIBLIST.value not in ps_keywords_contents[k] and SearchKeyword.SATELLITE.value not in ps_keywords_contents[k] and SearchKeyword.L1C_L1A_RX_DATA_IND.value not in ps_keywords_contents[k]:
        next_line_miblist = ps_keywords_contents[k]
        if SearchKeyword.MIBLIST_INFO.value in next_line_miblist:
            infoclass_miblist_info = PatternExtract.miblist_info_pattern_search(next_line_miblist)
            infoclass_miblist.satellite = infoclass_miblist_info.satellite
            infoclass_miblist.frameoff = infoclass_miblist_info.frameoff
            break
        k = k + 1


def find_dl_info(i: int,ps_keywords_contents: list,infoclass_dl: InfoClass):
    '''
    查找dl上行相关数据信息并补充更新
    :param i:
    :param ps_keywords_contents:
    :param infoclass_dl:
    :return:
    '''
    lines_length = len(ps_keywords_contents)
    # 在后面提取下行的相关关键词信息,找到下一个tx结束
    k = i + 1
    while k < min(lines_length,i+200) and SearchKeyword.L1A_MAC_TX_DATA_IND.value not in ps_keywords_contents[k]:
        next_line_dl = ps_keywords_contents[k]
        # 下一行提取band值
        if k == i + 1 and SearchKeyword.DL_SCHEDULE_BAND.value in next_line_dl:
            next_line_dl_band = ps_keywords_contents[k]
            bandid = PatternExtract.ul_dl_schedule_bandid_pattern_search(next_line_dl_band)
            infoclass_dl.bandid = bandid

        # 匹配 L1C_L1A_RX_DATA_IND 提取bust_type、sub_chan、frameoff、crc
        if SearchKeyword.L1C_L1A_RX_DATA_IND.value in next_line_dl:
            infoclass_l1c_l1a_rx = PatternExtract.l1c_l1a_rx_data_ind_patten_search(next_line_dl)
            if infoclass_dl.fn == infoclass_l1c_l1a_rx.fn and infoclass_dl.tsn == infoclass_l1c_l1a_rx.tsn and infoclass_dl.bandid == infoclass_l1c_l1a_rx.bandid:
                infoclass_dl.burst_type = infoclass_l1c_l1a_rx.burst_type
                infoclass_dl.sub_chan = infoclass_l1c_l1a_rx.sub_chan
                infoclass_dl.frameoff = infoclass_l1c_l1a_rx.frameoff
                infoclass_dl.crc = infoclass_l1c_l1a_rx.crc

        # 匹配 L1C_L1A_BEAM_MEAS_IND 提取rssi、sinr
        if SearchKeyword.L1C_L1A_BEAM_MEAS_IND.value in next_line_dl:
            infoclass_l1c_l1a_beam_meas = PatternExtract.l1c_l1a_beam_meas_ind_patten_search(next_line_dl)
            if infoclass_dl.fn == infoclass_l1c_l1a_beam_meas.fn and infoclass_dl.tsn == infoclass_l1c_l1a_beam_meas.tsn:
                infoclass_dl.frameoff = infoclass_l1c_l1a_beam_meas.frameoff
                infoclass_dl.rssi = infoclass_l1c_l1a_beam_meas.rssi
                infoclass_dl.sinr = infoclass_l1c_l1a_beam_meas.sinr

        # 匹配 MAC_L1A_ADJUST_T_F_OFFSET_IND 提取 ta、fa、pa
        if infoclass_dl.crc == 0 and SearchKeyword.MAC_L1A_ADJUST_T_F_OFFSET_IND.value in next_line_dl:
            infoclass_t_f_offset = PatternExtract.mac_l1a_adjust_t_f_offset_ind_pattern_search(next_line_dl)
            infoclass_dl.ta = infoclass_t_f_offset.ta
            infoclass_dl.fa = infoclass_t_f_offset.fa
            infoclass_dl.pa = infoclass_t_f_offset.pa
        k = k + 1


def find_ul_info(i: int,ps_keywords_contents: list,infoclass_ul: InfoClass):
    '''
    查找ul下行相关数据信息并补充更新
    :param i:
    :param ps_pattern_contents:
    :param infoclass_ul:
    :return:
    '''
    lines_length = len(ps_keywords_contents)
    # 在后面提取下行的相关关键词信息,找到下一个tx结束
    k = i + 1
    while k < lines_length and SearchKeyword.L1A_MAC_TX_DATA_IND.value not in ps_keywords_contents[k]:
        next_line_ul = ps_keywords_contents[k]
        if SearchKeyword.UL_SCHEDULE.value in next_line_ul:
            infoclass_ul_schedule = PatternExtract.ul_schedule_patten_search(next_line_ul)
            if infoclass_ul.fn == infoclass_ul_schedule.fn and infoclass_ul.tsn == infoclass_ul_schedule.tsn:
                infoclass_ul.caridx = infoclass_ul_schedule.caridx
                infoclass_ul.burst_type = infoclass_ul_schedule.burst_type
                infoclass_ul.sub_chan = infoclass_ul_schedule.sub_chan
                infoclass_ul.crc = infoclass_ul_schedule.crc
        k = k + 1


def ps_data_deal(ps_files: list):
    '''
    数据查找和逻辑处理
    :param ps_files:
    :param pattern_rule:
    :return:
    '''
    psfile_result_list = []  # 存储最终结果：File对象列表
    # 遍历每个ps文件去找到每个ps文件中的所有信息
    for file in ps_files:
        # 获取当前文件对象的文件名称路径
        ps_file_path = file.file_path_name
        print("正在分析文件：")
        print(ps_file_path)
        # 获取该文件中所有符合所有匹配规则的行，做一次初筛，将不需要的以及异常的行数据踢除，减少对异常日志的异常处理，以及提升后续逻辑查找处理的速度
        ps_keywords_contents = file_operation.get_file_keywords_lines(ps_file_path, SearchKeyword.get_ps_search_keywords())
        # 一开始卫星ID，默认为-1
        satellite = -1
        # 波束切换计数器
        handover_number = 0
        lines_length = len(ps_keywords_contents)
        # lines = ["[1970-01-01 08:04:05:302712][Debug][3256376284]:ResLog_PrintfL1aSetDlSchedDesc:471 [RES] set DL schedule[1]: BURST_TYPE_PFCCH,SUB_CHAN_INVALID,CARRIER_TYPE_1,time[5045,16],carIdx(2),reCount(0),curSchedTime(0)","[1970-01-01 08:04:05:302712][Debug][3256376284]:ResLog_PrintfL1aSetDlSchedDesc:471 [RES] set DL schedule[1]: BURST_TYPE_PFCCH,SUB_CHAN_INVALID,CARRIER_TYPE_1,time[5045,16],carIdx(3),reCount(0),curSchedTime(0)"]
        # 如果开始有下行dl数据时，在开始未查找到卫星ID，则先往下获取到第一个开始的卫星ID值
        if satellite == -1:
            satellite = file_operation.find_start_statellite(ps_keywords_contents)

        # 根据关键词查找获取相关信息
        for i,line in enumerate(ps_keywords_contents):
            # 判断并提取卫星ID
            if SearchKeyword.SATELLITE.value in line:
                satellite = PatternExtract.satellite_pattern_search(line)

            # mib list查找
            if SearchKeyword.MIBLIST.value in line:
                infoclass_miblist =PatternExtract.miblist_pattern_search(line)
                # 在miblist后面查找当前mib对应的卫星id和波束号
                find_miblist_info(i, ps_keywords_contents, infoclass_miblist)
                file.info_list.append(infoclass_miblist)

            # 下行数据查找
            elif SearchKeyword.DL_SCHEDULE.value in line:
                infoclass_dl = PatternExtract.dl_schedule_patten_search(line)
                infoclass_dl.satellite = satellite
                # 在dl后面查找当前dl数据的rx、meas、tafapa等数据，并对当前dl数据做信息补充更新
                find_dl_info(i,ps_keywords_contents,infoclass_dl)
                file.info_list.append(infoclass_dl)

            # 上行数据查找
            elif SearchKeyword.L1A_MAC_TX_DATA_IND.value in line:
                infoclass_ul = PatternExtract.l1a_mac_tx_data_ind_patten_search(line)
                infoclass_ul.satellite = satellite
                # 在tx后面查找当前tx数据的ul数据，并对当前tx数据做信息补充更新
                find_ul_info(i,ps_keywords_contents,infoclass_ul)
                file.info_list.append(infoclass_ul)

            # 波束切换查找
            elif SearchKeyword.HANDOVER_START.value in line:
                handover_number = handover_number + 1
                # 出现波束切换开始标志时，一开始默认该切换失败
                infoclass_handover = PatternExtract.handover_faile_pattern_search(handover_number)
                infoclass_handover.satellite = satellite
                k = i + 1
                # 往后查找，如果在下一个波束切换开始前找到波束切换成功标志，则更新该波束切换为成功
                while k < lines_length and SearchKeyword.HANDOVER_START.value not in ps_keywords_contents[k]:
                    next_line_handover = ps_keywords_contents[k]
                    if SearchKeyword.HANDOVER_SUCCESS.value in next_line_handover and "for Rb_Id(1)" in next_line_handover:
                        infoclass_handover_success = PatternExtract.handover_success_pattern_search(handover_number)
                        infoclass_handover.ul_dl_type = infoclass_handover_success.ul_dl_type
                        infoclass_handover.burst_type = infoclass_handover_success.burst_type
                        break
                    k = k + 1
                file.info_list.append(infoclass_handover)
            else:
                continue

        psfile_result_list.append(file)
    return psfile_result_list


if __name__ == '__main__':
    ps_file_paths = file_operation.find_ps_files_list(r"C:\Users\lzc\Desktop\龙兴\20240907库尔勒_0102星_5703圈_移动通信_东芯手持终端\20240907库尔勒_0102星_5703圈_移动通信_东芯手持终端")

    ps_info_result_list = ps_data_deal(ps_file_paths)
    for ps_info_result_itm in ps_info_result_list:
        dsp_file_path = ps_info_result_itm.file_path_name.replace("_ps.dat", "_dsp.dat")
        file_operation.merge_dsp_filter_befor_rssi(dsp_file_path,ps_info_result_itm)
    # File.uptade_dsp_rssi_sinr(ps_info_result_list)
    # .xlsx文件保存，所有文件内容存入一个文件中，每个文件的数据一个sheet工作表
    file_operation.sava_data_xlsx(ps_info_result_list)




