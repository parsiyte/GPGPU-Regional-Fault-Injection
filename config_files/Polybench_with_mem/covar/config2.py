# =============================================================================
#                           CONFIGURATION FILE
# =============================================================================
# Directory of Binary File
directory = "./Samples/Polybench/COVAR/"
# Binary file
executable = "covar"

breakKernelStart = "covariance.cu:164"
# =============================================================================
#                Memory Analysis Configurations (optional)
# =============================================================================
use_memory_analysis = True                 # optional
memory_watchlist = [
                    ["166","*mean","1025"],
	                ["173","*mean","1025"],
                    ["179","*data","1025*1025"],
                    ["240","*symmat_outputFromGpu", "1025*1025"]
                   ]

