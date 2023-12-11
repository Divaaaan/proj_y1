class user_data:
    def __init__(self, id, name_from_file):
        self.id = id
        self.name_from_file = name_from_file


def init():
    global list_of_users_with_pass
    list_of_users_with_pass = []

