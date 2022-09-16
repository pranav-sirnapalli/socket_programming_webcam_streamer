#Importing the required libraries
#import the libraries
#socket ---> Library for creating sockets on client and server side.
#cv2 --->This library contains built in functions for displaying the video on a window.
#pickle -->This library is used for converting a Python object into a byte stream to store it in a file/database, maintain program state across sessions, or transport data over the network
#struct ---> This library is used to convert native Python data types such as strings and numbers into a string of bytes and vice versa. 
#imutils ---> A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, and displaying Matplotlib images easier with OpenCV

import socket,cv2, pickle,struct

# create socket
# Socket Create
#creat this socket to recieve requests from the client through this socket.
#AF_INET ---> IPv4 address, SOCK_STREAM ---> TCP connection is to be estabilished with this socket.

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#This address is got by running the server.py file.
host_ip = '192.168.56.1' # paste your server ip address here
port = 9999
client_socket.connect((host_ip,port)) # a tuple

#indicates that the literal should become a bytes literal 
data = b""

#Return the size of the struct (and hence of the string) corresponding to the given format
payload_size = struct.calcsize("Q")

while True:
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K
		if not packet: break
		data+=packet
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	#Converts the bytes into non byte values (e.g. integers, strings, etc.). 
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	while len(data) < msg_size:
		data += client_socket.recv(4*1024)
	frame_data = data[:msg_size]
	data  = data[msg_size:]
	frame = pickle.loads(frame_data)
	cv2.imshow("RECEIVING VIDEO",frame)
	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break
#close the client socket.
client_socket.close()
