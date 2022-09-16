#import the libraries
#socket ---> Library for creating sockets on client and server side.
#cv2 --->This library contains built in functions for displaying the video on a window.
#pickle -->This library is used for converting a Python object into a byte stream to store it in a file/database, maintain program state across sessions, or transport data over the network
#struct ---> This library is used to convert native Python data types such as strings and numbers into a string of bytes and vice versa. 
#imutils ---> A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, and displaying Matplotlib images easier with OpenCV

import socket, cv2, pickle,struct,imutils

# Socket Create
#creat this socket to recieve requests from the client through this socket.
#AF_INET ---> IPv4 address, SOCK_STREAM ---> TCP connection is to be estabilished with this socket.

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


host_name  = socket.gethostname()

#The below function directly gets the IP address of the host from the hostname.

host_ip = socket.gethostbyname(host_name)

print('HOST IP:',host_ip)

#Port number where we have to listen to requests

port = 9999

#store the IP address and port number in a tuple so that it can be binded later with the socket.

socket_address = (host_ip,port)

# Socket Bind
#This assigns an IP address and a port number to a socket instance.

server_socket.bind(socket_address)

# Socket Listen
#listen() makes a socket ready to listen to requests.
#The listen() function accepts a queue size through the parameter backlog. This denotes maximum number of connections that can be queued for this socket by the operating system

server_socket.listen(5)
print("LISTENING AT:",socket_address)

# Socket Accept
while True:
	#Blocks execution and waits for an incoming connection. When a client connects, it returns a new socket object representing the connection and a tuple holding the address of the client
	client_socket,addr = server_socket.accept()
	print('GOT CONNECTION FROM:',addr)
	if client_socket:
		#VideoCapture method of cv2 library helps us capture the a video from the camera
		#The arguments to the function are 
		# 1. video_path: Locationvideo in your system in string form with their extensions like .mp4, .avi, etc.
		# 2. device index: It is just the number to specify the camera. Its possible values ie either 0 or -1. 
		
		vid = cv2.VideoCapture(0)
		
		
		#vid.isOpened() will just check if the video file can be opened for reading or not.
		while(vid.isOpened()):
			
			#Capture the video frame by frame.
			img,frame = vid.read()
			
			#Resize the video captured by the frame.
			frame = imutils.resize(frame,width=320)
			
			#store the object data to the file. pickle. dump() function takes 3 arguments. The first argument is the object that you want to store.
			a = pickle.dumps(frame)
			
			#struct.pack takes non-byte values (e.g. integers, strings, etc.) and converts them to bytes
			message = struct.pack("Q",len(a))+a
			
			#send all the data to the client socket which requested.
			client_socket.sendall(message)
			
			#Used to display the video in a window.
			cv2.imshow('TRANSMITTING VIDEO',frame)
			
			#The waitKey(0) function returns -1 when no input is made whatsoever. As soon the event occurs i.e. a Button is pressed it returns a 32-bit integer.
			#The 0xFF in this scenario is representing binary 11111111 a 8 bit binary, since we only require 8 bits to represent a character we AND waitKey(0) to 0xFF. As a result, an 				integer is obtained below 255.
			#ord(char) returns the ASCII value of the character which would be again maximum 255.
			#Hence by comparing the integer to the ord(char) value, we can check for a key pressed event and break the loop.
			
			key = cv2.waitKey(1) & 0xFF
			if key ==ord('q'):
				#Close the client socket.
				client_socket.close()
