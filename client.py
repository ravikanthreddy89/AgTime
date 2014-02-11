import socket;
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
client_socket.connect(("localhost",5000));
while 1:
	data=raw_input("Enter some text to send and Quit to exit");
	if(data=="Quit"):
		client_socket.send(data);
		client_socket.close();
		break;
	else:
		client_socket.send(data);
