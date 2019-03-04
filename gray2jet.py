import numpy as np

def gray2jet(I):
    Iout = np.zeros((I.shape[0],I.shape[1],3),dtype=np.uint8)

    Iout[:,:,0] = baseTransform(I-0.25)
    Iout[:,:,1] = baseTransform(I)
    Iout[:,:,2] = baseTransform(I+0.25)

    return Iout

def baseTransform(v):
    vOut = np.zeros(v.shape,dtype=np.uint8)

    vOut[v<1/8]              = np.uint8(0)
    vOut[(v>=1/8) & (v<3/8)] = np.uint8(np.round(( v[(v>=1/8) & (v<3/8)] - 1/8) * 255/(1/4)))
    vOut[(v>=3/8) & (v<5/8)] = np.uint8(255)
    vOut[(v>=5/8) & (v<7/8)] = np.uint8(np.round((-v[(v>=5/8) & (v<7/8)] + 7/8) * 255/(1/4)))
    vOut[v>=7/8]             = np.uint8(0)

    return vOut
