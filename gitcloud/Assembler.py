import os
from re import S
"""--------------------------------------"""
class Assembler:
    #-------------------------------------
    def __init__(self, input_path: str,output_path: str):
        self.input_path = input_path
        self.output_path = output_path
    #-------------------------------------
    def combine_fragments(num_fragments,file_type,file_name):
        for i in range(num_fragments+1):
            print
    #-------------------------------------
    def assemble(self):
        try:
            info = open(os.path.join(self.input_path,"info.txt"), 'r')
        except:
            print("ERROR")
        else:
            num_fragments = int(info.readline())
            file_type = info.readline()
            file_name = info.readline() + file_type
            file_size = info.readline()           
            info.close()
            with open(f'{os.path.join(self.output_path,file_name)}', 'w') as f:
                for i in range(num_fragments+1):
                    path = os.path.join(self.input_path,str(i)+'.karp')
                    with open(f'{path}','r') as r:
                        f.write(r.read())
#----------------------------------------------
# test
input="/Users/yuvalkarp/Desktop/test.nosync/test1"
output="/Users/yuvalkarp/Desktop/test.nosync/to"
s = Assembler(input,output)
s.assemble()                        