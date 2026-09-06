from titlescreen import titlescreen
from functions import BOARDHEIGHT, BOARDWIDTH, player, bullet, bomb, torch, door, ammo, target, necromancer, boss, randomlocation, generatespace, moveplayer, dashplayer, activateward, tickplayerabilities, attackplayer, bombcoordinates, destroyterrain, bosshitbox, updateboss, updatedict, visiblecoordinates, lightcoordinates, fogdict, mapdict, printgameframe, hudlines, promptinput, threatconlvl, cursemodifiers, cursebag, runcurseshop, runshop


#GAME SETTINGS

STAGES = [
    {'level': 0, 'targets': 1, 'necromancers': 0, 'score': 3, 'ammo': 1, 'vision': 6, 'torches': 2},
    {'level': 1, 'targets': 3, 'necromancers': 0, 'score': 4, 'ammo': 1, 'vision': 5, 'torches': 3},
    {'level': 2, 'targets': 1, 'necromancers': 2, 'score': 5, 'ammo': 2, 'vision': 4, 'torches': 3}
]


#GENERAL FUNCTIONS

def startgame ():
    while True:
        titlescreen()
        user = promptinput('[Y/N]: ')
        if user == 'y':
            return True
        if user == 'n':
            return False


def continuestage (level, bag = None):
    while True:
        threatconlvl(level)
        acknowledgement = promptinput('[Y to continue/N to leave]: ')
        if acknowledgement == 'y':
            return runcurseshop(bag)
        if acknowledgement == 'n':
            print ('Thanks for playing!')
            return None


def occupiedcoordinates (play, targets, necromancers, bullets, bombs, ammopickup = None, blocked = None, torches = None):
    occupied = {tuple(play.location)}
    for item in targets + necromancers + bullets + bombs:
        occupied.add(tuple(item.location))
    if ammopickup is not None:
        occupied.add(tuple(ammopickup.location))
    if blocked is not None:
        occupied.update(blocked)
    if torches is not None:
        for item in torches:
            occupied.add(tuple(item.location))
    return occupied


def openlocation (play, targets, necromancers, bullets, bombs, ammopickup = None, blocked = None, space = None, torches = None):
    occupied = occupiedcoordinates(play,targets,necromancers,bullets,bombs,ammopickup,blocked,torches)
    return randomlocation(occupied,space)


def targetspace (settings, play, space):
    if settings['level'] == 0:
        return space.intersection(visiblecoordinates(play,space,settings['vision']))
    return space


def createstageentities (settings, play, space):
    targets = []
    necromancers = []
    bullets = []
    bombs = []
    torches = []

    for number in range(settings['torches']):
        location = openlocation(play,targets,necromancers,bullets,bombs,space = space,torches = torches)
        torches.append(torch(location,settings.get('torchradius',4)))
    for number in range(settings['targets']):
        location = openlocation(play,targets,necromancers,bullets,bombs,space = targetspace(settings,play,space),torches = torches)
        targets.append(target(location))
    for number in range(settings['necromancers']):
        location = openlocation(play,targets,necromancers,bullets,bombs,space = space,torches = torches)
        necromancers.append(necromancer(location))
    location = openlocation(play,targets,necromancers,bullets,bombs,space = space,torches = torches)
    ammopickup = ammo(location)
    return targets,necromancers,bullets,bombs,ammopickup,torches


def refillstageentities (settings, play, targets, necromancers, bullets, bombs, ammopickup, space, torches):
    while len(targets) < settings['targets']:
        location = openlocation(play,targets,necromancers,bullets,bombs,ammopickup,space = targetspace(settings,play,space),torches = torches)
        targets.append(target(location))
    while len(necromancers) < settings['necromancers']:
        location = openlocation(play,targets,necromancers,bullets,bombs,ammopickup,space = space,torches = torches)
        necromancers.append(necromancer(location))
    if ammopickup is None:
        location = openlocation(play,targets,necromancers,bullets,bombs,space = space,torches = torches)
        ammopickup = ammo(location)
    return ammopickup


def collectammo (play, ammopickup):
    if play.location == ammopickup.location:
        play.reload(cursed = False)
        play.notice = '~Ammo collected.~'
        return None
    return ammopickup


def playeraction (play, user, bullets, bombs, space):
    moveplayer(play,user,space)
    if play.model == '*' or play.health <= 0:
        return
    if user == 'q':
        dashplayer(play,space)
    if user == 'r':
        activateward(play)
    if user == 'e':
        if play.shoot():
            bullets.append(bullet(play.model,play.location,play.bulletrange))
        else:
            play.notice = '~No more ammo, find more to shoot.~'
    if user == 'b':
        if play.bombs <= 0:
            play.notice = '~No bombs left. Buy bombs in the shop.~'
        else:
            bombs.append(bomb(play.location,play.bombfuse,play.bombradius))
            play.bombs -= 1
            play.notice = '~Bomb armed. Move away before it explodes.~'


def targetdestroyed (play, item, targets):
    item.destroyed()
    targets.remove(item)
    play.score += 1
    play.reload()


def necromancerdestroyed (play, item, necromancers):
    item.destroyed()
    necromancers.remove(item)
    play.score += 1
    play.reload(2)


def updatebullets (play, bullets, targets, necromancers, space, enemyboss = None):
    remaining = []
    for item in bullets:
        if not item.active:
            item.active = True
        else:
            if item.maxrange is not None and item.travelled >= item.maxrange:
                continue
            item.movement()
            item.travelled += 1
        if tuple(item.location) not in space:
            continue

        hit = False
        for enemy in list(targets):
            if item.location == enemy.location:
                targetdestroyed(play,enemy,targets)
                hit = True
                break
        if hit:
            continue

        for enemy in list(necromancers):
            if item.location == enemy.location:
                enemy.damaged()
                if enemy.health <= 0:
                    necromancerdestroyed(play,enemy,necromancers)
                hit = True
                break
        if hit:
            continue

        if enemyboss is not None and tuple(item.location) in bosshitbox(enemyboss):
            enemyboss.damaged()
            updateboss(enemyboss)
            continue
        remaining.append(item)
    return remaining


def updatebombs (play, bombs, targets, necromancers, space, enemyboss = None, destroyedwalls = None):
    explosions = set()
    remaining = []
    for item in bombs:
        if not item.tick():
            remaining.append(item)
            continue

        destroyed = destroyterrain(item,space)
        if destroyedwalls is not None:
            destroyedwalls.update(destroyed)
        blast = bombcoordinates(item,space)
        explosions.update(blast)
        if tuple(play.location) in blast:
            if play.attacked():
                play.notice = '~You were caught in the blast.~'
            else:
                play.notice = '~Your ward absorbed the blast.~'
        for enemy in list(targets):
            if tuple(enemy.location) in blast:
                targetdestroyed(play,enemy,targets)
        for enemy in list(necromancers):
            if tuple(enemy.location) in blast:
                enemy.damaged(2)
                if enemy.health <= 0:
                    necromancerdestroyed(play,enemy,necromancers)
        if enemyboss is not None:
            if len(blast.intersection(bosshitbox(enemyboss))) > 0:
                enemyboss.damaged(2)
                updateboss(enemyboss)
    return remaining,explosions


def printgame (play, level = None, targets = None, necromancers = None, bullets = None, bombs = None, ammopickup = None, enemyboss = None, explosions = None, space = None, explored = None, vision = 5, destroyedwalls = None, scoregoal = 5, torches = None, exitdoor = None, revealed = False, curse = None):
    entitydict = updatedict(play,targets,necromancers,bullets,bombs,ammopickup,enemyboss,explosions,torches,exitdoor)
    if space is not None:
        if revealed or explored is None:
            entitydict = mapdict(entitydict,space,destroyedwalls)
        else:
            visible = lightcoordinates(play,space,vision,bullets,bombs,torches,explosions)
            explored.update(visible)
            entitydict = fogdict(entitydict,space,visible,explored,destroyedwalls)
    sidebar = hudlines(play,level,enemyboss,0 if bombs is None else len(bombs),scoregoal,curse)
    printgameframe(entitydict,sidebar,play.status == 'dead')


#THREATCON LEVELS

def opendoor (play, space, torches):
    locations = {
        coordinate for coordinate in space
        if abs(coordinate[0] - play.location[0]) + abs(coordinate[1] - play.location[1]) >= 6
    }
    if len(locations) == 0:
        locations = space
    location = openlocation(play,[],[],[],[],space = locations,torches = torches)
    return door(location)


def exitstage (play, settings, space, torches, curse):
    exitdoor = opendoor(play,space,torches)
    while True:
        printgame(play,settings['level'],space = space,scoregoal = settings['score'],torches = torches,exitdoor = exitdoor,revealed = True,curse = curse)
        if play.location == exitdoor.location:
            return play
        user = promptinput('[W/A/S/D/Q]: ')
        tickplayerabilities(play)
        if user == 'q':
            dashplayer(play,space)
        else:
            moveplayer(play,user,space)


def cursedsettings (settings, curse):
    stage = dict(settings)
    modifiers = cursemodifiers(curse)
    stage['vision'] = max(1,stage['vision'] + modifiers.get('vision',0))
    stage['necromancers'] = max(0,stage['necromancers'] + modifiers.get('necromancers',0))
    stage['ammo'] = max(0,stage['ammo'] + modifiers.get('ammo',0))
    stage['score'] = max(1,stage['score'] + modifiers.get('score',0))
    stage['torches'] = max(0,stage['torches'] + modifiers.get('torches',0))
    stage['health'] = modifiers.get('health',2)
    stage['bombs'] = modifiers.get('bombs',1)
    stage['torchradius'] = modifiers.get('torchradius',4)
    stage['dashcooldown'] = modifiers.get('dashcooldown',3)
    stage['wardcooldown'] = modifiers.get('wardcooldown',4)
    stage['bombradius'] = modifiers.get('bombradius',2)
    stage['bombfuse'] = modifiers.get('bombfuse',3)
    stage['bulletrange'] = modifiers.get('bulletrange')
    stage['reloadpenalty'] = modifiers.get('reloadpenalty',0)
    return stage


def runstage (settings, curse = None):
    settings = cursedsettings(settings,curse)
    play = player(settings['health'])
    play.ammo = settings['ammo']
    play.bombs = settings['bombs']
    play.dashcooldownbase = settings['dashcooldown']
    play.wardcooldownbase = settings['wardcooldown']
    play.bombradius = settings['bombradius']
    play.bombfuse = settings['bombfuse']
    play.bulletrange = settings['bulletrange']
    play.reloadpenalty = settings['reloadpenalty']
    space = generatespace(play.location)
    explored = set()
    destroyedwalls = set()
    targets,necromancers,bullets,bombs,ammopickup,torches = createstageentities(settings,play,space)
    printgame(play,settings['level'],targets,necromancers,bullets,bombs,ammopickup,space = space,explored = explored,vision = settings['vision'],destroyedwalls = destroyedwalls,scoregoal = settings['score'],torches = torches,curse = curse)

    while play.health > 0 and play.score < settings['score']:
        user = promptinput('[W/A/S/D/E/B/Q/R]: ')
        tickplayerabilities(play)
        play.notice = ''
        playeraction(play,user,bullets,bombs,space)
        ammopickup = collectammo(play,ammopickup)
        bullets = updatebullets(play,bullets,targets,necromancers,space)
        bombs,explosions = updatebombs(play,bombs,targets,necromancers,space,destroyedwalls = destroyedwalls)
        if play.score < settings['score']:
            attackplayer(play,necromancers,space)
            ammopickup = refillstageentities(settings,play,targets,necromancers,bullets,bombs,ammopickup,space,torches)
        printgame(play,settings['level'],targets,necromancers,bullets,bombs,ammopickup,None,explosions,space,explored,settings['vision'],destroyedwalls,settings['score'],torches,curse = curse)
    if play.health <= 0:
        return play
    return exitstage(play,settings,space,torches,curse)


#BOSS FIGHT

def resetplayer (play):
    play.location = [20,9]
    play.model = '^'
    play.score = 0
    if play.bombs < 1:
        play.bombs = 1
    play.status = 'alive'
    play.notice = ''
    play.dashcooldown = 0
    play.wardactive = False
    play.wardcooldown = 0
    play.dashcooldownbase = 3
    play.wardcooldownbase = 4
    play.bombradius = 2
    play.bombfuse = 3
    play.bulletrange = None
    play.reloadpenalty = 0


def bossminionlimit (enemyboss):
    if enemyboss.health < 4:
        return 3
    if enemyboss.health < 8:
        return 2
    return 1


def summonbossminion (play, enemyboss, targets, necromancers, bullets, bombs, ammopickup, space):
    if enemyboss.attackcounter != 0 or len(necromancers) >= bossminionlimit(enemyboss):
        return
    spawnspace = {
        coordinate for coordinate in space
        if abs(coordinate[0] - play.location[0]) + abs(coordinate[1] - play.location[1]) >= 6
    }
    if len(spawnspace) == 0:
        return
    location = openlocation(play,targets,necromancers,bullets,bombs,ammopickup,bosshitbox(enemyboss),spawnspace)
    necromancers.append(necromancer(location))
    play.notice = '~The boss summoned a necromancer.~'


def runboss (play):
    resetplayer(play)
    enemyboss = boss()
    targets = []
    necromancers = []
    bullets = []
    bombs = []
    space = generatespace(play.location,bosshitbox(enemyboss),arena = (2,2,37,15))
    destroyedwalls = set()
    enemyboss.newattack(space)
    location = openlocation(play,targets,necromancers,bullets,bombs,None,bosshitbox(enemyboss),space)
    ammopickup = ammo(location)
    printgame(play,None,targets,necromancers,bullets,bombs,ammopickup,enemyboss,space = space,destroyedwalls = destroyedwalls)

    while play.health > 0 and enemyboss.health > 0:
        user = promptinput('[W/A/S/D/E/B/Q/R]: ')
        tickplayerabilities(play)
        play.notice = ''
        playeraction(play,user,bullets,bombs,space)
        ammopickup = collectammo(play,ammopickup)
        if ammopickup is None:
            location = openlocation(play,targets,necromancers,bullets,bombs,None,bosshitbox(enemyboss),space)
            ammopickup = ammo(location)
        bullets = updatebullets(play,bullets,targets,necromancers,space,enemyboss)
        bombs,explosions = updatebombs(play,bombs,targets,necromancers,space,enemyboss,destroyedwalls)
        if enemyboss.health > 0:
            attackplayer(play,[enemyboss],space)
        if play.health > 0 and enemyboss.health > 0:
            attackplayer(play,necromancers,space)
            summonbossminion(play,enemyboss,targets,necromancers,bullets,bombs,ammopickup,space)
        printgame(play,None,targets,necromancers,bullets,bombs,ammopickup,enemyboss,explosions,space,destroyedwalls = destroyedwalls)

    if enemyboss.health <= 0 and play.health > 0:
        enemyboss.destroyed()
        printgame(play,None,targets,necromancers,bullets,bombs,ammopickup,enemyboss,space = space,destroyedwalls = destroyedwalls)
        print ('          ~You have won the game~         ')
        return True
    return False


def rundebuglevel (level):
    if level < len(STAGES):
        runstage(STAGES[level])
        return
    play = player()
    play.bombs = 1
    runboss(play)


def rungame (debuglevel = None):
    if debuglevel is not None:
        rundebuglevel(debuglevel)
        return
    if not startgame():
        print ('Okay. Hope to see you again!')
        return

    totscore = 0
    play = None
    bag = cursebag()
    for settings in STAGES:
        curse = None
        if settings['level'] > 0:
            curse = continuestage(settings['level'],bag)
            if curse is None:
                return
        play = runstage(settings,curse)
        if play.health <= 0:
            return
        totscore += play.score

    play = runshop(totscore,play)
    runboss(play)
