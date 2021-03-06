import Format_Manager
import random
import Arduino_Manager
import List_Manager
import Command_List


def commandhandler(text, Octavius_Vocab, Octavius_List_Manager, Octavius_Grammar, Octavius_Receiver):
    inputcommand = Format_Manager.lowercase_word(text)


    if Octavius_Grammar.is_question(inputcommand):
        Octavius_Receiver.send_message("I don't know how to answer questions yet")
        return

    elif inputcommand in Octavius_Vocab.gratitude:
        Octavius_Receiver.send_message("I am what my master made me")
        return

    command = Format_Manager.split_sentence(inputcommand)
    print(f'Received command: {inputcommand}')
    #Octavius_Receiver.send_message(f'Received command: {inputcommand}')
    print(len(command))

    if len(command) == 1:
        action = command[0]
        if action == 'talk':
            Command_List.talk(Octavius_Receiver)

        elif action in Octavius_Vocab.greetings:
            word = random.randint(0, len(Octavius_Vocab.greetings) - 1)
            Octavius_Receiver.send_message(f'{Octavius_Vocab.greetings[word]}')

        else:
            Octavius_Receiver.send_message("Command not recognised, please repeat")

    elif len(command) == 2:
        target = command[0]
        action = command[1]

        if target == 'lights' and ('on' in action or 'off' in action):
            if 'on' in action:
                for device in Octavius_List_Manager.devicelist:
                    if 'light' in device or 'lamp' in device:
                        Arduino_Manager.generateserialcommand(Octavius_List_Manager.devicelist, device, action)
                Command_List.Light_on()
                Octavius_Receiver.send_message("Turning lights on")
            else:
                for device in Octavius_List_Manager.devicelist:
                    if 'light' in device or 'lamp' in device:
                        Arduino_Manager.generateserialcommand(Octavius_List_Manager.devicelist, device, action)
                Command_List.Light_off()
                Octavius_Receiver.send_message("Turning lights off")

        elif target == 'light' and ('on' in action or 'off' in action):
            #todo if lights - turn off both
            if 'on' in action:
                Command_List.Light_on()
                Octavius_Receiver.send_message("Turning ceiling light on")
            else:
                Command_List.Light_off()
                Octavius_Receiver.send_message("Turning ceiling light off")



        elif (target in Octavius_List_Manager.devicelist or target == 'all') and (action == 'on' or action == 'off'):
            Octavius_Receiver.send_message(f"Turning {target} {action}")
            Arduino_Manager.generateserialcommand(Octavius_List_Manager.devicelist, target, action)

        elif 'update' in inputcommand:

            if 'device' in inputcommand:
                Octavius_List_Manager = List_Manager.updatedevicelist(Octavius_List_Manager, Octavius_Receiver, Octavius_Vocab)
                return

            elif 'affirmative' in inputcommand:
                Octavius_Vocab = Octavius_Vocab.updateaffirmatives(Octavius_Receiver)

        else:
            if action == 'on' or action == 'off':
                Octavius_Receiver.send_message(f"Device not currently listed, would you like to update device list?")
                if Octavius_Receiver.get_confirmation(Octavius_Vocab):
                    Octavius_List_Manager = List_Manager.updatedevicelist(Octavius_List_Manager)

                else:
                    Octavius_Receiver.send_message(f'Acknowledged, please repeat original command')

            else:
                Octavius_Receiver.send_message(f"Command not recognised, please repeat")

    else:
        Octavius_Receiver.send_message(f'Command not recognised, please repeat')