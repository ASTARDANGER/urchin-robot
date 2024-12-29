import matplotlib.colors as mplcolors
import numpy as np

## to plot with a gradient of color
def colorFader(c1="green",c2="red",mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mplcolors.to_rgb(c1))
    c2=np.array(mplcolors.to_rgb(c2))
    return mplcolors.to_hex((1-mix)*c1 + mix*c2)