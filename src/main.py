import os
import re

from modules import make_files

# namesファイル，#cfgファイル，dataに記述するサブディレクトリ，画像の幅，画像の高さ
make_files('testinput/test.names', "testcfgs/yolov4.cfg","base_dir/","640","640")