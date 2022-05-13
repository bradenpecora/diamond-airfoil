import numpy as np
import sys

alpha = float(sys.argv[1])
chord = float(sys.argv[2])

<<<<<<< HEAD
adjust = 0.60
=======
adjust = 0.5
>>>>>>> 757175320d10ede299d26443d8e89940b3515591

print(-1*adjust*chord*np.cos(alpha*np.pi/180))