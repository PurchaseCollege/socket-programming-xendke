# Team CORE4: JuanXGomez(Xendke), SharonLevin(shaerins), Luisa, Stephen
# Python 3
# Links Used:
#    https://www.tutorialspoint.com/python/python_networking.htm  
#    https://docs.python.org/3/library/sys.html
#    https://docs.python.org/3/library/socket.html
#    https://www.jmarshall.com/easy/http/
import sys
import socket

root = "root/" # the root folder for where the available files to serve are stored

def openFile(filename): # function that will return the file(filename) in form of bytes object
    global root
    return open(root + filename, "rb").read() # we will manipulate the root variable to point to the right root folder according to who we are serving to (mobile vs desktop) 

if __name__ == "__main__":
    if(len(sys.argv) > 2): # check if there are more than 2 arguments
        print("simple_server.py supports only one argument: port")
        sys.exit(0) # quit
    elif(len(sys.argv) == 1): # if no port argument passed, then port defaults to 3000
        port = 3000
    else:
        try:
            port = int(sys.argv[1]) # try to cast argument to int
        except ValueError:
            print(sys.argv[1], "is not a valid port number.")
            sys.exit(0) # quit if port couldn't be casted to int
    
    print("Web Server Starting...")
    # 0. Dynamically find IP for host
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    host_ip = s.getsockname()[0]
    print("IP: ", host_ip)
    # 1. Create a socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. "Bind" the socket to an IP and PORT
    my_socket.bind((host_ip, port))
    # 3. Begin "listening" on the socket
    my_socket.listen(5)
    print("Listening...")
    
    while(True): # keep accepting connections so that the server does not end after one "transaction"
        # 4. Begin "accepting" client connections
        conn, addr = my_socket.accept()
        # 5. Receive some data (up to 1024 bytes) FROM the client
        data = ''
        data = conn.recv(1024)
        
        data_string = str(data) # turn data to a string so we can more easily manipulate it
        print(data_string)
        
        if "iPhone" in data_string or "Android" in data_string: # if data_string contains the strings "iPhone" or "Android" change root to mobile/ directory
            root = "mobile/"
        else:
            root = "root/"

        get_string = "" # this string is gonna hold the command which we assume to be a form of a GET command

        for i in range(0, len(data_string)): # iterate through data_string and find first \r\n occurence 
            if(data_string[i:i+4] == "\\r\\n"):
                get_string = data_string[2:i] # get_string will be in the form "GET / HTTP/1.0"
                print(get_string)
                break

        if(get_string[0:3] == "GET"): # if the command was a GET command then find filename
            filename = ""
            for i in range(4, len(get_string)): # iterate through GET command and find first space after "/"
                if(get_string[i] == " "):
                    filename = get_string[5:i] # filename will be in the form "index.html" or "" in the case of "GET / HTTP.."
                    print(filename)
                    break
                
            # send basic HTTP header 
            conn.sendall(str.encode("HTTP/1.1 200 OK\n\n"))
            # send the file named filename and close connection
            if(not filename): # if filename empty, send index.html
                filename = "index.html"
            
            try:
                conn.sendall(openFile(filename)) # try to open filename and send
            except (FileNotFoundError, IsADirectoryError): # catch: file not found error or filename is dir, send 404.html instead
                print("404")
                conn.sendall(openFile("404.html"))
            
        conn.close()
	    
