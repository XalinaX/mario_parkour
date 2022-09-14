#this is a file for edit images(I do not have photoshop)
#PIL is a library that need to downloaad
from PIL import Image

walk=[]
def walke():
    global walk,walkp,name
    size=54,54
    walk.append(Image.open("./character/walk1.gif"))
    walk.append(Image.open( "./character/walk2.gif"))
    walk.append(Image.open( "./character/walk3.gif"))
    walk.append(Image.open("./character/walk4.gif"))
    walk[0].thumbnail(size,Image.ANTIALIAS)
    walk[0].save("walk1.gif")
    for a in range (0,4):
        name="walk"+str(a+1)+".gif"
        print (name)
        walk[a].thumbnail(size,Image.ANTIALIAS)
        walk[a].save(name)
        width, height = walk[a].size
        print (width,height)

walke()

