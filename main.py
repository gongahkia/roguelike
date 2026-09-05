from titlescreen import titlescreen
from functions import BOARDHEIGHT, BOARDWIDTH, player, bullet, bomb, ammo, target, necromancer, boss, randomlocation, generatespace, moveplayer, attackplayer, bombcoordinates, destroyterrain, bosshitbox, updateboss, updatedict, visiblecoordinates, fogdict, printdict, interface, promptinput, threatconlvl, runshop


#GAME SETTINGS

STAGES = [
    {'level': 0, 'targets': 1, 'necromancers': 0, 'score': 3, 'ammo': 1, 'vision': 6},
    {'level': 1, 'targets': 3, 'necromancers': 0, 'score': 4, 'ammo': 1, 'vision': 5},
    {'level': 2, 'targets': 1, 'necromancers': 2, 'score': 5, 'ammo': 2, 'vision': 4}
]


#GENERAL FUNCTIONS

def startgame ():
    while True:
        titlescreen()
        user = promptinput('[Y/N/0/1/2/3]: ')
        if user == 'y':
            return 'campaign'
        if user == 'n':
            return None
        if user in ['0','1','2','3']:
            return user


def continuestage (level):
    while True:
        threatconlvl(level)
        acknowledgement = promptinput('[Y to continue/N to leave]: ')
        if acknowledgement == 'y':
            return True
        if acknowledgement == 'n':
            print ('Thanks for playing!')
            return False


def occupiedcoordinates (play, targets, necromancers, bullets, bombs, ammopickup = None, blocked = None):
    occupied = {tuple(play.location)}
    for item in targets + necromancers + bullets + bombs:
        occupied.add(tuple(item.location))
    if ammopickup is not None:
        occupied.add(tuple(ammopickup.location))
    if blocked is not None:
        occupied.update(blocked)
    return occupied


def openlocation (play, targets, necromancers, bullets, bombs, ammopickup = None, blocked = None, space = None):
    occupied = occupiedcoordinates(play,targets,necromancers,bullets,bombs,ammopickup,blocked)
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

    for number in range(settings['targets']):
        location = openlocation(play,targets,necromancers,bullets,bombs,space = targetspace(settings,play,space))
        targets.append(target(location))
    for number in range(settings['necromancers']):
        location = openlocation(play,targets,necromancers,bullets,bombs,space = space)
        necromancers.append(necromancer(location))
    location = openlocation(play,targets,necromancers,bullets,bombs,space = space)
    ammopickup = ammo(location)
    return targets,necromancers,bullets,bombs,ammopickup


def refillstageentities (settings, play, targets, necromancers, bullets, bombs, ammopickup, space):
    while len(targets) < settings['targets']:
        location = openlocation(play,targets,necromancers,bullets,bombs,ammopickup,space = targetspace(settings,play,space))
        targets.append(target(location))
    while len(necromancers) < settings['necromancers']:
        location = openlocation(play,targets,necromancers,bullets,bombs,ammopickup,space = space)
        necromancers.append(necromancer(location))
    if ammopickup is None:
        location = openlocation(play,targets,necromancers,bullets,bombs,space = space)
        ammopickup = ammo(location)
    return ammopickup


def collectammo (play, ammopickup):
    if play.location == ammopickup.location:
        play.reload()
        play.notice = '~Ammo collected.~'
        return None
    return ammopickup


def playeraction (play, user, bullets, bombs, space):
    moveplayer(play,user,space)
    if play.model == '*' or play.health <= 0:
        return
    if user == 'e':
        if play.shoot():
            bullets.append(bullet(play.model,play.location))
        else:
            play.notice = '~No more ammo, find more to shoot.~'
    if user == 'b':
        if play.bombs <= 0:
            play.notice = '~No bombs left. Buy bombs in the shop.~'
        else:
            bombs.append(bomb(play.location))
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
            if tuple(item.location) not in space:
                continue
            remaining.append(item)
            continue
        item.movement()
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


def updatebombs (play, bombs, targets, necromancers, space, enemyboss = None):
    explosions = set()
    remaining = []
    for item in bombs:
        if not item.tick():
            remaining.append(item)
            continue

        destroyterrain(item,space)
        blast = bombcoordinates(item,space)
        explosions.update(blast)
        if tuple(play.location) in blast:
            play.attacked()
            play.notice = '~You were caught in the blast.~'
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


def printgame (play, level = None, targets = None, necromancers = None, bullets = None, bombs = None, ammopickup = None, enemyboss = None, explosions = None, space = None, explored = None, vision = 5):
    entitydict = updatedict(play,targets,necromancers,bullets,bombs,ammopickup,enemyboss,explosions)
    if space is not None and explored is not None:
        visible = visiblecoordinates(play,space,vision)
        explored.update(visible)
        entitydict = fogdict(entitydict,space,visible,explored)
    printdict(entitydict)
    interface(play,level,enemyboss,0 if bombs is None else len(bombs))


#THREATCON LEVELS

def runstage (settings):
    play = player()
    play.ammo = settings['ammo']
    play.bombs = 1
    space = generatespace(play.location)
    explored = set()
    targets,necromancers,bullets,bombs,ammopickup = createstageentities(settings,play,space)
    printgame(play,settings['level'],targets,necromancers,bullets,bombs,ammopickup,space = space,explored = explored,vision = settings['vision'])

    while play.health > 0 and play.score < settings['score']:
        user = promptinput('[W/A/S/D/E/B]: ')
        play.notice = ''
        playeraction(play,user,bullets,bombs,space)
        ammopickup = collectammo(play,ammopickup)
        bullets = updatebullets(play,bullets,targets,necromancers,space)
        bombs,explosions = updatebombs(play,bombs,targets,necromancers,space)
        attackplayer(play,necromancers,space)
        ammopickup = refillstageentities(settings,play,targets,necromancers,bullets,bombs,ammopickup,space)
        printgame(play,settings['level'],targets,necromancers,bullets,bombs,ammopickup,None,explosions,space,explored,settings['vision'])
    return play


#BOSS FIGHT

def resetplayer (play):
    play.location = [20,9]
    play.model = '^'
    play.score = 0
    if play.bombs < 1:
        play.bombs = 1
    play.status = 'alive'
    play.notice = ''


def runboss (play):
    resetplayer(play)
    enemyboss = boss()
    targets = []
    necromancers = []
    bullets = []
    bombs = []
    space = generatespace(play.location,bosshitbox(enemyboss))
    explored = set()
    enemyboss.newattack(space)
    location = openlocation(play,targets,necromancers,bullets,bombs,None,bosshitbox(enemyboss),space)
    ammopickup = ammo(location)
    printgame(play,None,targets,necromancers,bullets,bombs,ammopickup,enemyboss,space = space,explored = explored)

    while play.health > 0 and enemyboss.health > 0:
        user = promptinput('[W/A/S/D/E/B]: ')
        play.notice = ''
        playeraction(play,user,bullets,bombs,space)
        ammopickup = collectammo(play,ammopickup)
        if ammopickup is None:
            location = openlocation(play,targets,necromancers,bullets,bombs,None,bosshitbox(enemyboss),space)
            ammopickup = ammo(location)
        bullets = updatebullets(play,bullets,targets,necromancers,space,enemyboss)
        bombs,explosions = updatebombs(play,bombs,targets,necromancers,space,enemyboss)
        if enemyboss.health > 0:
            attackplayer(play,[enemyboss],space)
        printgame(play,None,targets,necromancers,bullets,bombs,ammopickup,enemyboss,explosions,space,explored)

    if enemyboss.health <= 0 and play.health > 0:
        enemyboss.destroyed()
        printgame(play,None,targets,necromancers,bullets,bombs,ammopickup,enemyboss,space = space,explored = explored)
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


def rungame ():
    selection = startgame()
    if selection is None:
        print ('Okay. Hope to see you again!')
        return
    if selection != 'campaign':
        rundebuglevel(int(selection))
        return

    totscore = 0
    play = None
    for settings in STAGES:
        if settings['level'] > 0:
            if not continuestage(settings['level']):
                return
        play = runstage(settings)
        if play.health <= 0:
            return
        totscore += play.score

    play = runshop(totscore,play)
    runboss(play)
