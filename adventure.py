import sys
import time
import json
import re

class inventory(object):  # inventory state management
    def __init__(self) -> None:
        super().__init__()
        self.inside_inventory = []


    def add(self, item):  # add item to inventory
        self.inside_inventory.append(item)

    def get(self, item):  # remove item from inventory
        self.inside_inventory.remove(item)


class Main_Engine(object):
    def __init__(self, file_name):  # constructor

        if (self.__getting_map(file_name)):
            self.which_room_index = 0
            self.__global_action_regex_creator()  # To create the regex for action words
            self.obj_inventory=inventory()
            self.__play_game()

    # Loading the map
    def __getting_map(self, file_name):  # internal function of the class to get the code
        try:
            with open(file_name) as json_file:
                # loading the list into the variable
                self.map_of_game_list = json.load(json_file)
        except Exception as e:
            self.printer("Please provde correct format of map")
            exit(1)
        try:
            if type(self.map_of_game_list) != list:  # checking type for defensive programming
                raise ValueError
        except Exception as e:
            self.printer("Please check the map file")
            return False
        return True

    # Printer based system
    def __name_beaut_str(self):
        return ("> "+self.map_of_game_list[self.which_room_index]["name"]+"\n")

    def _desc_beaut_str(self):
        return (self.map_of_game_list[self.which_room_index]["desc"]+"\n")

    def _exit__beaut_str(self):
        temp_dict = self.map_of_game_list[self.which_room_index]["exits"]
        temp_list = list(temp_dict.keys())
        if temp_list == []:
            return ("Exits: \n")
        else:
            return ("Exits: "+" ".join(temp_list)+"\n")

    def __items__beaut_str(self):
        if self.map_of_game_list[self.which_room_index].get("items"):
            temp_list = self.map_of_game_list[self.which_room_index]["items"]
            return ("Items: "+", ".join(temp_list)+"\n")
        else:
            return
        
    def __boss_text_beaut_str(self):
        return("\n End Level "+self.map_of_game_list[self.which_room_index].get("boss")+"\n")


    def room_context_printing(self):
        if self.map_of_game_list[self.which_room_index].get("boss"):
            self.printer(self.__boss_text_beaut_str())
        self.printer(self.__name_beaut_str())
        self.printer(self._desc_beaut_str())
        x = self.__items__beaut_str()
        if x != None:
            self.printer(x)
        
        self.printer(self._exit__beaut_str())

    def printer(self, str):
        try:
            # for c in str + '\n':
            #     sys.stdout.write(c)
            #     sys.stdout.flush()
            #     time.sleep(3./90)
            # for c in str + '\n':
            #     sys.stdout.write(c)
            #     sys.stdout.flush()
            # self.printer(str)
            print(str)
            return True
        except:
            return False

    # regex creation
    

    def __regex_creator_for_actions(self, action_list):
        temp_list = []
        for x in action_list:

            main_temp_string = ""
            for z in x:
                temp_string = "["+str(z).lower()+"|"+str(z).upper()+"]"
                main_temp_string = main_temp_string+temp_string
            temp_list.append("^"+main_temp_string+"$")

        return temp_list

    def __global_action_regex_creator(self):
        # New action command needed to added into this
        self.no_input_action = ["look", "inventory", "quit","help"]
        self.attribute_input_action = ["go", "get","drop"]
        

        regex_no_input_action_list = self.__regex_creator_for_actions(
            self.no_input_action)
        regex_attribute_input_action_list = self.__regex_creator_for_actions(
            self.attribute_input_action)

        # ziping the two no_input_action and regex_no_input_action so that we can get dictionary of values
        self.regex_no_input_action_dict = dict(
            zip(self.no_input_action, regex_no_input_action_list))

        self.regex_attribute_input_action_dict = dict(
            zip(self.attribute_input_action, regex_attribute_input_action_list))
        

    ### Helper function 
    def is_boss_room(self):
        if self.map_of_game_list[self.which_room_index].get("boss"): #helper function for winning condition
            return True 
        else:
            return False
        
    def what_is_required_for_winning(self):# helper function for the winning but to check if the user has the required items are not
        winning_condition=self.map_of_game_list[self.which_room_index]["winning"]
        for  i in winning_condition:
            if i in self.obj_inventory.inside_inventory:
                pass
            else:
                self.player_loose()
                return False # will not reach here as self.player_loose will exit if loose
        self.player_win_banner()
        return True # will not reach here as self.player_win_banner will exit if won
        
    
    def win_function(self):
        if self.is_boss_room():
            if self.what_is_required_for_winning():
                return True
            else: 
                return False
        else:
            return False
    
    def player_win_banner(self):
        #  Thanks to for ascii art https://www.asciiart.eu/people/occupations/kings
        print(r'''
        
                                                               o .,<>., o
                                                               |\/\/\/\/|
                                                               '========'
                                                               (_ SSSSSSs
                                                               )a'`SSSSSs
                                                              /_   SSSSSS
                                                              .=## SSSSS
                                                              .####  SSSSs
                                                              ###::::SSSSS
                                                             .;:::""""SSS
                                                            .:;:'  . .  \\
                                                           .::/  '     .'|
                                                          .::( .         |
                                                          :::)           \
                                                          /\(            /
                                                         /)            ( |
                                                       .'  \  .       ./ /
                                                    _-'    |\  .        |
                                  _..--..   .  /"---\      | ` |      . |
          -=====================,' _     \=(*#(7.#####()   |  `/_..   , (
                      _.-''``';'-''-) ,.  \ '  '+/// |   .'/   \  ``-.) \
                    ,'  _.-  ((    `-'  `._\    `` \_/_.'  )    /`-._  ) |
                  ,'\ ,'  _.'.`:-.    \.-'                 /   <_L   )"  |
                _/   `._,' ,')`;  `-'`'                    |     L  /    /
               / `.   ,' ,|_/ / \                          (    <_-'     \
               \ / `./  '  / /,' \                        /|`         `. |
               )\   /`._   ,'`._.-\                       |)            \'
              /  `.'    )-'.-,' )__)                      |\            `|
             : /`. `.._(--.`':`':/ \                      ) \             \
             |::::\     ,'/::;-))  /                      ( )`.            |
             ||:::::  . .::':  :`-(                       |/    .          |
             ||::::|  . :|  |==[]=:                       .        -       \
             |||:::|  : ||  :  |  |                      /\           `     |
 ___ ___     '|;:::|  | |'   \=[]=|                     /  \                \
|   /_  ||``|||:::::  | ;    | |  |                     \_.'\_               `-.
:   \_``[]--[]|::::'\_;'     )-'..`._                 .-'\``:: ` .              \
 \___.>`''-.||:.__,'     SSt |_______`>              <_____:::.         . . \  _/
                                                           `+a:f:......jrei"""
 __     __                            _   _                     _                              
 \ \   / /                           | | | |                   (_)                             
  \ \_/ /__  _   _    __ _ _ __ ___  | |_| |__   ___  __      ___ _ __  _ __  _ __   ___ _ __  
   \   / _ \| | | |  / _` | '__/ _ \ | __| '_ \ / _ \ \ \ /\ / / | '_ \| '_ \| '_ \ / _ \ '__| 
    | | (_) | |_| | | (_| | | |  __/ | |_| | | |  __/  \ V  V /| | | | | | | | | | |  __/ |    
    |_|\___/ \__,_|  \__,_|_|  \___|  \__|_| |_|\___|   \_/\_/ |_|_| |_|_| |_|_| |_|\___|_|    
                                                                                               
      
        
        ''')
        self.printer(self.map_of_game_list[self.which_room_index]["winning_text"])

        self.printer(r'''
     _       _       _      _______ _            ______ _   _ _____       _       _       _    
  /\| |/\ /\| |/\ /\| |/\  |__   __| |          |  ____| \ | |  __ \   /\| |/\ /\| |/\ /\| |/\ 
  \ ` ' / \ ` ' / \ ` ' /     | |  | |__   ___  | |__  |  \| | |  | |  \ ` ' / \ ` ' / \ ` ' / 
 |_     _|_     _|_     _|    | |  | '_ \ / _ \ |  __| | . ` | |  | | |_     _|_     _|_     _|
  / , . \ / , . \ / , . \     | |  | | | |  __/ | |____| |\  | |__| |  / , . \ / , . \ / , . \ 
  \/|_|\/ \/|_|\/ \/|_|\/     |_|  |_| |_|\___| |______|_| \_|_____/   \/|_|\/ \/|_|\/ \/|_|\/ 

  : Game Engine Created By Siddharth Jain    
        ''')

        # self.printer("******************** THE END ********************")
        exit(0)



    
    def player_loose(self):# helper function for loosing if the player dose not have item he will loose will be called in win_function()
       # banner from https://ascii.co.uk/art/skulls and https://onlineasciitools.com/convert-text-to-ascii-art
        print(r''' 
       ~~~~~~~~~
     /           \
    /             \
   | )           ( |
    \  /C\   /C\  /
    /  ~~~   ~~~  \
    \___  .^,  ___/
     `| _______ |'
  _   | HHHHHHH |   _
 ( )  \         /  ( )
(_) \  ~~~~^~~~~ ,/ (_)
  ~\ "\         /  /~
     \  \     /  /
       \  \v/  /
        >     <
       /  /^\  \
     /  /     \  \
 _~/ "/         \  \~_
( ) /             \ ( )
 (_)               (_)

  __     ______  _    _   _      ____   ____   _____ ______ 
 \ \   / / __ \| |  | | | |    / __ \ / __ \ / ____|  ____|
  \ \_/ / |  | | |  | | | |   | |  | | |  | | (___ | |__   
   \   /| |  | | |  | | | |   | |  | | |  | |\___ \|  __|  
    | | | |__| | |__| | | |___| |__| | |__| |____) | |____ 
    |_|  \____/ \____/  |______\____/ \____/|_____/|______|

        ''')
        print("Please Play again")
        exit(0)
        

   

    #### Operations 
     
    def __action_drop(self,get_item):
        if self.obj_inventory.inside_inventory!=[]:
            return self.is_item_in_inventory(get_item)
            # return False     
        else:
            self.printer("You're not carrying anything.")# Custom error 
            return False # TODO handle this

    def is_item_in_inventory(self,get_item):
        for i in self.obj_inventory.inside_inventory:
                get_item=get_item.strip()
                if i==get_item or i.lower()==get_item or i.upper()==get_item:# checking the input is in the inventory
                    temp_data=self.obj_inventory.inside_inventory.pop(self.obj_inventory.inside_inventory.index(get_item))
                    # print(temp_data)
                    if self.map_of_game_list[self.which_room_index].get("items"):
                        self.map_of_game_list[self.which_room_index]["items"].append(temp_data)
                    else:
                        self.map_of_game_list[self.which_room_index]["items"]=[]
                        self.map_of_game_list[self.which_room_index]["items"].append(temp_data)
                    return True # if found return True
        return False # if not found return False

    def __action_help(self):
        for i in self.attribute_input_action:
            print("  "+i+" ...")
        for i in self.no_input_action:
            print("  "+i)

    # to check if the go is possible
    def __go_action_is_it_possible(self, attribute):
        for index, i in enumerate(self.map_of_game_list[self.which_room_index]["exits"].keys()):
            if attribute.lower().strip() == i.lower().strip():
                value_of_key_in_map=i
                return True, index , value_of_key_in_map
        return False, "" ,""

    def __move_room(self, new_index):
        self.which_room_index = new_index

    def __action_go(self, attribute):
        # function to check if input is possible and get index of the new key
        possible, index_of_item,value_of_key_in_map = self.__go_action_is_it_possible(attribute)
        if possible:
            # to_index = list(self.map_of_game_list[self.which_room_index]["exits"].values())[
            #     index_of_item]  # get the index
            to_index = self.map_of_game_list[self.which_room_index]["exits"][value_of_key_in_map]
            self.__move_room(to_index)  # move the room
            self.printer(f"You go {value_of_key_in_map}.\n")
            return True
        else:
            # TODO integrate it with error spitting function
            self.printer(f"There's no way to go {attribute}.")
            return False

    def __action_quit(self):
        self.printer("Goodbye!")
        exit(0)

    def update_map(self,operation,item_name):
        if operation=="pop":
            for index,i in enumerate(self.map_of_game_list[self.which_room_index]["items"]):
                if i==item_name or i.lower()==item_name or i.upper()==item_name:
                    item_from_list=self.map_of_game_list[self.which_room_index]["items"].pop(index)# we can not trust user input
                    return item_from_list


    def __action_get(self,get_item):# get item action function :: 1
        
        if "items" in self.map_of_game_list[self.which_room_index]:
            if self.__get_me_items(item_name=get_item.strip()):# is item there 
                temp_item=get_item
                get_item=get_item.strip()
                item_from_list=self.update_map("pop",get_item)  # if there remove it from map
                self.add_item(item_from_list)# and add it to the inventory
                
                self.printer(f"You pick up the {temp_item}.")
              
            else:
                self.printer(f"There's no {get_item} anywhere.")# TODO ERROR 
                return False
        else:
            self.printer(f"There's no {get_item} anywhere.")#TODO ERROR output
            return False

    
                
    def __get_me_items(self,item_name=""):# to check the item :: 2 
        temp_list=self.map_of_game_list[self.which_room_index]["items"]
        if temp_list==[]:
            return False
        else:
            for i in temp_list:
                i=i.strip()
                if i==item_name or i.lower()==item_name or i.upper()==item_name:
                    return True
            return False
        

    def add_item(self,item_name): # add item to inventory:3
        self.obj_inventory.add(item_name)

    def __action_inventory(self):
        self.printer("Inventory:")
        for i in self.obj_inventory.inside_inventory:
            self.printer("  "+i)

    def input_parser(self):
        # parsing all the user input into this
        # will divide into a tuple having at into a tuple of having three index
        # will need to create all test cases where more than one
        # actions

        split_input_string = self.user_input.split()
        if len(split_input_string) > 1:
            findall_list_user_input = [("", split_input_string[0], " ".join(split_input_string[1:]))]
        elif len(split_input_string) == 1:
            findall_list_user_input = [(split_input_string[0], "", "")]
        else:
            findall_list_user_input = []

        # findall_list_user_input = re.findall(
        #     "^(?:\s*(\w+)\s*$)|^(?:\s*(\w+)\s+(.*)$)", self.user_input)
        if findall_list_user_input==[]:
            self.printer("Error, Please remove unnecessary character from parameters")
        elif  findall_list_user_input[0][0] != '' :
            if re.search(self.regex_no_input_action_dict["look"], findall_list_user_input[0][0]):
                # self.__lookup_actions()
                return True
                
            elif re.search(self.regex_no_input_action_dict["inventory"], findall_list_user_input[0][0]):
                # Link to inventory lookup function
                if self.obj_inventory.inside_inventory!=[]:
                    self.__action_inventory()
                    return False
                else:
                    self.printer("You're not carrying anything.")
                    return False
                
            elif re.search(self.regex_no_input_action_dict["quit"], findall_list_user_input[0][0]):
                self.__action_quit()
                
            elif re.search(self.regex_no_input_action_dict["help"], findall_list_user_input[0][0]):
                self.__action_help()
                return False
            else:
                # default
                # throw error no action like this
                # if those action which required parameters were not give so their custom functions need to be created
                if re.search(self.regex_attribute_input_action_dict["go"], findall_list_user_input[0][0]):
                    # TODO ERROR custom errror
                    self.printer("Sorry, you need to 'go' somewhere.")
                    return False
                if re.search(self.regex_attribute_input_action_dict["get"], findall_list_user_input[0][0]):
                    # TODO ERROR custom errror
                    self.printer("Sorry, you need to 'get' something.")
                    return False
                if re.search(self.regex_attribute_input_action_dict["drop"], findall_list_user_input[0][0]):
                    # TODO ERROR custom errror
                    if len(self.obj_inventory.inside_inventory)==[]:
                        self.printer("Sorry, you need to have something in inventory to drop something.")
                        return False
                    elif len(self.obj_inventory.inside_inventory)==[]:
                        self.printer("You have one item in inventory please specify the name")
                    else:
                        self.printer("Sorry, you need to give an item to drop")
                    # self.printer("Sorry, you need to have something in inventory to drop something.")
                    return False
                else:
                    self.printer("Error, Please give a correct input")
                return False
            return True
        # now to check those actions which will take arguments
        elif findall_list_user_input[0][0] == '' and findall_list_user_input[0][1] != '' and findall_list_user_input[0][2] != '':
            # To remove all white spaces from the input
            self.parameters_after_action = findall_list_user_input[0][2].strip()
            if re.search(self.regex_attribute_input_action_dict["get"], findall_list_user_input[0][1]):
                # link the function function go
           
                if (self.__action_get(findall_list_user_input[0][2])):
                    
                    return True
                else:
                    return False
                

            elif re.search(self.regex_attribute_input_action_dict["go"], findall_list_user_input[0][1]):
                return self.__action_go(self.parameters_after_action)
            elif re.search(self.regex_attribute_input_action_dict["drop"], findall_list_user_input[0][1]):
                # this will cotain function calling drop 
                if self.__action_drop(self.parameters_after_action):
                    self.printer(f"You drop the {findall_list_user_input[0][2]}.")
                    return False
            else:
                # write function to give error for action
                return False
           

        elif findall_list_user_input[0][0] == '' and findall_list_user_input[0][1] != '' and findall_list_user_input[0][2] == '':
            if re.search(self.regex_attribute_input_action_dict["get"], findall_list_user_input[0][1]):
                # custom error
                pass

            elif re.search(self.regex_attribute_input_action_dict["go"], findall_list_user_input[0][1]):
                # TODO ERROR custom
                self.printer("Sorry, you need to 'go' somewhere.")
            else:
                # generic error the action dose not exsists
                return False
            return False
        return False

    # Main game engine
    def __play_game(self):
        # starting_room = self.map_of_game_list[self.which_room_index]
        
        try:
            while (True):
                self.room_context_printing()
                self.win_function()
                flag = False
                while (True and not flag):
                    try:
                        self.user_input = input("What would you like to do? ")
                        flag = self.input_parser()
                    except EOFError:
                        self.printer("\nUse 'quit' to exit.")
        except KeyboardInterrupt:
            self.printer("\nYou pressed CTRL+C \n--------\nExiting\n--------")
            exit(0)

        # except Exception as e:  # TODO Add some data here
        #     self.printer(e)
        #     pass


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise NameError("Please provide a file in argrument")
    else:
        file_name = sys.argv[1]
    start = Main_Engine(file_name)
