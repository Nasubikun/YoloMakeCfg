import os
import re

from modules import YoloCfgParser

# input_file = input(".namesファイルを入力")
input_file = 'testinput/test.names'
input_name = os.path.splitext(os.path.basename(input_file))[0]

base_dir = "base_dir/"

base_cfg = "testcfgs/yolov4.cfg"
width = "640"
height = "640"
max_batches = "10000"
steps_1 = str(int(max_batches)*0.8)
steps_2 = str(int(max_batches)*0.9)

has_blank_line = False
classes = 0
objs = []

with open(input_file,"r") as f:

    for line in f:
        line.rstrip("\n")
        if line in ['\n','\r\n']:
            has_blank_line = True
        else:
            classes+=1
            objs.append(line)


with open(f"{base_dir}{input_name}.names","w") as f:
    for obj in objs:
        f.write(obj)



train  = f"{base_dir}train.txt"
valid  = f"{base_dir}test.txt"
names = f"{base_dir}{input_name}.names"
backup = f"{base_dir}backup/"

with open(f"{base_dir}{input_name}.data","w") as f:
    f.write(f"classes = {classes}\n")
    f.write(f'train = "{base_dir}train.txt"\n')
    f.write(f'valid  = "{base_dir}test.txt"\n')
    f.write(f'names = "{base_dir}{input_name}.names"\n')
    f.write(f'backup = "{base_dir}backup/"\n')





parser = YoloCfgParser()
parser.read("testcfgs/yolov4-tiny.cfg")
parser.set_height(height)
parser.set_width(width)
parser.set_classes_and_filters(1)
parser.write(base_dir+"_.cfg")