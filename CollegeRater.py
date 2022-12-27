import requests
from bs4 import BeautifulSoup
class CollegeRater:
    
    def __init__(self, college_name, college_id):
        self.name = college_name
        self.college_id = college_id
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}


    def CreateURL(self):
        URL = f"https://nces.ed.gov/collegenavigator/?q={self.name}&s=all&id={self.college_id}"
        #print(URL)
        return URL

    def Fetch(self, URL):
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        admissions_table = soup.find('div', attrs={'id': "admsns"})
        #print(admissions_table.prettify())
        SATR_index = admissions_table.prettify().index("SAT Evidence-Based Reading and Writing")
        SATR_index = admissions_table.prettify().index("SAT Math")
        ACTC_index = admissions_table.prettify().index("ACT Composite")
        ACTR_index = admissions_table.prettify().index("ACT English")
        ACTM_index = admissions_table.prettify().index("ACT Math")
        #print(SATR_index)
        #print(admissions_table.prettify()[SATR_index: SATR_index+30])

        data = []
        tables = soup.findAll('table')
        for table in tables:
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty values
        print("Admission %:" , data[78])
        print("SAT ENGLISH:" , data[90])
        print("SAT MATH:" , data[91])
        print("ACT ENGLISH:" , data[93])
        print("ACT MATH:" , data[94])
        return 

    def Rate(self):
        score = 0
        return score


CR = CollegeRater("Princeton", 186131)
print(CR.CreateURL())
print(CR.Fetch(CR.CreateURL()))