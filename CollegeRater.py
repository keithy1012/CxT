import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
class CollegeRater:
    
    def __init__(self, college_name, college_id):
        self.name = college_name
        self.college_id = college_id
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        self.SAT25 = 0
        self.SAT75 = 0
        self.ACT25 = 0
        self.ACT75=0
        self.acceptance_rate=  0.0
        # [name, id, SAT25, SAT75, ACT25, ACT75, acceptance]


    def CreateURL(self):
        URL = f"https://nces.ed.gov/collegenavigator/?q={self.name}&s=all&id={self.college_id}"
        #print(URL)
        return URL

    def Fetch(self, URL):
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        dashboard= soup.find('div', class_="collegedash")
        print(dashboard.prettify)
        #ID_index = str(dashboard).index("IPEDS ID:")
        #IPED_ID = str(dashboard)[ID_index+10: ID_index+16]
        #print("IPEDS ID: ", IPED_ID)
        print("Address: ", dashboard.find("a", target_="_blank"))

        data = []
        tables = soup.findAll('table')
        for table in tables:
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty values
        
        print("Phone #:" , data[3])
        print("Website:" , data[4])

        print("Admission %:" , data[78])
        self.acceptance_rate = data[78][1];
        print("SAT ENGLISH:" , data[90])
        print("SAT MATH:" , data[91])
        self.SAT25 = data[90][1] + data[91][1]
        self.SAT75 = data[90][2] + data[91][2]        
        print("ACT ENGLISH:" , data[93])
        print("ACT MATH:" , data[94])
        self.ACT25 = data[93][1] + data[94][1]
        self.ACT75 = data[93][2] + data[94][2]   
        return 

    def GetRank(self, uni_full_name):
        URL = f"https://www.forbes.com/colleges/{uni_full_name}/?sh=691441da2b7d"
        print(URL)
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        rank = soup.find("div", class_="profile-heading--desktop")
        try:
            index = str(rank).index('#')
            c_rank = str(rank)[index+1:index+3]
            print("College Rank: ", c_rank)
            return c_rank
        except:
            index = random.random() * 1000
            return index


    def GetFullName(self, IPED_ID):
        df = pd.read_csv("CLEANED_UP_COLLEGES.csv", index_col=False)
        val =  (df[(df['UNITID']==IPED_ID)])["INSTNM"]
        result = ''.join([i for i in val if not i.isdigit()])
        print(result)
        result = result.replace(" ", "-")
        result = result.lower()
        return result

    def GetID(self):
        return self.college_id

    def Rate(self):
        score = 0
        return score

    def Run(self):
        CR = CollegeRater(self.name, self.college_id)
        CR.CreateURL()
        rank = CR.GetRank(CR.GetFullName(CR.GetID()))
       # CR.Fetch(CR.CreateURL())
        return rank #for now, we will use rank as the college's quantitative score

