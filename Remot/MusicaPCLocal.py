
import socket
import sys
import select


#python -m pip install pygame
import pygame # per la musica



if __name__ == '__main__':
        

    print ('Servidor per a posar música');
    print ('comandos: musica, close, stop');
    print ('');
    
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 20000)
    sock.bind(server_address)
    print  ('starting up on ' , sock.getsockname())
    sock.listen(1)
  
    

    
    while True:
        print  ('Waiting for a new connection')
        connection, client_address = sock.accept()
        try:
            print  ('client connected:', client_address)
            while True:
                #https://steelkiwi.com/blog/working-tcp-sockets/
                #https://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/select/index.html
                read_sockets, writable, exceptional  = select.select([connection] , [], [connection])


                    
                for s in read_sockets:
                    #mirem la conexió per wifi del PC
                    if s == connection:
                        print("Rebuda de la wifi")
                        try:
                            data = connection.recv(65535).decode("utf-8") 
                        except:
                            print("Error en la connexió al intentar llegir");
                            break;
                            
                        if data:
                            llista_linies_comandes=data.split("|")
                            for linia_comanda in llista_linies_comandes:
                                if linia_comanda:
                                    
                                    if len(linia_comanda) > 0 :  print  ('Comanda rebuda: %s ' % linia_comanda.replace('\n', ''))
                                    
                                    #Retornar al client la mateixa informació (no ho fem)
                                    #if debug: connection.sendall(bytearray(linia_comanda, 'utf-8'))
                                    comanda = linia_comanda.split()           
                                    print ("-" + comanda[0] + "-")
                                    if comanda[0] == "musica": 
                                        print ('dins música')
                                        if pygame.mixer.music.get_busy:
                                            print('Ja estem reproduint música, no fem res!')
                                        else:
                                            pygame.mixer.init(frequency=48000)
                                            if comanda[1] == "orient": 
                                                pygame.mixer.music.load('data\\ReisOrient.mp3')
                                            else:
                                                pygame.mixer.music.load('data\\MusicaHalloween.mp3')
                                            pygame.mixer.music.set_volume(1)
                                            pygame.mixer.music.play()  # start=POSICIO_MP3/1000
                                    elif comanda[0] == "stop": 
                                        pygame.mixer.music.stop()
                                    elif comanda[0] == "close": 
                                        sys.exit()
                                        
                        else:
                           print("Client desconectat")
                           s.close();
                          
                #Mirem si s'ha tancat la connexió
                if connection in exceptional: 
                    print("Connexió amb excepció")
                    break;


        except Exception as e: 
            print("Tenim una excepció i anem a tancar les connexions")
            print(e)
            traceback.print_exc()
            sock.close()
        finally:
            print("Anem a tancar les connexions")
            sock.close()
