# =============================================================================
#                           CONFIGURATION FILE
# =============================================================================
# Directory of Binary File
directory = "./Samples/CJP/"
# Binary file
executable = "CJP"

breakKernelStart = "implementation.cu:26"
# =============================================================================
#                Memory Analysis Configurations
# =============================================================================
use_memory_analysis = True                        # optional
memory_watchlist = [["51","*registers","4"],
		    		["57","*registers_pointer","32*4"],
		   			["67","ORedregisters","4"]]

