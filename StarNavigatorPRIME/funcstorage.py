consonants = list('BCDFGHJKLMNPQRSTVWXYZ')
vowels = list('AEIOU')
c = lambda t,col,back=None: colored(t,col,back)
scol: str = 'light_cyan'; ccol: str = 'light_green'; stcol: str = 'light_yellow'
err = lambda txt: cprint(txt,'white','on_light_red')

# commented means implemented

# def seccoordget(coords):
#     try:
#         for s in sectors:
#             if s.head[0] >= coords[0] > s.corner[0] and s.head[1] >= coords[1] > s.corner[1]:
#                 return s
#     except:
#         err(' ! INVALID SECTOR !')

# noinspection PyTypeChecker  lol
def indexFind(n):
    indexfound = []
    for x in range(len(starObjects)):
        if n in starObjects[x].name:
            cprint(starObjects[x].name,stcol)
            cprint(f'{starObjects[x].x}\n{starObjects[x].y}',ccol)
            print(f'found {n} after {x+1} tries')
            indexfound.append(starObjects[x])
    print(f'found {len(indexfound)} instance(s) of {n}')
    return indexfound

# def dist2D(coords1, coords2):
#     # it looks scary but don't worry it's just a plug and chug
#     return math.sqrt((coords2[0] - coords1[0]) ** 2 + (coords2[1] - coords1[1]) ** 2)


sectorside, secperside = 0, 0
def divsectors2D():
    global sectorside, secperside  # declared global because i have to for some reason
    sectorside = int(galaxydim*divfactor)
    secperside = int(galaxydim/sectorside)  # declare int out of paranoia
    sectorcount = secperside**2  # all of this math is probably unnecessary but i can't be fucked to rewrite it
    corner = [-galaxydim/2,-galaxydim/2]
    head = [-galaxydim/2+sectorside,-galaxydim/2+sectorside]
    print(sectorcount, secperside, sectorside)
    passes = 0
    for y in range(secperside):
        for h in range(secperside):
            sectors.append(Sector(passes,head,corner))
            corner = [corner[0]+sectorside, corner[1]]
            head = [head[0]+sectorside, head[1]]
            passes += 1
        corner = [-galaxydim/2,corner[1]+sectorside]
        head = [-galaxydim/2+sectorside,head[1]+sectorside]
    print(f'''
passes      - {passes}
sectorcount - {sectorcount}
galaxydim   - {galaxydim}
sectorside  - {sectorside} (galaxydim/{divfactor})
secperside  - {secperside}
    ''')

def whereami(p=False):
    global mysector
    success = False
    print('YOU ARE AT:', c(playercoords, ccol))
    for s in sectors:
        if s.head[0] >= playercoords[0] > s.corner[0] and s.head[1] >= playercoords[1] > s.corner[1]:  # head/corner is [x,y]
            mysector = s
            success = True
            break
    if not success:
        mysector = None
    if p:
        try:
            print('\nIN SECTOR', c(mysector.number, scol))
            print('SECTOR BOUNDS:',c(f'{sectors[mysector.number].corner} {sectors[mysector.number].head}',scol))
        except:
            err(' ! INVALID SECTOR !')
    try: return mysector.number
    except: return None

def readsec(sec,p=False):
    num = sec.number
    center = [sectors[num].corner[0] + (sectorside / 2),
    sectors[num].corner[1] + (sectorside / 2)]
    if p:
        while True:
            print(f'''
    SECTOR NUMBER {c(sectors[num].number,scol)}
    STARS : {c(len(sectors[num].stars),stcol)}
    CORNER: {c(sectors[num].corner,scol)}
    HEAD  : {c(sectors[num].head,scol)}
    CENTER: {c(center,scol)}\n
    DISTANCE FROM CORNER: {dist2D(playercoords
                    , sectors[num].corner)}
    DISTANCE FROM HEAD  : {dist2D(playercoords
                    , sectors[num].head)}
    DISTANCE FROM CENTER: {dist2D(playercoords,center)}\n
    [L] for list of stars, [I] to search the index, else [B]ack
                        ''')
            func = input('> ')
            if func == 'L':
                listsecstars(num)
            if func == 'I':
                indexFind(input('> '))
            if func == 'B':
                break
    if not p:
        return len(sectors[num].stars)

# noinspection PyTypeChecker
def secfinder():
    global mysector
    whereami()
    try:
        print('CURRENTLY AT SECTOR', c(mysector.number, scol))
    except:
        err(' ! INVALID SECTOR !')
    cprint('[C]oord OR [N]umber or [ENTER] for current', ccol)
    func = input('> ')
    if func == 'C':
        print('INPUT COORDS')
        findertargetX = int(input('X = '))
        findertargetY = int(input('Y = '))
        target = [findertargetX, findertargetY]
        print('TARGET SECTOR:', c(seccoordget(target),scol))

        return seccoordget(target)
    if func == 'N':
        # noinspection PyTypeChecker
        cprint('INPUT SECTOR NUMBER', ccol)
        num = int(input('> '))
        try: return sectors[num]
        except: err(' ! INVALID SECTOR !')
    else:
        try: return mysector
        except:
            err(' ! INVALID SECTOR !')
            mysector = None

def listsecstars(sec):
    try:
        cprint('________________________________________','dark_grey')
        for star in sectors[sec].stars:
            print('    ', c(star.name,stcol),'\n',
                  star.x,'\n',star.y)
        print('\n',len(sectors[sec].stars),'STARS IN SECTOR')
    except: err(' ! INVALID SECTOR !')

def roughmap():
    global mysector, secperside
    secarray = np.empty((secperside,secperside))
    p = 0
    for y in range(secperside):
        for x in range(secperside):
            # if mysector.number == p:  TODO mark location on textmap
            #     print('found it',mysector.number,p)
            # secarray[x,y] = c(len(sectors[p].stars),ccol)
            # else:
            secarray[x,y] = len(sectors[p].stars)
            p += 1
    secarray = np.flip(secarray, axis=0)
    return secarray

# noinspection PyTypeChecker
def go():
    global playercoords, mysector
    cprint(f'WORLD BOUNDS:{[-galaxydim/2,-galaxydim/2]},{[galaxydim/2,galaxydim/2]}',ccol)
    cprint('INPUT DESIRED LOCATION',ccol)
    gotoX = float(input('X = '))
    gotoY = float(input('Y = '))
    goto = [gotoX,gotoY]
    target = seccoordget(goto)
    try:
        print(f'TARGET SECTOR: {c(target.number,scol)}\n'
              f'TARGET STARS: {c(len(target.stars),stcol)}')
    except: err(' ! INVALID SECTOR !')
    LD = dist2D(playercoords,goto)
    print(LD,'LD AWAY\nor',LD/365,'LY AWAY\n',
          c('to GO, type CONFIRM','white','on_magenta'))
    confirmation = input('\n>>    ')
    if confirmation == 'CONFIRM':
        playercoords = goto
        try:
            mysector = sectors[whereami(True)]
        except: err(' ! INVALID SECTOR !')