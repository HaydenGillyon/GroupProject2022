"""
!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!

Only run tests if there are no currently active games.
"""

from os import listdir, remove
import pickle
import sys

sys.path.append('../game_code')

import pre_game

import unittest


class TestGameclassFunctions(unittest.TestCase):

    def setUp(self):
        self.t1 = pre_game.Game("test")

    def test_create_code(self):
        assert type(self.t1.code) is int, "Code isn't an integer"
        assert len(str(self.t1.code)) == 4, "Code is the wrong length"


class TestCreatingLobby(unittest.TestCase):

    def setUp(self):
        self.t1 = TestRequest(None)
        self.t2 = TestRequest(3)
        self.t3 = TestRequest("test")

    def test_null_username(self):
        assert pre_game.create_lobby(self.t1) is False, "A null username created a lobby"

    def test_int_username(self):
        assert pre_game.create_lobby(self.t2) is False, "An integer username created a lobby"

    def test_valid_username(self):
        pre_game.create_lobby(self.t3)
        files = listdir("../game_code/active_games")

        assert len(files) == 1, "A lobby wasn't created with a valid username"

        with open("../game_code/active_games/" + files[0], "rb") as file:
            game = pickle.load(file)

        assert game.host.username == "test", "The host username is incorrect"

    def tearDown(self):
        files = listdir("../game_code/active_games")
        for x in files:
            remove("../game_code/active_games/" + x)


class TestLobbyJoin(unittest.TestCase):
    
    def setUp(self):
        self.t1 = TestRequest("test")
        self.t2 = TestRequest("test")
        self.t3 = TestRequest("test")

        self.host = TestRequest("host")
        

    def test_null_code(self):
        assert pre_game.join_lobby(self.t1, None) is False, "Joined lobby with null code"

    def test_wrong_code(self):
        assert pre_game.join_lobby(self.t2, 0000) is False, "Joined lobby with wrong code"

    def test_right_code(self):
        pre_game.create_lobby(self.host)
        files = listdir("../game_code/active_games")
        code = int(files[0][:4])
        assert pre_game.join_lobby(self.t3, code) is True, "Didn't join lobby with right code"

    def tearDown(self):
        files = listdir("../game_code/active_games")
        for x in files:
            remove("../game_code/active_games/" + x)


class TestRequest:

    def __init__(self, name):
        self.session = {'username': name}

if __name__ == "__main__":
    unittest.main()
