import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
class CollegeRater:
    
    def __init__(self, college_name, college_id):
        self.name = college_name
        self.college_id = college_id
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    def CreateURL(self):
        full_name = self.GetFullName(self.college_id)
        URL = f"https://nces.ed.gov/collegenavigator/?q={full_name}&s=all&id={self.college_id}"
        return URL

    def Fetch(self, URL):
        print(URL)
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        data = []
        tables = soup.findAll('table')
        acceptance_rate = 0
        SAT25r=0
        SAT75r=0
        SAT25m=0
        SAT75m=0
        ACT25r=0
        ACT75r=0
        ACT25m=0
        ACT75m=0
        for table in tables:
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols] 
                data.append([ele for ele in cols if ele])# Get rid of empty values
                index = 0
                for ele in cols:
                    if ("Percent admitted" in ele and len(ele)<20):
                        acceptance_rate =cols[index+1]
                    if ("SAT Evidence-Based Reading and Writing" in ele):
                        SAT25r = cols[index+1]
                        SAT75r = cols[index+2]  
                    if ("SAT Math" in ele):
                        SAT25m = cols[index+1]
                        SAT75m = cols[index+2]  
                    if ("ACT English" in ele):
                        ACT25r = cols[index+1]
                        ACT75r = cols[index+2]
                    if ("ACT Math" in ele):
                        ACT25m = cols[index+1]
                        ACT75m = cols[index+2]
                    index +=1
        print(SAT25r)
        print(SAT25m)
        if (str(SAT25r).isdigit() and str(SAT25m).isdigit()):
            SAT25 = SAT25r + SAT25m
            SAT75 = SAT75r + SAT75m    
            ACT25 = ACT25r + ACT25m
            ACT75 = ACT75r + ACT75m  
        else:
            SAT25 = 1300
            SAT75 = 1400
            ACT25 = 16
            ACT75 = 24   

        rank = self.GetRank(self.GetFullName(self.GetID()))

        return [acceptance_rate, SAT25, SAT75, ACT25, ACT75, rank]

    def Rate(self, stats): #stats is returned list from Fetch
        # temporary calculation: score = SAT25 + SAT75 + ACT25 + ACT75 - rank / acceptance_rate
        print(stats[0])
        stats[0] = str(stats[0]).strip('%')
        stats = [int(x) for x in stats]
        if (stats[0] != 0):
            score = (stats[1] + stats[2] + stats[3] + stats[4]  - stats[5]) / stats[0]
        else:
            stats[0] = 50
            score = (stats[1] + stats[2] + stats[3] + stats[4]  - stats[5]) / stats[0]
        return score


    def GetRank(self, uni_full_name):
        URL = f"https://www.forbes.com/colleges/{uni_full_name}/?sh=691441da2b7d"
        print(URL)
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        rank = soup.find("div", class_="profile-heading--desktop")
        try:
            index = str(rank).index('#')
            c_rank = str(rank)[index+1:index+3]
            return c_rank
        except:
            index = random.random() * 1000
            return index


    def GetFullName(self, IPED_ID):
        df = pd.read_csv("csv\\CLEANED_UP_COLLEGES.csv", index_col=False)
        val =  (df[(df['UNITID']==IPED_ID)])["INSTNM"]
        result = ''.join([i for i in val if not i.isdigit()])
        result = result.replace(" ", "+")
        result = result.lower()
        return result

    def GetID(self):
        return self.college_id

    def Run(self):
        CR = CollegeRater(self.name, self.college_id)
        stats = CR.Fetch(CR.CreateURL())
        C_score = CR.Rate(stats)
        return C_score
