import csv
import config as conf
from random import uniform

# temporary files directories
fault_map = "temp/fault_map.txt"
output_golden = conf.output + "_gold"
directory = conf.directory
title = ['Block', 'Thread', 'reg/addr', 'Bit', 'Inst', 'Old Value','New Value', 'Type']
                                                            
# =============================================================================
#                       DATA I/O
# =============================================================================
def init_csv():
    with open(directory + conf.output_csv, mode='w') as csv_file:
        csv_file = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file.writerow(title)

 
def write_row_csv(row, path = directory + conf.output_csv):
    with open(path, mode='a') as csv_file:
        csv_file = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        new_row = [row[0:3], row[3:6]] + row[6:] 
        csv_file.writerow(new_row)


def list2csv(data, path = directory + "fault_map.csv"):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def csv2list(path = directory + "fault_map.csv"):
    with open(path) as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def txt2list(path):
    with open (path, 'r') as f:
        results = f.read().split(",")
    return results


def list2txt(row, path = directory + fault_map, delimiter = ","):
    f = open(path, "w")
    f.write(str(row[0]))  # for avoiding extra comma first index wrote manually
    for r in row[1:]:
        f.write(delimiter + str(r))  # write list to file
    f.close()

def str2txt(data, path = directory + fault_map):
    f = open(path, "w")
    f.write(str(data))
    f.close()


def rand_uniform(num, mini = 0, decrease = 0):
    rand = uniform(int(mini), int(num) - decrease)
    if rand > int(rand) + 0.5:
         return int(rand) + 1
    else :
        return int(rand)
# =============================================================================
#                               MEMORY ANALYSIS  
# =============================================================================