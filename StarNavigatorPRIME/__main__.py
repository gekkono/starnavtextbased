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
starTarget = 20000000
dim3 = False
galaxydim = 40000000  # in LIGHT DAYS. the milky way is about 36500000 LD across but we "round up"
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

# begin builtin functions
# these are intended to be used by the base game and shouldn't be modified or moved
def dist2D(coords1, coords2):  # it looks scary but don't worry it's just a plug and chug
    return math.sqrt((coords2[0] - coords1[0]) ** 2 + (coords2[1] - coords1[1]) ** 2)

def seccoordget(coords):
    try:  # find which sector a set of coords is in
        for s in sectors:
            if s.head[0] >= coords[0] > s.corner[0] and s.head[1] >= coords[1] > s.corner[1]:
                return s
    except:
        err(' ! INVALID SECTOR !')
        return None

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

# end builtin functions ------------------------------------------------------------------------------
# begin worldgen functions
# these shouldn't be touched at all, even by me

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

# end worldgen functions ------------------------------------------------------------------------------
# begin generation
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
        time.sleep(5)
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
    time.sleep(2)
    managed_sectorchunks = manager.list([[],[],[],[],[],[],[],[],[],[],[],[]])
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
        time.sleep(5)
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

# whereami(True)
# print(roughmap())

# end game generation ------------------------------------------------------------------------------
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
# begin a long list of stupid if-then programs
    if func == 'exec':
        try:
            exec(input('> '))
        except: err('ERROR IN EXECUTION')