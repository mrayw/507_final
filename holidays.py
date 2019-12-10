import requests, json
from datetime import datetime,timedelta
from bs4 import BeautifulSoup

class Holiday:
    def __init__(self, list=["National Food Day","January 01"]):
        self.holiday = list[0]
        self.dateString = list[1]

        m = {"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10", "November":"11", "December":"12"}
        self.month = m[list[1].split()[0]]
        if len(list[1].split()[1]) == 2:
            self.day = list[1].split()[1]
        else:
            self.day = "0"+list[1].split()[1]
        self.dateTime = self.month + "-" + self.day

        today = datetime.now().date()
        next_year = [[1,today]]
        day_of_year = 1
        while day_of_year < 366:
            next_date = today + timedelta(days=day_of_year)
            next_year.append([day_of_year+1,next_date])
            day_of_year += 1
        for obj in next_year:
            if self.dateTime == obj[1].strftime("%m-%d"):
                self.dayOfYear = obj[0]

        food_words = []
        for word in list[0].split():
            if word == "Day":
                pass
            elif word == "National":
                pass
            else:
                food_words.append(word)
        self.searchTerm = " ".join(food_words)

    def __str__(self):
        return self.holiday + " is on " + self.dateString

CACHE_FNAME = 'holidays_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def holidays_unique_key(url):
  return url

def holidays_request_using_cache(url):
    unique_ident = holidays_unique_key(url)

    if unique_ident in CACHE_DICTION:
        # print("Fetching cached Holiday data...")
        return CACHE_DICTION[unique_ident]
    else:
        # print("Request new Holiday data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

def Holiday_scrape():
    baseurl = "https://foodimentary.com/"
    page_text = holidays_request_using_cache(baseurl)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    menu_soup = page_soup.find(class_='menu')
    link_soup = menu_soup('a')
    strings = []
    for link in link_soup:
        month_text = holidays_request_using_cache(link['href'])
        month_soup = BeautifulSoup(month_text, 'html.parser')
        month = month_soup.find('h1').text.split()[0]
        obj = month_soup.find(string="Daily Holidays").parent.parent.next_siblings
        for thing in obj:
            try:
                if thing.text == "":
                    pass
                elif thing.text[0].lower() not in "abcdefghijklmnopqrstuvwxyz":
                    pass
                elif thing.text.split()[0] == "Buy":
                    break
                else:
                    try:
                        for str in thing.text.split("\n"):
                            clean_str = ""
                            #remove unnecessary char from strings
                            for char in str:
                                if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.' ":
                                    clean_str += char
                            #Add spaces to strings without spaces
                            if "Continue" in clean_str.split():
                                pass
                            elif " " not in clean_str:
                                spaces_str = ""
                                for char2 in clean_str:
                                    if char2 in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                                        new_char = (" "+char2)
                                        spaces_str += new_char
                                    else:
                                        spaces_str += char2
                                if spaces_str[-1] == " ":
                                    strings.append(spaces_str[1:-1])
                                else:
                                    strings.append(spaces_str[1:])
                            #remove front space from string
                            elif (clean_str[0] and clean_str[-1]) == " ":
                                strings.append(clean_str[0:-1])
                            elif clean_str[0] == ' ':
                                strings.append(clean_str[1:])
                            else:
                                strings.append(clean_str)
                    except:
                        strings.append(clean_str.text)
            except:
                pass


    active_holiday = ""
    holiday_objects = []

    for str in strings:
        if str[-1] in "0123456789":
            active_holiday = str
        else:
            holiday_objects.append(Holiday([str,active_holiday]))

    return holiday_objects

# test = Holiday_scrape()
# for obj in test:
#     print(obj.dateTime, obj.dayOfYear, obj.dateString)
