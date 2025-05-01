import unittest

from TBDquest_logic import Item
from TBDquest_logic import KeyItem
from TBDquest_logic import LockItem
from TBDquest_logic import Player
from TBDquest_logic import Room
from TBDquest_logic import get_game

class TestExamine(unittest.TestCase):

    def test_examine_happy_path_in_room(self):
        player1 = Player()
        test_room_1 = Room(1,"Test Room","this is a test room")
        player1.current_room = test_room_1
        generic_object = Item(1,"Perfectly generic object",True,"This is a perfectly generic object")
        test_room_1.add_item(generic_object)
        result = player1.examine_item("Perfectly generic object")

        self.assertEqual("This is a perfectly generic object", result)

    def test_examine_happy_path_in_inv(self):
        player2 = Player()
        generic_object = Item(1, "Perfectly generic object", True, "This is a perfectly generic object")
        player2.inventory.add(generic_object)
        result = player2.examine_item("Perfectly generic object")

        self.assertEqual("This is a perfectly generic object", result)

    def test_examine_failure(self):
        player3 = Player()
        test_room_3 = Room(1, "Test Room", "this is a test room")
        player3.current_room = test_room_3
        generic_object = Item(1, "Perfectly generic object", True, "This is a perfectly generic object")
        test_room_3.add_item(generic_object)
        result = player3.examine_item("pumpkin")

        self.assertEqual("pumpkin is not in your inventory or the room",result)

    def test_examine_room(self):
        test_room_3 = Room(1, "Test Room", "this is a test room")
        result = test_room_3.describe()

        self.assertEqual(f" You are currently in the Test Room. this is a test room",result)

class TestTakeItem(unittest.TestCase):

    def test_take_happy_path(self):
        player4 = Player()
        test_room_4 = Room(1,"Test Room","this is a test room")
        player4.current_room = test_room_4
        generic_object = Item(1,"Perfectly generic object",True,"This is a perfectly generic object")
        test_room_4.add_item(generic_object)
        message_result = player4.take_item("Perfectly generic object")
        inventory = set()
        result = inventory
        for item in player4.inventory:
            inventory.add(item.name)

        self.assertSetEqual(result,{"Perfectly generic object","hand"})
        self.assertEqual(message_result,"You pick up the Perfectly generic object")

    def test_take_failure_not_carry(self):
        player5 = Player()
        test_room_5 = Room(1,"Test Room","this is a test room")
        player5.current_room = test_room_5
        door = Item(1,"door",False,"A heavy metal door")
        test_room_5.add_item(door)
        message_result = player5.take_item("door")
        inventory = set()
        result = inventory
        for item in player5.inventory:
            inventory.add(item.name)

        self.assertSetEqual(result, {"hand"})
        self.assertEqual(message_result, "You can not pick up the door")

    def test_take_failure_not_in_room(self):
        player6 = Player()
        test_room_6 = Room(1, "Test Room", "this is a test room")
        player6.current_room = test_room_6
        generic_object = Item(1, "Perfectly generic object", True, "This is a perfectly generic object")
        test_room_6.add_item(generic_object)
        message_result = player6.take_item("pumpkin")
        inventory = set()
        result = inventory
        for item in player6.inventory:
            inventory.add(item.name)

        self.assertSetEqual(result,{"hand"})
        self.assertEqual(message_result,"pumpkin is not in the room")

class TestUseItem(unittest.TestCase):

    def test_use_happy_path_lock_in_room(self):
        player7 = Player()
        test_room_7 = Room(1, "Test Room", "this is a test room")
        player7.current_room = test_room_7
        test_lock = LockItem(1,"test lock",False,"This is a test lock",1,True)
        test_key = KeyItem(2,"test key",True,"This is a test key",1)
        player7.current_room.add_item(test_lock)
        player7.add_inv(test_key)
        player7.use_item("test key","test lock")

        self.assertEqual(test_lock.locked,False)

    def test_use_happy_path_lock_in_inv(self):
        player7 = Player()
        test_room_7 = Room(1, "Test Room", "this is a test room")
        player7.current_room = test_room_7
        test_lock = LockItem(1,"test lock",True,"This is a test lock",1,True)
        test_key = KeyItem(2,"test key",True,"This is a test key",1)
        player7.add_inv(test_lock)
        player7.add_inv(test_key)
        player7.use_item("test key","test lock")

        self.assertEqual(test_lock.locked,False)

    def test_use_failure_not_inv(self):
        player8 = Player()
        test_room_7 = Room(1, "Test Room", "this is a test room")
        player8.current_room = test_room_7
        test_lock = LockItem(1, "test lock", False, "This is a test lock", 1, True)
        message_result = player8.use_item("test key","test lock")

        self.assertEqual("test key is not in your inventory",message_result)
        self.assertEqual(test_lock.locked,True)

    def test_use_failure_not_in_room(self):
        player8 = Player()
        test_room_8 = Room(1, "Test Room", "this is a test room")
        player8.current_room = test_room_8
        test_key = KeyItem(1, "test key", True, "This is a test key", 1)
        test_lock = LockItem(2, "test lock", False, "This is a test lock", 1, True)
        player8.add_inv(test_key)
        message_result = player8.use_item("test key","test lock")

        self.assertEqual("test lock is not in the room",message_result)
        self.assertEqual(test_lock.locked,True)

    def test_use_failure_not_instance_key(self):
        player9 = Player()
        test_room_9 = Room(1, "Test Room", "this is a test room")
        player9.current_room = test_room_9
        pumpkin = Item(1,"pumpkin",True,"a pumpkin")
        test_lock = LockItem(2, "test lock", False, "This is a test lock", 1, True)
        player9.add_inv(pumpkin)
        player9.current_room.add_item(test_lock)
        message_result = player9.use_item("pumpkin","test lock")

        self.assertEqual("you don't see a way that pumpkin can be used",message_result)
        self.assertEqual(test_lock.locked, True)

    def test_use_failure_not_instance_lock(self):
        player10 = Player()
        test_room_10 = Room(1, "Test Room", "this is a test room")
        player10.current_room = test_room_10
        pumpkin = Item(1,"pumpkin",True,"a pumpkin")
        test_key = KeyItem(2, "test key", False, "This is a test key", 1)
        player10.add_inv(test_key)
        player10.current_room.add_item(pumpkin)
        message_result = player10.use_item("test key","pumpkin")

        self.assertEqual("you don't see a way that pumpkin can be used",message_result)

    def test_use_failure_key_not_lock(self):
        player11 = Player()
        test_room_11 = Room(1, "Test Room", "this is a test room")
        player11.current_room = test_room_11
        test_key = KeyItem(1, "test key", True, "This is a test key", 1)
        test_lock = LockItem(2, "test lock", False, "This is a test lock", 2, True)
        player11.current_room.add_item(test_lock)
        player11.add_inv(test_key)
        message_result = player11.use_item("test key","test lock")

        self.assertEqual("test key can not be used like that", message_result)
        self.assertEqual(test_lock.locked,True)

class TestGoTo(unittest.TestCase):
    def test_go_to_happy_path(self):
        player12 = get_game().get_player()
        test_room_12a = Room(1, "Test Room A", "this is a test room")
        test_room_12b = Room(2,"Test Room B","this is another test room")
        test_room_12a.add_adjacent_room(test_room_12b)
        test_room_12b.add_adjacent_room(test_room_12a)
        player12.current_room = test_room_12a
        message_result = player12.travel_to("Test Room B")

        self.assertEqual("You walk to Test Room B",message_result)
        self.assertEqual(player12.current_room,test_room_12b)

    def test_go_to_back_and_forth(self):
        player13 = get_game().get_player()
        test_room_12a = Room(1, "Test Room A", "this is a test room")
        test_room_12b = Room(2, "Test Room B", "this is another test room")
        test_room_12a.add_adjacent_room(test_room_12b)
        test_room_12b.add_adjacent_room(test_room_12a)
        player13.current_room = test_room_12a
        player13.travel_to("Test Room B")
        player13.travel_to("Test Room A")
        player13.travel_to("Test Room B")
        player13.travel_to("Test Room A")

        self.assertEqual(player13.current_room, test_room_12a)

    def test_go_to_failure(self):
        player14 = get_game().get_player()
        test_room14a = Room(1,"Test Room A","this is a test room")
        test_room_14b = Room(2, "Test Room B", "this is another test room")
        test_room_14b.add_adjacent_room(test_room14a)
        player14.current_room = test_room14a
        message_result = player14.travel_to("Test Room B")

        self.assertEqual("Test Room B can not be traveled to",message_result)
        self.assertEqual(player14.current_room,test_room14a)













