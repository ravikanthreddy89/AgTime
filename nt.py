from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import select
import struct, time, thread;

class AgTime:
	lClock=0;
	pClock=0;
	count=0;

#NTP client object that queries NTP server for time.
class Ntp:
	
	def __init__(self):
		# # Set the socket parameters 
		self.host = "pool.ntp.org"
		self.port = 123
		self.buf = 1024
		self.address = (self.host,self.port)
		self.msg = '\x1b'+47*'\0'
		# reference time (in seconds since 1900-01-01 00:00:00)
		self.TIME1970 = 2208988800 # 1970-01-01 00:00:00

	def time(self):
		# connect to server
		client = socket.socket( AF_INET, SOCK_DGRAM)
		client.sendto(self.msg, self.address)
		data, address = client.recvfrom( self.buf )

		retval=struct.unpack("!12I",data);
		t = retval[10]
		t -= self.TIME1970
		return t;


def server(portno):
	# List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = portno;
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                 
             
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                	print data; 
                except:
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
	

def send(data,portno):
	client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	client_socket.connect(("localhost",portno));
	client_socket.send(data);
	client_socket.close();



if __name__ == "__main__":
	#create an ntp object
	ntp=Ntp();
	#create a time-stamp object
	time_stamp=AgTime();
	#launch a server thread
	thread.start_new_thread(server,(int(sys.argv[1]),));
	while 1:
		data=raw_input("Enter some text to send");
		portno=raw_input("Enter portno");
		send(data,int(portno));	
		
        print "Exiting";
