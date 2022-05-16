import gdb
import sys
import os

sys.path.append(os.getcwd())  # genellestirilecek
import config as conf
# =============================================================================
# Configurations
# =============================================================================
verbose = conf.verbose              # Log level
executable = conf.executable        # Path of executable
breakpoint = conf.breakKernelStart  # Location of breakpoint
args = conf.args                    # Argument list
directory = conf.directory          # Directory of execution
# =============================================================================
# Initial Setup
# =============================================================================
def setup():
    if verbose > 1:
        print('Running GDB from: %s\n' % (gdb.PYTHONDIR))

    gdb.execute("set pagination off")
    gdb.execute("set print pretty")
    gdb.execute("set confirm off")
    # gdb.execute("set print thread-events")
    if verbose > 1:
        print('\nReading gdb env..\n')
        print('\nSetup complete !!\n')
    gdb.execute("cd " + directory)
    gdb.execute('file ' + executable)

    if args != "":
        gdb.execute('set args ' + args)



# def signal_handler(sig, frame):
#    print("SIGNAL DETECTED)


def register_stop_handler():
    gdb.events.stop.connect(stop_handler)
    gdb.events.exited.connect(exit_handler)
    gdb.events.inferior_call
    # unregister
    # gdb.events.stop.disconnect(stop_handler)
    if verbose > 1:
        print('\nDone setting stop-handler\n')


def exit_handler(event):
    if verbose > 1:
        print('EXIT EVENT: %s' % (event))
    gdb.execute("q")


def stop_handler(event):
    if verbose > 1:
        print('EVENT: %s' % (event))
    
    if (isinstance(event, gdb.BreakpointEvent)):
        cuda_info()         # Focus block
        clear_breakpoints() # Clear breakpoint 
        gdb.execute("c")    # Continue
    
    else:
        
        print("CRASH")
        gdb.execute("c")
        # EVENT: <gdb.SignalEvent object at > -->CRASH


def cuda_info():
    if verbose > 2:
        print("CUDA Focus kernel")
        print("-" * 50)

    # bu kisimda hala problem var
    # eger listeinin uzunlugu birse ilki degilse bunu yap
    string = gdb.execute("info cuda threads ", to_string=True)
    try:
        string = string.split(".")[-2]  # There is no newline. Thus, splitted by "." 
        active_blocks = string.split(")")[-3]
        active_threads = string.split(")")[-2]
        active_blocks = active_blocks.split("(")[1]
        active_threads = active_threads.split("(")[1]
    except:
        print ("Exception")
        active_blocks = string.split(")")[2]
        active_threads = string.split(")")[3]
        active_blocks = active_blocks.split("(")[1]
        active_threads = active_threads.split("(")[1]        
    row = [active_blocks, active_threads]
    
    end_line = conf.breakKernelStop
    start_line = breakpoint
    if ":" in start_line:
        start_line = start_line.split(":")[1]
    next_line = str(int(start_line)+1)   

    if ":" in end_line:
        end_line = end_line.split(":")[1]
    if end_line == "":
        print("End line is not defined ",next_line)
        end_line = next_line
    if (int(start_line) > int(end_line)):
        print("end line is smaller than start line next line assumed to be endline")
        end_line = next_line
    # Finds instruction count between current and next_line 
    text_inst = gdb.execute("disassemble /m", to_string=True)
    if (end_line in text_inst):
        text_inst = text_inst.split("=>")[1].split("\n"+ end_line)[0]
    else:
        print ("Line %s is not fount in disassemble content" %(next_line))
        text_inst = text_inst.split("=>")[1].split("\n"+ next_line)[0]    
    text_inst = text_inst.split("\n")
         
    inst = []
    for text in text_inst:
        if (">:\t" in text) and (" " == text[-1]) :
            inst.append(text)


    inst_number = len(inst)
    # This print required for communication with tool 
    print("Profiler_info = [" + row[0] +","+ row[1] + "," + str(inst_number) + "]")



def set_breakpoint():
	try:
		gdb.execute('break ' + breakpoint)
		if verbose > 1:
        		print('Done setting breakpoint %s\n' % breakpoint)
	
	except Exception as ex:
		print('Error inserting breakpoint %s' % (breakpoint))
		print(ex)


def clear_breakpoints():
    try:
        gdb.execute('delete')
        if verbose > 1:
            print('deleted breakpoints')
    except:
        print('Error cleaning breakpoints')

setup()
set_breakpoint()
register_stop_handler()
# signal.signal(signal.SIGINT, signal_handler)
# print("THREAD RUNNING???" + gdb.InferiorThread.is_running())
gdb.execute("r")
