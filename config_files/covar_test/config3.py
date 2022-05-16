# ============================================================================
#                           CONFIGURATION FILE
# ============================================================================
# Directory of Binary File
directory = "./Samples/Polybench/COVAR/"

# Binary file
executable = "COVAR"

# Arguments, if not neccessary fill blank string ""
args = ""

# number of fault
num_fault = 1000

breakKernelStart = "covariance.cu:166"

# Output Results destination of Execution   ****Required for SDC check***
output = "Output.txt"

