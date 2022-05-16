import gdb
import os
import sys
sys.path.append(os.getcwd()) # append current path
# import signal
import common as cm
import config as conf
import time
# =============================================================================
#   Configurations
# =============================================================================
verbose = conf.verbose                              # Log level
executable = conf.executable                        # Path of executable
breakKernelStart = conf.breakKernelStart            # Location of breakpoint
breakConditional = conf.breakConditional            # Breakpoint condition
args = conf.args                                    # Argument list
directory = conf.directory                          # Directory of execution
fault_reg = conf.fault_reg                          # Fault region/reg or memory
use_output_line = conf.use_output_line              # Output analysis
use_memory_analysis = conf.use_memory_analysis      # Memory analysis
memory_output_path = conf.memory_output_path        # Output save informations
memory_watchlist = conf.memory_watchlist            # Variable information list 
breakCount = 0                                      # Count of breakpoint hits
breakX = ""
# =============================================================================
#   Initial Setup
# =============================================================================

if use_memory_analysis:
    memory_out = []
    line_list = []

#if use_output_line:
#    output_line, output_var, output_length = conf.output_info.split(",")

def setup():
    global breakX
    if verbose > 2:
        print('Running GDB from: %s\n' % (gdb.PYTHONDIR))
    
    gdb.execute("set print pretty")
    gdb.execute("set pagination off")
    gdb.execute("set confirm off") # prevent multiple hangs

    if use_memory_analysis or use_output_line:
        gdb.execute("set max-value-size unlimited")
        gdb.execute("set cuda launch_blocking on")        
       
    # gdb.execute("set print thread-events")

    gdb.execute("cd " + directory)
    gdb.execute('file ' + executable)

    if args != "":
        gdb.execute('set args ' + args)
    
    print('\nInjection Setup complete !!\n') 
    info = cm.txt2list(cm.fault_map)
    #print("BREAKNUMBER INFO %s" %(info))
    #print("BREAKNUMBER SET %s" %(info[0]))#info[:3]
    #global breakNumber
    breakX = info[8]
    print("BREAKNUMBER BREAK %s" %(breakX))#info[:3]
    


def register_stop_handler():
    gdb.events.stop.connect(stop_handler)
    gdb.events.exited.connect(exit_handler)
    gdb.events.inferior_call
    # unregister
    # gdb.events.stop.disconnect(stop_handler)
    if verbose > 2:
        print('\nDone setting stop-handler\n')


def exit_handler(event):
    print("=" * 72)
    print("Script completed!")
    print("=" * 72)
    if verbose > 1:
        print('EXIT EVENT: %s' % (event))
    
    if use_memory_analysis:
        #if verbose > 2 :
        #    print("length mem_out = %d"%(len(memory_out)))
        cm.list2txt(memory_out, path=memory_output_path)
        cm.list2txt(line_list, path="linelist.txt")
        # analyser.save_watchlist()

    gdb.execute("q")
    

def stop_handler(event):

    global breakCount, memory_out, line_list, breakKernelStart

    current_line = gdb.execute("info line", to_string=True).split(" ")[1]            
    #if verbose:
#    print("=" * 72)
#    print(" Line %s" %(current_line))
#    print("=" * 72)
    print('EVENT: %s' % (event))
        #fn = event.breakpoints[0]


    #current_th = gdb.execute("cuda thread", to_string=True)
    #print("THREAD %s" %(current_th))
    #current_bl = gdb.execute("cuda block", to_string=True)
    #print("BLOCK %s" %(current_bl))
    
    if (isinstance(event, gdb.BreakpointEvent)):

        if ":" in breakKernelStart: # when breakline is not a number "foo.cu:11"
            breakKernelStart = breakKernelStart.split(":")[1]
            
        if breakConditional != "":
            if breakCount == 0: #the first breakpoint
                #print('First breakpoint')
                #clear_breakpoints()
                #set_breakpoint(breakConditional)
                breakCount = 1
                gdb.execute("b " + breakConditional)

            elif breakCount == 1:

                #print('Second breakpoint')
                #clear_breakpoints()
                #print('Conditional breakpoint ' + fn.condition)
                #print("-" * 72)
                #print("Fault injection at line %s" %(current_line))
                #print("-" * 72)
                fault_injection(cm.fault_map) 
                clear_breakpoints()
                #print("Fault_injection done!")
                
                if use_memory_analysis:
                    analyser.set_breaks()
                  
#                if use_output_line:
#                    set_breakpoint(output_line)             
                breakCount += 1

            elif breakCount > 1:
                # to make sure both case work properly breakcount -1 
                if use_memory_analysis:
                    mem_out, index = analyser.mem_read(current_line)
                    memory_out.extend(mem_out)
                    line_list.extend(index)
                breakCount += 1
                
#                if current_line == output_line and use_output_line:
#                    output = gdb.execute("print " + output_var + "@" + output_length,
#                                         to_string=True)
#                    cm.str2txt(output[6:-2], path = conf.output_name)

        else:
            if breakCount == 0:
                #print("Fault injection at step %d" %(breakNumber))
                #gdb.execute("c")
                clear_breakpoints()
                gdb.execute("stepi " + breakX)
            elif breakCount > 0:
                if use_memory_analysis:
#                    print("-" * 72)
#                    print("Memory reading at line %s" %(current_line))                    
#                    print("-" * 72)
                    mem_out, index = analyser.mem_read(current_line)
                    memory_out.extend(mem_out)
                    line_list.extend(index)
                    #print("Memory reading done!")
                breakCount += 1
                gdb.execute("c")
    elif (isinstance(event, gdb.SignalEvent)):# EVENT: <gdb.SignalEvent object at > -->CRASH
        print("CRASH EVENT")
        #clear_breakpoints()
        gdb.execute("q") 
    elif (isinstance(event, gdb.StopEvent)):#comes here after stepi _IO
        #print("STOP EVENT")
        fault_injection(cm.fault_map)
        if use_memory_analysis:
            analyser.set_breaks()
            
        breakCount += 1
        gdb.execute("c")
    
        


class mem_analysis:
    def __init__(self, memory_watchlist):
        
        self.memory_watchlist = memory_watchlist
        try:
            # spliting 3 coloumns into 3 list
            var_info = list(map(list, zip(*self.memory_watchlist))) 
            
            self.break_points = var_info[0]
            self.var_names = var_info[1]
            self.var_length = var_info[2] 
            
            self.newline = "0" # in case of setting brea
            self.oldline = "0"
            self.break_number = "99"
            self.new_watchlist = []
        except: 
            print("There is an error in watchlist")
            exit       
    
    # Manual memory analysis        
    def mem_read(self, current_line, clear=True, set_end=False):             
        if set_end:
            break_num = self.find_break_num()
            if verbose > 2:
                print(int(self.break_number), int(break_num))

            if int(self.break_number) != int(break_num):
                self.set_endline_break(current_line)
        
        index = [] # index of current line in watchpoint list
        line = [] # current line 
        try:
            for i, b in enumerate(self.break_points):
                if b  == current_line:
                    index.append(i)
                    line.append(current_line)
                #index = [self.break_points.index(current_line)]
        except:
            try:
                # in case of set_end
                index = [self.break_points.index(self.oldline)]
            except:
                print("Error while finding index!")
                return [], []
        
        if verbose:
            print("Current line position in Watchlist = ",index)
        
        mem_out = []  # This list storage memory outputs
        try:
            for i in index:
                tic = time.time()
                # Read memory due to watchlist index
                if verbose > 1:
                    print ("Analyzer try to read %s@%s"%(self.var_names[i],self.var_length[i]))
                mem_out.append(gdb.execute("print " + self.var_names[i] + "@" + 
                                           self.var_length[i], to_string=True))
                if verbose > 1:
                    print ("Memory reading time is %.2fs" %(time.time() - tic))
        except:
            print("Error while memory reading!")
        
        print ("Hit breakpoints are cleaning up...")
        
        if clear:
            # Clear hit breakpoints
            self.clear()
        
        list3 = list(zip(index,line))
        return mem_out, list3





    def set_endline_break(self, current_line):
        if verbose > 2:
            print("Finding end address of function...")
        
        text = gdb.execute("disassemble /m", to_string=True)
        addr = text.split("}")[-1].split("<")[0]
        
        if "=>" in addr:
            addr = addr.split("=>")[1]
        if verbose > 2:
            print("End address of line is" + addr)
        text = gdb.execute("b *" + addr, to_string = True)  
        
        self.break_number = text.split(" ")[1]
        self.newline = str(int(text.split("line ")[1][:-2]))
        
        if self.newline not in self.break_points:
            
            self.break_points.append(self.newline)
            self.oldline = str(int(current_line))       
            try:
                print(self.break_points)
                print(current_line)
                index1 = self.break_points.index(str(int(current_line)))
                print (index1)
                self.var_length.append(self.var_length[index1])
                self.var_names.append(self.var_names[index1])
            except:
                print ("Error while setting new watchline")
        else:
            # bazen art arda eklemeye devam ediyor
            gdb.execute("del " + self.break_number) 

    def find_break_num(self):
        global num
        text = gdb.execute("info break ", to_string=True).split("\n")
        #line = "0"  # initialize line
        for i, tex in enumerate(text): 
            if "already" in tex:  
                # Bu print silinebilir
                if verbose > 2:
                    print(text[i-1])
                num = text[i-1].split(" ")[0]
            else:
                num = "0"
        return num  #, line
    

    def clear(self):   
        text = gdb.execute("info break ", to_string=True).split("\n")

        #line = "0"  # initialize line
        for i, tex in enumerate(text): 
            if "already" in tex:  
                # Bu print silinebilir
                """if verbose > 2:
                    print ("hit breakpoints")
                    print(text[i-1])"""
                #line = text[i-1].split(":")[1]
                num = text[i-1].split(" ")[0]        
                try:
                    gdb.execute("del " +  str(num))
                    print("Breakpoint %s cleaned" %(num))
                except:
                    print("No breakpoint at line")       

    def save_watchlist(self):
            for point, name, length in zip(self.break_points,self.var_names,self.var_length):
                self.new_watchlist.append(point + "," + name + "," + length)        
            cm.list2txt(self.new_watchlist, path="denemee.txt", delimiter="\n")
    
    def set_breaks(self):
        for points in self.break_points:
            gdb.execute("b " + str(points))
        if verbose > 2:
            print("Set_breaks completed")


def cuda_focus(block, thread):
    if verbose > 2:
        print("Focus to block (%s, %s, %s)" % (block[0], block[1], block[2]))
        print("Focus to thread (%s, %s, %s)" % (thread[0], thread[1], thread[2]))
    text = "(" + block[0] + "," + block[1] + "," + block[2] + ")"
    text2 = "(" + thread[0] + "," + thread[1] + "," + thread[2] + ")"
    
    try:
        gdb.execute("cuda block " + text + " thread " + text2)
    except:
        print("Error while focusing\nProgram will terminated")
        gdb.execute("q")
        exit


def fault_injection(fault_map_path): 
    # This print is important for communication with main script    
    info = cm.txt2list(fault_map_path)
    block = info[:3]
    thread = info[3:6]
    variable = info[6]     # it can be register or local,shared ...
    bit = info[7]

    #cuda_focus(block, thread) # focus cuda blocks/threads
    
    # determine old value from string
    if fault_reg == "reg":
        prefix = "$R"
    else:
        prefix = "*(" + fault_reg + " int) "

    old_value = gdb.execute("p " + prefix + variable, to_string=True)
    old_value = old_value.split("= ")[1].replace("\n", "")
    # Changing Bit
    temp = 1 << int(bit)
    gdb.execute("set " + prefix + variable + " ^= " + str(temp))

    # determine new value from string
    new_value = gdb.execute("p " + prefix + variable, to_string=True)
    new_value = new_value.split("= ")[1].replace("\n", "")
    
    # With this print tool communicate fault info with cuda-gdb 
    if verbose > 2:
        print("new value of reg")
        gdb.execute("p " + prefix + variable)
    print("Fault_info = [" + old_value + "," + new_value + "]")



def set_breakpoint(breakpoint):
    try:
        gdb.execute('break ' + str(breakpoint))
        if verbose > 2:
            print('Done setting breakpoint %s\n' % breakpoint)
            print("-" * 72)
    except Exception as ex:
            print('Error while inserting breakpoint %s' % (breakpoint))
            print(ex)


def clear_breakpoints():
    try:
        gdb.execute('del ')
        if verbose > 2:
            print('Cleaning up breakpoints')
    except Exception as ex:
        print('Error while cleaning up breakpoints')
        print(ex)


setup()
set_breakpoint(breakKernelStart)

if use_memory_analysis:
    analyser = mem_analysis(memory_watchlist)
    
register_stop_handler()
# signal.signal(signal.SIGINT, signal_handler)
# print("THREAD RUNNING???" + gdb.InferiorThread.is_running())
gdb.execute("r")
