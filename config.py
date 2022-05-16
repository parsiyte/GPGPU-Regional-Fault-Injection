# =============================================================================
#                           CONFIGURATION FILE
# =============================================================================
# Print extra information (optional) 0, 1 ,2 ,3.  3 means print everything
verbose = 3
clean = False               # To clean temp files
Profile_flag = True         # Use profiler
Fault_creator_flag = True   # Use Fault generator 
Fault_injector_flag = True       # Use Fault injector


# To load exist config file 
# Hazir bir config dosyasini eklemek icin en alttaki importu guncellestirin!!!


# =============================================================================
#                 Directory Configurations
# =============================================================================
# Directory of Binary File
directory = "./Samples/Polybench/GRAMSCHM/"
# Binary file
executable = "gramschmidt"

# Arguments, if not neccessary fill with blank string ""
args = ""

# Output results destination of Execution   ****Required for SDC check***
output = "Output.txt"

# Fault injection Results output file 
output_csv = "Fault_injection_results.csv"
# =============================================================================
#                 General Fault Injection Configurations
# =============================================================================
# number of fault
num_fault = 1000

breakKernelStart = "covariance.cu:159"
#breakConditional = "saxpy.cu:29 if i > 5"
breakConditional = ""

# maximum wait time
hang_factor = 20

# Fault injection memory type/ fault region
# reg, const, @global, @local, @shared, @generic
fault_reg = "reg"
# =============================================================================
#               Specific Fault Injection Configurations
# =============================================================================
# In case of specific address space
min_address = "0x140"
max_address = "0x250" # address space interval

# In case of fault with specific block and thread
# Example: "1, 0, 0", otherwise ""
# Coordinates are consequently x y z
block_idx = ""
thread_idx = ""

# In case of fault with specific register,
# Example: register_id = "12" or left it blank
register_id = ""

# maximum register number
max_register = 64

# maximum bit number
max_bit = 32

breakNumber = 0
# =============================================================================
#                 Output Analysis (optional)
# =============================================================================
# if there is not saved output just determine the output info and location
use_output_line = False
#          Output line, Output variable, Output length
output_info = "310, *G_outputFromGpu, 512*512"
output_name = "deneme.txt"
# =============================================================================
#                Memory Analysis Configurations (optional)
# =============================================================================
use_memory_analysis = True

source_path = "covariance.cu"                          # optional
memory_output_path = "memory_out.txt"           # output of the analysis
line_list_path = "linelist.txt"                 # saved memory lines  
memory_watchlist = [["159","*E","512*512"],   # 3rd kernel read E
                    ["160","*F","512*512"],   # 3rd kernel read F
                    ["264","*G_outputFromGpu", "512*512"]] # after 3rd kernel read G


# =============================================================================
#               Load Config File
# =============================================================================
use_load_config = True
config_path = "./config_files/bicg_cpe_test/"


if use_load_config:


    
    import sys
    try:        
        f = open("run_number.txt","r")
        number =  int(f.read())
        f.close()
    except:
        number = 0
        print("config 0")
        
    sys.path.append(config_path)    
    if number == 1:  
        print("config 1")
        from config1 import *
    if number == 2:    
        print("config 2")
        from config2 import *
    if number == 3:    
        print("config 3")
        from config3 import *
    if number == 4:    
        print("config 4")
        from config4 import *
#    if number == 5:    
#        print("config 5")
#        from config5 import *
#    if number == 6:    
#        print("config 6")
#        from config6 import *
#    if number == 7:    
#        print("config 7")
#        from config7 import *
#    if number == 8:    
#        print("config 8")
#        from config8 import *
#    if number == 9:    
#        print("config 9")
#        from config9 import *
#    if number == 10:    
#        print("config 10")
#        from config10 import *
#    if number == 11:    
#        print("config 11")
#        from config11 import *
#    if number == 12:    
#        print("config 12")
#        from config12 import *
#    if number == 13:    
#        print("config 13")
#        from config13 import *
   
    
