import re

class YoloCfgParser():
    def read(self,path: str):
        with open(path,'r') as f:
            self.raw_cfg = f.read()
            self.cfg_iter = self.raw_cfg.split('\n')

    def write(self,path: str):
        with open(path,'w') as f:
            for line in self.cfg_iter:
                f.write(line+"\n")

    def show_raw(self):
        print(self.raw_cfg)

    def _set_index_value(self,indexes: list,replace_txt: str):
        for index in indexes:
            self.cfg_iter[index] = replace_txt

    def _set_elem_value(self,element,value):
        replace_txt = f"{element}={value}"
        replace_indexes = []
        pattern = f'{element}='
        compiled_pattern = re.compile(pattern)
        for i,line in enumerate(self.cfg_iter):
            if compiled_pattern.match(line):
                replace_indexes.append(i)
        for index in replace_indexes:
            self.cfg_iter[index] = replace_txt

    # def set_height(self,height):
    #     replace_txt = f"height={height}"
    #     replace_indexes = []
    #     cfg_iter = self.cfg.split('\n')
    #     for i,line in enumerate(cfg_iter):
    #         if 'height' in line:
    #             print(line)
    #             replace_indexes.append(i)
    #     for index in replace_indexes:
    #         cfg_iter[index] = replace_txt
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
                print(i)
                print(line)
                yolo_sec_indexes.append(i)
        return yolo_sec_indexes
    
    def _find_filters_to_change(self,yolo_sec_indexes):
        filters_indexes = []
        for i,line in enumerate(self.cfg_iter):
            if re.match('filters',line):
                print(i)
                print(line)
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
        replace_txt = f"filters={filters}"
        self._set_index_value(filters_indexes_to_change,replace_txt)