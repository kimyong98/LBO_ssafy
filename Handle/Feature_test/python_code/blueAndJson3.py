from bluetooth import *
import json
from collections import OrderedDict as ORD
import threading

def input_and_send(sock):
    print("\nType something\n")
    while True:
        send_json = {}
        info_json = {}
        data_json = {}

        name = 1 # It's const
        print("time?: ", end="")
        time = input()
        print("How Servo: ", end="")
        servo  = int(input())
        print("How buzzer: ", end="")
        beep = int(input())


        info_json["name"] = name
        info_json["time"] = time;

        data_json["servo"] = servo
        data_json["beep"] = beep

        send_json["info"] = info_json
        send_json["data"] = data_json

        print("Send Json", end="")
        print(send_json)

        send_string = json.dumps(send_json)

        print("Send String", end="")
        send_string += '@'
        print(send_string)

        if len(send_string) == 0: break
        sock.send(send_string)
        sock.send("\n")
        
def rx_and_echo(sock):
    #sock.send("\nsend anything\n")
    while True:
        data_string = ""

        while True:
            ret = data_string.find('@')
            if ret != -1:
                #print(ret)
                break
            temp = sock.recv(buf_size).decode('utf-8')
            #print(temp)
            data_string += temp

        data_string = data_string[:-1]
        print(data_string)
        '''
        if data_string:
            print(data_string)
        ''' 
        print("JSON")        
        if data_string:
            data_json = json.loads(data_string)
            #print(data_json)


            name = int(data_json["info"]["name"])
            time = data_json["info"]["time"]

            print("Info: [name: {0}] [time : {1}]".format(name, time))

            uwb = float(data_json["data"]["uwb"])
            print("Uwb: {0}".format(uwb))

            gyro_x = float(data_json["data"]["imu"]["gyro"]["x"])
            gyro_y = float(data_json["data"]["imu"]["gyro"]["y"])
            gyro_z = float(data_json["data"]["imu"]["gyro"]["z"])
            gyro_w = float(data_json["data"]["imu"]["gyro"]["w"])
            print("Gyro: [x: {0}] [y: {1}] [z: {2}] [w: {3}]".format(gyro_x, gyro_y, gyro_z, gyro_w))

            
            acc_x = float(data_json["data"]["imu"]["acc"]["x"])
            acc_y = float(data_json["data"]["imu"]["acc"]["y"])
            acc_z = float(data_json["data"]["imu"]["acc"]["z"])
            print("Acc: [x: {0}] [y: {1}] [z: {2}]".format(acc_x, acc_y, acc_z))

            Button = int(data_json["data"]["button"])
            print("Button: {0}".format(Button))

            #print(data_string.decode('utf-8'))


def bluetooth_communication(sock):
    input_thread = threading.Thread(target=input_and_send, args=(sock,))
    rx_thread = threading.Thread(target=rx_and_echo, args=(sock,))
    
    input_thread.start()
    rx_thread.start()

    input_thread.join()
    rx_thread.join()

#MAC address of ESP32
addr = "08:D1:F9:D7:94:8A"
#uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
#service_matches = find_service( uuid = uuid, address = addr )
service_matches = find_service( address = addr )

buf_size = 4096;

if len(service_matches) == 0:
    print("couldn't find the SampleServer service =(")
    sys.exit(0)

for s in range(len(service_matches)):
    print("\nservice_matches: [" + str(s) + "]:")
    print(service_matches[s])
    
first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

port=1
print("connecting to \"%s\" on %s, port %s" % (name, host, port))

# Create the client socket
sock=BluetoothSocket(RFCOMM)
sock.connect((host, port))

print("connected")

#input_and_send()
#rx_and_echo()

bluetooth_communication(sock)


sock.close()
print("\n--- bye ---\n")


