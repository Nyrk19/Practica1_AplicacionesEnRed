#!/usr/bin python3
import socket
import pandas as pd
from io import StringIO
import time

"""HOST = "127.0.0.1"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor"""
HOST = input("Ingrese el Host: ")
PORT = int(input("Ingrese le Puerto: "))
buffer_size = 1024
Gato = pd.DataFrame()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    while True:
        nivel = input("Ingresa el nivel: ")
        TCPClientSocket.sendall(str.encode(nivel))
        data = TCPClientSocket.recv(buffer_size)
        if data == b"Ingrese una cadena valida":
            print(data.decode())
        else:
            break
    print("\nSeleccionó nivel ",nivel)
    inicio = time.time()
    Gato = pd.read_csv(StringIO(data.decode()), sep=";")
    print(Gato)
    while True:
        coordenada = input("Ingresa tu coordenada a tirar (ejemplo A1): ")
        TCPClientSocket.sendall(str.encode(coordenada))
        data = TCPClientSocket.recv(buffer_size)
        columna = chr(data[0])
        fila = chr(data[1])
        if data != b"Ingrese una coordenada valida:":
            Gato.at[int(coordenada[1]), coordenada[0]] = 'X'
            print(Gato)
            time.sleep(1)
            if (data != b"Perdiste" and data != b"Ganaste" and data != b"Empataste"):
                Gato.at[int(fila), columna] = 'O'
                print(Gato)
            else:
                if(data == b"Perdiste"):
                    data = TCPClientSocket.recv(buffer_size)
                    columna = chr(data[0])
                    fila = chr(data[1])
                    Gato.at[int(fila), columna] = 'O'
                    print(Gato)
                    print("Perdiste")
                else:
                    print(data.decode())
                fin = time.time()
                break
        else:
            print(data.decode())
    seg = int(fin)-int(inicio)
    min = int(seg/60)
    segf = seg - (min*60)
    print("El juego duró:",min,"min",segf,"seg")
    TCPClientSocket.close()
