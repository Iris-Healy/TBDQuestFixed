
class Item:
    '''defines the class item taking an Item ID item name description and a boolean if it can be picked up or not'''
    def __init__(self, iid:int, item_name:str, carry:bool, description:str):
        self.iid = iid
        self.name = item_name
        self.description = description
        self.carry = carry

class KeyItem(Item):
    '''defines a key item adding a key value'''
    def __init__(self, iid:int, item_name:str, carry:bool, description:str, key:int):
        super().__init__(iid, item_name, carry, description)
        self.iid = iid
        self.name = item_name
        self.description = description
        self.carry = carry
        self.key = key

class LockItem(Item):
    '''defines a lock item adding attributes for lock value and a boolean for locked'''
    def __init__(self,iid:int, item_name:str, carry:bool, description:str, lock:int, locked:bool):
        super().__init__(iid, item_name, carry, description)
        self.iid = iid
        self.name = item_name
        self.description = description
        self.carry = carry
        self.lock = lock
        self.locked = locked

class Room:
    """Class that defines game rooms holding Items and connected to adjacent rooms"""
    def __init__(self, rid:int, name:str, description:str):
        self.rid = rid
        self.name = name
        self.description = description
        self.room_items = []
        self.adjacents = []

    def describe(self):
        '''function for describing the room a player is in'''
        print(f" You are currently in the {self.name}. {self.description}")

    def add_item(self, i: Item):
        '''function for adding an item to a room'''
        self.room_items.append(i)

    def add_adjacent_room(self, adjacent_room):
        '''function for adding an exit to the room'''
        self.adjacents.append(adjacent_room)

    def get_adjacent_rooms(self):
        '''getter for accessing adjacent rooms'''
        return self.adjacents

class Player:
    '''player initialization'''
    def __init__(self):
        self.inventory = set()
        self.current_room = start_room
        self.inventory.add(hand)

    def input_command(self):
        '''handles inputting command stripping player input and making it lowercase'''
        command = input(">").strip().lower()
        self.process_command(command)

    def process_command(self, command):
        '''Processing for commands'''
        if command == "take":
            item_name = input(f"Which item do you wish to take\n >")
            self.take_item(item_name)

        elif command == "check inventory":
            #check inv returns all items in your inventory
            print("Your inventory contains:")
            for item in self.inventory:
                print(item.name)

        elif command == "examine item":
            #calls examine_item function
            examine_target = input(f"What would you like to examine\n >")
            self.examine_item(examine_target)

        elif command == "examine room":
            #prints the description of the room the player is in
            print(self.current_room.description)

        elif command == "use":
            #calls the use_item function taking player input for the key and lock targets
            key_target = input("Which item would you like to use\n >")
            lock_target = input("Which item would you like to use it on\n >")
            self.use_item(key_target,lock_target)

        elif command == "go":
            #calls the go function taking user input as the go target
            go_target = input("Where would you like to go? \n >")
            self.travel_to(go_target)

        elif command == "exit":
            #calls the get gamestate setter to set playing to false exiting the loop
            Game.set_gamestate(game,False)

        elif command == "help":
            #lists commands for the player
            print(f"commands are listed as followed\n"
                  f" go - travel to new room \n"
                  f" take - appends item to your inventory \n"
                  f" check inventory - list contents of your inventory \n"
                  f" use - use a item on something \n"
                  f" examine item - examines an item in room or inventory \n"
                  f" examine room - examines the room you are currently in \n"
                  f" save - saves the game state \n"
                  f" load - loads game from last save \n"
                  f" exit - exits the game")

    def take_item(self, item_name):
        '''take item function takes input from player in '''
        i_found = False
        #loops through items in current room searching for an item name that matches player com
        for item in self.current_room.room_items:
            if item.name == item_name and item.carry == True:
                i_found = True
                self.inventory.add(item)
                self.current_room.room_items.remove(item)
            elif item.name == item_name and item.carry == False:
                print(f"You can not pick up the {item_name}")
        if i_found:
            print(f"You pick up the {item_name}")
        if not i_found:
            print(f"{item_name} is not in the room")

    def examine_item(self, examine_target):
        e_item = None
        for examined_item in self.current_room.room_items:
            if examined_item.name == examine_target:
                e_item = examined_item
        for examined_item in self.inventory:
            if examined_item.name == examine_target:
                e_item = examined_item
        if e_item is not None:
            print(e_item.description)
        else:
            print(f"{examine_target} is not in your inventory or the room")

    def travel_to(self, go_target):
        g_room = None
        for room in Room.get_adjacent_rooms(self.current_room):
            if room.name == go_target:
                g_room = room

        if g_room is not None:
            Player().current_room = g_room
            print(f"You walk to the {g_room.name}")
        else:
            print(f"{go_target} can not be traveled to")

    def use_item(self, key_target, lock_target):
        key = None
        lock = None
        k_found = False
        l_found = False
        for k_item in self.inventory:
            if k_item.name == key_target:
                key = k_item
                k_found = True
        for l_item in self.current_room.room_items:
            if l_item.name == lock_target:
                lock = l_item
                l_found = True

        if not k_found:
            print(f"{key_target} is not in your inventory")
        elif not l_found:
            print(f"{lock_target} is not in the room")
        elif not isinstance(key,KeyItem):
            print(f"you don't see a way that {key_target} can be used")
        elif not isinstance(lock,LockItem):
            print(f"you don't see a way that {lock_target} can be used")
        elif key.key != lock.lock:
            print(f"{key.name} can not be used like that")
        elif key.key == lock.lock:
            lock.locked = False

        if not lock1.locked:
            print(f"The lock falls off the door you should be able to open it now")
        if not lock1.locked and not door1.locked:
            print(f"The door swings open revealing an entrance to another room")
            start_room.add_adjacent_room(test_room1)


class Game:
    def __init__(self):
        self.player = Player()
        self.current_room = start_room
        self.playing = True

    def get_gamestate(self):
        return self.playing

    def set_gamestate(self,x:bool):
        self.playing = x

    def start_game(self):
        print("you awake in a strange room you don't remember anything")
        while self.playing:
            self.player.input_command()
            self.player.process_command(self)
            if not self.playing:
                print(f"Thank you for playing!")
                break



start_room = Room(1, "start room", "The room is very plain there is a door to the north with a lock on it."
                                           "Above the door there is a sign reading Test Chamber 1"
                                           " there is a pumpkin on the floor in the center of the room."
                                           " to the west there is a console on the wall", )
test_room1 = Room(2,"Test Chamber 1","this is a test room")
hand = KeyItem(0,"hand",True,"your hand",0)
pumpkin = Item(1, "pumpkin", True, "what pumpkin? there is a shiny copper key on the floor")
console = Item(2, "console", False, "its stuck to the wall", )
key1 = KeyItem(3, "key", True, "a shiny key", 1, )
lock1 = LockItem(4, "lock", True, "A padlock on a door", 1, True)
door1 = LockItem(5,"door",False,"A generic metal door",0,True)
start_room.add_item(pumpkin)
start_room.add_item(console)
start_room.add_item(key1)
start_room.add_item(lock1)
start_room.add_item(door1)

game = Game()
game.start_game()

