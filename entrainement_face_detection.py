import cv2
import numpy as np
import face_recognition
import os
import pickle

path = 'peronnes'
images = []
classNames = []
personsList = os.listdir(path)
#print(personsList)

for cl in personsList:
    curPersonn = cv2.imread(f'{path}/{cl}')
    images.append(curPersonn)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

def findEncodeings(image):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodeings(images)
#print(encodeListKnown)
print('Encoding Complete.')

# Enregistrement des encodages dans un fichier (p.ex., pickle)
with open("encodings.pkl", "wb") as f:
    pickle.dump(encodeListKnown, f)

