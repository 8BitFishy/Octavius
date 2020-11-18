
def updatedevicelist(Octavius_List_Manager, Octavius_Receiver, Octavius_Vocab):
    Octavius_Receiver.send_message(f"Updating device list")
    Octavius_Receiver.send_message(f'Current devices:')
    for device in Octavius_List_Manager.devicelist:
        Octavius_Receiver.send_message(device)

    Octavius_Receiver.send_message('Which device would you like to replace?')

    incomplete = True
    loops = 3
    while incomplete and loops > 0:
        loops -= 1
        response1 = Octavius_Receiver.get_response()
        Octavius_Receiver.send_message(response1)
        print(Octavius_List_Manager.devicelist)
        print(response1)

        if response1 == '':
            loops = 0
        elif response1 in Octavius_List_Manager.devicelist:
            incomplete = False
        else:
            Octavius_Receiver.send_message('Device not in list')

    Octavius_Receiver.send_message('and the name for the new device is?')

    if loops != 0:
        incomplete = True
        loops = 3
        while incomplete and loops > 0:
            loops -= 1
            response2 = Octavius_Receiver.get_response()
            Octavius_Receiver.send_message(response2)
            if response2 == '':
                loops = 0
            elif response2 in Octavius_List_Manager.devicelist:
                Octavius_Receiver.send_message('Device already listed, please choose another name')
                continue
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
        return Octavius_List_Manager

    else:

        with open('devicelist.txt', 'w') as f:
            for i in range(len(Octavius_List_Manager.devicelist)):
                if Octavius_List_Manager.devicelist[i] != response1:
                    f.write(str(Octavius_List_Manager.devicelist[i]))
                    f.write("\n")
                else:
                    f.write(str(response2))
                    f.write("\n")
                    Octavius_List_Manager.devicelist[i] = response2

        Octavius_Receiver.send_message('New device list:')

        for device in Octavius_List_Manager.devicelist:
            Octavius_Receiver.send_message(device)
        return Octavius_List_Manager
