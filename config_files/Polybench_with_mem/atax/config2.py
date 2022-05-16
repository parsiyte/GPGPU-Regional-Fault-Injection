# =============================================================================
#                           CONFIGURATION FILE
# =============================================================================
# Directory of Binary File
directory = "./Samples/Polybench/ATAX/"
# Binary file
executable = "atax"

breakKernelStart = "atax.cu:107"
# =============================================================================
#                Memory Analysis Configurations 
# =============================================================================
use_memory_analysis = True                   
memory_watchlist = [["114","*tmp","4096"],
		        	["184","*y_outputFromGpu","4096"]]

