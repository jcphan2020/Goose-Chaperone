import comvis as cs

keepAlive = True
while(keepAlive):
    r = cs.get_detections()
    i=0
    while i<len(r):
        if (r[i][cs.CLASSES_IDX] == cs.HUMAN):
            print("Do Human Action")
        if (r[i][cs.CLASSES_IDX] == cs.BIRD):
            print("Do Bird Action")
        i+=1