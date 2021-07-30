import socket
import sys
import threading
import time
from queue import Queue
no_of_thread = 2
job_no = [1,2]
queue = Queue()
allcon = []
alladdr = []


def create_socket():
    try:
        global host
        global port
        global s
        host = socket.gethostname()    
        IPAddr = socket.gethostbyname(host)    
        print("Your Computer Name is:" + host)    
        print("Your Computer IP Address is:" + IPAddr)  
        port = 8080
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(1)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()




def accepting_connection():
   for c in allcon:
        c.close()

   del allcon[:]
   del alladdr[:]

   while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  
            allcon.append(conn)
            alladdr.append(address)

            print("Connection has been established :" + address[0])


        except:
            print("Error accepting connections")


def start_cmd():
   
    while True:  
        cmd = input('COMMAND:')
        if cmd =='list':
                list_conn()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None :
                send_target_commands(conn)
        else:
            print("UNKNOW COMMAND")

def list_conn():
    results = ''

    for i, conn in enumerate(allcon):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del allcon[i]
            del alladdr[i] 
            continue

        results = str(i) + "   " + str(alladdr[i][0]) + "   " + str(alladdr[i][1]) + "\n"

    print("----Clients----" + "\n" + results)


def get_target(cmd):
   try:
        target = cmd.replace('select ', '')  
        target = int(target)
        conn = allcon[target]
        print("You are now connected to :" + str(alladdr[target][0]))
        print(str(alladdr[target][0]) + ">", end="")
        return conn
       

   except:
        print("Selection not valid")
        return None

def send_target_commands(conn):
    try: 
             while True:
                print('CMD:')
                cmd2 = input()
                if cmd2 == 'quit':
                    break
                else: 
                    msg = input(str(">>:"))
                    msg = msg.encode(encoding="ascii")
                    conn.send(msg)
                    print("massege sent")
                    print("")
                    incoming_msg = conn.recv(20480)
                    incoming_msg = incoming_msg.decode()
                    print("Client:", incoming_msg)
                    print("")
    except :
        print ("ERROR IN SENDING")
       


def create_workers():
    for _ in range(no_of_thread):
        t = threading.Thread(target=work)
        t.deamon = True
        t.start()


def work ():
    while True:
        x =queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_cmd()
        queue.task_done()

def create_jobs():
    for x in job_no:
        queue.put(x)
    queue.join()
         
create_workers()
create_jobs()
            

