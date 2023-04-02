"# stevens-project1-515-adventure" 


# Classes
## Main_Engine
* The main class where the engine is coded
* This contains all the funcionalities

## inventory
* contains all the inventory operations and storage

---

---


# Functions 

### __play_game
* This is the location the game will be intitated
* Here the main logic and while loop is there
* Try catch is handled here 


---
## Input parsing 
### __global_action_regex_creator
* This is the function which will be creating the regex for all the action words
* The output of this function will be used in the validation of the action commands
* Output is a list of the strings which is required for regex 
* <h2> if you need to add a new command please add in the respective list </h2>

---
# Registering a new action

if you want to register a new function you will need to add it into either of the list :
* no_input_action : if no parameter is required for the action ( parameter are attributes which are required for the action )
* attribute_input_action: if a parameter is required for the action you will need to add into this list

This will create the custom regex and be registerd in the help also ( This is like the table which the Professor asked for )

then you will need to register the function of the <b> input_parser()</b>

Now if you have no attribute based action then the format will be 
<code>

elif re.search(self.regex_no_input_action_dict["action_name"], findall_list_user_input[0][0]):

</code>


# Architecture 
<img src="https://chargearth.com/static//images/cs515/map_architecture.png">