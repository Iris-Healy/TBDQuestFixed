import TBDquest_logic

start_room = Room(1,"start", "this is a test room")
perfectly_generic_object = Item(1, "Perfectly Generic Object","A Perfectly Generic Object")
start_room.add_item(perfectly_generic_object)

game = Game()
game.start_game()