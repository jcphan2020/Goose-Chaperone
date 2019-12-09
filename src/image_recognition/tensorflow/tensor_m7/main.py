import comvis

keepAlive = True
while(keepAlive):
    r = comvis.get_detections()
    print(r)