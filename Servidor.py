#!/usr/bin python3
import datetime
import socket
import pandas as pd
from io import StringIO
import random

def validar(m,car):
    if m == 3 and ((Gato.at[0, 'A'] == Gato.at[0, 'B'] == Gato.at[0, 'C'] == car) or \
                   (Gato.at[1, 'A'] == Gato.at[1, 'B'] == Gato.at[1, 'C'] == car) or \
                   (Gato.at[2, 'A'] == Gato.at[2, 'B'] == Gato.at[2, 'C'] == car) or \
                   (Gato.at[0, 'A'] == Gato.at[1, 'A'] == Gato.at[2, 'A'] == car) or \
                   (Gato.at[0, 'B'] == Gato.at[1, 'B'] == Gato.at[2, 'B'] == car) or \
                   (Gato.at[0, 'C'] == Gato.at[1, 'C'] == Gato.at[2, 'C'] == car) or \
                   (Gato.at[0, 'A'] == Gato.at[1, 'B'] == Gato.at[2, 'C'] == car) or \
                   (Gato.at[0, 'C'] == Gato.at[1, 'B'] == Gato.at[2, 'A'] == car)):
        if car == 'X':
            return 1
        if car == 'O':
            return 0
    elif m == 5 and (
            (Gato.at[0, 'A'] == Gato.at[0, 'B'] == Gato.at[0, 'C'] == Gato.at[0, 'D'] == Gato.at[0, 'E'] == car) or \
            (Gato.at[1, 'A'] == Gato.at[1, 'B'] == Gato.at[1, 'C'] == Gato.at[1, 'D'] == Gato.at[1, 'E'] == car) or \
            (Gato.at[2, 'A'] == Gato.at[2, 'B'] == Gato.at[2, 'C'] == Gato.at[2, 'D'] == Gato.at[2, 'E'] == car) or \
            (Gato.at[3, 'A'] == Gato.at[3, 'B'] == Gato.at[3, 'C'] == Gato.at[3, 'D'] == Gato.at[3, 'E'] == car) or \
            (Gato.at[4, 'A'] == Gato.at[4, 'B'] == Gato.at[4, 'C'] == Gato.at[4, 'D'] == Gato.at[4, 'E'] == car) or \
            (Gato.at[0, 'A'] == Gato.at[1, 'A'] == Gato.at[2, 'A'] == Gato.at[3, 'A'] == Gato.at[4, 'A'] == car) or \
            (Gato.at[0, 'B'] == Gato.at[1, 'B'] == Gato.at[2, 'B'] == Gato.at[3, 'B'] == Gato.at[4, 'B'] == car) or \
            (Gato.at[0, 'C'] == Gato.at[1, 'C'] == Gato.at[2, 'C'] == Gato.at[3, 'C'] == Gato.at[4, 'C'] == car) or \
            (Gato.at[0, 'D'] == Gato.at[1, 'D'] == Gato.at[2, 'D'] == Gato.at[3, 'D'] == Gato.at[4, 'D'] == car) or \
            (Gato.at[0, 'E'] == Gato.at[1, 'E'] == Gato.at[2, 'E'] == Gato.at[3, 'E'] == Gato.at[4, 'E'] == car) or \
            (Gato.at[0, 'A'] == Gato.at[1, 'B'] == Gato.at[2, 'C'] == Gato.at[3, 'D'] == Gato.at[4, 'E'] == car) or \
            (Gato.at[4, 'A'] == Gato.at[3, 'B'] == Gato.at[2, 'C'] == Gato.at[1, 'D'] == Gato.at[0, 'E'] == car)):
        if car == 'X':
            return 1
        if car == 'O':
            return 0
    else:
        return 2


fecha_inicio = datetime.datetime(2000, 10, 9)
fecha_final = datetime.datetime(2023, 3, 8)
diferencia = fecha_final - fecha_inicio

dias_vividos = diferencia.days
modulo_tres = dias_vividos % 3

print("Días vividos:", dias_vividos)
print("Módulo 3 de los días vividos:", modulo_tres)
print("Por lo tanto toca realizar el 'Gato Dummy'")

"""HOST = "127.0.0.1"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)"""
HOST = input("Ingrese el Host: ")
PORT = int(input("Ingrese le Puerto: "))
buffer_size = 1024
Gato = pd.DataFrame()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")

    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        print("Conectado a", Client_addr)
        print("Esperando eleccion de nivel... ")
        while True:
            nivel = Client_conn.recv(buffer_size)
            if nivel == b"principiante":
                n = 3
                strGto = """A;B;C\n ; ; \n ; ; \n ; ; """
                Client_conn.sendall(str.encode(strGto))
                numrnd = [0, 1, 1, 2]
                break
            elif nivel == b"avanzado":
                n = 5
                strGto = """A;B;C;D;E\n ; ; ; ; \n ; ; ; ; \n ; ; ; ; \n ; ; ; ; \n ; ; ; ; """
                Client_conn.sendall(str.encode(strGto))
                numrnd = [0, 0, 1, 1, 2, 2, 2, 3, 4, 4]
                break
            Client_conn.sendall(b"Ingrese una cadena valida")
        nCeldas = n*n
        Gato = pd.read_csv(StringIO(strGto), sep = ";")
        cont = 0
        while True:
            celda = Client_conn.recv(buffer_size)
            columna = chr(celda[0])
            fila = chr(celda[1])
            if ((n == 3) and ((columna == 'A' or columna == 'B' or columna == 'C') and (fila == '0' or fila == '1' or fila == '2'))) or ((n == 5) and ((columna == 'A' or columna == 'B' or columna == 'C' or columna == 'D' or columna == 'E') and (fila == '0' or fila == '1' or fila == '2' or fila == '3' or fila == '4'))):
                if Gato.at[int(fila), columna] == ' ':
                    coor = columna+fila
                    print("Se recibio la coordenada:",coor)
                    Gato.at[int(fila), columna] = 'X'
                    cont = cont + 1
                    val = validar(n, 'X')
                    if (cont < nCeldas) and val == 2:
                        cont = cont + 1
                        while True:
                            filcol=random.sample(numrnd, 2)
                            if(filcol[0]==0):
                                columna = 'A'
                            elif(filcol[0]==1):
                                columna = 'B'
                            elif(filcol[0]==2):
                                columna = 'C'
                            elif(filcol[0]==3):
                                columna = 'D'
                            elif(filcol[0]==4):
                                columna = 'E'
                            if Gato.at[filcol[1],columna] == ' ':
                                break
                        mensaje = (columna + str(filcol[1]))
                        Gato.at[filcol[1], columna] = 'O'
                        val = validar(n, 'O')
                        if val == 2:
                            Client_conn.sendall(str.encode(mensaje))
                            print("Se envio la coordenada:",mensaje)
                        else:
                            break
                    else:
                        break
                else:
                    Client_conn.sendall(b"Ingrese una coordenada valida:")
            else:
                Client_conn.sendall(b"Ingrese una coordenada valida:")
        if val == 1:
            Client_conn.sendall(b"Ganaste")
        elif val == 0:
            Client_conn.sendall(b"Perdiste")
            Client_conn.sendall(str.encode(mensaje))
            print("Se envio la coordenada:", mensaje)
        elif val == 2:
            Client_conn.sendall(b"Empataste")