from socket import AF_INET, SOCK_DGRAM
import sys;
import socket;
import select;
import thread;
import pickle;
import struct;
import time;
import threading;


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

class server(threading.Thread):
	def __init__(self,portNo):
		threading.Thread.__init__(self);
		self.PORTNO=portNo;
		self.server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
		self.server_socket.bind(("",self.PORTNO));
		self.CONNECTION_LIST=[];
		self.RECV_BUFFER=4096;

	def run(self):
		self.server_socket.listen(10);
		self.CONNECTION_LIST.append(self.server_socket);
		print "Server started on port :"+str(self.PORTNO);
		
		while(1):
			read_sockets,write_sockets,error_sockets=select.select(self.CONNECTION_LIST,[],[]);
			for sock in read_sockets:
				if sock==self.server_socket:
					sockfd, addr= self.server_socket.accept();
					self.CONNECTION_LIST.append(sockfd);
					print "Message rxd from (%s %s)",addr
				else:
					try:
						data=pickle.loads(sock.recv(self.RECV_BUFFER));
						if data:
							thread.start_new_thread(recv,(data,));
					except:
						sock.close();
						self.CONNECTION_LIST.remove(sock);
						continue;
		self.server_socket.close();

def recv(data):
	lock.acquire();
	
	print data;
	lock.release();


def send(data,portno):
	lock.acquire();
	global time_stamp;
	t_stamp={'pClock':0, 'lClock':0,'count':0};
	t_stamp['lClock']=max(time_stamp['lClock'],time_stamp['pClock']);
	if(t_stamp['lClock']==time_stamp['lClock']):
		time_stamp['count']=time_stamp['count']+1;
	else:
		time_stamp['count']=0;
	t_stamp['pClock']=time_stamp['pClock'];
	t_stamp['count']=time_stamp['count'];

	#update the time_stamp object to hold the event timestamp
	time_stamp['lClock']=t_stamp['lClock'];
	time_stamp['pClock']=t_stamp['pClock'];
	time_stamp['count']=t_stamp['count'];
	client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	client_socket.connect(("pollux.cse.buffalo.edu",portno));
	client_socket.send(pickle.dumps(t_stamp));
	client_socket.close();
	lock.release();


if __name__ == "__main__":
	#create a global lock for mutual exclusion
	global lock;
	lock=threading.RLock();
        #create an ntp object
	ntp=Ntp();
	#create a time-stamp object
	global time_stamp;
	time_stamp= {'pClock':0, 'lClock':0,'count':0};
        #launch a server thread
	server_thread=server(int(sys.argv[1]));
	server_thread.start();
	while 1:
		data=raw_input("Enter some text to send");
		portno=raw_input("Enter portno");
		if(data!="quit"):
			thread.start_new_thread(send,(data,int(portno)));	
		else:
			break;
        print "Exiting";
