import numpy as np
import sys

x = np.float128(sys.argv[1])
alpha = np.float128(sys.argv[2])

print(x*np.sin(np.pi/180*alpha))

