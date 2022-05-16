# =============================================================================
#                           CONFIGURATION FILE
# =============================================================================
# Directory of Binary File
directory = "./Samples/Polybench/COVAR/"
# Binary file
executable = "covar"

breakKernelStart = "covariance.cu:195"
# =============================================================================
#                Memory Analysis Configurations (optional)
# =============================================================================
use_memory_analysis = True                        # optional  
memory_watchlist = [["240","*symmat_outputFromGpu", "1025*1025"]] # after 3rd kernel read G

