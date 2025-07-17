def fix_file(file_path,file_name,max_peak,min_peak):
    fixed_file= file_name + ".msp"

    r = open(file_path + '\\' + file_name, 'r')#正式读写
    f = open(file_path + '\\' + fixed_file, 'w')
    lines = 'abn '
    while lines:
        lines = r.readline()
        if 'NAME:' in lines.upper():
            while 'Num Peaks' not in lines:
                f.write(lines)
                lines = r.readline()
            lines = r.readline()
            peak_list=[]
            while lines != '\n':
                peak_list.append(lines.strip('\n'))
                lines = r.readline()

            new_peak_list=peak_cal(peak_list,max_peak,min_peak)
            f.write('Num Peaks: '+ str(len(new_peak_list))+'\n')
            for peaks in range(0, len(new_peak_list)):
                f.write(str(round(new_peak_list[peaks][0],5)) + " " + str(round(new_peak_list[peaks][1],5)) +" "+ new_peak_list[peaks][2] + '\n')

            f.write('\n')
    r.close()


def peak_cal(peak_list,max_peak=1000,min_peak=0.1):
    peak_list=peak_list_trans(peak_list, min_peak=min_peak)
    new_peak_count = 0
    new_peak_list = []

    for new_peak in range(len(peak_list)):
        if new_peak == 0:
            new_peak_list.append(list(peak_list[new_peak]))
        elif peak_list[new_peak][0] != peak_list[new_peak - 1][0]:
            new_peak_count += 1
            new_peak_list.append(list(peak_list[new_peak]))
            new_peak_list[-1][3] = new_peak_count
        peak_list[new_peak][3] = new_peak_count

    for peaks in range(len(new_peak_list)):
        overlap_rows = [row for row in peak_list if row[3] == peaks]
        if len(overlap_rows) != 1:
            values = [row[1] for row in overlap_rows]
            peaknames = [row[2] for row in overlap_rows]
            new_peak_list[peaks][1] = value0(values)
            new_peak_list[peaks][2] = peak_name0(peaknames)

    max_value = max(new_peak_list, key=lambda x: x[1])[1]
    for row in new_peak_list:
        row[1] = row[1] / max_value * max_peak

    return new_peak_list

def value0(values):
    values.sort()
    value0 = values[0]
    for value in values:
        value0 = value0 + (value - value0) / 8
    return value0

def peak_name0(peak_names):
    peak_names=list(peak_names)
    peak_name0 = peak_names[0]
    for peak_name in range(1, len(peak_names)):
        peak_name0 = peak_name0[:-1] + '/' + peak_names[peak_name][1:]
    return  peak_name0

def peak_list_trans(peak_list,min_peak=0.1):
    peak_list = [i for i in peak_list if i]
    peak_list = [line.replace('\t', ' ').split(' ', maxsplit=2) for line in peak_list]
    peak_list = [[float(row[0]), float(row[1]), row[2]] for row in peak_list]
    peak_list = [[a, b, c, 0] for a, b, c in peak_list if a > 0 and b > min_peak]
    peak_list.sort(key=lambda x: x[0], reverse=True)
    return peak_list

