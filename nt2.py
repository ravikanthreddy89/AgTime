from socket import AF_INET, SOCK_DGRAM
import sys;
import socket;
import select;
import thread;
import pickle;
import struct;
import time;
import threading;


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
	global recvCount;
	recvCount=recvCount+1;
	global time_stamp;
	t_message=data;
	t_stamp= {'pClock':0, 'lClock':0,'count':0};
	
	#recv part of algorithm starts from here
	t_stamp['lClock']=max(time_stamp['lClock'],t_message['lClock'],time_stamp['pClock']);
	if(t_stamp['lClock']==t_message['lClock'] and t_stamp['lClock']==time_stamp['lClock']):
		t_stamp['count']=max(time_stamp['count'],t_message['count'])+1;
	elif (t_stamp['lClock']==time_stamp['lClock']):
		t_stamp['count']=time_stamp['count']+1;
	elif(t_stamp['lClock']==t_message['lClock']):
		t_stamp['count']=t_message['count']+1;
	else:
		t_stamp['count']=0;

	time_stamp['lClock']=t_stamp['lClock'];
	time_stamp['pClock']=t_stamp['pClock'];
	time_stamp['count']=t_stamp['count'];
	print data;
	lock.release();


def send(hostName,portno):
	lock.acquire();
	global sendCount;
	sendCount=sendCount+1;
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
	client_socket.connect((hostName,portno));
	client_socket.send(pickle.dumps(t_stamp));
	client_socket.close();
	lock.release();


if __name__ == "__main__":
	#create a global lock for mutual exclusion or atomic events
	global lock;
	lock=threading.RLock();
	#create a time-stamp object
	global time_stamp;
	time_stamp= {'pClock':0, 'lClock':0,'count':0};
	#get the localhost's ip/hostname
	thisHost=socket.getfqdn();
	print "Host name : ",thisHost,"Type of hostname :",type(thisHost);
	#we don't need this right now.
	localIP=socket.gethostbyname(thisHost);
	hosts={};
	#variables to keep track of event counts
	global recvCount;
        recvCount=0;
        global sendCount;
        sendCount=0;


	#read the hosts file and save the list of hosts into a dict
	try:
		hostsFile=open(sys.argv[1]);
	except IOError:
		print "Error occured in trying to read the file"
	except :
		print "Error : Something went wrong while opening file"
	count=0;
	for line in hostsFile:
		if(line.strip()== thisHost):
			continue;
		else:
			hosts[count]=line;
			count=count+1;
	
	for keys in hosts:
		print hosts[keys],"Type:",type(hosts[keys]);
        #launch a server thread
	server_thread=server(int(5000));
	server_thread.start();

	if(thisHost=="pollux.cse.buffalo.edu"):
		# pollux is our playboy hitting at other hosts
		thread.start_new_thread(send,("sol.cse.buffalo.edu",5000));
		thread.start_new_thread(send,("silversun.cse.buffalo.edu",5000));
		thread.start_new_thread(send,("sol.cse.buffalo.edu",5000));
		thread.start_new_thread(send,("silversun.cse.buffalo.edu",5000));
		thread.start_new_thread(send,("coldplay.cse.buffalo.edu",5000));
		thread.start_new_thread(send,("coldplay.cse.buffalo.edu",5000));
        else :
		# other hosts listening for messages from playboy pollux
		while 1:
			data=raw_input("Enter \"quit\" to exit");
			if(data=="quit"):
				break;
		print "Total number of messages rxd :", recvCount;
		print "Total number of messages sent :", sendCount;
		
        print "Exiting";
