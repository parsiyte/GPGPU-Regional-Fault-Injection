# GPU-FI
FTGPGPU - Hardware Fault Tolerance Analysis for General Purpose Graphics Processor Unit Applications
### Config
Configrations can be found in config.py
### Configration example
```python
# Print extra information (optional)
verbose = False

"""
    Injection Informations
"""
# Directory of Binary File
directory = "./Samples/SAXPY/"

# Binary file
executable = "saxpyG"

# Arguments, if not neccessary fill blank string ""
args = ""

# number of fault
num_fault = 10

# list of breakpoints
breakpoints = ["saxpy.cu:29 if i < 5"] 

# Output Results destination of Execution   ****Required for SDC check***
output = "Output.txt"

"""
    Spesific Fault Injection
"""

# In case of fault with spesific block and thread  "1, 0, 0", otherwise ""
#  Coordinates are consequently x y z 
block_idx = ""
thread_idx = ""

# In case of fault with spesific registers, EX register_id = "12"
register_id = ""

# maximum registers number
#max_register = 256
max_register = 64

# maximum bit number
max_bit = 32

"""
    Others
"""
# Fault injection Results output file 
output_csv = "Fault_injection_results.csv"

# maximum wait time
hang_factor = 20
```
# Run
To run application;
```sh
$ python3 Fault_injector.py
```
# Notes for users
- Registers number must be filled manually default **256**. It can be found in Profiler.py as **active_registers**
- Execution must give output result as a text file and it must be specified in config.py. 

# To do list
- [X] SDC check script
- [X] Add kill script in Hang Condition
- [X] Find Maximum register number
- [X] Try with different examples
- [X] Make optimizations 
- [X] Convert program into 3-step Injector
- [X] Add conditional Breakpoints
- [X] Prepare Config File
