# =============================================================================
#                           CONFIGURATION FILE
# =============================================================================
# Directory of Binary File
directory = "./Samples/Polybench/COVAR/"
# Binary file
executable = "covar"

breakKernelStart = "covariance.cu:159"
# =============================================================================
#                Memory Analysis Configurations
# =============================================================================
use_memory_analysis = True
memory_watchlist = [["161","*mean","1025"],   
		            ["166","*mean","1025"],
		            ["173","*mean","1025"],
                    ["179","*data","1025*1025"],   
                    ["240","*symmat_outputFromGpu", "1025*1025"]] 

