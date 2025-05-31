import os
import numpy as np
print(os.getcwd())
test123 = np.loadtxt("Data/Messung1_BPF.csv",skiprows = 1,delimiter = ',')
print(test123)