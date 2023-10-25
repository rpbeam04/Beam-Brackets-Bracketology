#import bracket
import csv

field = bracket.field
tl = bracket.tl

def game(team,opp):
  pace = (team['Adv Stats']['Pace'] + opp['Adv Stats']['Pace']) / 2
  hsc = ((team['Ratings']['ORtg'] + opp['Ratings']['DRtg']) / 2 *
                   (pace / 100))
  asc = ((opp['Ratings']['ORtg'] + team['Ratings']['DRtg']) / 2 *
                   (pace / 100))
  return hsc
  return asc

bracket = open('odds.csv')
bracke = csv.reader(bracket)
rows = []
for row in bracke:
    rows.append(row)
bracket.close()

r=1
n=1
for row in rows:
  k=0
  for cell in row:
    for team in field:
      if(cell.lower()==team['name'].lower()):
        for opp in field:
          if(rows[r][k].lower()==opp['name'].lower()):
            game(team,opp)
              
            n+=1
    k+=1
  r+=1