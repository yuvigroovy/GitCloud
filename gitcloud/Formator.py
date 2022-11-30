
import os
import subprocess

class Formator:

    max_fregment_size = 268435456 #256 MB 
    bs=1024 #block size in bytes


    def __init__(self,cloud_path: str,file_name: str):
        self.cloud_path = cloud_path
        self.file_name = file_name

    
    def make_fragment(inf: str,of: str,offset: int,size: int):
        if(size==0):
            count = ''
            bs = "bs=512" #to be changed - inefficient
            offset *= int(Formator.max_fregment_size/512)
        else:
            count = f"count={int(size/Formator.bs)}"  
            bs = f"bs={Formator.bs}"
            offset *= int(Formator.max_fregment_size/Formator.bs)
        
        

        bash_command = (f"dd if={inf} {bs} skip={offset} {count} of={of}.karp")
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    def fragmentize(self, path: str,num_of_fregments: int, remain_fragment_size: float, file_size: int):
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
                f.write(f"{num_of_fregments+1}\n{extention}\n{self.file_name}\n{file_size}")
            for i in range(num_of_fregments):
                Formator.make_fragment(path,folder_path+'/'+str(i),i,Formator.max_fregment_size)
            Formator.make_fragment(path,folder_path+'/'+str(num_of_fregments) ,num_of_fregments,0)

    def format(self,path: str): #get a file's path 
        file_size = os.path.getsize(path)
        if(file_size > Formator.max_fregment_size):
            num_of_fragments = int(file_size / Formator.max_fregment_size)
            remain_fragment_size = file_size % Formator.max_fregment_size
            Formator.fragmentize(self, path,num_of_fragments,remain_fragment_size,file_size)
        else:
            self.fragmentize(self, path,0,0,file_size)       

#test

t = Formator("/Users/yuvalkarp/Desktop/test.nosync/", "test1")
t.format("/Users/yuvalkarp/Desktop/test.nosync/20221014_174206.mp4")
