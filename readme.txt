Michael White
mrayw@umich.edu

SI507 Fall 2019
Instructor: Pedja Klasnja

Title: National 'Stupid National Food Holiday' day

Challenge Score: 16

______________________________________
What does it do (in general):
Presents users with the nearest upcoming national food holiday, a related recipe, and a 1-star (or 5-star) review for the recipe. Users can toggle between 1 or 5 star reviews. They can navigate forward ('Next Holiday') or backward ('Prior Holiday').

______________________________________
How To Run

Run 'control.py' to initiate this program.

Once the DB is populated, launch '127.0.0.1:5000/reviews/1/1' in your browser.
The structure of the url is: '/reviews/<day>/<rating>'. So, '/reviews/1/1' loads Today (1) and 1 star reviews (1). Tomorrow's 5-star reviews would be '/reviews/2/5'.

______________________________________
Python Modules

requests
json
datetime
bs4
flask
sqlite3
sys

______________________________________
Structure/Process.

1. 'holiday.py' uses BeautifulSoup to crawl and collect stupid food holidays (all 400+). This information is stored in a cache: 'holiday_cache.json'
2. 'HolidayReviews.db' is created with these tables: 'Calendar', 'Holidays', 'Reviews'
3. The Calendar table is inserted with 366 rows, one for each day starting Today.
4. The Holidays table is inserted with 400+ rows, one for each holiday.
5. Holidays are used to search for reviews +/- 12 days from Today. 'bon_appetit.py' uses BeautifulSoup to crawl and collect.
**Steps 1-5 are all coordinated through 'model.py', and wrapped into function: 'init_all()'.
6. A flask front-end with 1 template. By default the template presents a 1-star review for the nearest holiday to today. Users can navigate forward and backward to the next holidays, and can choose between 5 or 1 star reviews.
7. When users go beyond the +/- 12 days from Today, the program scrapes more reviews from the Bon Appetit website.

______________________________________
Data Storage

HolidayReviews.db
bonAppetit_cache.json
holidays_cache.json

______________________________________
Data Sources:

The following two websites were accessed using Beautiful Soup. It is necessary to Import bs4 module in python. No authentication or key is necessary to access this.

1. https://foodimentary.com/ (8 challenge points)
- I crawled this website to create a database table ('Holidays') that contains the following columns:
  - "Id" unique Id for each holiday
  - "Date" (1-366) which is the 'Day of the Year' starting with todays date. It is a Foreign Key linked to 'Calendar.Id' This helps with navigation and sorting, and means the database needs to be refreshed daily.
  - "DateString" is the string of the date ie: "December 10".
  - "Holiday" string of the holiday name ie: National Pizza Day.
  - "Food" string, the holiday with 'national' and 'day' stripped, used as a search term in Bon Appetit website.
- I used another table ('Calendar') to help ingest the Holidays. Many holidays occur on single dates.

**** Class definition: class Holiday was used to ingest data from the holiday website before insertion into the DB.

2. https://www.bonappetit.com/ (8 challenge points)
- I crawled this website using the "Food" column related to the holiday. The "Food" was input in the following url: https://www.bonappetit.com/search/FOOD?content=recipe
- I parsed the 20 results, filtering out sponsored posts.
- I gathered the links for recipes and scraped the recipe pages for reviews that are either 1-star or 5-stars.
- These reviews are organized in a database table ('Reviews') that contains the following columns:
  - "Id" unique Id for each review
  - "Recipe" string name of recipe
  - "Review" string user review
  - "Rating" int. either 1 or 5.
  - "Link" url for the recipe page
  - "Holiday" int. Foreign Key linked to Holiday.Id

**** Class definition: class Review was used to ingest data from Bon Appetit before insertion into the DB.
