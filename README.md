# sjain70 (sjain70@stevens.edu) Siddharth Jain
# Project Adventure.py
"# stevens-project1-515-adventure" 


## Please open this file in a readme viewer 


### github : https://github.com/siddharth1998/stevens-project1-515-adventure

### Estimated Time :: 45 hours

### Testing :: Manual testing ( written at the end of readme)

### any bugs or issues you could not resolve :: NO

### an example of a difficult issue or bug and how you resolved : The assignment was easy on handling the parser was a difficult thing I first created regex then removed that and used split functionality

# Extensions 
Chosen Extensions:
1. Drop
2. Help
3. Winning and loosing

# Interesting stuff :
1. run the program using <code style="color:red;font-size:20px"> python3 adventure.py cyber.map cool </code>
* in above cool argument will change the printing type

# Classes
## Main_Engine
* The main class where the engine is coded
* This contains all the funcionalities

## inventory
* Contains all the inventory operations and storage

The main idea was to load the json file as an object and move around in the map rather than tackling each room. Then each operation is handled using methods in Main_Engine.

---

---


# Important Functions 

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


## __action_drop
* Handling the drop options from inventory append operation in the items list in map

## __action_go
* Handling the move operation and traverse <code>self.map_of_game_list </code>



## __action_get
* Handling the taking  of items from <code>self.map_of_game_list</code> into <code>inventory.inside_inventory</code>


## __action_quit
* Quit the Program


## __action_help
* Printing out the actions from the two mapping lists
<i> It is important to note that I could have class.__dict__ to get a new created function having specefic format like action__* where *= name of the action word</i>

## room_context_printing
* Function to handle look function and printing the state of the room

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


# Extensions 
Chosen Extensions:
1. Drop
2. Help
3. Winning and loosing

# Game Map Architecture 
<img src="https://chargearth.com/static//images/cs515/map_architecture.png"> 
<!-- Hosted on my site  -->
<h2><i>The game is about a hacker who is deployed in a russia to disable their capabilities to strike. ( No intentions to harm anyone's sentiments, I respect all humans from all around world, made this story to make it spicy ) </i></h2>

<hr>
<hr>

## Winning Condition
There is no game without winning and loosing:
To win in this game engine you must have certain items which should be there 
as per the format the winning dictionary should look like 

In this room if the player enters, the player will have no control, if they collect the items in the game then only the game outcome will be achived, if suppose the items are not collected then player will loose, and suppose they have the items which are prohibited are in their inventory then also they will loose, they will have to <code>drop</code> it.

<code>{</br>"name": "name of room",</br>
  "desc": "description of activities going on in the last room ",</br>
  "exits": { "south":7},</br>
  "boss":"True",</br>
  "winning_text":" Bam Bam, You used the Desert Eagle gun to kill those soldiers, and inserted the malware, \n the Navy seal team blasted open the ceiling to help you come out, malware has spread through the interconnected networks, we have saved the world, the world owes you a debt agent 'SHOGUN'",</br>
  "winning":["system intel","id card","USB","Desert Eagle Gun"]</br>
  "not_to_have":["cyanide", "lighter","vodka"]</br>
 }</code>

To create a winning room you will need to add <br>
"boss":"True",<-- This denotes winning room will print out the endlevel note</br> 
"winning_text":"bla bla"  <-- This denotes the text after winning </br>
"winning": ["a","b"] <-- The items required for winning  </br>
"not_to_have": ["c","d"] <-- The items which should not be there in the inventory </br>

## My game cyber.map

The game is simple where you will need to collect some items and drop some items, if you collect it in the gameplay, to win: if you have the following items you will win : "system intel","id card","USB","Desert Eagle Gun" and reach the end room  or else loose, apart from that you will need to drop items like :  "cyanide", "lighter","vodka" if you have taken it or else you will loose. You will have to drop the items in any room before reaching the end room. You will get a warning room also so that players can be cautioned about it.

I could have made more things in it but the time constraint was a problem.


## Things which can be different :
* When getting an item having case sensitive items like getting "ROSE", "rose" </br>
Now if you type <code>get ROSE</code> then => in inventory ROSE will go, now if you type <code> get ROSE </code> then => rose will go into inventory


<hr>

## Test Cases

1. Note that case does not matter for any verbs, and arbitrary whitespace is allowed. ( Solved using regex stored in <code> findall_list_user_input </code> )
2. If there is no exit in that direction, go should give an error message.  ( Solved in <code> __action_go </code>)
3. If Uppercase GO with uppercase direction is given then You go direction in map is given which is the exact item in dictionary.
4. When a player successfully goes to a new room, you should show that room’s description ( Solved as in point 2)
5. Look is showing the same state
6. Trying to get things that aren’t there should produce an error message. 
7. Quit testing with CTRL+D and CTRL+C
8. Help is giving correct '...' for the correct option
9. Help spits out dynamically ( I used a 2 lists which acted as a table ) in list : <code> no_input_action </code> will contain all the action key words with no parameters and <code> attribute_input_action </code> will contain the action keywords which require parameters
10. Drop action is working and the transfer of element from inventory to map is working, if no items then give error.
11. Winning condition is also working. Both winning and loosing have been tested

# Future work 
* Auto complete
* More work on the story
* Interaction like : attack, trade etc
