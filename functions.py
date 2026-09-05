import random
import time


#GAME SETTINGS

BOARDWIDTH = 41
BOARDHEIGHT = 19


#CLASS OBJECTS

class player:

    def __init__ (self, health = 2, location = None):
        self.health = health
        self.location = [20,9] if location is None else list(location)
        self.model= '^'
        self.ammo = 1
        self.score = 0
        self.bombs = 0
        self.status = 'alive'
        self.notice = ''

    def face (self, face:str):
        if face == 'w':
            self.model = '^'
        elif face == 'a':
            self.model = '<'
        elif face == 's':
            self.model = 'V'
        elif face == 'd':
            self.model = '>'

    def movement (self, direction:str):
        if direction == 'w':
            self.location[1] += 1
        elif direction == 'a':
            self.location[0] -= 1
        elif direction == 's':
            self.location[1] -= 1
        elif direction == 'd':
            self.location[0] += 1

    def shoot (self):
        if self.ammo <= 0:
            return False
        self.ammo -= 1
        return True

    def reload (self, amount = 1):
        self.ammo += amount

    def attacked (self):
        self.health -= 1
        if self.health <= 0:
            self.health = 0
            self.model = 'F'
            self.status = 'dead\n\n               ~GAME OVER~               \n            THANKS FOR PLAYING            '

    def deconstruct (self):
        self.model=''


class bullet:

    def __init__ (self, playermodel, playerlocation):
        self.model = '&'
        self.location = list(playerlocation)
        self.active = False

        if playermodel == '^':
            self.direction = 'up'
            self.location[1] += 1
        elif playermodel == 'V':
            self.direction = 'down'
            self.location[1] -= 1
        elif playermodel == '<':
            self.direction = 'left'
            self.location[0] -= 1
        elif playermodel == '>':
            self.direction = 'right'
            self.location[0] += 1

    def movement (self):
        if self.direction == 'up':
            self.location[1] += 1
        elif self.direction == 'down':
            self.location[1] -= 1
        elif self.direction == 'left':
            self.location[0] -= 1
        elif self.direction == 'right':
            self.location[0] += 1


class bomb:

    def __init__ (self, location, fuse = 3, radius = 2):
        self.location = list(location)
        self.model = 'B'
        self.fuse = fuse
        self.radius = radius

    def tick (self):
        self.fuse -= 1
        return self.fuse <= 0


class ammo:

    def __init__(self, location = None, model = 'a'):
        self.location = randomlocation() if location is None else list(location)
        self.model = model

    def destroyed (self):
        self.model = ' '


class target:

    def __init__(self, location = None, model = 't'):
        self.location = randomlocation() if location is None else list(location)
        self.model = model

    def destroyed (self):
        self.model = ' '


class necromancer:

    def __init__ (self, location = None, model = 'N', health = 3):
        self.location = randomlocation() if location is None else list(location)
        self.model = model
        self.attacksquaremodel1 = '!'
        self.attacksquaremodel2 = '#'
        self.health = health
        self.xcoord = self.location [0]
        self.attackcounter = 0

    def attack (self):
        self.attackcounter += 1
        if self.attackcounter > 2:
            self.attackcounter = 0
    #0 is safe, 1 is a forecasted attack, and 2 deals damage

    def damaged (self, amount = 1):
        self.health -= amount

    def destroyed (self):
        self.model = ' '


class boss:

    def __init__ (self, health = 10, model = '~(〃￣ω￣〃)~'):
        self.location = [14,1]
        self.health = health
        self.model = model
        self.attacksqmodel1 = '!'
        self.attacksqmodel2 = '#'
        self.lines = 'PuNy MoRtAl, yoU dArE cHalLenGE mE?'
        self.attackcounter = 0
        self.newattack()

    def newattack (self):
        self.xcoord = random.randint(0,BOARDWIDTH - 1)
        self.ycoord = random.randint(0,BOARDHEIGHT - 1)
        self.xcoord2 = random.randint(0,BOARDWIDTH - 1)
        self.ycoord2 = random.randint(0,BOARDHEIGHT - 1)

    def damaged (self, amount = 1):
        self.health -= amount

    def phase2 (self):
        self.lines = 'pReParE FoR yOuR eTerNaL SuFFeRiNg!'
        self.model = '  ~(◍•ᴗ•◍)~  '

    def phase3 (self):
        self.lines = "Hold on, i need go toliet break pls "
        self.model = ' ヾ(๑╹ꇴ◠๑)ﾉ '

    def phase4 (self):
        self.lines = 'Bro give chance pls I first time :('
        self.model = '  ~~(´З`)~~  '

    def destroyed (self):
        self.lines = 'NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!'
        self.model = '   (◕﹏◕✿)   '

    def attack (self):
        self.attackcounter += 1
        if self.attackcounter > 2:
            self.attackcounter = 0
            self.newattack()


#GENERAL FUNCTIONS

def randomlocation (occupied = None):
    if occupied is None:
        occupied = set()

    while True:
        location = [random.randint(1,BOARDWIDTH - 1),random.randint(1,BOARDHEIGHT - 1)]
        if tuple(location) not in occupied:
            return location


def clampplayer (player):
    if player.location[0] < 0:
        player.location[0] = 0
    if player.location[0] >= BOARDWIDTH:
        player.location[0] = BOARDWIDTH - 1
    if player.location[1] < 0:
        player.location[1] = 0
    if player.location[1] >= BOARDHEIGHT:
        player.location[1] = BOARDHEIGHT - 1


def moveplayer (player, user):
    if player.model == '*':
        if user in ['w','a','s','d']:
            player.face(user)
            player.movement(user)
        elif user == 'e':
            player.notice = "~You are immobilized. Can't shoot!~"
        elif user == 'b':
            player.notice = "~You are immobilized. Can't plant bombs!~"
        clampplayer(player)
        return

    if player.model == '^' and user == 'w':
        player.movement(user)
    elif player.model == '<' and user == 'a':
        player.movement(user)
    elif player.model == 'V' and user == 's':
        player.movement(user)
    elif player.model == '>' and user == 'd':
        player.movement(user)
    player.face(user)
    clampplayer(player)


def attackcoordinates (enemy):
    attackdict = {}
    if enemy.attackcounter == 0:
        return attackdict

    model = enemy.attacksquaremodel1 if isinstance(enemy, necromancer) else enemy.attacksqmodel1
    if enemy.attackcounter == 2:
        model = enemy.attacksquaremodel2 if isinstance(enemy, necromancer) else enemy.attacksqmodel2

    if isinstance(enemy, necromancer):
        for y in range(BOARDHEIGHT):
            attackdict[(enemy.xcoord,y)] = model

    if isinstance(enemy, boss):
        for x in range(BOARDWIDTH):
            attackdict[(x,enemy.ycoord)] = model
            attackdict[(x,enemy.ycoord2)] = model
        for y in range(BOARDHEIGHT):
            attackdict[(enemy.xcoord,y)] = model
            attackdict[(enemy.xcoord2,y)] = model
    return attackdict


def attackplayer (player, enemies):
    for enemy in enemies:
        enemy.attack()
        if enemy.attackcounter == 2:
            if tuple(player.location) in attackcoordinates(enemy):
                player.model = '*'
                player.attacked()


def bombcoordinates (item):
    blast = set()
    for x in range(item.location[0] - item.radius,item.location[0] + item.radius + 1):
        for y in range(item.location[1] - item.radius,item.location[1] + item.radius + 1):
            if abs(x - item.location[0]) + abs(y - item.location[1]) <= item.radius:
                if x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT:
                    blast.add((x,y))
    return blast


def bosshitbox (enemy):
    hitbox = set()
    for x in range(16,25):
        hitbox.add((x,1))
    return hitbox


def updateboss (enemy):
    if enemy.health < 2:
        enemy.phase4()
    elif enemy.health < 4:
        enemy.phase3()
    elif enemy.health < 8:
        enemy.phase2()


#ENTITY LOGGING AND PRINTING

def addentity (entitydict, location, model):
    if len(model) == 1:
        coordinate = tuple(location)
        if coordinate[0] >= 0 and coordinate[0] < BOARDWIDTH and coordinate[1] >= 0 and coordinate[1] < BOARDHEIGHT:
            entitydict[coordinate] = model
        return

    for index,char in enumerate(model):
        coordinate = (location[0] + index,location[1])
        if coordinate[0] >= 0 and coordinate[0] < BOARDWIDTH:
            entitydict[coordinate] = char


def updatedict (player, targets = None, necromancers = None, bullets = None, bombs = None, ammo = None, enemyboss = None, explosions = None):
    entitydict = {}
    targets = [] if targets is None else targets
    necromancers = [] if necromancers is None else necromancers
    bullets = [] if bullets is None else bullets
    bombs = [] if bombs is None else bombs
    explosions = set() if explosions is None else explosions

    for enemy in necromancers:
        entitydict.update(attackcoordinates(enemy))
    if enemyboss is not None:
        entitydict.update(attackcoordinates(enemyboss))
    for coordinate in explosions:
        entitydict[coordinate] = '*'
    if ammo is not None and ammo.model != ' ':
        addentity(entitydict,ammo.location,ammo.model)
    for item in targets:
        if item.model != ' ':
            addentity(entitydict,item.location,item.model)
    for enemy in necromancers:
        if enemy.model != ' ':
            addentity(entitydict,enemy.location,enemy.model)
    for item in bombs:
        addentity(entitydict,item.location,item.model)
    if enemyboss is not None:
        addentity(entitydict,enemyboss.location,enemyboss.model)
    for item in bullets:
        addentity(entitydict,item.location,item.model)
    addentity(entitydict,player.location,player.model)
    return entitydict


def printscreen (lines):
    print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    for line in lines:
        print (f'X{line[:BOARDWIDTH].ljust(BOARDWIDTH)}X')
    print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')


def printdict (entitydict):
    lines = []
    for y in reversed(range(BOARDHEIGHT)):
        string = ''
        for x in range(BOARDWIDTH):
            string += entitydict.get((x,y),' ')
        lines.append(string)
    printscreen(lines)


#HUD

def hudlines (player, level = None, enemyboss = None, armedbombs = 0):
    lines = []
    if level is not None:
        lines.append(f'      THREATCON: {level}')
    if enemyboss is not None:
        lines.append(f'      BOSS HEALTH: {enemyboss.health}')
        lines.append(f'    {enemyboss.lines}')
        lines.append('    -----------------------------------')
    lines.append(f'      HEALTH: {player.health}')
    lines.append(f'      AMMO: {player.ammo}')
    lines.append(f'      BOMBS: {player.bombs}  ARMED: {armedbombs}')
    lines.append(f'      SCORE: {player.score}')
    lines.append(f'      PLAYER: {player.status}')
    if player.notice != '':
        lines.append(f'    {player.notice}')
    return lines


def interface (player, level = None, enemyboss = None, armedbombs = 0):
    print('\n'.join(hudlines(player,level,enemyboss,armedbombs)))


def interface2 (player, enemyboss, armedbombs = 0):
    interface(player,None,enemyboss,armedbombs)


def threatconlvl (threatcon_lvl):
    lines = []
    for row in range(8):
        lines.append('')
    lines.append('                ~NOTICE~')
    lines.append(f'   YOU ARE MOVING TO THREATCON LEVEL {threatcon_lvl}')
    for row in range(8):
        lines.append('')
    printscreen(lines)


#SHOP

class shop:
    def __init__ (self):
        self.pointer = 0
        self.items = ['HEALTH','AMMO','BOMBS']

    def move (self, direction):
        if direction == 'w':
            self.pointer -= 1
        if direction == 's':
            self.pointer += 1
        if self.pointer < 0:
            self.pointer = 0
        if self.pointer >= len(self.items):
            self.pointer = len(self.items) - 1

    def itemvalue (self, player, item):
        if item == 'HEALTH':
            return player.health
        if item == 'AMMO':
            return player.ammo
        return player.bombs

    def changeitem (self, player, item, amount):
        if item == 'HEALTH':
            player.health += amount
        elif item == 'AMMO':
            player.ammo += amount
        elif item == 'BOMBS':
            player.bombs += amount

    def buy (self, player, points):
        item = self.items[self.pointer]
        if points <= 0:
            print ('No more points left to spend. Sell [V] items to buy [B] others.')
            time.sleep(1.5)
            return points
        if self.itemvalue(player,item) >= 5:
            print (f'Max {item.lower()} of 5 reached.')
            time.sleep(0.75)
            return points
        self.changeitem(player,item,1)
        return points - 1

    def sell (self, player, points):
        item = self.items[self.pointer]
        minimum = 0 if item == 'BOMBS' else 1
        if self.itemvalue(player,item) <= minimum:
            if item == 'BOMBS':
                print ('No bombs left to sell!')
            else:
                print (f'Base {item.lower()} {minimum}, cannot be sold!')
            time.sleep(0.75)
            return points
        self.changeitem(player,item,-1)
        return points + 1

    def screenlines (self, player, points):
        lines = ['','','                ~WELCOME~','               TO THE SHOP','','']
        for index,item in enumerate(self.items):
            pointer = ' --> ' if self.pointer == index else '     '
            value = self.itemvalue(player,item)
            markers = ''
            for number in range(value):
                markers += 'O ' if item == 'HEALTH' else '& ' if item == 'AMMO' else 'B '
            lines.append(f'     {pointer} {item:<6} |{markers:<10}|')
            lines.append('')
        lines.append(f'           POINTS LEFT: {points}')
        return lines

    def printscreen (self, player, points):
        printscreen(self.screenlines(player,points))


def runshop (num, player):
    s = shop ()

    while True:
        s.printscreen(player,num)
        user = input ('[W/S/B/V/E]: ').lower()
        if user == 'w' or user == 's':
            s.move(user)
        elif user == 'b':
            num = s.buy(player,num)
        elif user == 'v':
            num = s.sell(player,num)
        elif user == 'e':
            exitinput = input ('Would you like to continue to the next stage?\n[Y/N]: ').lower()
            if exitinput == 'y':
                return player
            if exitinput == 'n':
                print ('Okay. Continue browsing.')
                time.sleep(1.5)
