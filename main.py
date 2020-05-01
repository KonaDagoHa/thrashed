# THRASHED: Endless fighting!

from random import randint, randrange, choice

# Each offensive and defensive action is stored as a tuple (damage multiplier, armor multiplier)
offense = {
    "punch": (1, 0),
    "stab": (1, 0),
    "slash": (2, 1),
    "bash" :(1, 2)
}

defense = {
    "block": (0, 1),
    "parry": (1, 1),
    "dodge": (0, 1),
    "brace": (0, 2)
}

# Each weapon is stored as a tuple (durability, max damage, max armor, offensive actions, defensive actions, duplicates)
# Durability decreases by 1 after each kill
weapons = {
    "fists": [-1, 1, 1, "punch", "block", 0],
    "dagger": [3, 2, 2, "stab", "dodge", 0],
    "sword": [3, 3, 2, "slash", "parry", 0],
    "shield": [3, 2, 3, "bash", "brace", 0],
    "fork": [3, 4, 4, "stab", "parry", 0]
}

# Player starts at level 1 with 5 health
player = {
    "name": "",
    "level": 1,
    "health": 5,
    "weapons": ["fists"],
    "kills": 0,
    "deaths": 0,
    "xp": 0,
    "levelUp": 10
}

# Enemies
goblin = {
    "name": "goblin",
    "level": 1,
    "health": 3,
    "weapons": ["fists", "dagger", "sword", "shield"]
}

skeleton = {
    "name": "skeleton",
    "level": 1,
    "health": 3,
    "weapons": ["fists", "dagger", "sword", "shield"]
}

zombie = {
    "name": "skeleton",
    "level": 1,
    "health": 3,
    "weapons": ["fists", "dagger", "sword", "shield"]
}

shadow = {
    "name": "shadow",
    "level": 1,
    "health": 3,
    "weapons": ["fists", "dagger", "sword", "shield"]
}

playerTurn = True
currentPlayerHealth = player["health"]
currentKills = 0
highestScore = ["", 0]


def getAndCheckValidInput(prompt=str(), validChoices=set()):
    """
    Prompt and test player input until input is one of the valid choices

    :param prompt: string representing text to be displayed to player as prompt
    :param validChoices: set of integers representing valid choices
    :return: integer of the player's valid input

    Usage: inp = getAndCheckValidInput("Are you a robot?", {0, 1})
    """
    choice = int()
    try:
        choice = int(input(prompt))
    except ValueError:
        pass
	# Loops until player enters valid input
    while choice not in validChoices:
        try:
            choice = int(input("Not possible. Try again.\n"))
        except ValueError:
            continue
    return choice


def encounterEnemy(playerSurprised=bool()):
    """
    Randomly generate enemy for player to encounter next along with the text accompanying the enemy
    Text of enemy changes based on who has the first turn in combat

    :param playerSurprised: boolean determining whether player or enemy has first turn (True -> enemy has first turn)
    :return: dict containing enemy stats and items

    Usage: enemy = encounterEnemy(True)
    """
    global playerTurn
    chooseEnemy = randint(0, 3)
    enemyName = ""
    enemyIntro = ""
    enemy = dict()

    if chooseEnemy == 0:  # Goblin
        enemyName = "A goblin"
        enemy = goblin
        if not playerSurprised:
            enemyIntro = "snarls a few feet in front of you."
            playerTurn = True
        else:
            enemyIntro = "jumps at you from behind!"
            playerTurn = False
    elif chooseEnemy == 1:  # Skeleton
        enemyName = "A skeleton"
        enemy = skeleton
        if not playerSurprised:
            enemyIntro = "rattles his bones in front of you."
            playerTurn = True
        else:
            enemyIntro = "throws a tooth at you from behind!"
            playerTurn = False
    elif chooseEnemy == 2:  # Zombie
        enemyName = "A zombie"
        enemy = zombie
        if not playerSurprised:
            enemyIntro = "growls and shuffles toward you."
            playerTurn = True
        else:
            enemyIntro = "charges at you from behind!"
            playerTurn = False
    elif chooseEnemy == 3:  # Shadow
        enemyName = "A shadow"
        enemy = shadow
        if not playerSurprised:
            enemyIntro = "appears and makes whooshing sounds at you."
            playerTurn = True
        else:
            enemyIntro = "appears and teleports behind you!"
            playerTurn = False



    print("{enemy} {intro}".format(enemy = enemyName, intro = enemyIntro))
    return enemy


def actionValue(actor=dict(), weapon=str(), action=str(), offensive=bool()):
    """
    Calculate damage or temporary armor based on whether actor chose offensive or defensive action

    :param actor: dict containing stats and items of the actor doing to action
    :param weapon: string name of weapon actor uses
    :param action: string name of action actor uses (connected to weapon)
    :param offensive: boolean of whether action was offensive or defense (True -> offensive)
    :return: integer value of the action the actor took (damage or temporary armor)

    Usage: player_damage = actionValue(player, "sword", "slash", True)
        enemy_damage = actionValue(goblin, "dagger", "dodge", False) ...
    """
    if offensive:
        # Randomly calculate damage using randint(0, max damage of weapon + actor level) * (damage multiplier of action)
        return randint(0, weapons[weapon][1] + actor["level"]) * offense[action][0]
    else:
        # Randomly calculate temporary armor using randint(0, max armor of weapon + actor level) * (armor multiplier of action)
        return randint(0, weapons[weapon][2] + actor["level"]) * defense[action][1]

# Return list [choseOffensiveAction, weapon name, action name]
# Prompts player for combat action on turn
def combatMenu():
    """
    Show the menu of choices for the player to choose weapon and corresponding action

    :return: list of boolean whether action was offensive, string name of weapon, string name of action

    Usage: player_choices = combatMenu()
    """

    options = set()

    print("What do you use?")
    # Loops until every weapon is displayed in combat menu
    for option in range(1, len(player["weapons"]) + 1):
        print("({}) {}          ".format(option, player["weapons"][option - 1].capitalize()), end = '')
        options.add(option)
    # Index for weapon
    weapIndex = getAndCheckValidInput("\n", options) - 1
    # Index for action
    actIndex = getAndCheckValidInput("What do you do?\n"
                                     "(1) Attack          (2) Defend\n",
                                     {1, 2}) + 2

    # String names for weapon and action
    weapName = player["weapons"][weapIndex]
    actName = weapons[weapName][actIndex]

    # Return [bool action was offensive, string name of weapon, string name of action]
    if actIndex - 2 == 1:
        # Offensive
        return [True, weapName, actName]
    elif actIndex - 2 == 2:
        # Defensive
        return [False, weapName, actName]


# Takes dict parameter enemy
def runCombat(enemy=dict()):
    """
    Run combat sequence until either player or enemy is dead
    At start of player turn, enemy's next action is calculated and printed
    Player then chooses what to do and result of action is printed
    At start of enemy turn, result of enemy's action is printed

    :param enemy: dict containing enemy's stats and items

    Usage: runCombat(goblin)
    """

    global playerTurn, currentPlayerHealth
    # Enemy health increase after every kill
    enemyHealth = enemy["health"] + (currentKills // 2)
    tempPlayerArmor = 0
    tempEnemyArmor = 0
    playerChoices = list()
    healthChange = 0

    # Randomly choose available weapon using 0 (inclusive) to length of number of weapons (exclusive)
    chooseWeapon = randrange(0, len(enemy["weapons"]))
    # String name of enemy weapon
    enemyWeapon = enemy["weapons"][chooseWeapon]

    # Combat ends when player or enemy is killed
    while currentPlayerHealth > 0 and enemyHealth > 0:
        # Calculate enemy action for next turn
        # Randomly choose between offense or defense action
        chooseAction = randint(0, 1) + 3
        # String name of enemy action
        enemyAction = weapons[enemyWeapon][chooseAction]

        if chooseAction == 3:
            # Offense
            enemyDamage = actionValue(enemy, enemyWeapon, enemyAction, True)

            healthChange = enemyDamage - tempPlayerArmor
            if healthChange < 0:
                healthChange = 0
            currentPlayerHealth -= healthChange

            print("The {enemy} prepares to {action} with its {weapon}.".format(enemy=enemy["name"], action=enemyAction,
                                                                               weapon=enemyWeapon))
        else:
            # Defense
            tempEnemyArmor = actionValue(enemy, enemyWeapon, enemyAction, False)
            print("The {enemy} prepares to {action} with its {weapon}".format(enemy=enemy["name"], action=enemyAction,
                                                                              weapon=enemyWeapon))

        if not playerTurn:   # Enemy's turn

            if chooseAction == 3:
                # Offense
                if healthChange > 0:
                    print("Ow! The {enemy}'s {action} hits you for {damage} health.".format(action = enemyAction, enemy = enemy["name"], damage = healthChange))
                elif tempPlayerArmor > 0:
                    print("You {pAction} the {eAction}! The enemy hits you for {damage} health.".format(pAction = playerChoices[2], eAction = enemyAction, damage = healthChange))
                else:
                    print("The {enemy} misses.".format(enemy = enemy["name"], damage = healthChange))

            tempPlayerArmor = 0
            playerTurn = True

        if playerTurn and currentPlayerHealth > 0:  # Player's turn
            print("Your health: {}          {} health: {}".format(currentPlayerHealth, enemy["name"].capitalize(), enemyHealth))

            playerChoices = combatMenu()


            if playerChoices[0]:
                # Offensive
                # Number of duplicate weapons added as additional damage
                playerDamage = actionValue(player, playerChoices[1], playerChoices[2], True) + weapons[playerChoices[1]][5]
                healthChange = playerDamage - tempEnemyArmor
                if healthChange < 0:
                    healthChange = 0
                enemyHealth -= healthChange

                if healthChange > 0:
                    print("You {action} the {enemy} for {damage} health!".format(action = playerChoices[2], enemy = enemy["name"], damage = healthChange))
                elif tempEnemyArmor > 0:
                    print("{eAction}! You deal {damage} damage to the {enemy}.".format(eAction = enemyAction.capitalize(), damage = healthChange, enemy = enemy["name"]))
                else:
                    print("You miss!")
            else:
                # Defensive
                tempPlayerArmor = actionValue(player, playerChoices[1], playerChoices[2], False) + weapons[playerChoices[1]][5]
                print("You prepare to {action}.".format(action = playerChoices[2]))

            tempEnemyArmor = 0
            playerTurn = False


def showHighscore():
    """
    Prints message to player if they achieved a new high score

    Usage: showHighScore()
    """
    global highestScore, currentKills
    if currentKills > highestScore[1]:
        print("You've set a new high score for enemies killed!", end=' ')
        if player["kills"] > 0:    # True only if not first time dying
            print("You beat {prevPlayer} by {killDiff} kills.".format(prevPlayer = highestScore[0], killDiff = currentKills - highestScore[1]))
        highestScore = (player["name"], currentKills)
    elif currentKills == highestScore[1]:
        print("You've killed the same amount of enemies as {prevPlayer}!".format(prevPlayer=highestScore[0]))
        highestScore = (player["name"], currentKills)
    print()


def dieAndRespawn():
    """
    Kill and reset player health and current number of kills
    Prints out message describing death

    Usage: dieAndRespawn()
    """

    global currentPlayerHealth, currentKills, player
    if currentKills == 1:
        suffix = "y"
    else:
        suffix = "ies"
    print("YOU GOT THRASHED...")
    print("And this life, you've thrashed {kills} enem{s}.".format(kills = currentKills, s = suffix))
    showHighscore()
    currentPlayerHealth = player["health"]
    player["kills"] += currentKills
    currentKills = 0

    player["name"] = input("You wake up from a deep sleep. What is your name?\n")
    print("Looking ahead, you see the pale light. You head towards it.")


def findItem():
    """
    Check if player found a new item after killing enemy
    Increase number of weapon duplicates if item found already exists
    Weapon durability resets to 3 if new item is found

    Usage: findItem()
    """
    # 25% chance of finding item
    success = randint(0, 3) == 0
    if success:
        weaponFound = choice(tuple(weapons.keys()))
        while weaponFound == "fists":
            weaponFound = choice(tuple(weapons.keys()))


        print("You found a {}!".format(weaponFound))
        if weaponFound in player["weapons"]:
            # If weapon in duplicate, increase weapon modifier
            weapons[weaponFound][5] += 1
            print("It looks cooler than what you have. You toss your old {} away.".format(weaponFound))
        else:
            player["weapons"].append(weaponFound)
            player["weapons"].sort()
        weapons[weaponFound][0] = 3


def endEncounter(enemy=dict()):
    """
    End encounter with enemy by calculating XP gained and whether player leveled up
    Decrease durability of random weapon
    Check if new item is found

    :param enemy: dict containing stats and items of enemy player just killed

    Usage: endEncounter(goblin)
    """
    global currentKills, player
    currentKills += 1

    # xp added after every encounter: kills + deaths + level
    xpGained = currentKills + player["deaths"] + player["level"]
    player["xp"] += xpGained

    print("You kill the {enemy} and gain {xp} XP.".format(enemy=enemy["name"], xp=xpGained))

    if player["xp"] >= player["levelUp"]:
        # 1.5 times more xp needed for next level up
        player["levelUp"] *= 1.5
        player["health"] += 1
        player["level"] += 1
        player["xp"] = 0
        print("You leveled up! You are now Level {}.".format(player["level"]))
        # Update enemy levels
        goblin["level"] = player["level"]
        skeleton["level"] = player["level"]
        zombie["level"] = player["level"]
        shadow["level"] = player["level"]
        # Update enemy base health
        goblin["health"] += 1
        skeleton["health"] += 1
        zombie["health"] += 1
        shadow["health"] += 1

    # Random weapon loses durability
    randWeapIndex = randrange(0, len(player["weapons"]))
    randWeapName = player["weapons"][randWeapIndex]
    if randWeapName != "fists":
        # Lose 1 durability
        weapons[randWeapName][0] -= 1
        print("Your {} loses durability.".format(randWeapName), end=' ')
        if weapons[randWeapName][0] < 0:
            # If negative durability, lose one duplicate
            weapons[randWeapName][5] -= 1
            print("You feel like it became weaker!", end='')
            # Reset durability
            weapons[randWeapName][0] = 3
            if weapons[randWeapName][5] < 0:
                # If negative duplicate, reset to 0
                weapons[randWeapName][5] = 0
        print()

    findItem()

    input("Press Enter to continue...")


# Introduction
input("Press Enter to start...")
player["name"] = input("What is your name?\n")
highestScore[0] = player["name"]

inp = getAndCheckValidInput("You stand in front of a massive metal gate leading into darkness. What do you do?\n"
                            "(1) Enter          (2) Leave\n",
                            {1, 2})
if inp == 1:
    inp = getAndCheckValidInput("You pry open the gate and face a tunnel. It's too dark.\n"
                                "As your eyes adjust, you see a distant pale light at what seems to be the end. What do you do?\n"
                                "(1) Go forward          (2) Turn back\n",
                                {1, 2})
else:
    print("You're right. There's no reason to do it. You turn around and head back home.")
    quit()

# Intro fight
currentEnemy = dict()
if inp == 2:
    currentEnemy = encounterEnemy(True)
else:
    currentEnemy = encounterEnemy(False)
runCombat(currentEnemy)
if currentPlayerHealth <= 0:
    print("So many regrets, yet you feel as if there are more to come.")
    dieAndRespawn()
elif currentPlayerHealth <= player["health"] // 2:
    endEncounter(currentEnemy)
    print("You barely survive. As you rest, you begin to feel the true magnitude of your injuries.", end = ' ')
else:
    endEncounter(currentEnemy)
    print("You revel in your victory. Checking for injuries, you find nothing but mere scratches.", end = ' ')

inp = getAndCheckValidInput("You look back at gate. This is your last chance to leave. What do you do?\n"
                            "(1) Continue on          (2) Turn back\n", {1, 2})
if inp == 2:
    print("That's enough adventure for today. You head out the gate and go home.")
    quit()
else:
    print("You go further into the tunnel, towards the pale light...")

print("Prepare to get THRASHED!")

# Uncomment this line to show end game
#currentKills = 20

endGameKills = 20
while True:
    # Game loop
    while currentKills < endGameKills:
        currentEnemy = encounterEnemy(bool(randint(0, 1)))
        runCombat(currentEnemy)
        if currentPlayerHealth <= 0:
            dieAndRespawn()
        else:
            endEncounter(currentEnemy)

    while True:
        # When player has killed 20 consecutive enemies ...
        inp = getAndCheckValidInput("Finally, you approach the light at the end of the tunnel. It's blinding! And hot! What do you do?\n"
                                    "(1) Go forward          (2) Turn back\n", {1, 2})
        if inp == 1:
            inp = getAndCheckValidInput("You take a few steps forward, but the heat begins to overwhelm you. Your skin starts to burn.\n"
                                  "You hear a faint whistling coming from the light. What do you do?\n"
                                  "(1) Go forward          (2) Turn back\n", {1, 2})
            if inp == 1:
                inp = getAndCheckValidInput("You force your legs to move forward, but when you feel skin melting, "
                                      "you fall to your knees. You don't know if you'll be able to handle any more of "
                                      "this excruciating pain.\nFrom the light you hear the faint whistle rise to a "
                                      "defeaning pitch. What do you do?\n"
                                      "(1) Go forward          (2) Lay down\n", {1, 2})
                if inp == 1:
                    print("You crawl towards the light. When you reach out your hand, the pain begins to deaden.\n"
                          "You feel a coolness beginning to cover your body. The light fades...")
                    print("You WIN")
                    quit()
                elif inp == 2:
                    inp = getAndCheckValidInput("You lay down on the cool ground. It's soothing, but not enough. You feel the heat searing "
                                          "your back. What do you do?\n"
                                          "(1) Get up          (2) Stay down\n", {1, 2})
                    if inp == 1:
                        print("You raise your head. You can't. You feel a blast of heat barrage your face.\n"
                              "You can feel anything anymore...")
                        print("You LOSE")
                        quit()
                    elif inp == 2:
                        print("You stay down. It's the only thing you can do. Soon, the heat deadens all feeling...")
                        print("You LOSE")
                        quit()
            elif inp == 2:
                print("You can't move your legs. There's something wrong. You feel the heat begin to consume you...")
                print("You LOSE")
                quit()

        elif inp == 2:
            inp = getAndCheckValidInput("You turn away from the light. Suddenly, it hisses and sputters. Are you sure?\n"
                                        "(1) Yes, I just want to go home          (2) I've changed my mind. Turn back\n", {1, 2})
            if inp == 1:
                print("As you walk away, the light screeches, shooting out wild flares. You feel the warmth on your back "
                      "dissipate as the shadow in front of you disappears.\nWhen you look back at where the light should be, "
                      "you see only darkness...\n")
                inp = getAndCheckValidInput("You reach the metal gate at the beginning of the tunnel What do you do?\n"
                                      "(1) Go home          (2) I've changed my mind. Turn back\n", {1, 2})
                if inp == 1:
                    print("You head home, wishing to forget everything you've seen in the tunnel...")
                    print("You LOSE")
                    quit()
                elif inp == 2:
                    print("You get the feeling the tunnel has repopulated...")
                    endGameKills += 20
                    break
            elif inp == 2:
                continue
