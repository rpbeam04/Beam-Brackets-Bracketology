import data
import bracket
import operator

tl = data.stl

bubble = bracket.LFB
bubble+=bracket.LFI
bubble+=data.FFO
bubble+=data.NFO
with open('Bubble.txt','w') as f:
  for team in tl:
    if team['name'] in bubble:
      bubble[bubble.index(team['name'])] = (team['name']+' ('+str(int(team['Overall']['W']))+'-'+str(int(team['Overall']['L']))+')\n')
  for bub in bubble:
    f.write(f'{bub}')

with open('movers.txt','w') as f:
  movers = bracket.diffs
  movers.sort(key=operator.itemgetter('s_diff'),reverse=True)
  for team in movers:
    f.write(f"{team['name']} {team['s_diff']}\n")
  for team in bracket.outs:
    f.write(team+'\n')
  
with open('canva.txt','w') as f:
  ff = []
  for i in range(0,7,2):
    for j in range(1,5):
      ff.append(bracket.rows[j][i])
  for fo in ff:
    f.write(f'{fo.strip()}\n')
  f.write('******\n')
  r = []
  for i in range(0,4):
    r.append([])
  for ct, row in enumerate(bracket.rows):
    if ct > 6 and ct < 30:
      r[0].append(row[0])
      r[1].append(row[6])
      r[2].append(row[2])
      r[3].append(row[4])
  for l in r:
    for t in l:
      f.write(f'{t.strip()}\n')
    f.write('******\n')

file = open('Ncaa.txt','r')
data = file.read()
field = data.split('\n')
i = 0
for team in field:
  field[i]=team.upper()
  i+=1
file.close()

file = open('foes.txt','r')
data = file.read()
foes = data.split('\n')
i = 0
for team in foes:
  foes[i]=team.upper()
  i+=1
file.close()

def game(team,opp):
  pace = (team['Adv Stats']['Pace'] + opp['Adv Stats']['Pace']) / 2
  hsc = ((team['Ratings']['ORtg'] + opp['Ratings']['DRtg']) / 2 *
                   (pace / 100))
  asc = ((opp['Ratings']['ORtg'] + team['Ratings']['DRtg']) / 2 *
                   (pace / 100))
  global hos
  hos = hsc
  global aws
  aws = asc

file = open('Scores.txt','w')

k = 0
while(k<len(field)):
  j=0
  for tea in tl:
    if(tea['name'].upper() == field[k]):
      team = tl[j]
      print('yes')
    j+=1
  j=0
  for tea in tl:
    if(tea['name'].upper() == foes[k]):
      opp = tl[j]
      print('and')
    j+=1
  game(team,opp)
  line = team['name']+','+str(round(hos,1))+','+opp['name']+','+str(round(aws,1))
  file.write(line+'\n')
  k+=1

file.close()