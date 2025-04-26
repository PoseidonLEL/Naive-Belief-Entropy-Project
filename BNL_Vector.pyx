from numpy import float32, zeros


cpdef void lova_remove(list array, str element): #Faster than python .remove() function
    cdef int i
    for i in range(len(array)):
        if(array[i]==element):
            del array[i]
            break

cpdef int sin(list array, str find): #Faster than python "in" operator
    cdef str i
    for i in array:
        if(find==i):
            return 1
    return 0

cpdef float BNL_Distance(str string1, str string2, int bL, int len1):
    cdef str sO
    cdef str sT
    cdef int max_len = 0
    cdef int len2 = len(string2)
    
    if (len1 == len2):
        sO = string1
        sT = string2
        max_len = len2 // bL
    elif (len1 < len2):
        sO = string1.ljust(len2, ' ')
        sT = string2
        max_len = len2 // bL
    else:
        sO = string1
        sT = string2.ljust(len1, ' ')
        max_len = len1 // bL

    cdef list substrings1 = []
    cdef list substrings2 = []
    cdef int i
    for i in range(0, max_len * bL, bL):
        substrings1.append(sO[i:i+bL])
        substrings2.append(sT[i:i+bL])

    cdef float common_count = 0.0
    cdef str sub1
    for sub1 in substrings1:
        if (sin(substrings2,sub1)):
            common_count += 1
            lova_remove(substrings2,sub1)

    return common_count / max_len


def massBNL(inStr,stringArr,BL):
    cdef int lenSTR = len(inStr)
    cdef int lenArr = len(stringArr)
    cdef list return_array = [0.0]*lenArr
    cdef int i
    for i in range(lenArr):
        return_array[i] = BNL_Distance(inStr,stringArr[i],BL,lenSTR)
    return float32(return_array)


def BNL_Vector():
    return "Use massBNL()"
