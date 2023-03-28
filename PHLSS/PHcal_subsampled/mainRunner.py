import os
import sys

toCalList = sys.argv[1].split("qwerty")
k = sys.argv[2]

i = 0
for toCal in toCalList:
    # thisName = subfolders_item+";"+param_dict[subfolders_item].split()[0]+";"+param_dict[subfolders_item].split()[1]+";"+str(j)+";"+str(k)+";"+str(i)

    config = toCal.split("__")
    subfolders_item = config[0]
    subfolders_item_1 = config[1]
    subfolders_item_2 = config[2]
    num1 = config[3]
    num2 = config[4]
    num3 = config[5]

    os.system("python main.py "+subfolders_item+" "+subfolders_item_1+" "+subfolders_item_2+" "+num1+" "+num2+" "+num3+" "+k+" "+sys.argv[3]+" "+sys.argv[4]+" "+sys.argv[5])
    i += 1

print("job done, instances processed: " + str(i))
