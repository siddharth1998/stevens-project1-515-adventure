import sys
import json

class inventory(object):
    def __init__(self) -> None:
        super().__init__()
        self.inside_inventory=[]
    
    def get(self,item):# add item to inventory 
        self.inside_inventory.append(item)
    
    def get(self,item): # remove item from inventory
        self.inside_inventory.remove(item)

class Main_Engine(object):
    def __init__(self,file_name):
        
        self.__getting_map(file_name)

    def __getting_map(self,file_name):#internal function of the class to get the code
        try:
            with open(file_name) as json_file:
                map_of_game_list=json.load(json_file)
            # opened_file=open(file_name)
        except Exception as e :
            print("Please provde correct format of map")
            exit(1)
        try:
            if type(map_of_game_list)!=list:
                raise ValueError
        except Exception as e:
            print("Please check the map file")
        for i in map_of_game_list:
            print(i)
        

        
if __name__=="__main__":
    

    if len(sys.argv)==1:
        raise NameError("Please provide a file in argrument")
    else:
        file_name=sys.argv[1]
    start=Main_Engine(file_name)
    # start.getting_map(file_name)
    print(file_name)