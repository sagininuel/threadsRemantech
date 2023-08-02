import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 7777
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
KILL_LINE = "kill"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"\nYou are connected to the server!\nYou shall receive a unique ID upon your first query.\n ")
    print(f"Please key in any expression with the following operands \n\n ['+','-','/' and '*'] \n")
    print(f"Valid Operations:\nSum -> (+)\nSubtraction -> (-)\nMultiplication -> (*)\nDivision -> (/)\n")

    print(f"Example: 3/2*12-37+1 ")
    connected = True
    while connected:
        msg = input("\nType in an expression below ( type <kill> to end the client program ) \n>> ")

        client.send(msg.encode(FORMAT))

        if msg == KILL_LINE:
            connected = False
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            answer = ''
            ID = ''
            start = 0
            for i in range(len(msg)):
                if (msg[i] == '_'):
                    start = 1
                    continue       
                elif(start):
                    for j in range(len(msg)-i):
                        ID+=msg[i+j]
                    break
                else:
                    answer+=msg[i]
                    
            print(f"\n ---Incoming message from server for ID:{ID} --- ")
            print(f"Answer = {answer}  <rounded to 3dp>\nClient ID: {ID} \n")
            
            file = open("/results/")
            file = open("result_"+ID+".txt","a") # To append to the text file replace "w" with "a"
            # file.write("Solution to: ")
            # file.write(inputString)
            # file.write(" is -> ")
            file.write(answer)
            file.write("\n")
            file.close()


            f = open("result_"+ID+".txt","r")
            print("\nThe answer '"+answer+"' was stored in the 'result_"+ID+".txt' file\n")


            
if __name__ == "__main__":
    main()