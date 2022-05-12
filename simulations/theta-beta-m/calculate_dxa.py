import numpy as np
import sys

alpha = float(sys.argv[1])
chord = float(sys.argv[2])

adjust = 0.5

print(-1*adjust*chord*np.cos(alpha*np.pi/180))