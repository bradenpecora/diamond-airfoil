import numpy as np
import sys

x = float(sys.argv[1])
alpha = float(sys.argv[2])

print(x*np.cos(np.pi/180*alpha))

