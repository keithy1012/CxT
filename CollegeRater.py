import requests
from bs4 import BeautifulSoup
class CollegeRater:
    
    def __init__(self, college_name, college_id):
        self.name = college_name
        self.college_id = college_id
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}


    def CreateURL(self):
        URL = f"https://nces.ed.gov/collegenavigator/?q={self.name}&s=all&id={self.college_id}"
        print(URL)
        return URL

    def Fetch(self, URL):
        r = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        admissions_table = soup.find('div', attrs={'id': "admsns"})
        return 
    def Rate(self):
        score = 0
        return score

