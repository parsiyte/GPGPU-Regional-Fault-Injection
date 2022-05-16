# =============================================================================
#                           CONFIGURATION FILE
# =============================================================================
# Directory of Binary File
directory = "./Samples/Polybench/3MM/"

# Binary file
executable = "3mm"

breakKernelStart = "3mm.cu:137"
# =============================================================================
#                Memory Analysis Configurations
# =============================================================================
use_memory_analysis = True                     
memory_watchlist = [["159","*E","512*512"],     # 3rd kernel read E
                    ["160","*F","512*512"],     # 3rd kernel read F
                    ["264","*G_outputFromGpu", "512*512"]] # after 3rd kernel read G


    
