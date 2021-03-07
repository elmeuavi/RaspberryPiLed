import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
server_address = (sys.argv[1], 10000)
print ( 'connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    
    message = 'This is the message.  It will be repeated.'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))

    #amount_received = 0
    #amount_expected = len(message)
    #while amount_received < amount_expected:
    #    data = sock.recv(1600)
    #    amount_received += len(data)
    #    print ('received client' , data)

        
    message = '|color A|theaterChaseIteracions 200 10'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
    time.sleep(5)

    message = '|color A|theaterChaseTempsTotal 400 5000 3'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
    time.sleep(5)

    
    
    
    message = '|rainbowIteracions 20 5'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
    time.sleep(5)

    message = '|rainbowTempsTotal 20 5000'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
    time.sleep(5)

    message = '|rainbowCycleIteracions 20 5'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
    time.sleep(5)

    message = '|rainbowCycleTempsTotal 20 5000'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
    time.sleep(5)

    message = '|theaterChaseRainbow 100 5000'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
    time.sleep(5)


    
    message = '|incremental 20 1'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
      
    time.sleep(4)

    message = '|color A'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
      
    message = '|incremental 20 2'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
      
    time.sleep(4)
    
    message = '|color A|vano 2000 2'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
      
    time.sleep(4)
      
    message = '|color R'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))

    message = '|intensitat 50'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))

    message = '|omplir'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))

    time.sleep(2)
    
    message = '|colorRGB 0 255 255|intensitat 255'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))


    message = '|omplir'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))

    time.sleep(2)
    
    message = '|creixer 5000 '
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))

    time.sleep(2)

    message = '|decreixer 4000'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))

    time.sleep(2)
    
    message = '|netejar'
    print ('sending ' , message)
    sock.sendall(bytearray(message, 'utf-8'))
    
    
finally:
    sock.close()
