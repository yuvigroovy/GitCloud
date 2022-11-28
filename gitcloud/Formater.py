from ast import Break
import os
import subprocess

class Formater:

    max_fregment_size = 1073741824 #1.0 GB 
    bs=512 #block size in bytes


    def __init__(self,cloud_path: str,file_name: str):
        self.cloud_path = cloud_path
        self.file_name = file_name

    
    def make_fragment(inf: str,of: str,offset: int,size: int):
        offset *= int(Formater.max_fregment_size/Formater.bs)
        bash_command = (f"dd if={inf} bs={Formater.bs} skip={offset} count={int(size/Formater.bs)} of={of}.txt")
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    def fragmentize(self, path: str,num_of_fregments: int, remain_fragment_size: float):
        #make a folder for fragmented file: 
        folder_path = os.path.join(self.cloud_path,self.file_name)
        try:
            os.mkdir(folder_path)
        except:
            print("ERROR")
        else:
            _,extention = os.path.splitext(path)

            #create info file
            with open(os.path.join(folder_path,'info.txt'), 'w') as f:
                f.write(f"n{num_of_fregments}t{extention}")
            for i in range(num_of_fregments):
                Formater.make_fragment(path,folder_path+'/'+str(i),i,Formater.max_fregment_size)
            #Formater.make_fragment(path,num_of_fregments,num_of_fregments,remain_fragment_size+remain_fragment_size%Formater.bs)

        


    
    def format(self,path: str): #get a file's path 
        file_size = os.path.getsize(path)
        print(file_size)
        if(file_size > Formater.max_fregment_size):
            num_of_fragments = int(file_size / Formater.max_fregment_size)
            remain_fragment_size = file_size % Formater.max_fregment_size
            Formater.fragmentize(self,path,num_of_fragments,remain_fragment_size)

#test

t = Formater("/Users/yuvalkarp/Desktop/test.nosync/", "test1")
t.format("/Users/yuvalkarp/Desktop/test.nosync/20221014_174206.mp4")
