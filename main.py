from titlescreen import titlescreen
from functions import player, bullet, ammo, target, necromancer, boss, dictcreator, dictcreatorwbullets, dictcreator3, dictcreatorwbullets3, dictcreator6, dictcreatorwbullets6, dictcreator9, dictcreatorwbullets9, interface2, runshop, printdict, interface, threatconlvl
import time

def rungame ():

    condition = True
    
    while condition == True:
        titlescreen()
        user = input ('[Y/N]: ')
        
        if user == 'y':
            condition = False

        if user == 'n':
            print ('Okay. Hope to see you again!')
            exit()


########################################################

    p = player()
    t = target()
    a = ammo()
    totscore = 0
   
    printdict(dictcreator(p, t, a))
    interface(p)
    numbullets = 0
    threatcon_lvl = 0

########################################################

    while threatcon_lvl == 0:

        user = input('[W/A/S/D/E]: ')
        p.notice = ''


        #handling orientation and movement of player
        if p.model == '^' and user == 'w':
                p.movement(user)
        if p.model == '<' and user == 'a':
            p.movement (user)
        if p.model == 'V' and user == 's':
            p.movement (user)
        if p.model == '>' and user == 'd':
            p.movement (user)
        p.face(user)

        if p.location[0]< 0:
            p.location[0] = 0 
        if p.location[0] > 40: 
            p.location[0] = 40  
        if p.location[1] < 0: 
            p.location[1] = 0  
        if p.location[1] > 18:
            p.location[1] = 18

        if p.location == a.location:
            p.reload()
            a.destroyed()
            a = ammo()

        if numbullets == 1:
            b.movement()
            if b.location == t.location:
                b.collision()
                p.reload()
                p.notice = ''
                p.score += 1
                numbullets = 2

            elif b.location[0] < 0 or b.location[0] > 41 or b.location[1] < 0 or b.location[1] > 19:
                b.collision()
                p.reload()
                p.notice = ''
                numbullets = 0
        
        elif numbullets == 2:
            b.disappear()
            t.destroyed()
            numbullets = 3

        elif numbullets == 3:
            t = target()
            numbullets = 0
            #t = target()

        #handling shooting 
        if user == 'e':
            if numbullets == 0:
                if p.ammo > 0:
                    p.shoot()
                    b = bullet(p.model,p.location)
                    print(b.location)
                    printdict(dictcreatorwbullets(p, t, b, a))
                    numbullets = 1

                if p.ammo == 0:
                    p.notice = '~No more ammo, find more to shoot.~'
                
        if numbullets == 0:
            printdict(dictcreator(p, t, a))

        if numbullets == 1 or numbullets == 2 or numbullets == 3:
            printdict(dictcreatorwbullets(p, t, b, a))

        if p.score > 2:
            totscore += p.score
            threatcon_lvl += 1
            p.deconstruct()
            break

        interface(p)

########################################################

    while threatcon_lvl == 1:
        threatconlvl(threatcon_lvl)
        
        acknowledgement = input('[Y to continue/N to leave]')

        if acknowledgement == 'n':
            print ('Thanks for playing!')
            exit()

        else:
            break

        
    
    p = player()
    t1 = target()
    t2 = target()
    t3 = target()
    a = ammo()
    numbullets = 0
    p.ammo = 1
    p.notice = ''

    printdict(dictcreator3(p,t1,t2,t3,a))
    interface(p)

    while threatcon_lvl == 1:
    
        user = input('[W/A/S/D/E]: ')
        p.notice = ''


        #handling orientation and movement of player
        if p.model == '^' and user == 'w':
                p.movement(user)
        if p.model == '<' and user == 'a':
            p.movement (user)
        if p.model == 'V' and user == 's':
            p.movement (user)
        if p.model == '>' and user == 'd':
            p.movement (user)
        p.face(user)

        if p.location[0]< 0:
            p.location[0] = 0 
        if p.location[0] > 40: 
            p.location[0] = 40  
        if p.location[1] < 0: 
            p.location[1] = 0  
        if p.location[1] > 18:
            p.location[1] = 18        

        if p.location == a.location:
            p.reload()
            a.destroyed()
            a = ammo()

        if numbullets == 1:
            b.movement()

            if b.location == t1.location:
                b.collision()
                p.reload()
                p.notice = ''
                p.score += 1
                numbullets = 2

            elif b.location == t2.location:
                t2.destroyed()
                numbullets = 4

            elif b.location == t3.location:
                t3.destroyed()
                numbullets = 5

            elif b.location[0] < 0 or b.location[0] > 41 or b.location[1] < 0 or b.location[1] > 19:
                b.collision()
                p.reload()
                p.notice = ''
                numbullets = 0
        
        elif numbullets == 2:
            b.disappear()
            t1.destroyed()
            numbullets = 3

        elif numbullets == 3:
            t1 = target()
            numbullets = 0
            #t = target()

        elif numbullets == 4:
            t2 = target()
            numbullets = 0

        elif numbullets == 5:
            t3 = target()
            numbullets = 0

        #handling shooting 
        if user == 'e':
            if numbullets == 0:
                if p.ammo == 0:
                    p.notice = '~No more ammo, find more to shoot.~'
    
                if p.ammo > 0:
                    p.shoot()
                    b = bullet(p.model,p.location)
                    print(b.location)
                    printdict(dictcreatorwbullets3(p, t1, t2, t3, b, a))
                    numbullets = 1

            if numbullets == 1:
                if p.ammo == 0:
                    p.notice = '~No more ammo, find more to shoot.~'
                
        if numbullets == 0:
            printdict(dictcreator3(p,t1,t2,t3,a))

        if numbullets == 1 or numbullets == 2 or numbullets == 3 or numbullets == 4 or numbullets == 5:
            printdict(dictcreatorwbullets3(p, t1, t2, t3, b, a))

        interface(p)

        if p.score > 2:
            totscore += p.score
            threatcon_lvl += 1
            p.deconstruct()
            t1.destroyed()
            t2.destroyed()
            t3.destroyed()
            break


########################################################

    while threatcon_lvl == 2:
        threatconlvl(threatcon_lvl)
        
        acknowledgement = input('[Y to continue/N to leave]')

        if acknowledgement == 'n':
            print ('Thanks for playing!')
            exit()

        else:
            break
    
    p = player()
    t1 = target()
    n1 = necromancer()
    n2 = necromancer()
    a = ammo()
    numbullets = 0
    p.ammo = 1
    p.notice = ''

    printdict(dictcreator6(p,t1,n1,n2,a))
    interface(p)

    while threatcon_lvl == 2:
        if p.health <= 0:
            time.sleep(4.5)
            exit()

        user = input('[W/A/S/D/E]: ')
        p.notice = ''

#when player is attacked by necromancer
        if p.model == '*':
            if user == 'w':
                p.model = '^'
                p.movement (user)
            elif user == 'a':
                p.model = '<'
                p.movement (user)
            elif user == 's':
                p.model = 'V'
                p.movement (user)
            elif user == 'd':
                p.model = '>'
                p.movement (user)

    #handling orientation and movement of player
        if p.model == '^' or p.model == '<' or p.model == 'V' or p.model == '>':   
            if p.model == '^' and user == 'w':
                    p.movement(user)
            if p.model == '<' and user == 'a':
                p.movement (user)
            if p.model == 'V' and user == 's':
                p.movement (user)
            if p.model == '>' and user == 'd':
                p.movement (user)
            p.face(user)

        if p.location[0]< 0:
            p.location[0] = 0 
        if p.location[0] > 40: 
            p.location[0] = 40  
        if p.location[1] < 0: 
            p.location[1] = 0  
        if p.location[1] > 18:
            p.location[1] = 18

        n1.attack()
        n2.attack()        

        if p.location == a.location:
            p.reload()
            a.destroyed()
            a = ammo()

        if n1.xcoord == p.location[0]:
            if n1.attackcounter == 2:
                p.model = '*'
                p.attacked()
                if user == 'e':
                    p.notice = "~Necromancer froze you. Can't shoot!~"
            else:
                pass

        if n2.xcoord == p.location[0]:
            if n2.attackcounter == 2:
                p.model = '*'
                p.attacked()
                if user == 'e':
                    p.notice = "~Necromancer froze you. Can't shoot!~"

        if numbullets == 1:
            b.movement()

            if b.location == t1.location:
                b.collision()
                p.reload()
                p.notice = ''
                p.score += 1
                numbullets = 2

            elif b.location == n1.location:
                #n1.collision()
                n1.damaged()
                if n1.health <= 0:
                    n1.destroyed()
                    numbullets = 4
                    p.score += 1
                    p.reload()
                    p.reload()
                else:
                    numbullets = 0

            elif b.location == n2.location:
                #n2.collision()
                n2.damaged()
                if n2.health <= 0:
                    n2.destroyed()
                    numbullets = 5
                    p.score += 1
                    p.reload()
                    p.reload()
                else:
                    numbullets = 0

            elif b.location[0] < 0 or b.location[0] > 41 or b.location[1] < 0 or b.location[1] > 19:
                b.collision()
                p.reload()
                p.notice = ''
                numbullets = 0
        
        elif numbullets == 2:
            b.disappear()
            t1.destroyed()
            numbullets = 3

        elif numbullets == 3:
            t1 = target()
            numbullets = 0
            #t = target()

        elif numbullets == 4:
            n1 = necromancer()
            numbullets = 0

        elif numbullets == 5:
            n2 = necromancer ()
            numbullets = 0

        #handling shooting 
        if p.model == '^' or p.model == '<' or p.model == 'V' or p.model == '>':
            if user == 'e':
                if numbullets == 0:
                    if p.ammo == 0:
                        p.notice = '~No more ammo, find more to shoot.~'
        
                    if p.ammo > 0:
                        p.shoot()
                        b = bullet(p.model,p.location)
                        #print(b.location)
                        printdict(dictcreatorwbullets6(p, t1, n1, n2, b, a))
                        numbullets = 1
                
                if numbullets == 1:
                    if p.ammo == 0:
                        p.notice = '~No more ammo, find more to shoot.~'
                
        if numbullets == 0:
            printdict(dictcreator6(p, t1, n1, n2, a))

        if numbullets == 1 or numbullets == 2 or numbullets == 3 or numbullets == 4 or numbullets == 5:
            printdict(dictcreatorwbullets6(p, t1, n1, n2, b, a))

        interface(p)

        if p.score > 2:
            totscore += p.score
            threatcon_lvl += 1
            p.deconstruct()
            t1.destroyed()
            n1.destroyed()
            n2.destroyed()
            a.destroyed()
            break

########################################################
    while threatcon_lvl == 3:
        threatconlvl(threatcon_lvl)
    
        acknowledgement = input('[Y to continue/N to leave]')

        if acknowledgement == 'n':
            print ('Thanks for playing!')
            exit()

        else:
            break
    
    val = runshop(totscore, p)

########################################################

    while threatcon_lvl == 3:
        threatconlvl(threatcon_lvl)
    
        acknowledgement = input('[Y to continue/N to leave]')

        if acknowledgement == 'n':
            print ('Thanks for playing!')
            exit()

        else:
            break

    playerhealth = int(val[0])
    playerammo = int(val[1])

    p = player()
    boz = boss()
    a = ammo()
    numbullets = 0
    p.notice = ''

    p.health = playerhealth
    p.ammo = playerammo

    printdict(dictcreator9(p,boz,a))
    interface2(p,boz)

    while threatcon_lvl == 3:

        if p.health <= 0:
            time.sleep(4.5)
            exit()

        user = input('[W/A/S/D/E]: ')
        p.notice = ''

    #when player is attacked by boss
        if p.model == '*':
            if user == 'w':
                p.model = '^'
                p.movement (user)
            elif user == 'a':
                p.model = '<'
                p.movement (user)
            elif user == 's':
                p.model = 'V'
                p.movement (user)
            elif user == 'd':
                p.model = '>'
                p.movement (user)

    #handling orientation and movement of player
        if p.model == '^' or p.model == '<' or p.model == 'V' or p.model == '>':   
            if p.model == '^' and user == 'w':
                    p.movement(user)
            if p.model == '<' and user == 'a':
                p.movement (user)
            if p.model == 'V' and user == 's':
                p.movement (user)
            if p.model == '>' and user == 'd':
                p.movement (user)
            p.face(user)

        if p.location[0]< 0:
            p.location[0] = 0 
        if p.location[0] > 40: 
            p.location[0] = 40  
        if p.location[1] < 0: 
            p.location[1] = 0  
        if p.location[1] > 18:
            p.location[1] = 18

        boz.attack()   

        if p.location == a.location:
            p.reload()
            a.destroyed()
            a = ammo()

        if boz.xcoord == p.location[0]:
            if boz.attackcounter == 2:
                p.model = '*'
                p.attacked()
                if user == 'e':
                    p.notice = "~Boss immobilized you. Can't shoot!~"
        
        if boz.ycoord == p.location[1]: 
            if boz.attackcounter == 2:
                p.model = '*'
                p.attacked()
                if user == 'e':
                    p.notice = "~Boss immobilized you. Can't shoot!~"

        if boz.xcoord2 == p.location[0]:
            if boz.attackcounter == 2:
                p.model = '*'
                p.attacked()
                if user == 'e':
                    p.notice = "~Boss immobilized you. Can't shoot!~"
        
        if boz.ycoord2 == p.location[1]: 
            if boz.attackcounter == 2:
                p.model = '*'
                p.attacked()
                if user == 'e':
                    p.notice = "~Boss immobilized you. Can't shoot!~"

        if numbullets == 1:
            b.movement()

            if b.location[1] == 1:
                if b.location[0] >= 16 and b.location[0] <= 24:
                    b.collision()
                    p.notice = ''
                    numbullets = 2

            elif b.location[0] < 0 or b.location[0] > 41 or b.location[1] < 0 or b.location[1] > 19:
                b.collision()
                p.reload()
                p.notice = ''
                numbullets = 0
        
        elif numbullets == 2:
            b.disappear()
            boz.damaged()
            numbullets = 0

        #handling shooting 
        if p.model == '^' or p.model == '<' or p.model == 'V' or p.model == '>':
            if user == 'e':
                if numbullets == 0:
                    if p.ammo == 0:
                        p.notice = '~No more ammo, find more to shoot.~'
        
                    if p.ammo > 0:
                        p.shoot()
                        b = bullet(p.model,p.location)
                        #print(b.location)
                        printdict(dictcreatorwbullets9(p,boz,b,a))
                        numbullets = 1
                
                if numbullets == 1:
                    if p.ammo == 0:
                        p.notice = '~No more ammo, find more to shoot.~'

        if boz.health < 8:
            boz.phase2()

        if boz.health < 4:
            boz.phase3()

        if boz.health < 2:
            boz.phase4()
                
        if numbullets == 0:
            printdict(dictcreator9(p,boz,a))

        if numbullets == 1 or numbullets == 2:
            printdict(dictcreatorwbullets9(p, boz, b, a))

        interface2(p,boz)


    #placeholder for gameover screen
        if boz.health <= 0:
            boz.destroyed()
            threatcon_lvl += 1
            try:
                printdict(dictcreator9(p,boz,a))
            except:
                printdict(dictcreatorwbullets9(p, boz, b, a))
            interface2(p,boz)
            print ('          ~You have won the game~         ')
            exit()

########################################################
