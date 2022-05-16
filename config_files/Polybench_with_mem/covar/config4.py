# =============================================================================
#                           CONFIGURATION FILE
# =============================================================================
# Directory of Binary File
directory = "./Samples/Polybench/COVAR/"
# Binary file
executable = "covar"

breakKernelStart = "covariance.cu:178"
# =============================================================================
#                Memory Analysis Configurations (optional)
# =============================================================================
use_memory_analysis = True                         # optional 
memory_watchlist = [["179","*data","1025*1025"],   # 3rd kernel read F
                    ["240","*symmat_outputFromGpu", "1025*1025"]] # after 3rd kernel read G

