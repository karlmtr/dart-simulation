import numpy as np

def to_cartesian(r,t) : 
    """
    Polar coordinates to cartesian.
    Theta (t) has to be in degrees
    """
    x = r * np.cos(np.radians(t))
    y = r * np.sin(np.radians(t))
    return x,y

def to_polar(x,y):
    """
    Cartesian coordinates to polar. 
    """
    r = np.sqrt(x**2 + y**2)
    t = np.rad2deg(np.arctan2(y,x))
    return r,t



    

