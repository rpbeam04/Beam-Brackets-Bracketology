import data
import csv
import random
import operator

print('b')

LFB = []
LFI = []
FFO = data.FFO
NFO = data.NFO
FFAL = data.ffAL
FF16 = data.ff16s

bracket = open('bracket.csv')
bracke = csv.reader(bracket)
rows = []
for row in bracke:
    rows.append(row)
bracket.close()

field = data.field
tl = data.tl

seed = 1
for team in field:
  team['seed'] = seed
  if((field.index(team)+1)%4==0):
    seed+=1

for team in field:
  team['r'] = 'U'

print('y1')

regs = ['E', 'M', 'S', 'W']
ps = 1
a = 1
for team in field:
    if (len(regs) == 0):
        regs = ['E', 'M', 'S', 'W']
    if(team['seed']%2==1):
      r = 0
    if(team['seed']%2==0 and team['seed']!=12):
      r = len(regs)-1
    if(team['seed']==12):
      r = len(regs)-1
    team['r'] = regs[r]
    o=0
    while(o<len(field)):
      if(field[o]['r']==team['r'] and field[o]['seed']+team['seed']==17):
        while(field[o]['conf']==team['conf'] and o<0):
          r = random.randint(0, len(regs) - 1)
          team['r'] = regs[r]
          print(team['conf'])
          o=0
      o+=1
    team['key'] = regs[r] + str(team['seed'])
    regs.remove(regs[r])

print('y2')

for team in FF16:
  field.append(team)

d=3
for team in field:
  if('r' not in team.keys()):
    team['r']=field[len(field)-d]['r']
    team['key']=field[len(field)-d]['key']
    team['seed']=field[len(field)-d]['seed']
    d+=1

field.reverse()
fk = len(field)
for team in field:
  if(team['AQ']==0):
    break
  fk-=1
field.reverse()

m=0
for team in FFAL:
  field.insert(fk+m,team)
  m+=1

d=1
for team in field:
  if('r' not in team.keys()):
    if(field[fk-d]['AQ']==1):
      d+=1
    team['r']=field[fk-d]['r']
    team['key']=field[fk-d]['key']
    team['seed']=field[fk-d]['seed']
    d+=1

FFt = []
for team in field:
  for opp in field:
    if(team['key']==opp['key'] and team['name']!=opp['name'] and team['seed']!=16):
      FFt.append(team)



k = 0
for team in field:
  for ff in FFt:
    if(team['name']==ff['name']):
      field[k] = ff
  k+=1

field.reverse()
ctr = 1
for team in field:
  if(team['AQ']==0 and ctr>4 and ctr<=8):
    LFB.append(team['name'])
    ctr+=1
  if(team['AQ']==0 and ctr<=4):
    LFI.append(team['name'])
    ctr+=1
LFI.reverse()
LFB.reverse()
field.reverse()

rgs = ['EAST','MIDWEST','SOUTH','WEST']
rks = ['E','M','S','W']

ffhead = []
ffgames = []
ffkeys = []
for team in field:
  for opp in field:
    if(team['key']==opp['key'] and team['name']!=opp['name']):
      reg = team['key'][0]
      i = 0
      for r in rks:
        if(reg == r):
          hdr = rgs[i]
        i+=1
      seed = team['seed']
      if(hdr+' '+str(seed) not in ffhead):
        ffhead.append(hdr+' '+str(seed))
        game = [team['name'],opp['name']]
        if(seed == 16):
          g=0
          for gt in game:
            game[g]=gt.upper()
            team['name'] = team['name'].upper()
            opp['name'] = opp['name'].upper()
            g+=1
        ffgames.append(game)
        ffkeys.append(team['key'])

east = []
south = []
midw = []
west = []
for team in field:
  if(team['r']=='E'):
    east.append(team)
  if(team['r']=='M'):
    midw.append(team)
  if(team['r']=='W'):
    west.append(team)
  if(team['r']=='S'):
    south.append(team)

l = 1
seedsort = []
while(l<17):
  seeds = []
  seedsort.append(seeds)
  l+=1
for team in field:
  seedsort[team['seed']-1].append(team)

prev = open('prev.csv','r')
prev = csv.reader(prev)
prows = []
for row in prev:
  prows.append(row)

prev_seeds = []
for row in prows:
  if(prows.index(row)>0):
    prev_seeds.append({'name':row[1],'prev':row[0]})

names = []
outs = []
for team in field:
  names.append(team['name'].lower())
for team in prev_seeds:
  if team['name'].lower() not in names:
    outs.append(f"{team['name']} -")
    

for team in field:
  team['prev']=0
  for p in prev_seeds:
    if(team['name'].lower()==p['name'].lower()):
      team['prev']=int(p['prev'])

for team in field:
  if(team['prev']==0):
    team['s_diff']='+'
  else:
    team['s_diff']=team['seed']-team['prev']

for team in field:
  if(team['s_diff']!='+'):
    if(type(team['s_diff'])==int):
      if(team['s_diff']>0):
        team['s_diff']='\u2207'+str(team['s_diff'])
    if(team['s_diff']==0):
      team['s_diff']=''
    if(type(team['s_diff'])==int):
      if(team['s_diff']<0):
        sdif = team['s_diff']*(-1)
        team['s_diff']='\u0394'+str(sdif)

diffs = []
for team in field:
  if team['s_diff'] != '':
    diffs.append(team)

ffodds = []
for ele in ffgames:
  g = []
  for elem in ele:
    g.append(elem)
  ffodds.append(g)

for game in ffgames:
  f=0
  for team in game:
    for ps in field:
      if(team==ps['name']):
        game[f] = team+' '+ps['s_diff']
    f+=1

#CSV writing prep
for team in field:
  if(team['AQ']==1):
    team['name']=team['name'].upper()
f = 0
r = 0
for ff in rows[1]:
    if (ff != ''):
        rows[1][r] = ffhead[f]
        rows[2][r] = ffgames[f][0]
        rows[3][r] = ffgames[f][1]
        f += 1
    r += 1

for row in rows:
    c = 0
    if (rows.index(row) > 3):
        for cell in row:
            for team in field:
                if (team['key'] == cell and team['key'] not in ffkeys):
                    row[c] = team['name']+' '+team['s_diff']
                if(team ['key'] == cell  and team['key'] in ffkeys):
                    for key in ffkeys:
                      if(key == team['key']):
                        j = ffkeys.index(key)
                    row[c] = 'First Four'
            c += 1

print('y')

l = 0
for row in rows:
    if (rows.index(row) >= 32):
        c = 0
        for cell in row:
            if (cell == 'LB'):
                row[c] = LFB[l]
            if (cell == 'LI'):
                row[c] = LFI[l]
            if (cell == 'FO'):
                row[c] = FFO[l]
            if (cell == 'NO'):
                row[c] = NFO[l]
                l += 1
            c += 1

brack = open('bracketoutput.csv', 'w', newline='')
output = csv.writer(brack)
for row in rows:
    output.writerow(row)
brack.close()

file = open('field.txt','w')
for team in field:
  file.write(str(team['seed'])+' '+team['name']+' ('+team['Rec']+')'+'\n')
file.close()

file = open('csvfield.csv','w')
file.write('seed,name'+'\n')
for team in field:
  file.write(str(team['seed'])+','+team['name']+'\n')
file.close()

#experimental predictor bracket
brackt = open('bracket.csv')
brack = csv.reader(brackt)
orows = []
for orow in brack:
    orows.append(orow)

f = 0
r = 0
for ff in orows[1]:
    if (ff != ''):
        orows[1][r] = ffhead[f]
        orows[2][r] = ffodds[f][0]
        orows[3][r] = ffodds[f][1]
        f += 1
    r += 1

for orow in orows:
    c = 0
    if (orows.index(orow) > 3):
        for cell in orow:
            for team in field:
                if (team['key'] == cell and team['key'] not in ffkeys):
                    orow[c] = team['name']
                if(team ['key'] == cell  and team['key'] in ffkeys):
                    for key in ffkeys:
                      if(key == team['key']):
                        j = ffkeys.index(key)
                    orow[c] = ffhead[j]
            c += 1

print('y')

bids = open('bids.txt','w')
clist = []
for team in field:
  if(team['conf'] not in clist):
    clist.append(team['conf'])

bid = []
for c in clist:
  bid.append({'name':c,'count':0})

for conf in bid:
  for team in field:
    if(team['conf']==conf['name']):
      conf['count']+=1

bid.sort(key=operator.itemgetter('count'),reverse=True)
for conf in bid:
  bids.write(conf['name']+' ('+str(conf['count'])+')\n')
bids.close()

odds = open('bracketlines.csv','w',newline='')
lines = csv.writer(odds)
for orow in orows:
  if(orows.index(orow)<30):
    lines.writerow(orow)
odds.close()

def rounder(num):
  if(num<0):
    num = -num
    av = True
  rn = round(num,0)
  r = num - rn
  if(r<.334):
    rounded = rn
    rounded = int(rounded)
  if(r>=.334 and r <.667):
    rounded = rn +0.5
  if(r>=.667):
    rounded = rn+1
    rounded = int(rounded)
  if(av==True):
    rounded = -rounded
  return rounded