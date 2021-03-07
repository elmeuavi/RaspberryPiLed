#PER ATACAR EL SERVIDOR VIA SHELL
#exec 3<>/dev/tcp/hostname/port
#echo "request" 1>&3
#response="$(cat <&3)"
#TANCAR LA CONNEXIO:
#exec 3<&-
#
#curl -H "Host:" -H "User-Agent:" -H "Accept:" -H "Content-Length:" -H "Content-Type:" -d "hola" -X POST --max-time 0,1 192.168.1.144:10000  


import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10000)
sock.bind(server_address)
print  ('starting up on %s port %s' , sock.getsockname())
sock.listen(1)

while True:
    print  ('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print  ('client connected:', client_address)
        while True:
            data = connection.recv(16)
            print  ('received servidor' , str(data))
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()
