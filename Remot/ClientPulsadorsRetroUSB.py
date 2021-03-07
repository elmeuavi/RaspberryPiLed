import serial
import socket



            
sIpRaspberry = "192.168.1.144"
iPort = 10000
            
            
if __name__ == '__main__':


    print('Inicialitzem el client socket TCP/IP:')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (sIpRaspberry, iPort)
    print ( 'connecting to %s port %s ...' % server_address)
    sock.connect(server_address)
    

    
    print('Inicialitzem el client USB...')
    connexioSerialUSB = serial.Serial('COM4',9600,timeout = None)

    #la primera comanda la despreciem perquè pot arribar mitja comanda
    comanda= connexioSerialUSB.readline().decode("utf-8") .rstrip("\r\n")

    
    try:
        while True:
            if connexioSerialUSB.inWaiting():
                comanda= connexioSerialUSB.readline().decode("utf-8") .rstrip("\r\n")
                print(comanda)

                # mirem si és un comentari
                if comanda[0:1] != "@" and comanda != "":
                    sock.sendall(bytearray(comanda.strip(), 'utf-8'))

    finally:
        connexioSerialUSB.close()    