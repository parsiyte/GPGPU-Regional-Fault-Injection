# =============================================================================
#                           CONFIGURATION FILE
# =============================================================================
# Directory of Binary File
directory = "./Samples/CJP/"
# Binary file
executable = "CJP"

breakKernelStart = "implementation.cu:30"
# =============================================================================
#                Memory Analysis Configurations (optional)
# =============================================================================
use_memory_analysis = True
memory_watchlist = [["51","*registers","4"],
		    		["57","*registers_pointer","32*4"],
		    		["67","ORedregisters","4"]] 

