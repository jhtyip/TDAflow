import sys
import tarfile
import os

toCalList = sys.argv[4].split("qwerty")
k = sys.argv[5]

fileList = []
for toCal in toCalList:
    config = toCal.split("__")
    subfolders_item = config[0]
    subfolders_item_1 = config[1]
    subfolders_item_2 = config[2]
    num1 = config[3]
    num2 = config[4]
    num3 = config[5]

    fileList.append(subfolders_item.replace("/", "")+"_"+num1+"_"+num2+"_"+num3+"_"+k+".npy")

tarName = sys.argv[1]+"_"+sys.argv[2]+"_"+sys.argv[3]+"_"+k+".tar.gz"
tar = tarfile.open(tarName, "w:gz")
for file in fileList:
    tar.add(file)
    os.remove(file)
tar.close()
