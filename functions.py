import random
import time

#CLASS OBJECTS

class player:

    def __init__ (self, health = 2, location =  [20,9]):
        #print ('player is instantiated')
        self.health = health
        self.location = location
        self.model= '^'
        self.ammo = 1
        self.score = 0
        self.bombs = 0
        self.status = 'alive'
        self.notice = ''
        #attack state is 1, upon attacking, it becomes zero, and requires one movement to recover

    def face (self, face:str):
        if face == 'w':
            self.model = '^'
        elif face == 'a':
            self.model = '<'
        elif face == 's':
            self.model = 'V'
        elif face == 'd':
            self.model = '>'
        else:
            pass

    def movement (self, direction:str):
        if direction == 'w':
            self.location[1] += 1
        elif direction == 'a':
            self.location[0] -= 1
        elif direction == 's':
            self.location[1] -= 1
        elif direction == 'd':
            self.location[0] += 1
        else:
            pass
    
    def shoot (self):
        if self.ammo <= 0:
            print ('No more ammo!')
        else:
            self.ammo -= 1

    def reload (self):
        self.ammo += 1
        
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
        #print ('bullet is instantiated')
        self.model = '&'
        if playermodel == '^':
            self.direction = 'up'
            self.location = [playerlocation[0],playerlocation[1]+1]

        if playermodel == 'V':
            self.direction = 'down'
            self.location = [playerlocation[0],playerlocation[1]-1]

        if playermodel == '<':
            self.direction = 'left'
            self.location = [playerlocation[0]-1,playerlocation[1]]

        if playermodel == '>':
            self.direction = 'right'
            self.location = [playerlocation[0]+1,playerlocation[1]]     

    def movement (self):
        if self.direction == 'up':
            self.location[1] += 1

        if self.direction == 'down':
            self.location[1] -= 1

        if self.direction == 'left':
            self.location[0] -= 1

        if self.direction == 'right':
            self.location[0] += 1

    def collision (self):
        self.model = '*'

    def disappear (self):
        self.model = ' '

class ammo:

    def __init__(self, model = 'a'):
        #print ('ammo is instantiated')
        self.location = [(random.randint(1,40)),(random.randint(1,18))]
        self.model = model

    def destroyed (self):
        self.model = ' '

class target:

    def __init__(self, location = [40,18], model = 't'):
        #print ('target is instantiated')
        self.location = [(random.randint(1,40)),(random.randint(1,18))]
        #print (self.location)
        #self.location = location
        self.model = model

    def destroyed (self):
        self.model = ' '

class necromancer:
    
    def __init__ (self, model = 'N', health = 3):
        #print ('Necromancer is instantiated')
        self.location = [(random.randint(1,40)),(random.randint(1,18))]
        self.model = model
        self.attacksquaremodel1 = '!'
        self.attacksquaremodel2 = '#'
        self.health = health
        self.xcoord = self.location [0]
        self.ycoord = self.location [1]
        self.attackcounter = 0

    def attack (self):
        self.attackcounter += 1
        if self.attackcounter > 2:
            self.attackcounter = 0 
    #0 is for intiial spawn state, 1 is for forecasted attack where attacked squares become '!', 2 is for attack, where attacked squares become '#' and deal damage
        
    def collision (self):
        self.model = '*'

    def damaged (self):
        self.health -= 1

    def destroyed (self):
        self.model = ' '

class boss:

    def __init__ (self, health = 10, model = '~(〃￣ω￣〃)~'):
        print ('boss is instantiated')
        self.location = [(random.randint(1,40)),(random.randint(1,19))]
        self.location2 = [(random.randint(0,41)),(random.randint(1,19))]
        self.health = health
        self.model = model
        self.attacksqmodel1 = '!'
        self.attacksqmodel2 = '#'
        self.xcoord = self.location[0]
        self.ycoord = self.location[1]
        self.xcoord2 = self.location2[0]
        self.ycoord2 = self.location2[1]
        self.lines = 'PuNy MoRtAl, yoU dArE cHalLenGE mE?'
        self.attackcounter = 0        

    def damaged (self):
        self.health -= 1

    def phase2 (self):
        #self.health = 5-7
        #length of model = 9
        self.lines = 'pReParE FoR yOuR eTerNaL SuFFeRiNg!'
        self.model = '  ~(◍•ᴗ•◍)~  '

    def phase3 (self):
        #self.health = 2-4
        #length of model = 9
        self.lines = "Hold on, i need go toliet break pls "
        self.model = ' ヾ(๑╹ꇴ◠๑)ﾉ '

    def phase4 (self):
        #self.health 0-1
        #length of model = 9
        self.lines = 'Bro give chance pls I first time :('
        self.model = '  ~~(´З`)~~  '

    def destroyed (self):
        self.lines = 'NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!'
        self.model = '   (◕﹏◕✿)   '

    def attack (self):
        self.attackcounter += 1
        if self.attackcounter > 2:
            self.attackcounter = 0

def interface (player):
    print(f'\t      HEALTH: {player.health}\n\t      AMMO: {player.ammo}\n\t      SCORE: {player.score}\n\t      PLAYER: {player.status}\n    {player.notice}    ')

#THREATCON 0

def dictcreator (player, target, ammo):
    #print (player.location)
    permdict = {}
    for y in range (0,19):
        string = ''
        for x in range (0,41):
            if player.location == [x,y]:
                string += player.model
            elif target.location == [x,y]:
                string += target.model
            elif ammo.location == [x,y]:
                string += ammo.model
            else:
                string += ' '
        permdict [y] = string
    return permdict

def dictcreatorwbullets (player, target, bullet, ammo):
    #print (player.location, bullet.location)
    permdict = {}
    for y in range (0,19):
        string = ''
        for x in range (0,41):
            if player.location == [x,y]:
                string += player.model
            elif bullet.location == [x,y]:
                string += bullet.model
            elif target.location == [x,y]:
                string += target.model 
            elif ammo.location == [x,y]:
                string += ammo.model
            else:
                string += ' '
        permdict [y] = string
    return permdict

#THREATCON 1

def dictcreator3 (player, target1, target2, target3, ammo):
    #print (player.location)
    permdict = {}
    for y in range (0,19):
        string = ''
        for x in range (0,41):
            if player.location == [x,y]:
                string += player.model
            elif target1.location == [x,y]:
                string += target1.model
            elif target2.location == [x,y]:
                string += target2.model
            elif target3.location == [x,y]:
                string += target3.model
            elif ammo.location == [x,y]:
                string += ammo.model
            else:
                string += ' '
        permdict [y] = string
    return permdict

def dictcreatorwbullets3 (player, target1, target2, target3, bullet, ammo):
    #print (player.location, bullet.location)
    permdict = {}
    for y in range (0,19):
        string = ''
        for x in range (0,41):
            if player.location == [x,y]:
                string += player.model
            elif bullet.location == [x,y]:
                string += bullet.model
            elif target1.location == [x,y]:
                string += target1.model
            elif target2.location == [x,y]:
                string += target2.model
            elif target3.location == [x,y]:
                string += target3.model 
            elif ammo.location == [x,y]:
                string += ammo.model
            else:
                string += ' '
        permdict [y] = string
    return permdict

#THREATCON 2

def dictcreator6 (player, target1, necromancer1, necromancer2, ammo):
    #print (player.location)
    permdict = {}
    for y in range (0,19):
        string = ''
        for x in range (0,41):
            if player.location == [x,y]:
                string += player.model
            elif necromancer1.location == [x,y]:
                string += necromancer1.model
            elif necromancer2.location == [x,y]:
                string += necromancer2.model
            elif target1.location == [x,y]:
                string += target1.model
            elif ammo.location == [x,y]:
                string += ammo.model
            elif necromancer1.xcoord == x:
                if necromancer1.attackcounter == 0:
                    string += ' '
                if necromancer1.attackcounter == 1:
                    string += necromancer1.attacksquaremodel1
                if necromancer1.attackcounter == 2:
                    string += necromancer1.attacksquaremodel2
            elif necromancer2.xcoord == x:
                if necromancer2.attackcounter == 0:
                    string += ' '
                if necromancer2.attackcounter == 1:
                    string += necromancer2.attacksquaremodel1
                if necromancer2.attackcounter == 2:
                    string += necromancer2.attacksquaremodel2
            else:
                string += ' '
        permdict [y] = string
    return permdict

def dictcreatorwbullets6 (player, target1, necromancer1, necromancer2, bullet, ammo):
    #print (player.location, bullet.location)
    permdict = {}
    for y in range (0,19):
        string = ''
        for x in range (0,41):
            if player.location == [x,y]:
                string += player.model
            elif bullet.location == [x,y]:
                string += bullet.model
            elif necromancer1.location == [x,y]:
                string += necromancer1.model
            elif necromancer2.location == [x,y]:
                string += necromancer2.model
            elif target1.location == [x,y]:
                string += target1.model
            elif ammo.location == [x,y]:
                string += ammo.model
            elif necromancer1.xcoord == x:
                if necromancer1.attackcounter == 0:
                    string += ' '
                if necromancer1.attackcounter == 1:
                    string += necromancer1.attacksquaremodel1
                if necromancer2.attackcounter == 2:
                    string += necromancer1.attacksquaremodel2
            elif necromancer2.xcoord == x:
                if necromancer2.attackcounter == 0:
                    string += ' '
                if necromancer2.attackcounter == 1:
                    string += necromancer2.attacksquaremodel1
                if necromancer2.attackcounter == 2:
                    string += necromancer2.attacksquaremodel2
            else:
                string += ' '
        permdict [y] = string
    return permdict

#SHOP

class shop:
    def __init__ (self):
        self.health = 'O O '
        self.ammo = '& '
        self.bombs = ''
        self.pointer1 = ' --> '
        self.pointer2 = '     '
        self.pointer3 = '     '
        self.spaces1 = '      '
        self.spaces2 = '        '
        self.spaces3 = '          '
        #print ('shop has been instantiated')

    def buy_health (self,number,points):

        if points <= 0:
                print ('No more points left to spend. Sell [V] items to buy [B] others.')
                points = 0
                time.sleep(1.5)
                return points


        elif len (self.health) >= 10:
            print ('Max health of 5 reached.')
            time.sleep(0.75)
            return points
    
        else:
            for itervar in range (number):
                self.health += 'O '
                points -= 1
            num = int(5-(len(self.health)/2))
            self.spaces1 = ''
            for itervar in range(num):
                self.spaces1 += '  ' 
            return points
            
    #add increase/decrease health to player object

    def sell_health (self,number,points):
        if len (self.health) <=4:
            print ('Base Health 2, cannot be sold!')
            time.sleep(0.75)
            return points

        elif len (self.health) > 4:
            for itervar in range (number):
                self.health = self.health.replace('O ', '', 1)
                points += 1
        num = int(5-(len(self.health)/2))
        self.spaces1 = ''
        for itervar in range(num):
            self.spaces1 += '  '
        return points 

    #add increase/decrease health to player object

    def buy_ammo (self,number,points):

        if points <= 0:
                print ('No more points left to spend. Sell [V] items to buy [B] others.')
                points = 0
                time.sleep(1.5)
                return points

        elif len (self.ammo) >= 10:
            print ('Max ammo of 5 reached.')
            time.sleep(0.75)
            return points

    
        else:
            for itervar in range (number):
                self.ammo += '& '
                points -= 1

            num = int(5-(len(self.ammo)/2))
            self.spaces2 = ''
            for itervar in range(num):
                self.spaces2 += '  '
            return points
    #add increase/decrease ammo to player object


    def sell_ammo (self,number,points):
        if len(self.ammo) <= 2:
            print ('Base ammo 1, cannot be sold!')
            time.sleep(0.75)
            return points

        elif len(self.ammo) > 2:
            for itervar in range(number):
                self.ammo = self.ammo.replace('& ', '', 1)
                points += 1
        num = int(5-(len(self.ammo)/2))
        self.spaces2 = ''
        for itervar in range(num):
            self.spaces2 += '  '
        return points
    #add increase/decrease ammo to player object
 

    def buy_bombs (self,number,points):

        if points <= 0:
                print ('No more points left to spend. Sell [V] items to buy [B] others.')
                points = 0
                time.sleep(1.5)
                return points

        elif len (self.bombs) >= 10:
            print ('Max number of bombs of 5 reached.')
            time.sleep(0.75)
            return points

        else:
            for itervar in range (number):
                self.bombs += 'B ' 
                points -= 1

            num = int(5-(len(self.bombs)/2))
            self.spaces3 = ''
            for itervar in range(num):
                self.spaces3 += '  '
            return points
    #add increase/decrease health to player object

    def sell_bombs (self,number,points):
        if len(self.bombs)<=0:
            print ('No bombs left to sell!')
            time.sleep(0.75)
            return points

        elif len(self.bombs)>0:
            for itervar in range(number):
                self.bombs = self.bombs.replace('B ','', 1)
                points += 1
        num = int(5-(len(self.bombs)/2))
        self.spaces3 = ''
        for itervar in range(num):
            self.spaces3 += '  '
        return points
    #add increase/decrease health to player object

    def pointer (self,direction):

        #current pointer position
        if self.pointer1 == ' --> ':
            p = 1
        if self.pointer2 == ' --> ':
            p = 2
        if self.pointer3 == ' --> ':
            p = 3

        #make pointer '>' that moves per input
        if direction == 'w':
            p -= 1
        if direction == 's':
            p += 1

        if p == 0:
            p = 1  
        elif p == 4:
            p = 3
        
        if p == 1:
            self.pointer1 = ' --> '
            self.pointer2 = '     '
            self.pointer3 = '     '
        elif p == 2:
            self.pointer1 = '     '
            self.pointer2 = ' --> '
            self.pointer3 = '     '
        elif p == 3:
            self.pointer1 = '     '
            self.pointer2 = '     '
            self.pointer3 = ' --> '


    def printscreen (self, points):
        permdict = {}
        for y in range (2):
            string = ''
            for x in range (41):
                string += ' '
            permdict [y] = string
            string = ''
        for y in range(2,3):
            string = '                ~WELCOME~                '
            permdict [y] = string
            string = ''
        for y in range (3,4):
            string = '               TO THE SHOP               '
            permdict[y] = string
            string = ''
        for y in range (4,6):
            for x in range (41):
                string += ' '
            permdict [y] = string
            string = ''
        for y in range (6,7):
            string = f'     {self.pointer1} HEALTH  |{self.health}{self.spaces1}|          '
            permdict [y] = string
            string = ''
        for y in range (7,9):
            for x in range (41):
                string += ' '
            permdict [y] = string
            string = ''
        for y in range (9,10):
            string = f'     {self.pointer2} AMMO    |{self.ammo}{self.spaces2}|          '
            permdict [y] = string
            string = ''
        for y in range (10,12):
            for x in range (41):
                string += ' ' 
            permdict [y] = string
            string = ''
        for y in range (12,13):
            string = f'     {self.pointer3} BOMBS   |{self.bombs}{self.spaces3}|          '
            permdict [y] = string
            string = ''
        for y in range (13,15):
            for x in range (41):
                string += ' ' 
            permdict [y] = string
            string = ''
        for y in range (15,16):
            string = f'           POINTS LEFT: {points}                '
            permdict [y] = string
            string = ''
        for y in range (16,19):
            for x in range (41):
                string += ' '
            permdict [y] = string
            string = ''

        #print (permdict)

        print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        for x,y in (permdict.items()):
            print (f'X{y}X')
        print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

def runshop (num, player):
    s = shop ()

    while True:
        s.printscreen(num)

        user = input ('[W/S/B/V/E]: ')
        
        if user == 'w':
            s.pointer ('w')
        
        if user == 's':
            s.pointer ('s')

        if user == 'b':
            
            if s.pointer1 == ' --> ':
                num = s.buy_health(1, num)
                player.health += 1

            elif s.pointer2 == ' --> ':
                num = s.buy_ammo(1, num)
                player.ammo += 1

            elif s.pointer3 == ' --> ':
                num = s.buy_bombs(1, num)
                player.bombs += 1
            
        if user == 'v':
            if s.pointer1 == ' --> ':
                num = s.sell_health(1, num)
                player.health -= 1

            elif s.pointer2 == ' --> ':
                num = s.sell_ammo(1, num)
                player.ammo -= 1

            elif s.pointer3 == ' --> ':
                num = s.sell_bombs(1, num)    
                player.bombs -= 1            
            
        if user == 'e':
            exitinput = input ('Would you like to continue to the next stage?\n[Y/N]: ')
            if exitinput == 'y':
                return [player.health,player.ammo,player.bombs]
            if exitinput == 'n':
                print ('Okay. Continue browsing.')
                time.sleep(1.5)

#THREATCON 3

def dictcreator9 (player, boss, ammo):
    #print (player.location)
    permdict = {}
    for y in range (0,1): 
        string = ''
        if boss.ycoord == y:
            if boss.attackcounter == 0:
                for x in range (0,41):
                    if player.location == [x,y]:
                        string += player.model
                    elif ammo.location == [x,y]:
                        string += ammo.model
                    elif boss.xcoord == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    elif boss.xcoord2 == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    else:
                        string += ' '
            if boss.attackcounter == 1:
                string = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            if boss.attackcounter == 2:
                string = '#########################################'
        elif boss.ycoord2 == y:
            if boss.attackcounter == 0:
                for x in range (0,41):
                    if player.location == [x,y]:
                        string += player.model
                    elif ammo.location == [x,y]:
                        string += ammo.model
                    elif boss.xcoord == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    elif boss.xcoord2 == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    else:
                        string += ' '
            if boss.attackcounter == 1:
                string = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            if boss.attackcounter == 2:
                string = '#########################################'
        else:
            for x in range (0,41):
                if player.location == [x,y]:
                    string += player.model
                elif ammo.location == [x,y]:
                    string += ammo.model
                elif boss.xcoord == x:
                    if boss.attackcounter == 0:
                        string += ' '
                    if boss.attackcounter == 1:
                        string += boss.attacksqmodel1
                    if boss.attackcounter == 2:
                        string += boss.attacksqmodel2
                elif boss.xcoord2 == x:
                    if boss.attackcounter == 0:
                        string += ' '
                    if boss.attackcounter == 1:
                        string += boss.attacksqmodel1
                    if boss.attackcounter == 2:
                        string += boss.attacksqmodel2
                else:
                    string += ' '
        permdict [y] = string
    for y in range (1,2):
        string = ''
        for x in range (0,14):
            if player.location == [x,y]:
                    string += player.model
            elif ammo.location == [x,y]:
                string += ammo.model
            elif boss.xcoord == x:
                if boss.attackcounter == 0:
                    string += ' '
                if boss.attackcounter == 1:
                    string += boss.attacksqmodel1
                if boss.attackcounter == 2:
                    string += boss.attacksqmodel2
            elif boss.xcoord2 == x:
                if boss.attackcounter == 0:
                    string += ' '
                if boss.attackcounter == 1:
                    string += boss.attacksqmodel1
                if boss.attackcounter == 2:
                    string += boss.attacksqmodel2
            else:
                string += ' '
        string += f'{boss.model}'
        for x in range (27,41):
            if player.location == [x,y]:
                    string += player.model
            elif ammo.location == [x,y]:
                string += ammo.model
            elif boss.xcoord == x:
                if boss.attackcounter == 0:
                    string += ' '
                if boss.attackcounter == 1:
                    string += boss.attacksqmodel1
                if boss.attackcounter == 2:
                    string += boss.attacksqmodel2
            elif boss.xcoord2 == x:
                if boss.attackcounter == 0:
                    string += ' '
                if boss.attackcounter == 1:
                    string += boss.attacksqmodel1
                if boss.attackcounter == 2:
                    string += boss.attacksqmodel2
            else:
                string += ' '
        permdict [y] = string 
    
    for y in range (2,19):
        #print(y)
        string = ''
        if boss.ycoord == y:
            if boss.attackcounter == 0:
                for x in range (0,41):
                    if player.location == [x,y]:
                        string += player.model
                    elif ammo.location == [x,y]:
                        string += ammo.model
                    elif boss.xcoord == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    elif boss.xcoord2 == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    else:
                        string += ' '
            if boss.attackcounter == 1:
                string = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            if boss.attackcounter == 2:
                string = '#########################################'
        elif boss.ycoord2 == y:
            if boss.attackcounter == 0:
                for x in range (0,41):
                    if player.location == [x,y]:
                        string += player.model
                    elif ammo.location == [x,y]:
                        string += ammo.model
                    elif boss.xcoord == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    elif boss.xcoord2 == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    else:
                        string += ' '
            if boss.attackcounter == 1:
                string = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            if boss.attackcounter == 2:
                string = '#########################################'
        else:
            #print ('ok')
            for x in range (0,41):
                if player.location == [x,y]:
                    string += player.model
                elif ammo.location == [x,y]:
                    string += ammo.model
                elif boss.xcoord == x:
                    if boss.attackcounter == 0:
                        string += ' '
                    if boss.attackcounter == 1:
                        string += boss.attacksqmodel1
                    if boss.attackcounter == 2:
                        string += boss.attacksqmodel2
                elif boss.xcoord2 == x:
                    if boss.attackcounter == 0:
                        string += ' '
                    if boss.attackcounter == 1:
                        string += boss.attacksqmodel1
                    if boss.attackcounter == 2:
                        string += boss.attacksqmodel2
                else:
                    string += ' '
        permdict [y] = string
    return permdict

def dictcreatorwbullets9 (player, boss, bullet, ammo):
    #print (player.location, bullet.location)
    permdict = {}
    for y in range (0,1):         
        string = ''
        if boss.ycoord == y:
            if boss.attackcounter == 0:
                for x in range (0,41):
                    if player.location == [x,y]:
                        string += player.model
                    elif ammo.location == [x,y]:
                        string += ammo.model
                    elif boss.xcoord == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    elif boss.xcoord2 == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    else:
                        string += ' '
            if boss.attackcounter == 1:
                string = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            if boss.attackcounter == 2:
                string = '#########################################'
        elif boss.ycoord2 == y:
            if boss.attackcounter == 0:
                for x in range (0,41):
                    if player.location == [x,y]:
                        string += player.model
                    elif ammo.location == [x,y]:
                        string += ammo.model
                    elif boss.xcoord == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    elif boss.xcoord2 == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    else:
                        string += ' '
            if boss.attackcounter == 1:
                string = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            if boss.attackcounter == 2:
                string = '#########################################'
        else:
            for x in range (0,41):
                if player.location == [x,y]:
                    string += player.model
                elif bullet.location == [x,y]:
                    string += bullet.model
                elif ammo.location == [x,y]:
                    string += ammo.model
                elif boss.xcoord == x:
                    if boss.attackcounter == 0:
                        string += ' '
                    if boss.attackcounter == 1:
                        string += boss.attacksqmodel1
                    if boss.attackcounter == 2:
                        string += boss.attacksqmodel2
                elif boss.xcoord2 == x:
                    if boss.attackcounter == 0:
                        string += ' '
                    if boss.attackcounter == 1:
                        string += boss.attacksqmodel1
                    if boss.attackcounter == 2:
                        string += boss.attacksqmodel2
                else:
                    string += ' '
        permdict [y] = string
    for y in range (1,2):
        string = ''
        for x in range (0,14):
            if player.location == [x,y]:
                string += player.model
            elif bullet.location == [x,y]:
                string += bullet.model
            elif ammo.location == [x,y]:
                string += ammo.model
            elif boss.xcoord == x:
                if boss.attackcounter == 0:
                    string += ' '
                if boss.attackcounter == 1:
                    string += boss.attacksqmodel1
                if boss.attackcounter == 2:
                    string += boss.attacksqmodel2
            elif boss.xcoord2 == x:
                if boss.attackcounter == 0:
                    string += ' '
                if boss.attackcounter == 1:
                    string += boss.attacksqmodel1
                if boss.attackcounter == 2:
                    string += boss.attacksqmodel2
            else:
                string += ' '
        string += f'{boss.model}'
        for x in range (27,41):
            if player.location == [x,y]:
                string += player.model
            elif bullet.location == [x,y]:
                string += bullet.model
            elif ammo.location == [x,y]:
                string += ammo.model
            elif boss.xcoord == x:
                if boss.attackcounter == 0:
                    string += ' '
                if boss.attackcounter == 1:
                    string += boss.attacksqmodel1
                if boss.attackcounter == 2:
                    string += boss.attacksqmodel2
            elif boss.xcoord2 == x:
                if boss.attackcounter == 0:
                    string += ' '
                if boss.attackcounter == 1:
                    string += boss.attacksqmodel1
                if boss.attackcounter == 2:
                    string += boss.attacksqmodel2
            else:
                string += ' '
        permdict [y] = string 
        string = ''

    for y in range (2,19):
        string = ''
        if boss.ycoord == y:
            if boss.attackcounter == 0:
                for x in range (0,41):
                    if player.location == [x,y]:
                        string += player.model
                    elif ammo.location == [x,y]:
                        string += ammo.model
                    elif boss.xcoord == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    elif boss.xcoord2 == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    else:
                        string += ' '
                string = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            if boss.attackcounter == 2:
                string = '#########################################'
            permdict [y] = string        
        elif boss.ycoord2 == y:
            if boss.attackcounter == 0:
                for x in range (0,41):
                    if player.location == [x,y]:
                        string += player.model
                    elif ammo.location == [x,y]:
                        string += ammo.model
                    elif boss.xcoord == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    elif boss.xcoord2 == x:
                        if boss.attackcounter == 0:
                            string += ' '
                        if boss.attackcounter == 1:
                            string += boss.attacksqmodel1
                        if boss.attackcounter == 2:
                            string += boss.attacksqmodel2
                    else:
                        string += ' '
            if boss.attackcounter == 1:
                string = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            if boss.attackcounter == 2:
                string = '#########################################'
            permdict [y] = string        
        else:
            for x in range (0,41):
                if player.location == [x,y]:
                    string += player.model
                elif bullet.location == [x,y]:
                    string += bullet.model
                elif ammo.location == [x,y]:
                    string += ammo.model
                elif boss.xcoord == x:
                    if boss.attackcounter == 0:
                        string += ' '
                    if boss.attackcounter == 1:
                        string += boss.attacksqmodel1
                    if boss.attackcounter == 2:
                        string += boss.attacksqmodel2
                elif boss.xcoord2 == x:
                    if boss.attackcounter == 0:
                        string += ' '
                    if boss.attackcounter == 1:
                        string += boss.attacksqmodel1
                    if boss.attackcounter == 2:
                        string += boss.attacksqmodel2
                else:
                    string += ' '
        permdict [y] = string
    return permdict

def interface2 (player, boss):
    print(f'\t      BOSS HEALTH:{boss.health}\n    {boss.lines}\n    -----------------------------------    \n\t      HEALTH: {player.health}\n\t      AMMO: {player.ammo}\n\t      PLAYER: {player.status}\n    {player.notice}    ')


#GENERAL FUNCTIONS

def threatconlvl (threatcon_lvl):
    permdict = {}
    for row in range(8):
        string = ''
        for column in range(41):
            string += ' '
        permdict[row] = string
    string = '                ~NOTICE~                 '
    permdict [9] = string
    string = f'   YOU ARE MOVING TO THREATCON LEVEL {threatcon_lvl}   '
    permdict[10] = string
    string = ''
    for row in range(11,19):
        string = ''
        for column in range(41):
            string += ' '
        permdict[row] = string

    print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    for ok,yes in (permdict.items()):
        print (f'X{yes}X')
    print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') 

def printdict (permdict):
    print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    for x,y in reversed(permdict.items()):
        print (f'X{y}X')
    print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
 


