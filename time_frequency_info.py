import os
import re
import pprint
from prettytable import PrettyTable


def main():
    filepath = input("请输入待分析日志路径：")
    while filepath != 'q':
        if os.path.isdir(filepath) or os.path.isfile(filepath):
            psfile_list = get_all_psfile(filepath)
        else:
            psfile_list = get_all_psfile("/")

        for i, psfile in enumerate(psfile_list):
            fp = open(psfile)
            lines = fp.readlines()
            fp.close()

            print("*****{}*****\n".format(psfile))
            tf_info = get_time_frequency_info(lines)
            table = PrettyTable(['UE', 'satellite', 'start_fn', 'end_fn', 'tsn', 'caridx', 'beamid', 'bandid'])
            [table.add_row(tf_info[i]) for i in range(len(tf_info))]
            print(table)

        filepath = input("\n继续输入或点击'q'退出：")

    exit()


def get_time_frequency_info(lines):
    tf_info_list = []
    ueid = 'None'
    satelliteid = 'None'
    # fn = 'None'
    # tsn = 'None'
    # beamid = 'None'
    # bandid = 'None'
    for i, line in enumerate(lines):
        if "Imsi(15)" in line:
            ueid = get_ueid(lines, i)

        elif "satelliteId" in line:
            match = re.search(r"satelliteId=(\d+)", line)
            if match:
                satid = match.group(1)
                satelliteid = get_satellite(satid)

        elif "MAC_L1A_TX_DATA_REQ (TRANS_CHAN_DCH" in line:
            match = re.search(r"fn=(\d+),tsn=(\d+),beamId=(\d+),bandId=(\d+)", line)
            if match:
                fn, tsn, beamid, bandid = match.groups()
                caridx = get_caridx(lines, i)
                real_tsn = int(int(tsn) / 8) if int(tsn) > 4 else int(tsn)
                if len(tf_info_list) == 0:
                    tf_info_list.append([ueid, satelliteid, fn, 0, real_tsn, caridx, beamid, bandid])
                elif beamid == tf_info_list[-1][6]:
                    tf_info_list[-1][3] = fn
                elif beamid != tf_info_list[-1][6]:
                    tf_info_list.append([ueid, satelliteid, fn, 0, real_tsn, caridx, beamid, bandid])
                else:
                    continue
    # check
    for row in range(max(0, len(tf_info_list) - 1)):
        if tf_info_list[row][3] == 0:
            tf_info_list[row][3] = "ERROR"

    return tf_info_list


def get_all_psfile(path):
    path_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if (file not in path_list) and file.endswith("ps.dat"):
                file_path = os.path.join(root, file)
                path_list.append(file_path)

    return path_list


def get_caridx(lines, index):
    caridx = 'None'
    for i, line in enumerate(lines[index:min(index + 200, len(lines))]):
        if "set UL schedule[1]" in line:
            match = re.search(r"carIdx\((\d+)\)", line)
            if match:
                caridx = match.group(1)
                break

    return caridx


def get_ueid(lines, index):
    ueid = 'None'
    for i, line in enumerate(lines[index:min(index + 30, len(lines))]):
        if re.search(r'\b([0-9a-z]{2}\s){14}[0-9a-z]{2}\b', line):
            imsi = re.search(r'\b([0-9a-z]{2}\s){14}[0-9a-z]{2}\b', line).group()
            ueid = "10" + imsi[-4] + imsi[-1]

    return ueid


def get_satellite(satid):
    satelliteid = "None"
    if satid == "1":
        satelliteid = "01"
    elif satid == "2":
        satelliteid = "02"
    elif satid == "19":
        satelliteid = "04"

    return satelliteid


if __name__ == '__main__':
    main()
