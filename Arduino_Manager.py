import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.flush()


#HANDLING SERIAL COMMANDS
def generateserialcommand(devicelist, target, action):

    if target == 'all':
        for i in range(len(devicelist)):
            command = f"{i+1} {action}\n"
            command = command.encode('UTF-8')
            sendcommand(command)
    else:
        for i in range(len(devicelist)):
            if devicelist[i] == target:
                command = f"{i+1} {action}\n"
                command = command.encode('UTF-8')
                sendcommand(command)
                print(f"Turning {target} {action}")
    return

def sendcommand(command):
    print("writing serial command")
    ser.write(command)
    print(command)
    time.sleep(1)
    print("returning from send command")
    return