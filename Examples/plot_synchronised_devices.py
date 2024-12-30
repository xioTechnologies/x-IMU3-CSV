import sys

import matplotlib.pyplot as plt
import ximu3csv

devices = ximu3csv.read("Logged Data")

plt.grid()
plt.legend()

plt.show(block="dont_block" not in sys.argv)  # don't block when script run by CI
