import face_compare
import dmm
import os

image,video = dmm.download()
face_compare.work(image,video)
os.remove(image)
os.remove(video)