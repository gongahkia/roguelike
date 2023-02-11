def titlescreen ():
    permdict = {}
    for y in range (0,5):
        string = ''
        for x in range (41):
            string += ' '
        permdict [y] = string
        string = ''
    for y in range (5,6):
        string = '          ---------------------          '
        permdict [y] = string
        string = ''
    for y in range(6,7):
        string = '          |       R.I.P       |          '
        permdict [y] = string
        string = ''
    for y in range (7,8):
        string = '          |     ENTER KEY     |          '
        permdict[y] = string
        string = ''
    for y in range (8,9):
        string = '          ---------------------          '
        permdict [y] = string
        string = ''
    for y in range (9,11):
        for x in range (41):
            string += ' '
        permdict [y] = string
        string = ''
    for y in range (11,12):
        string = '            PRESS [Y] TO PLAY            '
        permdict [y] = string
        string = ''
    for y in range (12,16):
        for x in range (41):
            string += ' '
        permdict [y] = string
        string = ''

    #print (permdict)

    print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    for x,y in (permdict.items()):
        print (f'X{y}X')
    print ('X          ~@gongahkia on Github~         X')
    print ('X                                         X')
    print ('X                                         X')
    print ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
