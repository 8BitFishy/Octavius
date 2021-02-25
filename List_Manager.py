import os
import Format_Manager

class List_Manager:
    def __init__(self, devices, devicelist, protectedwords, listdict):
        self.devices = devices
        self.devicelist = devicelist
        self.protectedwords = protectedwords
        self.listdict = listdict
        
    def Create_New_List(self, Octavius_Vocab, Octavius_Receiver):
        #name list
        Octavius_Receiver.send_message(f"What would you like the list to be called?")
        response1 = Octavius_Receiver.get_response()
        

        #start adding items to a list
        incomplete = True
        while incomplete:
            #receive item names until '/end' is input
            Octavius_Receiver.send_message(f"Okay, what would you like to add to {Format_Manager.capitalise_word(response1)}?")
            Octavius_Receiver.send_message(f"Type '/end' to finish")
            response2 = ''
            responselist = []
            while response2 != '/end': 
                response2 = Octavius_Receiver.get_response()
                responselist.append(response2)
                
            #remove /end from list and add to listdict
            del responselist[-1]

            #read back to user
            Octavius_Receiver.send_message(f"List '{Format_Manager.capitalise_word(response1)}' with items:")
            for item in responselist:
                Octavius_Receiver.send_message(item)
            
            #confirm user would like to save list
            Octavius_Receiver.send_message(f"Would you like to save this list?")
            response3 = Octavius_Receiver.get_response()
            
            #if response is affirmative, save list to text file and add to listdict
            if response3 in Octavius_Vocab.affirmativelist:
                self.listdict.update({f"response1" : responselist})
                with open(f"lists/List - {response1}.txt", "w") as f:
                    for item in responselist:
                        f.write(item)
                        f.write("\n")
                Octavius_Receiver.send_message(f"List saved")
                incomplete = False
            #if no response, exit
            elif response3 == '':
                Octavius_Receiver.send_message(f"Timed out, exiting...")
                incomplete = False
            #otherwise repeat
            else:
                Octavius_Receiver.send_message(f"Acknowledged")


        return
                

    def updatedevicelist(self, Octavius_Receiver, Octavius_Vocab):
        Octavius_Receiver.send_message(f"Updating device list")
        Octavius_Receiver.send_message(f'Current devices:')
        for device in self.devicelist:
            Octavius_Receiver.send_message(device)

        Octavius_Receiver.send_message('Which device would you like to replace?')

        incomplete = True
        loops = 3
        while incomplete and loops > 0:
            loops -= 1
            response1 = Octavius_Receiver.get_response()
            Octavius_Receiver.send_message(response1)
            print(self.devicelist)
            print(response1)

            if response1 == '':
                loops = 0
            elif response1 in self.devicelist:
                incomplete = False
            else:
                Octavius_Receiver.send_message('Device not in list')


        if loops != 0:
            Octavius_Receiver.send_message('and the name for the new device is?')
            incomplete = True
            loops = 3
            while incomplete and loops > 0:
                loops -= 1
                response2 = Octavius_Receiver.get_response()
                Octavius_Receiver.send_message(response2)
                if response2 == '':
                    loops = 0
                elif response2 in self.devicelist:
                    Octavius_Receiver.send_message('Device already listed, please choose another name')
                    continue
                elif response2 in self.protectedwords:
                    Octavius_Receiver.send_message('This name is protected, please choose another')

                else:
                    Octavius_Receiver.send_message('Are you sure?')
                    response3 = Octavius_Receiver.get_response()
                    print(response3)
                    if response3 == '':
                        loops = 0
                    elif response3 in Octavius_Vocab.affirmativelist:
                        incomplete = False
                    else:
                        Octavius_Receiver.send_message('Please repeat device name')

        if loops == 0:
            Octavius_Receiver.send_message("Timed out, exiting...")
            return self

        else:

            with open('SystemLists/devicelist.txt', 'w') as f:
                for i in range(len(self.devicelist)):
                    if self.devicelist[i] != response1:
                        f.write(str(self.devicelist[i]))
                        f.write("\n")
                    else:
                        f.write(str(response2))
                        f.write("\n")
                        self.devicelist[i] = response2

            Octavius_Receiver.send_message('New device list:')

            for device in self.devicelist:
                Octavius_Receiver.send_message(device)
            return self



def Generate_Lists():
    
    directory = 'SystemLists'
    filename = 'protectedwords.txt'
    dir = os.path.join(f"{directory}/", filename)
    with open(dir) as f:
        protectedwords = f.read().splitlines()
        for i in range(len(protectedwords)):
            protectedwords[i] = protectedwords[i].lower()
            protectedwords[i].rstrip()
            
    devicelist = []
    devices = []
    filename = 'devicelist.txt'      
    dir = os.path.join(f"{directory}/", filename)
    with open(dir) as f:
        line = f.read().splitlines()
        for i in line:
            colour, plug, device = i.rsplit("-")
            devicelist.append([colour, plug, device])
        for i in range(len(devicelist)):
            devicelist[i][0] = devicelist[i][0].lower()
            devicelist[i][0].rstrip()
            devicelist[i][1] = int(devicelist[i][1])
            devicelist[i][2] = devicelist[i][2].lower()
            devicelist[i][2].rstrip()
            devices.append(devicelist[i][2])


    print(f"Devices = {devices}")
    directory = 'lists'
    listdict = {}
    for files in os.walk(directory):
        filelist = list(files[2])
        for file in filelist:
            if 'List - ' in file:
                dir = os.path.join(f"{directory}/", file)
                with open(dir) as f:
                    listcontents = f.read().splitlines()
                    for i in range(len(listcontents)):
                        listcontents[i] = listcontents[i].lower()
                        listcontents[i].rstrip()

                listname = file.replace("List - ", "", 1)
                listname = listname.replace(".txt", "", 1)
                listdict[listname] = listcontents
    Octavius_Lists = List_Manager(devices, devicelist, protectedwords, listdict)
    
    return Octavius_Lists


def Read_List(targetlist, Octavius_Receiver):
    print(targetlist)
    for item in targetlist:
        Octavius_Receiver.send_message(item)
    return



    
