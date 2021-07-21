import re
import os

def make_files(names_input: str,cfg_input: str,base_dir: str,width,height):


    input_file_dir = os.path.dirname(names_input)
    input_name = os.path.splitext(os.path.basename(names_input))[0]


    objs = pick_objs(names_input)
    classes = len(objs)


    with open(f"{input_file_dir}/{input_name}.names","w") as f:
        for obj in objs:
            f.write(obj)

    data_list = make_data_file(base_dir, input_name,classes)

    with open(f"{input_file_dir}/{input_name}.data","w") as f:
        for line in data_list:
            f.write(line)


    parser = YoloCfgParser()
    parser.read(cfg_input)
    parser.set_height(height)
    parser.set_width(width)
    parser.set_classes_and_filters(1)
    parser.write(f"{input_file_dir}/{input_name}.cfg")

def pick_objs(names_input):
    objs = []

    with open(names_input,"r") as f:

        for line in f:
            line.rstrip("\n")
            if not line in ['\n','\r\n']:
                objs.append(line)
    return objs

def make_data_file(base_dir,input_name,classes):
    dst = []
    dst.append(f"classes = {classes}\n")
    dst.append(f'train = "{base_dir}train.txt"\n')
    dst.append(f'valid  = "{base_dir}test.txt"\n')
    dst.append(f'names = "{base_dir}{input_name}.names"\n')
    dst.append(f'backup = "{base_dir}backup/"\n')
    return dst

class YoloCfgParser():

    log = []
    def read(self,path: str):
        with open(path,'r') as f:
            self.raw_cfg = f.read()
            self.cfg_iter = self.raw_cfg.split('\n')

    def write(self,path: str):
        with open(path,'w') as f:
            for line in self.cfg_iter:
                f.write(line+"\n")
        self.show_log()

    def show_log(self):
        for l in self.log:
            print(f"{l[0]} : {l[1]} → {l[2]}")

    def show_raw(self):
        print(self.raw_cfg)

    def _add_log(self,line_number,before,after):
        if before!=after:
            self.log.append([line_number,before,after])

    def _replace_text(self,indexes: list,new_text: str):
        for index in indexes:
            self._add_log(index,self.cfg_iter[index], new_text)
            self.cfg_iter[index] = new_text

    def _set_elem_value(self,element,value):
        new_text = f"{element}={value}"
        replace_indexes = []
        pattern = f'{element}='
        compiled_pattern = re.compile(pattern)
        for i,line in enumerate(self.cfg_iter):
            if compiled_pattern.match(line):
                replace_indexes.append(i)
        self._replace_text(replace_indexes, new_text)

    # def set_height(self,height):
    #     new_text = f"height={height}"
    #     replace_indexes = []
    #     cfg_iter = self.cfg.split('\n')
    #     for i,line in enumerate(cfg_iter):
    #         if 'height' in line:
    #             print(line)
    #             replace_indexes.append(i)
    #     for index in replace_indexes:
    #         cfg_iter[index] = new_text
    #     self.cfg = "\n".join(cfg_iter)
    #     print(self.cfg)
    
    def set_height(self,height):
        self._set_elem_value("height",height)

    def set_width(self,width):
        self._set_elem_value("width",width)

    def set_classes_and_filters(self,classes):
        self._set_elem_value("classes",classes)
        filters = 3*int(classes)+15
        self._set_filters(filters)

    def _find_yolo_secs(self):
        yolo_sec_indexes = []
        for i,line in enumerate(self.cfg_iter):
            if re.match('\[yolo\]',line):

                yolo_sec_indexes.append(i)
        return yolo_sec_indexes
    
    def _find_filters_to_change(self,yolo_sec_indexes):
        filters_indexes = []
        for i,line in enumerate(self.cfg_iter):
            if re.match('filters',line):

                filters_indexes.append(i)

        filters_indexes_to_change = []
        for index in yolo_sec_indexes:
            temp_index = -1
            for i in filters_indexes:
                if i < index:
                    temp_index = i
                else:
                    break
            filters_indexes_to_change.append(temp_index)
            print(filters_indexes_to_change)
        return filters_indexes_to_change
            

    def _set_filters(self,filters):
        yolo_sec_indexes = self._find_yolo_secs()
        filters_indexes_to_change = self._find_filters_to_change(yolo_sec_indexes)
        new_text = f"filters={filters}"
        self._replace_text(filters_indexes_to_change,new_text)