import numpy as np

def line_intersec(S1, S2) :

    test = False

    p = S1[0]
    r = S1[1] - S1[0]
    q = S2[0]
    s = S2[1] - S2[0]

    N = np.cross((p-q),s)
    D = np.cross(s,r)

    if D==0 and N==0 :
        print("segments are colinear")
        intersection = 0
    elif D==0 and N!=0 :
        print("segments are parallel")
        intersection = 0
    else :
        t = np.cross((p-q),s) / np.cross(s,r)
        intersec  = p + r*t
        if np.argsort([intersec, S1[0][0], S1[0][1]])[0] == 1 or np.argsort([intersec, S1[1][0], S1[1][1]])[1] ==1 :
            print("point is on segment")
            test = True
        else :
            print("point not on segment")

    return test, intersec
