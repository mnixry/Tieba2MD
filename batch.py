from API import api
from avalon_framework import Avalon
import os

filePath = Avalon.gets('File Place?')
with open(filePath) as f:
    perLink = f.readlines()
perID = []
for i in perLink:
    postID = int((i.split('/'))[-1].split('?')[0])
    perID.append(postID)
Avalon.info(str(perID))
for i in perID:
    fileName = str(postID) + '.md'
    # fullBehavior(postID=postID, fileName=fileName, onlySeeLZ=False)
