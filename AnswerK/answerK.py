from answerK_func import *

greetings()
db = csv_to_dict("database.txt")
main_page(*main_menu(db))



