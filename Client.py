import socket


s = socket.socket()
host= input(str("Please enter host Name of Server:"))
port = 8080
try :
        s.connect((host, port))
        print("Connected to Server")

        s.recv(20480)
        s.send(str.encode(' '))

        while True:
                incoming_msg = s.recv(1024)
                incoming_msg = incoming_msg.decode()
                print(host, " : " +incoming_msg)
                print("")
                msg = input(str(">>:"))
                msg = msg.encode(encoding="ascii")
                s.send(msg)
                print("massege sent")
                print("")
except :
    print ("ERROR IN CONNECTING TO SERVER")
