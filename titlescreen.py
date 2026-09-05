from functions import printscreen


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
        string = '        PRESS [Y] FOR CAMPAIGN        '
        permdict [y] = string
        string = ''
    for y in range (12,13):
        string = '       DEBUG: [0] [1] [2] [3]       '
        permdict [y] = string
        string = ''
    for y in range (13,16):
        for x in range (41):
            string += ' '
        permdict [y] = string
        string = ''

    lines = []
    for x,y in (permdict.items()):
        lines.append(y)
    lines.append('          ~@gongahkia on Github~         ')
    lines.append('')
    lines.append('')
    printscreen(lines)
