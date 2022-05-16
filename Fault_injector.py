import os
import time
import filecmp
from subprocess import Popen, PIPE, TimeoutExpired
import common as cm
import config as conf
from pathlib import Path  # mkdir for log file
from datetime import datetime
# =============================================================================
#                             Configurations
# =============================================================================
from importlib import reload  

def main():
    # list of configurations
    conf_list = [1, 2, 3, 4] 

    for i in conf_list:
        # Controling config.py via run_number.txt
        f = open("run_number.txt", "w")
        f.write(str(i)) 
        f.close()     
        reload(conf)     
        print("Configration %d is loaded" %(i))
        
        # init global variables
        setup()

        if conf.Profile_flag:
            Profiler()
        # Fault map generator
        if conf.Fault_creator_flag:
            Fault_creator()
        if conf.Fault_injector_flag:
            Fault_injector()    
    
    if conf.clean:
        os.system("rm run_number.txt")
# =============================================================================


def Process_execution(command, timeoutx):
    print("Process_execution")
    #proc = Popen(command, stdout=PIPE, stderr=PIPE, close_fds=True)    
    proc = Popen(command, stdout=PIPE, stderr=PIPE)    
    print(proc)
    try:
        out, err = proc.communicate(timeout=timeoutx)
        print("after communicate")
        fault_type = "Masked" 
    except TimeoutExpired:
        proc.kill()
        print("after kill")
        out, err = proc.communicate()
        fault_type = "Hang"
    except Exception as ex:
        print("inside exception")
        print(ex)
    print(proc.returncode)
    return out.decode(), err.decode(), fault_type
# =============================================================================
#                             Setup folders
# =============================================================================
def setup():
    global verbose, num_fault, executable, thread_idx, block_idx, register_id
    global directory, fault_reg, max_step_count
    verbose = conf.verbose
    num_fault = conf.num_fault
    executable = conf.executable
    thread_idx = conf.thread_idx
    block_idx = conf.block_idx
    register_id = conf.register_id
    directory = conf.directory
    fault_reg = conf.fault_reg
    
    try: 
        os.system("rm -r /tmp/cuda-dbg/") # Clear GDB Lock file if exist
    except:
        if verbose: 
            print("No GDB lock file")
    
    try:
        Path(directory + "temp").mkdir(parents=True, exist_ok=True)
    
    except:
        print("Error while creating temp folder")
    cm.init_csv()   # Insert Heading to Summary csv file
# ============================================================================
#                             Profiler
# ============================================================================
#if conf.Profile_flag:
def Profiler():
    print("=" * 72)
    print("\t\t\tGolden Run")
    print("=" * 72)
    
    tic = time.time()
    Profiler_text = os.popen("cuda-gdb -x Profiler_GDB.py").read()
    golden_time = time.time() - tic
    
    if verbose > 1:
        print (Profiler_text)    
    try:    
        # Collect profiling informations
        info = Profiler_text.split("Profiler_info = [")[1].split("]")[0]
        info = info.split(",") 
        info.append(golden_time)    
    except Exception as ex:
        print("There is an error in profiler phase")
        print(ex)
        exit
        
    if verbose:
        print("Profiling Completed")
        print("Profile time = %f" % (golden_time))
        print('-' * 40)
        print('{:^14s}{:^14s}Inst' .format(*cm.title))
        print('-' * 40)
        print('({:<3s},{:<3s},{:<1s})    ({:<3s},{:<3s},{:<1s})  {:>3s}'.format(*info[:-1]))
    cm.list2txt(info,path = directory + "golden_info.txt")
    # profiling infoyu yazdır
    os.rename(directory + conf.output, directory + cm.output_golden)  # keep golden out
    print("Profiling ok")

# =============================================================================
#                             FAULT_CREATOR
# =============================================================================
#if conf.Fault_creator_flag:
def Fault_creator():
    print("=" * 72)
    print("\t\t\tFault Map Generator")
    print("=" * 72)
   
    
    
    info = cm.txt2list(path = directory + "golden_info.txt")
    fault_location = []
    for i in range(num_fault):
        if block_idx == "":
            # Block number higher than block idx. maximum limit is decreased by 1
            block_x = cm.rand_uniform(info[0])
            block_y = cm.rand_uniform(info[1])
            block_z = cm.rand_uniform(info[2])
        else :
            block_id = block_idx.split(",")
            block_x = int(block_id[0])
            block_y = int(block_id[1])
            block_z = int(block_id[2])
        
        if thread_idx == "":
            thread_x = cm.rand_uniform(info[3])
            thread_y = cm.rand_uniform(info[4])
            thread_z = cm.rand_uniform(info[5])
        else:
            thread_id = thread_idx.split(",")
            thread_x = int(thread_id[0])
            thread_y = int(thread_id[1])
            thread_z = int(thread_id[2])
        bit = cm.rand_uniform(conf.max_bit - 1) 
        inst_num = cm.rand_uniform(info[6])
    
        if fault_reg == "reg":
            if register_id == "":
                register = cm.rand_uniform(conf.max_register - 1)
            else:
                register = int(register_id)
            fault_location.append([block_x, block_y, block_z, thread_x,
                                   thread_y, thread_z, register, bit, inst_num])
        else:
            address = cm.rand_uniform(mini = int(conf.min_address, 16),
                                       num = int(conf.max_address, 16))
        
            fault_location.append([block_x, block_y, block_z, thread_x,
                                   thread_y, thread_z, hex(address), bit, inst_num])
    cm.list2csv(fault_location) # write fault informations to harddisc
    
    print("Fault Map generating completed")


# =============================================================================
#                            FAULT INJECTOR
# =============================================================================
#if conf.Fault_injector:      
def Fault_injector():
    print("=" * 72)
    print("\t\t\tFault injection")
    print("=" * 72)
    # -------------------------------------------------------------------------
    #               Storage SDC outputs and etc
    # -------------------------------------------------------------------------
    # to copy a masked mem_output once 
    print(str(num_fault) + " fault will be injected on " + conf.executable)     
    SDC_dir = "SDC_outputs"
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y-%H-%M-%S")

    print("-" * 40)  
    if verbose > 1:  
        print("SDC folders are preparing...")
    try:
        os.mkdir(SDC_dir)
    except:
        if verbose > 1: 
            print("Output folder already exist!")
    
    SDC_dir += "/" + conf.executable
    try:
        os.mkdir(SDC_dir)
    except:
        if verbose > 1: 
            print("Execution folder exist")
    
    SDC_dir += "/" + date_time
    os.mkdir(SDC_dir)
    
    try:
        os.mkdir(SDC_dir + "/Outputs")
        if conf.use_memory_analysis:
        	os.mkdir(SDC_dir + "/Memory_outs")
    except:
        if verbose > 1: 
            print("Folders already exist!")
    SDC_out_dir = SDC_dir + "/Outputs/"
    if conf.use_memory_analysis:
    	SDC_mem_dir = SDC_dir + "/Memory_outs/"
    print("Preparation is done!")
    print("-" * 40)
    
    
    # -------------------------------------------------------------------------
    #               Fault injector setup & run
    # -------------------------------------------------------------------------        
    fault_map = cm.csv2list() # communication with GDB script
    
    # To calculate maximun wait time.
    info = cm.txt2list(path = directory + "golden_info.txt")
    golden_time = float(info[-1])

    # Check Hang condition 
    max_wait_time =  golden_time * conf.hang_factor  # Max wait time for hang cond.
    max_wait_time = int(max_wait_time + 1)        
    print ("Maximum wait time is %ds"%max_wait_time)
    # initialize counters
    sdc_count = 0
    hang_count = 0
    crash_count = 0

    Results = [] # The list that keeps faults results
    global output_text, err  # for spyder var. explorer
    for i in range(num_fault):
        cm.list2txt(fault_map[i])     # for communication with cuda-gdb


        # Execution of script
        tic = time.time()

        output_text, err, fault_type = Process_execution(["cuda-gdb", "-x",
                                       "Fault_injector_GDB.py"], max_wait_time)
                                       
        print("Return from Fault_injector_GDB")                                       
        
        fault_time = time.time() - tic   
        
        if verbose > 2:
        	print(output_text)
        if i == 0:
            print("Fault Injection time = %fs" % (fault_time))

    
        if fault_time >= max_wait_time :
            hang_count += 1
            fault_type = "Hang"
            print("Hang")
            
        elif "CRASH" in output_text: # or (err != "" and "warning" not in err):
            fault_type = 'Crash'
            crash_count += 1
            print("Crash")
            
        # Check SDC condition  
        # Compare the files, returning True if they seem equal, False otherwise.
        elif filecmp.cmp(directory + conf.output, directory + cm.output_golden) == False :
            fault_type = 'SDC'
            sdc_count += 1
            print("SDC")
            
            # if SDC, save get a copy of the output file (to compare criticality etc)
            os.system("cp " + (directory + conf.output) + " " + (SDC_out_dir + 
                                                         conf.output + str(i)))
            
            if conf.use_memory_analysis:                
                os.system("cp " + (directory + conf.memory_output_path) +" "+
                                (SDC_mem_dir + conf.memory_output_path + str(i)))
                      
        
        # Collect injection information
        try:

            try:
                # Read fault injection info from gdb output
                values = output_text.split("Fault_info = [")[1].split("]")[0]
                values = values.split(",")
                blocks = output_text.split(", block (")[1].split("), thread (" )[0]
                threads = output_text.split(", thread (")[1].split("), device")[0]
                blocks = blocks.split(",")
                threads = threads.split(",")
                
                Results.append(blocks + threads +fault_map[i][-3:] + values + [fault_type])
            except:
                # No fault information content in output of gdb
                values = [fault_type, fault_type]
                Results.append(fault_map[i] + values + [fault_type])
            # Print and save
            #print(Results)
            #print(values)
            #print(Results[-1])
            if verbose:
                if i == 0:  # Print title of columns
                    print('-' * 72)
                    print('{:<3s}{:^12s}{:^12s}{:<10s}{:<4s}{:<12s}{:<12s}{:<7s}{:<7s}'
                                                      .format("#",*cm.title))
                print('-' * 72)  
                # Results of iteration
                print('{:<4d}({:<3s} {:<2s} {:>1s})  ({:<3s} {:<3s} {:<1s}) {:^10s}{:^3s}{:^12s}{:^12s}{:^7s}{:^7s}'
                                                    .format(i, *Results[-1]))
            cm.write_row_csv(Results[-1])  # write row to csv

        except Exception as ex:

            print("There is an error in injection phase")
            print(ex)
            #exit
        print("%d completed" %(i)) 
        #time.sleep(3) # Sleep for 3 seconds
    # =======================================================================
    # Fault Injection Completed
    # =======================================================================
    count_masked = num_fault - sdc_count - crash_count - hang_count
    print("\nFault injection Completed")
    print("In %d Fault injection, %d SDC, %d Crash, %d Hang, and %d masked"
          %(num_fault, sdc_count, crash_count, hang_count, count_masked))
    print("The detailed result can be found in %s\n" %(conf.output_csv))
 
    os.system("cp " + (directory + conf.output_csv) + " " +
                                (SDC_dir + "/" + conf.output_csv ))
    os.system("cp " + (directory + conf.line_list_path) + " " +
                                (SDC_dir + "/" + conf.line_list_path ))

    if conf.clean:  
        try:
            os.system("rm -r " + directory + "temp")
            os.system("rm " + directory + cm.output_golden)
            os.system("rm " + directory + conf.memory_output_path)
        except:
            print("temp directory does not exist")



if __name__ == "__main__":
    main()
