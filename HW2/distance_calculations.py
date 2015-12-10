import DTW_EDRP

def convert_to_1D(y):
    z = []
    s = sorted(set(x[0] for x in y))
    ti = []
    i = 0
    count = 0
    for val in y:
        last = False
        if val[0] == s[i]:
            ti.append(val[1])
        else:
            last = True
            i += 1
            ti.sort()
            z += ti
            ti = []
            ti.append(val[1])
        if last == True and i == (len(s) - 1) and count == (len(y) - 1):
            z+=ti
        elif count == (len(y) - 1):
            z+=ti
        count +=1
    return z

if __name__ == "__main__":
    print len(y1)
    y1_1D = convert_to_1D(y1)
    print len(y1_1D)
    print len(y2)
    y2_1D = convert_to_1D(y2)
    print len(y2_1D)
    print len(y3)
    y3_1D = convert_to_1D(y3)
    print len(y3_1D)
    print len(y4)
    y4_1D = convert_to_1D(y4)
    print len(y4_1D)
    ##between track 1 and track 2:
    dist_1_2_DTW = DTW_EDRP.calculate_path(y1_1D, y2_1D,DTW_EDRP.distance_matrix_DTW)[1]
    dist_1_2_EDRP = DTW_EDRP.calculate_path(y1_1D,y2_1D,DTW_EDRP.distance_matrix_EDRP)[1]
    print dist_1_2_DTW
    print dist_1_2_EDRP
    dist_1_3_DTW = DTW_EDRP.calculate_path(y1_1D, y3_1D,DTW_EDRP.distance_matrix_DTW)[1]
    dist_1_3_EDRP = DTW_EDRP.calculate_path(y1_1D,y3_1D,DTW_EDRP.distance_matrix_EDRP)[1]
    print dist_1_3_DTW
    print dist_1_3_EDRP
    dist_1_4_DTW = DTW_EDRP.calculate_path(y1_1D, y4_1D,DTW_EDRP.distance_matrix_DTW)[1]
    dist_1_4_EDRP = DTW_EDRP.calculate_path(y1_1D,y4_1D,DTW_EDRP.distance_matrix_EDRP)[1]
    print dist_1_4_DTW
    print dist_1_4_EDRP



