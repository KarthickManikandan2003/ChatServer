import socket
import threading

class Client:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        while 1:
            try:
                host = input('Enter IP address of the server: ')
                port = int(input('Enter port number: '))
                self.s.connect((host,port))
                
                break
            except:
                print("Couldn't connect to server")

        self.username = input('Enter Username: ')
        print('''     
        1) Enter message\n
        2) Share image
        ''')


        self.s.send(self.username.encode())
        
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()
        
    def handle_messages(self):
        while 1:
            msg=self.s.recv(1024)
            if(msg.decode()=='1'):
              
              msg=self.s.recv(1024)
              while not msg.decode():
                    msg=self.s.recv(1024)
              print("\n"+"Chat:"+"\n"+str(msg.decode()+"\n"))

            if(msg.decode()=='2'):
              file=open('client_image.png','wb')
              image_chunk=self.s.recv(2048)
              while image_chunk:
                  file.write(image_chunk)
                  image_chunk=self.s.recv(2048)
              file.close()
              
    def input_handler(self):
        while 1:
            choice=int(input("Enter choice: "))
            if(choice==1):
             self.s.send(('1').encode())
             print("Enter message")
             self.s.send((self.username+' - '+input()).encode())

            else:
             self.s.send(('2').encode())
             print("Enter file name")
             file=open(input(),'rb')
             image_data=file.read(2048)
             while image_data:
                 self.s.send(image_data)
                 image_data=file.read(2048)
             file.close()
            
client = Client()
