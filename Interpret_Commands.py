import Format_Manager
import random
#import Arduino_Manager
import List_Manager
import Command_List

def commandhandler(text, Octavius_Vocab, Octavius_Lists, Octavius_Grammar, Octavius_Receiver, Octavius_Camera_Manager, Octavius_RF_Manager):
    
    inputcommand = Format_Manager.lowercase_word(text)

    #If received message is a question or expression of gratitude (real or sarcastic) respond accordingly
    if Octavius_Grammar.is_question(inputcommand):
        Octavius_Receiver.send_message("I don't know how to answer questions yet")
        return

    elif inputcommand in Octavius_Vocab.gratitude:
        Octavius_Receiver.send_message("I am what my master made me")
        return

    #otherwise
    else:
        #split message into words
        command = Format_Manager.split_sentence(inputcommand)
        print(f'Received command: {inputcommand}')
        #Octavius_Receiver.send_message(f'Received command: {inputcommand}')
        print(len(command))

        #if message is one word long
        if len(command) == 1:
            action = command[0]
            #if word is talk, talk
            if action == 'talk':
                Command_List.talk(Octavius_Receiver)
                return
                
            if action == 'photo':
                image_file = Octavius_Camera_Manager.Take_Picture()
                Octavius_Receiver.send_image(image_file)
                return

            #if word is a greeting, respond
            elif action in Octavius_Vocab.greetings:
                word = random.randint(0, len(Octavius_Vocab.greetings) - 1)
                Octavius_Receiver.send_message(f'{Octavius_Vocab.greetings[word]}')
                return
            #otherwise indicate lack of understanding
            else:
                Octavius_Receiver.send_message("Command not recognised, please repeat")
                return


        #if message is two words long
        elif len(command) == 2:
            target = command[0]
            action = command[1]
            
            #if target is a number, convert to an integer
            if target.isnumeric():
                target = int(target)
                
            if action.isnumeric():
                action = int(action)
                
            if target == 'video' and action%1 == 0 and action != 0:
                Octavius_Receiver.send_message("Capturing video...")
                video_file = Octavius_Camera_Manager.Take_Video(action)
                Octavius_Receiver.send_message("Video captured, sending...")
                Octavius_Receiver.send_video(video_file)
                Octavius_Receiver.send_message("Video sent...")
                return
            
            if 'on' in action or 'off' in action:
                
                #if target includes 'lights' (plural)
                if target == 'lights':
                    Command_List.All_Lights(action, Octavius_Lists, Octavius_Receiver)
                    return
                    
                #if target contains 'light'(singular) 
                elif target == 'light':
                    Command_List.Ceiling_Light(action, Octavius_Receiver)
                    return
                
                #if target contains a name from the device list or 'all'
                elif (target in Octavius_Lists.devices or target == 'all' or (target >= 1 and target <= 5)):
                    #send command to arduino to activate specified device
                    Octavius_Receiver.send_message(f"Turning {target} {action}")
                    Octavius_RF_Manager.Code_Picker(Octavius_Lists.devicelist, target, action)
                    #Arduino_Manager.generateserialcommand(Octavius_Lists.devicelist, target, action)
                
                #if message contains 'on' or 'off, but the other word is not a device, ask if user would like to update device list
                else:
                    Octavius_Receiver.send_message(f"I did not recognise that command, would you like to update device list?")
                    #if response is affirmative, start updating device list
                    if Octavius_Receiver.get_confirmation(Octavius_Vocab):
                        Octavius_Lists = Octavius_Lists.updatedevicelist(Octavius_Receiver, Octavius_Vocab)
                    #otherwise exit
                    else:
                        Octavius_Receiver.send_message(f'Acknowledged, please repeat original command')

            #if message contains 'create' or 'write' or 'new' and 'list'
            elif ('new' in target or 'create' in target or 'write' in target or 'add' in target) and 'list' in action:
                Octavius_Lists.Create_New_List(Octavius_Vocab, Octavius_Receiver)
                
            #if message contains 'read'
            elif 'read' in target or 'list' in target:
                
                #if asked to read out lists/reminders, do so
                if 'lists' in action or 'reminders' in action:
                    Octavius_Receiver.send_message(f'Current lists:')
                    for x in Octavius_Lists.listdict.keys():
                        Octavius_Receiver.send_message(x)

                #if 'device' in input command (message is 'read devicelist' etc)
                elif 'device' in action:
                    List_Manager.Read_List(Octavius_Lists.devices, Octavius_Receiver)
                
                #if asked to read a specific reminder list, do so
                elif action in Octavius_Lists.listdict.keys():
                    List_Manager.Read_List(Octavius_Lists.listdict[action], Octavius_Receiver)

                    

            #if message contains 'update'
            elif 'update' in inputcommand:
                #and 'device, start updating device list
                if 'device' in inputcommand:
                    Octavius_Lists = Octavius_Lists.updatedevicelist(Octavius_Receiver, Octavius_Vocab)
                    return
                #or 'affirmative', start updating affirmatives (this will be replaced with a more useful function)
                elif 'affirmative' in inputcommand:
                    Octavius_Vocab = Octavius_Vocab.updateaffirmatives(Octavius_Receiver)
                    

                    
        #if message contains more words, do not understand
        else:
            Octavius_Receiver.send_message(f'Command not recognised, please repeat')
