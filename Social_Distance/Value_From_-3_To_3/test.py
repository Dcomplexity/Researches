import os
dd = "Test"
path = os.path.abspath(os.path.join(os.getcwd(), "../../"))
foldername = path + "/Results/Value_From_-3_To_3/%s/" %dd
if not os.path.isdir(foldername):
    print ("make folder")
    os.makedirs(foldername)
filename = foldername + "/test.txt"
f = open(filename, 'w')
f.write("hello world!")
f.close()