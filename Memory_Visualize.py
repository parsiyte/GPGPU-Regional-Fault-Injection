import numpy as np
import matplotlib.pyplot as plt
import sys
import os
# ===========================================================================
#                       Configurations
# ===========================================================================
# Bunu degistir 1
config_path = "./config_files/bicg_cpe_test/"
sys.path.append(config_path)

# Bunu degistir 2
import config4 as conf

# Bunu değiştir 3
# burada klasorleri elle numaraya göre adlandırmak lazım
# bu sdclerin icinde bulunxugu klasordur

folder_number = "4"
executable = conf.executable
mem_dirs = "./SDC_outputs/"+ executable +"/"+ folder_number +"/Memory_outs/"
line_list = "./SDC_outputs/"+ executable +"/"+ folder_number  +"/linelist.txt"


# to make title the line of source code, give path of source(optional)
source_path = ""
golden_path = mem_dirs + "memory_out.txt"
memory_out_path = mem_dirs + "memory_out.txt"


watchlist = conf.memory_watchlist
# ===========================================================================
#                        F
# ===========================================================================
def array2img(array,                     # Numpy array
              directory,                 # Directory to save figure
              name="arr.png",            # Name of saved figure
              title="sample title",      # Title of figure
              reshape=True, show=True, save=True):

    # if array is 1D reshape to make it 2D close to square matrix
    if reshape:
        n = array.shape[0]    # shape of 1D array
        ns = int(np.sqrt(n))  # square root of shape
        while n % ns:
            ns += 1

        array = np.reshape(array, (ns, int(n / ns)))

    if show:
        fig = plt.figure()
        imgplot = plt.imshow(array, animated=True)
        imgplot.set_cmap('nipy_spectral')
        plt.title(title)
        v = np.linspace(0, np.max(array), 10, endpoint=True)
        fig.colorbar(imgplot,  ticks=v)
    if save:
        plt.savefig(directory + "/" + name, bbox_inches='tight', dpi = 300)
        plt.close("all")
    return imgplot


def square_array(array):
    n = array.shape[0]    # shape of 1D array
    ns = int(np.sqrt(n))  # square root of shape
    while n % ns:
        ns += 1
    return np.reshape(array, (ns, int(n / ns)))    


# -----------------------------------------------------------------------------
#                   Load memory data 
# -----------------------------------------------------------------------------

def load_data(path):
    
    with open(path, "r") as myfile:
        data = myfile.readlines()  
    
    array = []   # Keeps array value
    second_array = []
    for text in data:
        text = text.split("{")[1]
        text = text.split("}")[0]
        text = text.split(",")
        array = []
        for num in (text):
            if "repeats" in num:
                    # i.e. 0 repeats 1024 times
                    num = num.split(" ")
                    try:
                        value = float(num[0])     # finds value
                    except:
                        value = float(num[1])     # finds value
                    repeat = int(float(num[-2]))  # finds repeats of value
                    array.extend(repeat * [value])
            else:
                    array.extend([float(num)])
        second_array.append(array)
    return second_array        


def get_diff(path, array, golden, diff, title, name):

    array = square_array(array)
    golden = square_array(golden)
    diff = square_array(diff)
    # coordinates differenct than 0
    temp = np.where(diff != 0)
    Diff_coor = list(zip(temp[0], temp[1]))
    diff_txt = open(path +"/"+ name + ".txt", "w")
    diff_rate = 100*np.divide(diff,golden)
    diff_rate_mean = diff_rate.mean()
    diff_rate_max = diff_rate.max()
    diff_mean = diff.mean()
    diff_max = diff.max()

    for coor in Diff_coor:
        diff_txt.write("-"*50)
        diff_txt.write("\n%s has diff at (%d, %d)"%(title, coor[0], coor[1]))
        diff_txt.write("\ngolden    = %E, \ninjected  = %E\ndiff      = %E \ncorr_rate = %f\n"
              %(golden[coor], array[coor],diff[coor], diff_rate[coor]))
        diff_txt.write("-"*50)
        diff_txt.write("\n")
    diff_txt.write("="*50)
    diff_txt.write("Difference mean and max = %f    %f"%(diff_mean, diff_max))
    diff_txt.write("Difference rate mean and max = %f    %f"%(diff_rate_mean, diff_rate_max))
    diff_txt.close()

# =============================================================================
#                        Memory Visualize
# =============================================================================
# "memory_out.txt"
golden_name ="memory_out.txt"
# -------------------------------------------------------------------------
#                 One-time readed arrays
# -------------------------------------------------------------------------
if source_path != "":
    with open(source_path, "r") as myfile:
        source = myfile.readlines()

with open (line_list, 'r') as f:
    line_lists = f.read()


golden_array = load_data(golden_path)

if "(" in line_lists:
    line_lists = line_lists.replace("'","")
    line_lists = line_lists.replace("(","")
    line_lists = line_lists.replace(")","").split(",")
lines = line_lists[1::2] # Elements starting from 1 iterating by 2 (odd)
watch_indexes = line_lists[0::2] # Elements starting from 0 iterating by 2
# -------------------------------------------------------------------------
#                   Output images Folder Preparation
# -------------------------------------------------------------------------
directory = "Output images"

try:
    os.mkdir(directory)
except:
    print("Output folder exist!")

directory += "/" + executable
try:
    os.mkdir(directory)
except:
    print("Execution folder exist!")

directory += "/" + folder_number   # or date time

try:
    os.mkdir(directory)  
except: 
    print("Folder name exist!")
  
injected_dir = directory + "/Injected/"
diff_dir = directory + "/Diff/"
try:
    os.mkdir(injected_dir)
    os.mkdir(diff_dir)  
except: 
    print("Diff and Injection folders exist!")        



for filename in os.listdir(mem_dirs):
    if golden_name in filename :
        # -------------------------------------------------------------------
        #               DATA load and folder preparations
        # -------------------------------------------------------------------
              
        memory_out_path = mem_dirs + filename
        # memory to img
        injected_array = load_data(memory_out_path)
        injected_dir = directory + "/Injected/"
        diff_dir = directory + "/Diff/"
       
        fault_number  = memory_out_path.split("txt")[1]
        injected_dir += fault_number
        diff_dir += fault_number
        
        try: 
            os.mkdir(injected_dir)
            os.mkdir(diff_dir)     
        except :
            print("folder exist")

        # -------------------------------------------------------------------
        #               Check difference and print outputs
        # -------------------------------------------------------------------
        try:
            for i, index in enumerate(watch_indexes):
                
                # -----------------------------------------------------------
                # Compare both array
                # -----------------------------------------------------------
                arr = np.array(injected_array[i])
                gold = np.array(golden_array[i])
                diff = gold - arr
                
                # -----------------------------------------------------------
                # Title preparation
                # -----------------------------------------------------------
                line_num = lines[int(index)]
                try:
                    listToStr = ' '.join(map(str, watchlist[int(index)]))
                    title =  listToStr
                except:
                    title = ""
                
                if source_path != "":
                    add_line = "\n" + line_num + "\n" + source[int(line_num)-1]
                    title += add_line[:40]
                    title = title.replace("	", "")
                    title = title.replace("\t", "")
            
                # -------------------------------------------------------------
                # Visualize and Save diff and injected arrays
                # -------------------------------------------------------------
                get_diff(diff_dir, arr, gold, diff, title, str(i))
                array2img(arr, injected_dir, title=title, name=conf.executable+
                                          "_inj"+fault_number+"_"+str(i)+".png")
                array2img(abs(diff), diff_dir, title=title, name=conf.executable+
                                         "_diff"+fault_number+"_"+str(i)+".png")
        except Exception as exp:
            print(exp,"FAIL!")
            exit 
        print("{:<17s} is converted!".format(filename))
print("Memory visualization done!")
