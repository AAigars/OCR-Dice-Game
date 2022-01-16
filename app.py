'''
    Dice Game - 20 Hour Project
        By AAigars (2019)
'''
import random, json, hashlib, inspect, itertools, time, os

'''
    Global Data
        Storing stuff I need to access globally from other classes.
    Keys/Values
        Accounts: An array which stores all of the logged in accounts, was gonna handle more than 2 but can't be bothered.
'''
globalData = {
    "Accounts": []
}

'''
    Functions
        These are the functions which are called by the menu class.

    Methods/Functions
        registerAccount: Registers your account, by using the Authentication Class.
        loginAccount: Logs into your account, by using the Authentication Class.
        playGame: Initalizes the Game class, adds all of the players in the global dictionary and starts the game.
'''
class Functions():
    def registerAccount():
        username = input("Enter the username: ")
        password = input("Enter the password: ")

        auth = Authentication()
        regRet = auth.registerAccount(username, password)
        if(regRet != False):
            print("Account has been registered.")
        else:
            print("Failed to register account.")

    def loginAccount():
        username = input("Enter the username: ")
        password = input("Enter the password: ")

        auth = Authentication()
        logRet = auth.loginAccount(username, password)
        if(len(globalData["Accounts"]) == 2):
            print("You have already logged in 2 accounts.")
        else:
            if(logRet != False):
                if(logRet in globalData["Accounts"]):
                    print("You have already logged into that account.");
                else:
                    print("You have logged in to " + logRet["Name"] + ".")
                    globalData["Accounts"].append(logRet)
            else:
                print("Incorrect username/password.")

    def playGame():
        if(len(globalData["Accounts"]) == 2):
            game = Game()
            game.createGame(5) # Max Rounds = 5
            for account in globalData["Accounts"]:
                game.createPlayer(account["Name"])
            game.startGame()
        else:
            print("You have not logged into 2 accounts.")

'''
    Authentication
        Handles all of the authentication, uses SHA-256 to hash the passwords so they are secure and not readable from a user.
    
    Methods/Functions
        getAccount: Loops through the accounts array and checks if the name of the account matches the argument.
        registerAccount: Hashes the password argument, creates a dictionary object and appends it to the accounts array and dumps to the json (accounts).
        loginAccount: Hashes the password argument, loops the account dictionary checks if the username and password match the parsed json object.
'''
class Authentication():
    def __init__(self):
        self.accounts = json.load(open("./accounts.json"));

    def getAccount(self, name):
        for account in self.accounts:
            if(account["Name"] == name):
                return name;

        return None;

    def registerAccount(self, name, password):
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest();

        for account in self.accounts:
            if(account["Name"] == name):
                return False

        self.accounts.append({
            "Name": name,
            "Password": hash
        });

        with open("./accounts.json", "w") as f:
            json.dump(self.accounts, f, sort_keys=True, indent=4);

        return self.getAccount(name)

    def loginAccount(self, name, password):
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest();

        for account in self.accounts:
            if(account["Name"] == name and account["Password"] == hash):
                return account

        return False

'''
    Game
        The actual main class which handles the whole game.

    Methods/Functions
        createGame: Creates a new dictionary with the keys "Current Round" and "Max Round".
        createPlayer: Appends a new dictionary to the players array, with "Name" and "Score".
        startGame: Handles the whole game aspect.
        calculateScore: Calculates the score, with the arguments given.
'''
class Game():
    def __init__(self):
        self.game = {};
        self.players = [];

    def createGame(self, maxRound):
        self.game = {
            "Current Round": 0,
            "Max Round": maxRound
        };

    def createPlayer(self, name, bot=False):
        self.players.append({
            "Name": name,
            "Score": 0
        });

    def startGame(self):
        plrIterator = itertools.cycle(self.players);

        for i, v in enumerate(range(self.game["Max Round"])):
            print("-----------------------------------------------------------")
            for x in range(2):
                curPlr = next(plrIterator);
                rolls = [random.randint(1, 6), random.randint(1, 6)];
                score = self.calculateScore(curPlr, rolls[0], rolls[1]);

                print("[-] Rolled 2 dice for {0} outcome {1} and {2}.".format(curPlr["Name"], rolls[0], rolls[1]));
                if(rolls[0] == rolls[1]):
                    rolls.append(random.randint(1, 6))
                    print("[!] {0} has rolled a double, the outcome of the third roll was {1} it has been added to the players score.".format(curPlr["Name"], rolls[2]))
                if(curPlr["Score"] < 0):
                    print("[#] {0} has reached below 0 score, the players score has been reset to 0.".format(curPlr["Name"]))
                    curPlr["Score"] = 0
                print("{0} Score: {1}\n".format(curPlr["Name"], curPlr["Score"]));
            if(i != self.game["Max Round"] - 1):
                input("Press Enter to start the new round.")
            else:
                winner = ""
                if(self.players[0]["Score"] > self.players[1]["Score"]):
                    winner = self.players[0]["Name"]
                else:
                    winner = self.players[1]["Name"] 
                print("-----------------------------------------------------------")
                print("[!] The game has finished.")
                print("Winner: {0}".format(winner))

    def calculateScore(self, plr, *args):
        retScore = 0;

        for roll in args:
            retScore += roll;

        if((retScore % 2) == 0):
            plr["Score"] += 10;
        else:
            plr["Score"] -= 5;

        return retScore;

'''
    Menu
        Handles all of the menu related stuff.

    Methods/Functions
        createMenu: Creates the menu.
'''
class Menu():
    def __init__(self):
        self.menuActive = True
        self.options = {
            0: ["Register Account", Functions.registerAccount],
            1: ["Login Account", Functions.loginAccount],
            2: ["Play Game", Functions.playGame]
        }
        self.createMenu()

    def createMenu(self):
        while self.menuActive:
            print("Welcome to the Dice Game.")
            
            for i, x in enumerate(self.options):
                print(i, ":", self.options[x][0])

            currentIndex = input("Enter the index for the option: ")
            try:
                currentIndex = int(currentIndex)
            except ValueError:
                print("You have not entered a integer for the index.")

            func = self.options[currentIndex][1];
            os.system("cls"); # Don't know a better solution for clearing screen.
            func();
            time.sleep(1);
            os.system("cls");

'''
    Main Entry Point
'''
menu = Menu()
menu.createMenu()