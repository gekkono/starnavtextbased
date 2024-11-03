import multiprocessing, time
import threading
import random, math, string, sys
rint = lambda x, y: random.randint(x, y)
import numpy as np
from colorama import just_fix_windows_console
just_fix_windows_console()
from termcolor import *
import pygame
import multiprocessing
import inflect
inflectengine = inflect.engine()

consonants = list('BCDFGHJKLMNPQRSTVWXYZ')
vowels = list('AEIOU')
c = lambda t,col,back=None: colored(t,col,back)
scol: str = 'light_cyan'; ccol: str = 'light_green'; stcol: str = 'light_yellow'
err = lambda txt: cprint(txt,'white','on_light_red')

cprint('''\n\n\n
this program is running the following (external) libraries:\n
NUMPY
COLORAMA
PYGAME
''','light_cyan')

# config ============
starTarget = 10000000
dim3 = False
galaxydim = 6400  # in LIGHT DAYS. the milky way is about 36500000 LD across but we "round up"
# 40000000 is the default
divfactor = 0.12
# galaxyheight = 4000
playercoords = [1,1]
debug = True
# end config ========
class Star:
    def __init__(self):
        self.x = random.gauss(mu=0, sigma=(galaxydim/5))
        if self.x > galaxydim: self.x = galaxydim - rint(100, 2000)
        if self.x < -galaxydim: self.x = -galaxydim + rint(100, 2000)
        self.y = random.gauss(mu=0, sigma=(galaxydim/5))
        if self.y > galaxydim: self.y = galaxydim - rint(100, 2000)
        if self.y < -galaxydim: self.y = -galaxydim + rint(100, 2000)
        # NOTICE: our galactic coords are in LIGHT DAYS, not light YEARS!
        # if dim3:  # lol that's never gonna happen
        #     self.z = random.gauss(0, 1000)
        #     if self.z > galaxyheight: self.z = galaxyheight - rint(100, 2000)
        #     if self.z < -galaxyheight: self.z = -galaxyheight - rint(100, 2000)
        namelist = random.choices(string.ascii_letters, k=32)
        self.name = ''.join(namelist) + '-' + str(rint(100, 999))
        self.cl = 0  # todo: star classes, satellites, bi systems, etc.
class Sector:
    def __init__(self, number, head, corner):
        self.number = number
        self.head = head
        self.corner = corner
        self.stars = []
class Planet:
    def __init__(self,ptype,pname=None,starobj=None):
        self.starobj = starobj
        if self.starobj and not pname:  # typical rng case
            self.pname = random.choices(vowels, k=6) + str(starobj.name[0,6])
        elif not self.starobj and not pname:  # generate rogue planet
            self.pname = random.choices(vowels, k=6) + '-ROGUE'
        elif self.starobj and pname:  # given name overrides system designation
            self.pname = pname
        else: self.pname = random.choices(vowels, k=6) + '-ROGUE'  # spawn rogue planet
class Station:
    def __init__(self,starobj,planet,name=None):
        if name: self.name = name
        else: self.name = random.choices(vowels, k=6) + '-' + str(rint(10, 99)) + '-' + str(rint(10, 99))
        self.starobj = starobj
        self.planet = planet

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

def dist2D(coords1, coords2):
    # it looks scary but don't worry it's just a plug and chug
    return math.sqrt((coords2[0] - coords1[0]) ** 2 + (coords2[1] - coords1[1]) ** 2)


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

def seccoordget(coords):
    try:
        for s in sectors:
            if s.head[0] >= coords[0] > s.corner[0] and s.head[1] >= coords[1] > s.corner[1]:
                return s
    except:
        err(' ! INVALID SECTOR !')

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

starObjects = []
def gen(returner,starstomake,procnum):
    starsmade = []  # stars made by THIS proc (for multiproc)
    for i in range(int(starstomake)):
        star = Star()
        # if debug: print(star.name, ' number: ', len(starsmade), ' of: ', starTarget)
        starsmade.append(star)
    returner.append(starsmade)
    print(f'****this is gen proc number {procnum} closing without issue')


def distributestars(procnum,returned):  # probably won't be needing this again -me before using it again
    receivedsectors = sectors
    # figure out which sectors we work on
    sectorcount = len(sectors)
    findstep = int(sectorcount/8)
    startat = int(findstep*procnum)
    if procnum != 7: reduc = -1
    else: reduc = 0
    workingsectors = receivedsectors[startat : (startat+findstep)]
    # print(f'>>>>i am process number {procnum} reporting: step {findstep} starting at {startat} ending at {startat+findstep}')
    for star in returned[procnum]:
        for s in workingsectors:
            if s.head[0] >= star.x > s.corner[0] and s.head[1] >= star.y > s.corner[1]:  # head/corner is [x,y]
                s.stars.append(star)
    # we have a chunk of sectors processed. now we must give it to the manager
    managed_sectorchunks[procnum] = workingsectors
    print(f'////this is distrib proc number {procnum} closing without issue')

numprocs = 12
if __name__ == '__main__':
    # freeze_support()
    manager = multiprocessing.Manager()
    return_list = manager.list()
    sectors = manager.list()
    divsectors2D()
    print('\n.  .  .\n')
    mysector = sectors[whereami()]
    print('\n\n\nCREATING', c(starTarget, 'light_magenta'),
          'STARS\nPLEASE WAIT\n'
    f'(in words, that is {inflectengine.number_to_words(starTarget)} stars)\n\n\n')

    jobs = []
    for i in range(numprocs):
        p = multiprocessing.Process(target=gen, args=(return_list,(int(starTarget/numprocs)),i))
        jobs.append(p)
        p.start()
        print(f'started proc {i} with {int(starTarget/numprocs)} stars to make')
    processing = True
    procsdead = 0
    while processing:
        time.sleep(2)
        for proc in jobs:
            if proc.is_alive():
                processing = True
            else:
                procsdead += 1
        if procsdead == numprocs:
            processing = False; print('****generation multiprocs closed')
        else: procsdead = 0
    time.sleep(2)
    for proc in jobs:
        proc.join()

    managed_sectorchunks = manager.list([[],[],[],[],[],[],[],[]])
    # the distrib processes will dump their results into their slot, index designated by procnum
    # this makes sure that the sectors are in order and do not get mixed up
    # we boil them down later

    jobs = []
    for i in range(numprocs):
        p = multiprocessing.Process(target=distributestars,
                                    args=(i,return_list))
        jobs.append(p)
        p.start()
        print(f'started proc {i} to distribute some stars')

    processing = True
    procsdead = 0
    while processing:
        time.sleep(2)
        for proc in jobs:
            if proc.is_alive():
                processing = True
            else:
                procsdead += 1
        if procsdead == numprocs:
            processing = False; print('////distribution multiprocs closed')
        else:
            procsdead = 0
    time.sleep(2)
    for proc in jobs:
        proc.join()

    # now we need to boil down those sectors into one big list again
    sectors = [
        x
        for xs in managed_sectorchunks
        for x in xs
    ]
    print(len(sectors),'sectors filled with stars!')

    print(c('\nGENERATION PHASE COMPLETED','light_magenta'))
    del starObjects, managed_sectorchunks, return_list, manager, jobs, processing, procsdead  # save some ram

whereami(True)
print(roughmap())

termrunning = True
while termrunning:
    print('- - - - - - - -')
    func = input('> ')
    if func == 'help':
        cprint('''
help.....- you are here! feel free to visit any time\n
where....- tells you where you are!
galmap...- shows a rough map of the galaxy
[WIP]stations.- tells you where stations are in this sector\n
secread..- detailed reading on this or other sectors
find.....- search for a star anywhere in the galaxy
dist.....- find the distance of another point or thing in space
plotter..- plan a trip across multiple waypoints\n
go.......- go to a different set of coordinates
        ''','magenta')
    if func == 'helpgodmode':
        cprint('''
genstars.........- generate more systems!
createstar.......- create a system at your current point
prunestars.......- remove some random stars
killstar.........- murder a specific star
        ''','light_magenta')
    if func == 'genstars':
        gen(int(input(c('STARS TO GENERATE','light_magenta')+'\n'+'> ')))
        cprint('GENSTAR PROC DONE','light_magenta')
    if func == 'prunestars':
        for x in range(int(input(c('NUMBER OF STARS TO PRUNE','light_red')+'\n'+'> '))):
            try:
                s = random.choice(sectors)#; print(s.number,len(s.stars)-1)
                y = s.stars[len(s.stars)-1]#; print(y)
                s.stars.remove(y)#; print('removed ', y)
            except:
                pass
    if func == 'where':
        whereami(True)
    if func == 'galmap':
        print(roughmap())
    if func == 'go':
        go()
    if func == 'stations':
        mysector = sectors[whereami()]
    if func == 'secread':
        readsec(secfinder(),True)
    if func == 'find':
        cprint('INPUT STRING < OR = 32 CHARS')
        indexFind(input('> '))

# todo: make dist less stupid!!!!!!!!!!!!!!!!!!!!
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

    if func == 'exec':
        exec(input('> '))

