import time
import file_deal
from pattern_rule_class import PatternRule
from info_class import InfoClass


def find_start_statellite(pattern_rule: PatternRule,contents: str) -> int:
    '''
    查找文件中第一个出现的最开始的卫星id
    :param pattern_rule:
    :param contents:
    :return:
    '''
    # 查找一开始的卫星ID初始值
    for i, statellite_line in enumerate(contents):
        if pattern_rule.satellite_pattern in statellite_line:
            satellite = pattern_rule.satellite_pattern_search(statellite_line)
            return satellite
        else:
            continue


def find_dl_info(i: int,ps_pattern_contents: list,infoclass_dl: InfoClass):
    '''
    查找dl上行相关数据信息并补充更新
    :param i:
    :param ps_pattern_contents:
    :param infoclass_dl:
    :return:
    '''
    lines_length = len(ps_pattern_contents)
    # 在后面提取下行的相关关键词信息,找到下一个tx结束
    k = i + 1
    while k < lines_length and pattern_rule.l1a_mac_tx_data_ind_pattern not in ps_pattern_contents[k]:
        next_line_dl = ps_pattern_contents[k]
        # 下一行提取band值
        if k == i + 1 and pattern_rule.dl_schedule_band_pattern in next_line_dl:
            next_line_dl_band = ps_pattern_contents[k]
            bandid = pattern_rule.ul_dl_schedule_bandid_pattern_search(next_line_dl_band)
            infoclass_dl.bandid = bandid

        # 匹配 L1C_L1A_RX_DATA_IND 提取bust_type、sub_chan、frameoff、crc
        if pattern_rule.l1c_l1a_rx_data_ind_pattern in next_line_dl:
            infoclass_l1c_l1a_rx = pattern_rule.l1c_l1a_rx_data_ind_patten_search(next_line_dl)
            if infoclass_dl.fn == infoclass_l1c_l1a_rx.fn and infoclass_dl.tsn == infoclass_l1c_l1a_rx.tsn and infoclass_dl.bandid == infoclass_l1c_l1a_rx.bandid:
                infoclass_dl.burst_type = infoclass_l1c_l1a_rx.burst_type
                infoclass_dl.sub_chan = infoclass_l1c_l1a_rx.sub_chan
                infoclass_dl.frameoff = infoclass_l1c_l1a_rx.frameoff
                infoclass_dl.crc = infoclass_l1c_l1a_rx.crc

        # 匹配 L1C_L1A_BEAM_MEAS_IND 提取rssi、sinr
        if pattern_rule.l1c_l1a_beam_meas_ind_pattern in next_line_dl:
            infoclass_l1c_l1a_beam_meas = pattern_rule.l1c_l1a_beam_meas_ind_patten_search(next_line_dl)
            if infoclass_dl.fn == infoclass_l1c_l1a_beam_meas.fn and infoclass_dl.tsn == infoclass_l1c_l1a_beam_meas.tsn:
                infoclass_dl.frameoff = infoclass_l1c_l1a_beam_meas.frameoff
                infoclass_dl.rssi = infoclass_l1c_l1a_beam_meas.rssi
                infoclass_dl.sinr = infoclass_l1c_l1a_beam_meas.sinr

        # 匹配 MAC_L1A_ADJUST_T_F_OFFSET_IND 提取 ta、fa、pa
        if infoclass_dl.crc == 0 and pattern_rule.mac_l1a_adjust_t_f_offset_ind_pattern in next_line_dl:
            infoclass_t_f_offset = pattern_rule.mac_l1a_adjust_t_f_offset_ind_pattern_search(next_line_dl)
            infoclass_dl.ta = infoclass_t_f_offset.ta
            infoclass_dl.fa = infoclass_t_f_offset.fa
            infoclass_dl.pa = infoclass_t_f_offset.pa
        k = k + 1


def find_ul_info(i: int,ps_pattern_contents: list,infoclass_ul: InfoClass):
    '''
    查找ul下行相关数据信息并补充更新
    :param i:
    :param ps_pattern_contents:
    :param infoclass_ul:
    :return:
    '''
    lines_length = len(ps_pattern_contents)
    # 在后面提取下行的相关关键词信息,找到下一个tx结束
    k = i + 1
    while k < lines_length and pattern_rule.l1a_mac_tx_data_ind_pattern not in ps_pattern_contents[k]:
        next_line_ul = ps_pattern_contents[k]
        if pattern_rule.ul_schedule_pattern in next_line_ul:
            infoclass_ul_schedule = pattern_rule.ul_schedule_patten_search(next_line_ul)
            if infoclass_ul.fn == infoclass_ul_schedule.fn and infoclass_ul.tsn == infoclass_ul_schedule.tsn:
                infoclass_ul.caridx = infoclass_ul_schedule.caridx
                infoclass_ul.burst_type = infoclass_ul_schedule.burst_type
                infoclass_ul.sub_chan = infoclass_ul_schedule.sub_chan
                infoclass_ul.crc = infoclass_ul_schedule.crc
        k = k + 1


def data_deal(ps_files: list, pattern_rule: PatternRule):
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
        # 获取该文件中所有符合所有匹配规则的行，做一次初筛，将不需要的行数据踢除，提升后续逻辑查找处理的速度
        ps_pattern_contents = file_deal.get_ps_pattern_info(ps_file_path,pattern_rule.get_all_info())
        # 一开始卫星ID，默认为-1
        satellite = -1
        # 波束切换计数器
        handover_number = 0
        lines_length = len(ps_pattern_contents)
        # lines = ["[1970-01-01 08:04:05:302712][Debug][3256376284]:ResLog_PrintfL1aSetDlSchedDesc:471 [RES] set DL schedule[1]: BURST_TYPE_PFCCH,SUB_CHAN_INVALID,CARRIER_TYPE_1,time[5045,16],carIdx(2),reCount(0),curSchedTime(0)","[1970-01-01 08:04:05:302712][Debug][3256376284]:ResLog_PrintfL1aSetDlSchedDesc:471 [RES] set DL schedule[1]: BURST_TYPE_PFCCH,SUB_CHAN_INVALID,CARRIER_TYPE_1,time[5045,16],carIdx(3),reCount(0),curSchedTime(0)"]
        # 如果开始有下行dl数据时，在开始未查找到卫星ID，则先往下获取到第一个开始的卫星ID值
        if satellite == -1:
            satellite = find_start_statellite(pattern_rule,ps_pattern_contents)

        # 根据关键词查找获取相关信息
        for i,line in enumerate(ps_pattern_contents):
            # 判断并提取卫星ID
            if pattern_rule.satellite_pattern in line:
                satellite = pattern_rule.satellite_pattern_search(line)
            # 下行数据查找
            if pattern_rule.dl_schedule_pattern in line:
                infoclass_dl = pattern_rule.dl_schedule_patten_search(line)
                infoclass_dl.satellite = satellite
                # infoclass_dl = pattern_rule.dl_schedule_patten_search(line)
                # infoclass_dl.satellite = satellite
                # # 在后面提取下行的相关关键词信息,找到下一个tx结束
                # k = i + 1
                # while k < lines_length and pattern_rule.l1a_mac_tx_data_ind_pattern not in ps_pattern_contents[k]:
                #     next_line_dl = ps_pattern_contents[k]
                #     # 下一行提取band值
                #     if k == i+1 and pattern_rule.dl_schedule_band_pattern in next_line_dl:
                #         next_line_dl_band = ps_pattern_contents[k]
                #         bandid = pattern_rule.ul_dl_schedule_bandid_pattern_search(next_line_dl_band)
                #         infoclass_dl.bandid = bandid
                #
                #     # 匹配 L1C_L1A_RX_DATA_IND 提取bust_type、sub_chan、frameoff、crc
                #     if pattern_rule.l1c_l1a_rx_data_ind_pattern in next_line_dl:
                #         infoclass_l1c_l1a_rx = pattern_rule.l1c_l1a_rx_data_ind_patten_search(next_line_dl)
                #         if infoclass_dl.fn == infoclass_l1c_l1a_rx.fn and infoclass_dl.tsn == infoclass_l1c_l1a_rx.tsn and infoclass_dl.bandid == infoclass_l1c_l1a_rx.bandid:
                #             infoclass_dl.burst_type = infoclass_l1c_l1a_rx.burst_type
                #             infoclass_dl.sub_chan = infoclass_l1c_l1a_rx.sub_chan
                #             infoclass_dl.frameoff = infoclass_l1c_l1a_rx.frameoff
                #             infoclass_dl.crc = infoclass_l1c_l1a_rx.crc
                #
                #     # 匹配 L1C_L1A_BEAM_MEAS_IND 提取rssi、sinr
                #     if pattern_rule.l1c_l1a_beam_meas_ind_pattern in next_line_dl:
                #         infoclass_l1c_l1a_beam_meas = pattern_rule.l1c_l1a_beam_meas_ind_patten_search(next_line_dl)
                #         if infoclass_dl.fn == infoclass_l1c_l1a_beam_meas.fn and infoclass_dl.tsn == infoclass_l1c_l1a_beam_meas.tsn:
                #             infoclass_dl.frameoff = infoclass_l1c_l1a_beam_meas.frameoff
                #             infoclass_dl.rssi = infoclass_l1c_l1a_beam_meas.rssi
                #             infoclass_dl.sinr = infoclass_l1c_l1a_beam_meas.sinr
                #
                #     # 匹配 MAC_L1A_ADJUST_T_F_OFFSET_IND 提取 ta、fa、pa
                #     if infoclass_dl.crc == 0 and pattern_rule.mac_l1a_adjust_t_f_offset_ind_pattern in next_line_dl:
                #         infoclass_t_f_offset = pattern_rule.mac_l1a_adjust_t_f_offset_ind_pattern_search(next_line_dl)
                #         infoclass_dl.ta = infoclass_t_f_offset.ta
                #         infoclass_dl.fa = infoclass_t_f_offset.fa
                #         infoclass_dl.pa = infoclass_t_f_offset.pa
                #     k = k+1
                # 在dl后面查找当前dl数据的rx、meas、tafapa等数据，并对当前dl数据做信息补充更新
                find_dl_info(i,ps_pattern_contents,infoclass_dl)
                file.info_list.append(infoclass_dl)

            # 上行数据查找
            elif pattern_rule.l1a_mac_tx_data_ind_pattern in line:
                infoclass_ul = pattern_rule.l1a_mac_tx_data_ind_patten_search(line)
                infoclass_ul.satellite = satellite
                # # 在后面提取下行的相关关键词信息,找到下一个tx结束
                # k = i + 1
                # while k < lines_length and pattern_rule.l1a_mac_tx_data_ind_pattern not in ps_pattern_contents[k]:
                #     next_line_ul = ps_pattern_contents[k]
                #     if pattern_rule.ul_schedule_pattern in next_line_ul:
                #         infoclass_ul_schedule = pattern_rule.ul_schedule_patten_search(next_line_ul)
                #         if infoclass_ul.fn == infoclass_ul_schedule.fn and infoclass_ul.tsn == infoclass_ul_schedule.tsn:
                #             infoclass_ul.caridx = infoclass_ul_schedule.caridx
                #             infoclass_ul.burst_type = infoclass_ul_schedule.burst_type
                #             infoclass_ul.sub_chan = infoclass_ul_schedule.sub_chan
                #             infoclass_ul.crc = infoclass_ul_schedule.crc
                #     k = k+1
                # 在tx后面查找当前tx数据的ul数据，并对当前tx数据做信息补充更新
                find_ul_info(i,ps_pattern_contents,infoclass_ul)
                file.info_list.append(infoclass_ul)

            # 波束切换查找
            elif pattern_rule.handover_start_pattern in line:
                handover_number = handover_number + 1
                # 出现波束切换开始标志时，一开始默认该切换失败
                infoclass_handover = pattern_rule.handover_faile_pattern_search(handover_number)
                k = i + 1
                # 往后查找，如果在下一个波束切换开始前找到波束切换成功标志，则更新该波束切换为成功
                while k < lines_length and pattern_rule.handover_start_pattern not in ps_pattern_contents[k]:
                    next_line_handover = ps_pattern_contents[k]
                    if pattern_rule.handover_success_pattern in next_line_handover:
                        infoclass_handover_success = pattern_rule.handover_success_pattern_search(handover_number)
                        infoclass_handover.ul_dl_type = infoclass_handover_success.ul_dl_type
                        infoclass_handover.burst_type = infoclass_handover_success.burst_type
                        break
                    k = k + 1
                file.info_list.append(infoclass_handover)
            else:
                continue

        psfile_result_list.append(file)
        file_deal.close_file_cache()
    return psfile_result_list


if __name__ == '__main__':
    time1 = time.time()
    ps_file_paths = file_deal.find_ps_files_list(r"D:\龙兴\05 在轨测试日志\总日志\佳木斯\20240406-下午-佳木斯-04星-1699圈次-移动通信-东芯\20240406-下午-佳木斯-04星-1699圈次-移动通信-东芯")
    pattern_rule = PatternRule()
    ps_info_result_list = data_deal(ps_file_paths, pattern_rule)
    file_deal.uptade_dsp_rssi_sinr(ps_info_result_list)
    # .xlsx文件保存，所有文件内容存入一个文件中，每个文件的数据一个sheet工作表
    file_deal.sava_data_xlsx(ps_info_result_list)
    time2 = time.time()
    print(time2 - time1)




