# Programa que simula um chat entre clientes e um servidor como ponto central
#
# Mateus-n00b, Maio de 2017
#
# Versao 1.0
#
# TODO: Matar as threads apos o fechamento da conexao
#
# Licensa GPLv3
#

from socket import *
from threading import Thread
import getopt
import sys

# Cria o socket
# Create the socket
sock = socket(AF_INET,SOCK_STREAM)
# Opcao para o reuso de portas
# Set to reuse the ports
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Server address
SERVER  = ""
# User name
NAME    = ""
# Defaul port
PORT   = 2222
# Armazena as 'conns' para iterar e enviar as msgs
# Keep the 'conns' to iterate trough them.
CLIENTs = []

# The connection handler
def connHandler(conn):
    while True:
        data = conn.recv(1024)
        for obj in CLIENTs:
            if obj != conn:
                # Tento enviar as msgs caso contrario removo a 'conn'
                try:
                    obj.send(data)
                except:
                    CLIENTs.remove(obj)

    sock.close()

# Lado servidor (Trata as conexoes que chegam)
# Server side (handle incoming connections)
def serverSide():
    global sock
    sock.bind(("",PORT))
    sock.listen(5)
    while True:
            try:
                # Accept the incoming connections
                conn, addr = sock.accept()

                if conn not in CLIENTs:
                    CLIENTs.append(conn)
                    t = Thread(None,connHandler,None,args=(conn,))
                    t.start()

            except Exception as err:
                print err
                sys.exit(-1)

# Cliente handler (lida com as msgs que chegam)
def clientRecv(sock):
    while True:
        data = sock.recv(1024)
        print "[%s] %s" % (data.split("+=+")[0],data.split("+=+")[1])
    sock.close()

# Lado cliente (envia e recebe as mensagens)
def clientSide():
    NAME = raw_input("Insira seu nome> ")

    # Tenta efetuar a conexao ou sai
    try:
        sock.connect((SERVER,PORT))
    except Exception as err:
        print err
        sys.exit(-1)

    msg = ""
    # Lembre-se de colocar essa ',' em args
    t = Thread(None,clientRecv,None,args=(sock,))
    t.start()
    while msg != "quit":
        msg = raw_input("> ")
        # Envia a mensagem com seu nome
        sock.send(NAME+"+=+"+msg)
    sock.shutdown(1)
    sock.close()
    sys.exit(0)

# NOTE: Melhorar a mensagem de help
if len(sys.argv) < 2:
    print "Usage: %s -t <serverSERVER> or -s (play as a server)" % sys.argv[0]
    sys.exit(-1)


# Pega os argumentos passados para o programa e os trata
opts,args =  getopt.getopt(sys.argv[1:],"hst:",["target,help"])
for o,a in opts:
    if o in ("-h","--help"):
        print "Usage: %s -t <serverSERVER> or -s (play as a server)" % sys.argv[0]
        sys.exit(0)
    elif o in ("-s", "--server"):
        # t = Thread(None,serverSide,None)
        # t.start()
        # Inicia o servidor
        serverSide()
    elif o in ("-t","--target"):
        SERVER = a
        # Inicia o cliente
        clientSide()
    else:
        print "Invalid option! Try -h."
        sys.exit(-1)
