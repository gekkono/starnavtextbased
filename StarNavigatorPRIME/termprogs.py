func = None
# todo: please for the love of god make this less stupid
if func == 'dist':
    while True:
        print(f'''
FIRST POINT
{c('[ENTER] for here',ccol)}
{c('[S] for system (star)',stcol)}
{c('[C] for sector (rough)',scol)}
[E] to manually enter
[B] to escape this program
''')
        func = input('> ')
        if func == 'S':
            while True:
                first = indexFind(input(''))
                if len(first) > 1:
                    print('TOO MANY RESULTS: ',len(first))
                    print('[R]etry OR BACK')
                    func = input('> ')
                    if func == 'R':
                        print('RERUNNING')
                    else:
                        break
                elif len(first) == 1:
                    first = [first[0].x, first[0].y]
                    break
                elif len(first) < 1:
                    print('NO RESULTS')
                    print('[R]etry OR BACK')
                    func = input('> ')
                    if func == 'R':
                        print('RERUNNING')
                    else:
                        break
        elif func == 'C':
            first = secfinder()
            print(first.number)
        elif func == 'E':
            while True:
                print('INPUT COORDS')
                try:
                    targetX = int(input('X = '))
                    targetY = int(input('Y = '))
                    first = [targetX, targetY]
                    targetsector = seccoordget(first)
                    break
                except: err(' ! INVALID SECTOR !')
        elif func == 'B':
            break
        else:
            first = playercoords
        print(f'''
SECOND POINT
{c('[ENTER] for here',ccol)}
{c('[S] for system (star)',stcol)}
{c('[C] for sector (rough)',scol)}
[E] to manually enter
[B] to escape this program
''')
        func = input('> ')
        if func == 'S':
            while True:
                try:
                    second = indexFind(input('STAR NAME\n> '))
                    if len(second) > 1:
                        print('TOO MANY RESULTS: ', len(second))
                        print('[N]arrow OR BACK')
                        func = input('> ')
                        if func == 'N':
                            print('RERUNNING')
                        else:
                            break
                    else:
                        second = [second[0].x, second[0].y]
                        break
                except:
                    pass
        elif func == 'C':
            while True:
                # try:
                    second = secfinder()
                    print(second.number)
                    break
                # except:
                #     pass
        elif func == 'E':
            while True:
                print('INPUT COORDS')
                try:
                    targetX = int(input('X = '))
                    targetY = int(input('Y = '))
                    second = [targetX, targetY]
                    targetsector = seccoordget(second)
                    break
                except: err(' ! INVALID SECTOR !')
        elif func == 'B':
            break
        else:
            second = playercoords
        try:
            print(first,'\n',second)
            print('DISTANCE BETWEEN P1 and P2:',dist2D(first,second))
        except:
            print('ERROR')

