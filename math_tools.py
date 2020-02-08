import numpy as np


def norm(S) :

    a = S[1,0] - S[0,0]
    b = S[1,1] - S[0,1]

    return np.sqrt(a**2 + b**2)

def distance(P0, P1) :

    return np.sqrt((P1[1]-P0[1])**2 + (P1[0]-P0[0])**2)

def get_intersection_point(S1, S2) :
    """ return point of intersection between S1 and S2
                    S1 n S2 = P
    by resolving with parametric segment equation :
                    r*t + p = s*u + q
    if no point finded, return []
    """

    test = False

    # parametric components of segments
    p = S1[0]
    r = S1[1] - S1[0]
    q = S2[0]
    s = S2[1] - S2[0]

    # numerator and denominator of t expression
    N = np.cross((p-q),s)
    D = np.cross(s,r)

    if D == 0 and N == 0 : pass # colinear
    elif D == 0 and N != 0 : pass # parallel
    else : # crossing straight lines
        t = N / D
        P  = p + r*t
        # is P in between segments?
        test1 = np.argsort([P[0], S1[0,0], S1[1,0]])[1] == 0
        test2 = np.argsort([P[1], S1[0,1], S1[1,1]])[1] == 0
        test3 = np.argsort([P[0], S2[0,0], S2[1,0]])[1] == 0
        test4 = np.argsort([P[1], S2[0,1], S2[1,1]])[1] == 0

        if test1 and test2 and test3 and test4 : # crossing segments
            test = True
            P = P.astype(int)
        else : pass # not crossing segments

    if not(test) : P = [] # if no intersections

    return P


def get_intersections_list(source, obstacle) :
    """ return all intersection between :
            - raylight from source (angle, aperture; number_of_ray)
            - segmennts of obstacle shape
    """

    # source parameter
    pos = source.pos
    angle = np.linspace(source.angle - source.aperture,
                        source.angle + source.aperture,
                        source.resolution)
    r = source.lenght

    # obstacle  parameter
    segments = obstacle

    intersections = list()
    for theta in angle :
        # for each theta return only one point, the closest one
        closest_P = []
        d_min = 2000

        for sgm in segments :

            # compute lightrays (from source to r*exp(i*theta)
            x0 = pos[0]
            y0 = pos[1]
            x1 = pos[0] + r*np.cos(theta)
            y1 = pos[1] + r*np.sin(theta)
            light = np.array([[x0, y0], [x1, y1]])

            # find intersection between lightray and segment
            P = get_intersection_point(light, sgm)

            # if no intersection lightray isnot stoped
            if (P == []) : P = light[1,:]

            # keep the closest P from source
            dist = distance(P, pos)
            if d_min > dist :
                d_min = dist
                closest_P = P

        # if we don't find any intersection
        if closest_P == [] : closest_P = P

        intersections.append(closest_P)

    return intersections


def get_intersection_point_debug(S1, S2) :
    test = False

    p = S1[0]
    r = S1[1] - S1[0]
    q = S2[0]
    s = S2[1] - S2[0]

    N = np.cross((p-q),s)
    D = np.cross(s,r)

    intersec = S1
    if D==0 and N==0 :
        #print("segments are colinear")
        intersec = S1
    elif D==0 and N!=0 :
        #print("segments are parallel")
        intersec = S1
    else :
        t = np.cross((p-q),s) / np.cross(s,r)
        intersec  = p + r*t
        test1 = np.argsort([intersec[0], S1[0,0], S1[1,0]])[1] == 0
        test2 = np.argsort([intersec[1], S1[0,1], S1[1,1]])[1] == 0
        test3 = np.argsort([intersec[0], S2[0,0], S2[1,0]])[1] == 0
        test4 = np.argsort([intersec[1], S2[0,1], S2[1,1]])[1] == 0
        if test1 and test2 and test3 and test4 :
            test = True
            intersec = np.array([[S1[0,0],S1[0,1]],[intersec[0],intersec[1]]])
        else :
            intersec=S1
            pass

    return test, intersec.astype(int)


if __name__ == '__main__' :
    a = np.array([[10,15], [30,1190]])
    b = np.array([[10,50],[15,100]])
    from matplotlib import pyplot as plt
    figure = plt.plot(a[:,0],a[:,1])
    figure2 = plt.plot(b[:,0],b[:,1])
    test, vect = get_intersection_point(a,b)
    print(test)
    print(vect)

    plt.show()

