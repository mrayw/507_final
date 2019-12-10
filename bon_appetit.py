import requests, json
from bs4 import BeautifulSoup

class Review:
    def __init__(self,holidayId,recipe="Test Name",review="Test Review",link="Test Link",term="Test Keyword",stars="1"):
        self.recipe = recipe
        self.review = review
        self.link = "https://www.bonappetit.com"+link
        self.food = term
        self.stars = stars
        self.holiday = holidayId

    def __str__(self):
        return self.review

CACHE_FNAME = 'bonAppetit_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def bonAppetit_unique_key(url):
  return url

def bonAppetit_request_using_cache(url):
    unique_ident = bonAppetit_unique_key(url)

    if unique_ident in CACHE_DICTION:
        # print("Fetching cached Bon Appetit data...")
        return CACHE_DICTION[unique_ident]
    else:
        # print("Request new Bon Appetit data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

def bonAppetit_scrape(holidayId,term,stars="1"):
    baseurl = "https://www.bonappetit.com/"
    search_url = baseurl + "search/"+term+"?content=recipe"
    page_text = bonAppetit_request_using_cache(search_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    results_soup = page_soup.find(class_='results-group')
    cards_soup = results_soup.find_all(class_='recipe-content-card')
    recipe_links = []
    for recipe in cards_soup:
        tag = recipe.find(class_='tag')
        if tag.text == 'recipes':
            try:
                link = recipe.find('a')['href']
                recipe_links.append(link)
            except:
                pass
    review_objects = []
    for link in recipe_links:
        recipe_text = bonAppetit_request_using_cache(baseurl+link)
        recipe_soup = BeautifulSoup(recipe_text, 'html.parser')
        review_soup = recipe_soup.find(class_='row--reviews')
        if review_soup != None:
            one_stars = review_soup.find(class_=stars+'-stars')
            if one_stars != None:
                recipe_name = recipe_soup.find('h1').text
                next_div = one_stars.findNext('div').text
                review_objects.append(Review(holidayId,recipe_name,next_div,link,term,stars))
    return review_objects

# test = bonAppetit_scrape("1","Brownie")
# for obj in test:
#     print(obj.review)
#     print("")
