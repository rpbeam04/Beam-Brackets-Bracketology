import csv
import operator
import math

print('run')

FFO = []
NFO = []

rat = open('Metrics/Ratings.csv')
sta = open('Metrics/Stats.csv')
oSta = open('Metrics/OppStats.csv')
ad = open('Metrics/Adv.csv')
oAd = open('Metrics/OppAdv.csv')
rate = csv.reader(rat)
stat = csv.reader(sta)
oStat = csv.reader(oSta)
adv = csv.reader(ad)
oAdv = csv.reader(oAd)
CSVs = [rate, stat, oStat, adv, oAdv]

# Init
headr = []
headr = next(rate)
rrows = []
for row in rate:
    rrows.append(row)

tl = []
k = 1
while k < len(rrows):
  team = {'name': rrows[k][1]}
  conf = rrows[k][2]
  if (conf == 'MAC (East)' or conf == 'MAC (West)'):
    conf = 'MAC'
  team['conf'] = conf
  tl.append(team)
  k += 1

cl = []
for team in tl:
  team['Overall'] = {}
  team['Stats'] = {}
  team['Opp Stats'] = {}
  team['Adv Stats'] = {}
  team['Opp Adv Stats'] = {}
  team['Ratings'] = {}
  if team['conf'] not in cl:
    cl.append(team['conf'])
cl.sort()
tl.sort(key=operator.itemgetter('name'))

# Stats
head = []
head = next(stat)
rows = []
for row in stat:
  rows.append(row)

ls = len(head)
test = 0
for r in rows:
  for team in tl:
    if (team['name'] == r[1]):
      ri = 0
      for stati in r:
        if (head[ri] == 'Overall'):
          stati = float(stati)
          team['Overall'][rows[0][ri]] = stati
        if (head[ri] == 'Conf.'):
          try:
            stati = float(stati)
          except:
            stati = 0
          team['Overall']['Conf ' + rows[0][ri]] = stati
        if (head[ri] == 'Points'):
          stati = float(stati)
          if (rows[0][ri] == 'Tm.'):
            label = 'PPG'
          if (rows[0][ri] == 'Opp.'):
            label = 'OPPG'
          team['Overall'][label] = stati
        if (head[ri] == 'Totals'):
          stati = float(stati)
          team['Stats'][rows[0][ri]] = stati
        ri += 1

format = 1
print('x1')

# Opp Stats
head = []
head = next(oStat)
rows = []
for row in oStat:
    rows.append(row)

ls = len(head)
test = 0
for r in rows:
    for team in tl:
        if (team['name'] == r[1]):
            ri = 0
            for stati in r:
                if (head[ri] == 'Opponent'):
                    stati = float(stati)
                    team['Opp Stats'][rows[0][ri]] = stati
                ri += 1

format = 1

# Adv Stats
head = []
head = next(adv)
rows = []
for row in adv:
    rows.append(row)

ls = len(head)
test = 0
for r in rows:
    for team in tl:
        if (team['name'] == r[1]):
            ri = 0
            for stati in r:
                if (head[ri] == 'School Advanced'):
                    stati = float(stati)
                    team['Adv Stats'][rows[0][ri]] = stati
                ri += 1

format = 1

# Opp Adv Stats
head = []
head = next(oAdv)
rows = []
for row in oAdv:
    rows.append(row)

ls = len(head)
test = 0
for r in rows:
    for team in tl:
        if (team['name'] == r[1]):
            ri = 0
            for stati in r:
                if (head[ri] == 'Opponent Advanced'):
                    stati = float(stati)
                    team['Opp Adv Stats'][rows[0][ri]] = stati
                ri += 1

format = 1

# Ratings
headr
rrows

print('x2')

ls = len(headr)
test = 0
for r in rrows:
    for team in tl:
        if (team['name'] == r[1]):
            ri = 0
            for stati in r:
                if (rrows[0][ri] == 'AP Rank'):
                    if(stati!=''):
                        team['Overall']['AP'] = int(stati)
                    if(stati==''):
                        team['Overall']['AP'] = 'NR'
                if (rrows[0][ri] == 'MOV'):
                    stati = float(stati)
                    team['Overall'][rrows[0][ri]] = stati
                if (headr[ri] == 'SRS'):
                    stati = float(stati)
                    team['Ratings'][rrows[0][ri]] = stati
                if (headr[ri] == 'Adjusted'):
                    stati = float(stati)
                    team['Ratings'][rrows[0][ri]] = stati
                ri += 1

format = 1

for team in tl:
  if team['conf'] == 'Ind':
    print(team['name'])
    tl.remove(team)

# BRVI Calcs
for team in tl:
    team['BRVI'] = {}
    team['BRVI']['Wins'] = 0
    team['BRVI']['Losses'] = 0
    team['BRVI']['Ties'] = 0
    team['BRVI']['Rank'] = 0
    team['BRVI']['Games'] = 0

for team in tl:
    for opp in tl:
        if (team['name'] != opp['name']):
            pace = (team['Adv Stats']['Pace'] + opp['Adv Stats']['Pace']) / 2
            hts = ((team['Ratings']['ORtg'] + opp['Ratings']['DRtg']) / 2 *
                   (pace / 100)) + 2
            aos = ((opp['Ratings']['ORtg'] + team['Ratings']['DRtg']) / 2 *
                   (pace / 100)) - 2
            ats = ((team['Ratings']['ORtg'] + opp['Ratings']['DRtg']) / 2 *
                   (pace / 100)) - 2
            hos = ((opp['Ratings']['ORtg'] + team['Ratings']['DRtg']) / 2 *
                   (pace / 100)) + 2
            if (hts > aos):
                team['BRVI']['Wins'] += 1
            if (hts < aos):
                team['BRVI']['Losses'] += 1
            if (hts == aos):
                team['BRVI']['Ties'] += 1
            if (ats > hos):
                team['BRVI']['Wins'] += 1
            if (ats < hos):
                team['BRVI']['Losses'] += 1
            if (ats == hos):
                team['BRVI']['Ties'] += 1
            team['BRVI']['Games'] += 2

for team in tl:
    team['BRVI%'] = (team['BRVI']['Wins'] +
                     0.5 * team['BRVI']['Ties']) / team['BRVI']['Games']

tl.sort(key=operator.itemgetter('BRVI%'), reverse=True)

i = 1
for team in tl:
    team['BRVIRk'] = i
    i += 1

print('b')
  
# BRVI+ Calcs
def BRVIplusGame(home, away):
    pace = (home['Adv Stats']['Pace'] + away['Adv Stats']['Pace']) / 2
    hstats = {}
    astats = {}
    hstats['SOS'] = 1 + (home['Overall']['SOS']) / pace
    astats['SOS'] = 1 + (away['Overall']['SOS']) / pace
    ftPfl = (home['Stats']['FTA'] / home['Opp Stats']['PF'] +
             away['Stats']['FTA'] / away['Opp Stats']['PF']) / 2
    hstats['2%'] = (home['Stats']['FG'] - home['Stats']['3P']) / (
        home['Stats']['FGA'] - home['Stats']['3PA'])
    hstats['3%'] = home['Stats']['3P%']
    astats['2%'] = (away['Stats']['FG'] - away['Stats']['3P']) / (
        away['Stats']['FGA'] - away['Stats']['3PA'])
    astats['3%'] = away['Stats']['3P%']
    hstats['OReb'] = home['Adv Stats']['ORB%'] / 100
    astats['OReb'] = away['Adv Stats']['ORB%'] / 100
    hstats['TO%'] = home['Adv Stats']['TOV%'] / 100
    astats['TO%'] = away['Adv Stats']['TOV%'] / 100
    hstats['3PA%'] = home['Adv Stats']['3PAr']
    hstats['2PA%'] = 1 - home['Adv Stats']['3PAr']
    astats['3PA%'] = away['Adv Stats']['3PAr']
    astats['2PA%'] = 1 - away['Adv Stats']['3PAr']
    # Weighting
    hstats['D2%'] = (home['Opp Stats']['FG'] - home['Opp Stats']['3P']) / (
        home['Opp Stats']['FGA'] - home['Opp Stats']['3PA'])
    hstats['3%'] = (hstats['3%'] + away['Opp Stats']['3P%']) / 2
    astats['D2%'] = (away['Opp Stats']['FG'] - away['Opp Stats']['3P']) / (
        away['Opp Stats']['FGA'] - away['Opp Stats']['3PA'])
    hstats['2%'] = (hstats['2%'] + astats['D2%']) / 2
    astats['2%'] = (astats['2%'] + hstats['D2%']) / 2
    astats['3%'] = (astats['3%'] + home['Opp Stats']['3P%']) / 2
    hstats['OReb'] = (hstats['OReb'] + away['Opp Adv Stats']['ORB%'] / 100) / 2
    astats['OReb'] = (astats['OReb'] + home['Opp Adv Stats']['ORB%'] / 100) / 2
    hstats['TO%'] = (hstats['TO%'] + away['Opp Adv Stats']['TOV%'] / 100) / 2
    astats['TO%'] = (astats['TO%'] + home['Opp Adv Stats']['TOV%'] / 100) / 2
    hstats['Rec Fouls'] = (home['Opp Stats']['PF'] + away['Stats']['PF']) / 2
    astats['Rec Fouls'] = (away['Opp Stats']['PF'] + home['Stats']['PF']) / 2

    hstats['2%'] *= hstats['SOS']
    hstats['3%'] *= hstats['SOS']
    astats['2%'] *= astats['SOS']
    astats['3%'] *= astats['SOS']
    hstats['OReb'] *= hstats['SOS']
    astats['OReb'] *= astats['SOS']
    hstats['TO%'] *= (1 / hstats['SOS'])
    astats['TO%'] *= (1 / astats['SOS'])

    hstats['SPOSS'] = (1 - (hstats['TO%'] +
                            (hstats['Rec Fouls'] / pace))) * pace
    astats['SPOSS'] = (1 - (astats['TO%'] +
                            (astats['Rec Fouls'] / pace))) * pace
    hstats['ScO'] = hstats['SPOSS'] * (
        1 + (hstats['OReb'] * (1 -
                               (hstats['TO%'] + hstats['Rec Fouls'] / pace))))
    astats['ScO'] = astats['SPOSS'] * (
        1 + (astats['OReb'] * (1 -
                               (astats['TO%'] + astats['Rec Fouls'] / pace))))
    hstats['2PA'] = hstats['2PA%'] * hstats['ScO']
    hstats['3PA'] = hstats['2PA%'] * hstats['ScO']
    astats['2PA'] = astats['2PA%'] * astats['ScO']
    astats['3PA'] = astats['2PA%'] * astats['ScO']
    hscore = 2 * (hstats['2%'] * hstats['2PA']) + 3 * (
        hstats['3%'] * hstats['3PA']) + ftPfl * hstats['Rec Fouls']
    ascore = 2 * (astats['2%'] * astats['2PA']) + 3 * (
        astats['3%'] * astats['3PA']) + ftPfl * astats['Rec Fouls']
    global hsco
    hsco = hscore
    global asco
    asco = ascore
    global soso
    soso = hstats['SOS']

print('+1')

for team in tl:
    team['BRVI+'] = {}
    team['BRVI+']['Wins'] = 0
    team['BRVI+']['Losses'] = 0
    team['BRVI+']['Ties'] = 0
    team['BRVI+']['Rank'] = 0
    team['BRVI+']['Games'] = 0

for team in tl:
    for opp in tl:
        if (team['name'] != opp['name']):
            BRVIplusGame(team, opp)
            if (hsco > asco):
                team['BRVI+']['Wins'] += 1
            if (hsco < asco):
                team['BRVI+']['Losses'] += 1
            if (hsco == asco):
                team['BRVI+']['Ties'] += 1
            team['BRVI+']['Games'] += 1

for team in tl:
    team['BRVI+%'] = (team['BRVI+']['Wins'] +
                      0.5 * team['BRVI+']['Ties']) / team['BRVI+']['Games']

tl.sort(key=operator.itemgetter('BRVI+%'), reverse=True)
i = 1
for team in tl:
    team['BRVI+Rk'] = i
    team['Beam'] = 1 * team['BRVI%'] + 0 * team['BRVI+%']
    i += 1

for team in tl:
  team['Overall']['APC'] = 0
  if(team['Overall']['AP']!='NR'):
    team['Overall']['APC'] = (26 - team['Overall']['AP'])/120

for team in tl:
  team['MMI'] = team['Overall']['W-L%'] + (team['Overall']['SOS'] /
                                             45) + team['Beam'] + (
                                                 team['Ratings']['NRtg'] / 90) + team['Overall']['APC']

print('calc done')

tl.sort(key=operator.itemgetter('MMI'), reverse=True)

all = open('Full_Ranks.txt','w')
r=1
for team in tl:
  all.write(str(r)+'. '+team['name']+' ('+team['conf']+', '+str(int(team['Overall']['W']))+'-'+str(int(team['Overall']['L']))+')\n')
  r+=1
all.close()

field = []
tlf = tl
inelig = ['Bellarmine', 'Lindenwood', 'Merrimack', 'Queens', 'St. Thomas', 'Southern Indiana', 'Stonehill', 'Tarleton State', 'Texas A&M-Commerce', 'UC San Diego', 'Utah Tech']

k=0
stl = []
while(k<len(tl)):
  stl.append(tl[k])
  k+=1

confch = ['Vermont','Houston','Duke','Kennesaw State','Virginia Commonwealth','Marquette','Montana State','UNC Asheville','Purdue','Texas','UC Santa Barbara','College of Charleston','Florida Atlantic','Northern Kentucky','Princeton','Iona','Kent State','Howard','Drake','San Diego State','Fairleigh Dickinson','Southeast Missouri State','Arizona','Colgate','Alabama','Furman','Texas A&M-Corpus Christi','Texas Southern','Oral Roberts','Louisiana','Gonzaga','Grand Canyon']

print('cochamp')
print(len(confch))

for team in tlf:
  for champ in confch:
    if(team['name']==champ):
      c = 0
      for conf in cl:
        if(team['conf']==conf):
          cl[c]=team['name']
        c+=1

for team in tlf:
  team['DQ'] = False
  team['CC'] = False
  for dq in inelig:
    if(team['name'] == dq):
      team['DQ'] = True
  for conf in cl:
    if(team['conf']==conf or team['name']==conf):
      team['CC'] = True
      tt = {}
      tt['name'] = team['name']
      tt['conf'] = team['conf']
      tt['AQ'] = 1
      tt['MMI'] = team['MMI']
      tt['Pace'] = team['Adv Stats']['Pace']
      tt['OEff'] = team['Ratings']['ORtg']
      tt['DEff'] = team['Ratings']['DRtg']
      tt['Rec'] = str(int(team['Overall']['W']))+'-'+str(int(team['Overall']['L']))
      field.append(tt)
      if(team['conf']==conf):
        cl.remove(team['conf'])
      elif(team['name']==conf):
        cl.remove(team['name'])

print('adq')

j=0
while(j<len(tlf)):
  if(tlf[j]['CC']==True):
    tlf.remove(tlf[j])
  else:
    j+=1

print(len(tl))
print(len(tlf))
print(len(stl))

ff16s = []
ff16s.append(field[len(field)-1])
ff16s.append(field[len(field)-2])
field.remove(field[len(field)-1])
field.remove(field[len(field)-1])

for team in ff16s:
  team['name']=team['name'].upper()

k = 0
while (len(field) < 64):
  if(tlf[k]['DQ'] != True):
    tt = {}
    tt['name'] = tlf[k]['name']
    tt['conf'] = tlf[k]['conf']
    tt['AQ'] = 0
    tt['MMI'] = tlf[k]['MMI']
    tt['Pace'] = tlf[k]['Adv Stats']['Pace']
    tt['OEff'] = tlf[k]['Ratings']['ORtg']
    tt['DEff'] = tlf[k]['Ratings']['DRtg']
    tt['Rec'] = str(int(tlf[k]['Overall']['W']))+'-'+str(int(tlf[k]['Overall']['L']))
    field.append(tt)
  k+=1

print(len(field))

ffAL=[]
while(len(ffAL)<2):
  if(tlf[k]['DQ']!=True):
    tt = {}
    tt['name'] = tlf[k]['name']
    tt['conf'] = tlf[k]['conf']
    tt['AQ'] = 0
    tt['MMI'] = tlf[k]['MMI']
    tt['Pace'] = tlf[k]['Adv Stats']['Pace']
    tt['OEff'] = tlf[k]['Ratings']['ORtg']
    tt['DEff'] = tlf[k]['Ratings']['DRtg']
    tt['Rec'] = str(int(tlf[k]['Overall']['W']))+'-'+str(int(tlf[k]['Overall']['L']))
    ffAL.append(tt)
  k+=1

while(len(FFO)<4):
  if(tlf[k]['DQ']!=True):
    FFO.append(tlf[k]['name'])
  k+=1
while(len(NFO)<4):
  if(tlf[k]['DQ']!=True):
    NFO.append(tlf[k]['name'])
  k+=1

field.sort(key=operator.itemgetter('MMI'), reverse=True)

print('d')

# Write for Checking
file = open('Write.txt', 'w')
for team in stl:
  file.write(str(team) + '\n')
file.close()