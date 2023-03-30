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
        # string manipulation for exits into lowercase for all character
        # for i in self.map_of_game_list:
        #     temp_dict={}
        #     for z in list(i["exits"]):
        #         temp_dict[z[0].lower()]=z[1]
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
            return 0
        else:
            return ("Exits: "+" ".join(temp_list)+"\n")

    def __items__beaut_str(self):
        if self.map_of_game_list[self.which_room_index].get("items"):
            temp_list = self.map_of_game_list[self.which_room_index]["items"]
            return ("Items: "+", ".join(temp_list)+"\n")
        else:
            return

    def room_context_printing(self):
        self.printer(self.__name_beaut_str())
        self.printer(self._desc_beaut_str())
        x = self.__items__beaut_str()
        if x != None:
            self.printer(x)
        self.printer(self._exit__beaut_str())

    def printer(self, str):
        try:
            for c in str + '\n':
                sys.stdout.write(c)
                sys.stdout.flush()
                time.sleep(3./90)
            # self.printer(str)
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
        no_input_action = ["look", "inventory", "quit"]
        attribute_input_action = ["go", "get"]

        regex_no_input_action_list = self.__regex_creator_for_actions(
            no_input_action)
        regex_attribute_input_action_list = self.__regex_creator_for_actions(
            attribute_input_action)

        # ziping the two no_input_action and regex_no_input_action so that we can get dictionary of values
        self.regex_no_input_action_dict = dict(
            zip(no_input_action, regex_no_input_action_list))

        self.regex_attribute_input_action_dict = dict(
            zip(attribute_input_action, regex_attribute_input_action_list))

    # to check if the go is possible
    def __go_action_is_it_possible(self, attribute):
        for index, i in enumerate(self.map_of_game_list[self.which_room_index]["exits"].keys()):
            if attribute.lower() == i.lower():
                return True, index
        return False, ""

    def __move_room(self, new_index):
        self.which_room_index = new_index

    def __action_go(self, attribute):
        # function to check if input is possible and get index of the new key
        possible, index_of_item = self.__go_action_is_it_possible(attribute)
        if possible:
            to_index = list(self.map_of_game_list[self.which_room_index]["exits"].values())[
                index_of_item]  # get the index
            self.__move_room(to_index)  # move the room
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
            for i in self.map_of_game_list[self.which_room_index]["items"]:
                if i.lower()==item_name:
                    self.map_of_game_list[self.which_room_index]["items"].pop(self.map_of_game_list[self.which_room_index]["items"].index(item_name))
                    return True

    

    def __action_get(self,get_item):# get item action function :: 1
        
        if "items" in self.map_of_game_list[self.which_room_index]:
            
            if self.__get_me_items(item_name=get_item.lower()):# is item there 
                temp_item=get_item
                get_item=get_item.lower()
                self.update_map("pop",get_item)  # if there remove it from map
                self.add_item(get_item)# and add it to the inventory
                self.printer(self.printer(f"You pick up the {temp_item}"))
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
                if i.lower().strip()==item_name.strip():
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

        findall_list_user_input = re.findall(
            "^(?:(\w+)\s*$)|^(?:(\w+)\s+(\w+\s*[\w\s,]*)$)", self.user_input)
        if findall_list_user_input==[]:
            self.printer("Error, Please give a correct input")
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
                pass
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
                else:
                    self.printer("Error, Please give a correct input")
                return False
            return True
        # now to check those actions which will take arguments
        elif findall_list_user_input[0][0] == '' and findall_list_user_input[0][1] != '' and findall_list_user_input[0][2] != '':
            # To remove all white spaces from the input
            self.parameters_after_action = findall_list_user_input[0][2].strip(
            )
            if re.search(self.regex_attribute_input_action_dict["get"], findall_list_user_input[0][1]):
                # link the function function go
                if (self.__action_get(findall_list_user_input[0][2])):
                    return True
                else:
                    return False
                

            elif re.search(self.regex_attribute_input_action_dict["go"], findall_list_user_input[0][1]):
                return self.__action_go(self.parameters_after_action)
            else:
                # write function to give error for action
                return False
            return True

        elif findall_list_user_input[0][0] == '' and findall_list_user_input[0][1] != '' and findall_list_user_input[0][2] == '':
            if re.search(self.regex_attribute_input_action_dict["get"], findall_list_user_input[0][1]):
                # custom error
                pass

            elif re.search(self.regex_attribute_input_action_dict["go"], findall_list_user_input[0][1]):
                # TODO ERROR custom
                self.printer("Sorry, you need to 'go' somewhere.")
                pass
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
                flag = False
                while (True and not flag):
                    try:
                        self.user_input = input("What would you like to do?  ")
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
