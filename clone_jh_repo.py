import os
import time

print ("Cloning latest info for coronavirus from John Hopkins university's git repo")
#clone latest info for coronavirus from John Hopkins university's git repo
os.system("rm -rf COVID-19")
os.system("git clone https://github.com/CSSEGISandData/COVID-19.git")

