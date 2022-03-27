from python_imagesearch.imagesearch import imagesearch, imagesearcharea
import time

time.sleep(2)





#for i in range(1,14):
    
    #pos = imagesearcharea(("./BOT/croppedBoxes/sc"+str(i)+".png"),66,148,1274,947,precision=0.8)
    #if pos[0] !=-1:
        #break

pos = imagesearch("./BOT/croppedBoxes/sc1.png",precision=0.7)
print(pos)
