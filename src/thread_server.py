import socket
from sqlite3 import connect
import threading


def sum(list):
    # print("Entered sum")
    sum = 0
    for i in range(len(list)):
        sum+=float(list[i])
    return sum


def divide(list):
    list+='+0'
    # print(list)
    # print("Entered divide")
    divide_flag = 0
    number = ''
    new_list = []
    for i in range(len(list)):
        if (list[i] == "/"):
            # print("found divide")
            new_list.append(number)
            number = ''
            divide_flag = 1
            continue

        if(list[i] != "+" and list[i] != "-" and list[i] != "*"):
            number+=list[i]
            # print(">",number)
            continue
        
        else:
            if (len(number) > 0):
                new_list.append(number)
                
                # print('ran')
                number = ''
            if (divide_flag == 1):
                # print(new_list)
                dividend = float(new_list.pop(-2))/float(new_list.pop(-1))
                # print(dividend)
                new_list.append(str(dividend))
                # print(new_list)
                divide_flag = 0
        
            # print('여기')
            new_list.append(str(list[i]))
            
    final_list = ''
    for i in range(len(new_list)):
        final_list+=new_list[i]
        
    return final_list

def multiply(list):
    list+='0'
    # print(list)
    # print("Entered multiply")
    multiply_flag = 0
    number = ''
    new_list = []
    for i in range(len(list)):
        if (list[i] == "*"):
            # print("found multiply")
            new_list.append(number)
            number = ''
            multiply_flag = 1
            continue

        if(list[i] != "+" and list[i] != "-"):
            number+=list[i]
            # print(">",number)
            continue
        
        else:
            if (len(number) > 0):
                new_list.append(number)
                
                # print('ran')
                number = ''
            if (multiply_flag == 1):
                # print(new_list)
                product = float(new_list.pop(-2))*float(new_list.pop(-1))
                # print(product)
                new_list.append(str(product))
                # print(new_list)
                multiply_flag = 0
        
            # print('여기')
            new_list+=str(list[i])
            
    final_list = ''
    for i in range(len(new_list)):
        final_list+=new_list[i]
        
    return final_list

            

def sortString(string):
    positive = []
    negative = []
    number = ''
    sign = 1
    
    # BODMAS
    after_divide = divide(string)
    # print("after divide")
    # print(after_divide)
    after_multiply = multiply(after_divide)
    # print("after multiply")
    # print(after_multiply)
    string = after_multiply

    for i in range(len(string)):
        if (string[i] == "+"):
            if (sign == 1):
                positive.append(number)
            else:
                negative.append(number)
            number = ''
            sign = 1
            continue
        elif (string[i] == "-"):
            if (i == 0):
                sign = 0
                continue
            if (sign == 1):
                positive.append(number)
            else:
                negative.append(number)
            number = ''
            sign = 0
            continue
                    
        else:
            number+=string[i]
            if (i == len(string)-1):
                if (sign == 1):
                    positive.append(number)
                else:
                    negative.append(number)
    
    print("Positive: ",positive)
    print("Negative: ",negative)

    return str(round(sum(positive) - sum(negative),3))


IP = socket.gethostbyname(socket.gethostname())
PORT = 7777
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
KILL_LINE = "kill"


def serve_client(connection, address):
    addr = str(address[1])
    ID = ''
    for i in range(len(addr)):ID+=addr[i]
            
    print(f"\nNew client assignment ID:{ID} is connected.")

    connected = True
    while connected:
        msg = connection.recv(SIZE).decode(FORMAT)
        if msg == KILL_LINE:
            connected = False
            print(f"\nClient ID:{ID} just left ..\n")
            continue
        
        print(f"Question from client ID:{ID} << {msg} >>")
       

        answer = 0
        answer = sortString(msg)
        answer = answer+'_'+ID
        connection.send(answer.encode(FORMAT))
        
        print(f"Response '{answer}' to the question '{msg}' was sent to ID:{address[1]}\n")
    
    print(f"Server still listening in for new clients ...")
    print(f" \n{threading.activeCount()-2} live connections remaining...\n")

    connection.close()

def main():
    print(" --- Initializing --- ")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f" --- Server is listening on --- \n IP: {IP} \n port:{PORT} ")

    # Handling multiple clients
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target = serve_client, args=(connection, address))
        thread.start()
        print(f" \n{threading.activeCount()-1} live connections...\n")

if __name__ == "__main__":
    main()