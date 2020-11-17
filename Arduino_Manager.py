#import serial
import time

#HANDLING SERIAL COMMANDS
def generateserialcommand(devicelist, target, action):

    if target == 'all':
        for device in devicelist:
            command = f"{device} {action}\n"
            command = command.encode('UTF-8')
            sendcommand(command)
    else:
        command = f"{target} {action}\n"
        command = command.encode('UTF-8')
        sendcommand(command)
        print(f"Turning {target} {action}")
    return

def sendcommand(command):
    print("writing serial command")
    #ser.write(command)
    print(command)
    time.sleep(1)
    print("returning from send command")
    return