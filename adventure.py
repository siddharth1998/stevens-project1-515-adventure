import sys
import time
import json
import re


class inventory(object):  # inventory state management
    def __init__(self) -> None:
        super().__init__()
        self.inside_inventory = []

    def get(self, item):  # add item to inventory
        self.inside_inventory.append(item)

    def get(self, item):  # remove item from inventory
        self.inside_inventory.remove(item)


class Main_Engine(object):
    def __init__(self, file_name):  # constructor

        if (self.__getting_map(file_name)):
            self.which_room_index = 0
            self.__global_action_regex_creator()  # To create the regex for action words
            self.__play_game()

    def __getting_map(self, file_name):  # internal function of the class to get the code
        try:
            with open(file_name) as json_file:
                # loading the list into the variable
                self.map_of_game_list = json.load(json_file)

        except Exception as e:
            print("Please provde correct format of map")
            exit(1)
        try:
            if type(self.map_of_game_list) != list:  # checking type for defensive programming
                raise ValueError
        except Exception as e:
            print("Please check the map file")
            return False
        # string manipulation for exits into lowercase for all character
        # for i in self.map_of_game_list:
        #     temp_dict={}
        #     for z in list(i["exits"]):
        #         temp_dict[z[0].lower()]=z[1]

        return True

    def update_room(self):  # function to update the room
        pass

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
            return ("Exits: "+" ".join(temp_list))
        # return(self.temp_list)
    

    def __play_game(self):
        # starting_room = self.map_of_game_list[self.which_room_index]
        try:
            while(True):
                self.printer(self.__name_beaut_str())
                self.printer(self._desc_beaut_str())
                self.printer(self._exit__beaut_str())
                self.user_input = input("What would you like to do?  ")
                self.input_parser()
                

        except Exception as e:  # TODO Add some data here
            print(e)
        # while (True):

    def printer(self, str):
        try:
            # for c in str + '\n':
            #     sys.stdout.write(c)
            #     sys.stdout.flush()
            #     time.sleep(3./90)
            print(str)
            return True
        except:
            return False

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

    def __go_action_is_it_possible(self,attribute):  # to check if the go is possible
        for index,i in enumerate(self.map_of_game_list[self.which_room_index]["exits"].keys()):
            if attribute.lower() == i.lower():
                    return True,index
        return False,""
      
    def __move_room(self,new_index):
        self.which_room_index=new_index

    def __action_go(self,attribute):
       print(attribute)
       possible,index_of_item=self.__go_action_is_it_possible(attribute)# function to check if input is possible and get index of the new key
       if possible:
           to_index=list(self.map_of_game_list[self.which_room_index]["exits"].values())[index_of_item]# get the index
           self.__move_room(to_index)# move the room
       else:
           print("please give correct parameter")# TODO integrate it with error spitting function 
                



    def input_parser(self):
        # parsing all the user input into this
        # will divide into a tuple having at into a tuple of having three index
        # will need to create all test cases where more than one
        # actions

        findall_list_user_input = re.findall(
            "^(?:(\w+)\s*$)|^(?:(\w+)\s+(\w+\s*[\w\s,]*)$)", self.user_input)
        if findall_list_user_input[0][0] != '':
            if re.search(self.regex_no_input_action_dict["look"],findall_list_user_input[0][0]):
                # link to look function 
                pass
            elif re.search(self.regex_no_input_action_dict["inventory"],findall_list_user_input[0][0]):
                # Link to inventory lookup function 
                pass
            elif re.search(self.regex_no_input_action_dict["quit"],findall_list_user_input[0][0]):
                # link to quit user function
                pass
            else:
                # default
                # throw error no action like this 
                print("Error")# TODO remove this 
                pass
        #now to check those actions which will take arguments
        elif findall_list_user_input[0][0] =='' and findall_list_user_input[0][1]!='' and findall_list_user_input[0][2]!='':
            # To remove all white spaces from the input 
            self.parameters_after_action=findall_list_user_input[0][2].strip()
            if re.search(self.regex_attribute_input_action_dict["get"],findall_list_user_input[0][1]):
                # link the function function go 
                pass

            elif re.search(self.regex_attribute_input_action_dict["go"],findall_list_user_input[0][1]):
                self.__action_go(self.parameters_after_action)
                
        elif findall_list_user_input[0][0] =='' and findall_list_user_input[0][1]!='' and findall_list_user_input[0][2]=='':
            if re.search(self.regex_attribute_input_action_dict["get"],findall_list_user_input[0][1]):
                # custom error 
                pass

            elif re.search(self.regex_attribute_input_action_dict["go"],findall_list_user_input[0][1]):
                # custom error 
                pass
            else:
                # generic error the action dose not exsists
                pass
           

    # def go_actions(self, choice_key: str):
    #     # TODO put in input parser Note that case does not matter for any verbs, and arbitrary whitespace is allowed.
    #     # TODO check the choice of the key is correct.

    #     self.which_room_index = self.map_of_game_list[self.which_room_index]["exits"][choice_key]

    #     print(self.which_room_index)

    #     return (True)
        # choice_key=str(choice_key).lower()
        # temp_list_extis=list(list(self.map_of_game_list[self.which_room_index][""]))
        # temp_list_extis=map(lambda x : (str(x)).lower(),temp_list_extis)



if __name__ == "__main__":

    if len(sys.argv) == 1:
        raise NameError("Please provide a file in argrument")
    else:
        file_name = sys.argv[1]
    start = Main_Engine(file_name)
    # start.getting_map(file_name)
