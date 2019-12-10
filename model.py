import sqlite3, sys
from datetime import datetime,timedelta
from holidays import Holiday_scrape
from bon_appetit import bonAppetit_scrape

DBNAME = "HolidayReviews.db"

def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Calendar';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Holidays';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Reviews';
    '''
    cur.execute(statement)

    conn.commit()

    statement = '''
        CREATE TABLE "Calendar" (
            "Id"	INTEGER PRIMARY KEY NOT NULL UNIQUE,
            "Date"	TEXT NOT NULL UNIQUE
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE "Holidays" (
        	"Id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "Date"	INTEGER NOT NULL,
            "DateString"	TEXT NOT NULL,
            "Holiday"	TEXT NOT NULL,
        	"Food"	TEXT NOT NULL,
            FOREIGN KEY(Date) REFERENCES Calendar(Id)
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE "Reviews" (
            "Id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        	"Recipe"	TEXT,
            "Review"    TEXT,
            "Rating"    INTEGER,
            "Link"    TEXT,
        	"Holiday"	INTEGER NOT NULL,
            FOREIGN KEY(Holiday) REFERENCES Holidays(Id)
        );
    '''
    cur.execute(statement)

    conn.commit()
    conn.close()

if len(sys.argv) > 1 and sys.argv[1] == '--init--':
    # print('Deleting db and starting over from scratch.')
    init_db()
else:
    # print('Leaving the DB alone.')
    pass

def insert_calendar():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    today = datetime.now().date()
    next_year = [[1,today.strftime("%m-%d")]]
    day_of_year = 1
    while day_of_year < 366:
        next_date = today + timedelta(days=day_of_year)
        next_year.append([day_of_year+1,next_date.strftime("%m-%d")])
        day_of_year += 1

    for date in next_year:
        insertion = (date[0],date[1])
        statement = 'INSERT INTO "Calendar" '
        statement += 'VALUES (?, ?)' #Id (day of year strating with todays date), Date String (mm-dd)
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def insert_holidays():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    holiday_objects = Holiday_scrape()
    for holiday in holiday_objects:
        insertion = (None, holiday.dayOfYear, holiday.dateString, holiday.holiday, holiday.searchTerm)
        statement = 'INSERT INTO "Holidays" '
        statement += 'VALUES (?, ?, ?, ?, ?)' #Id, Date, DateString, Holiday, Food
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def insert_reviews(holidayId,term,stars):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    review_objects = bonAppetit_scrape(holidayId,term,stars)
    # review_objects = bonAppetit_scrape("215","cheese","1")

    for review in review_objects:
        insertion = (None, review.recipe, review.review, review.stars, review.link, review.holiday)
        statement = 'INSERT INTO "Reviews" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?)' #Id, Recipe, Review, Rating, Link, Holiday
        cur.execute(statement, insertion)
        # print(insertion)
    conn.commit()
    conn.close()

def select_holiday(day):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    select_statement = 'SELECT h.Id, h.Date, h.Food, h.DateString, h.Holiday'
    join_statement = '''
    FROM Holidays as h '''
    where = '''
    WHERE h.Date =='''+str(day)
    order = '''
    ORDER BY h.Date'''
    limit = '''
    LIMIT 1'''

    statement = select_statement + join_statement + where + order + limit
    # print(statement)
    cur.execute(statement)
    return cur.fetchall()

def select_reviews(day,rating):

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    select_statement = 'SELECT h.Holiday, h.DateString, r.Review, r.Rating, r.Link, r.Recipe'
    join_statement = '''
    FROM Reviews as r
        JOIN Holidays as h
            ON r.Holiday = h.Id'''
    where = '''
    WHERE h.Date = '''+str(day)
    and_rating = ' AND r.Rating = '+str(rating)
    order = '''
    ORDER BY random()'''
    limit = '''
    LIMIT 1'''

    statement = select_statement + join_statement + where + and_rating + order + limit
    # print(statement)
    cur.execute(statement)
    return cur.fetchall()

def init_all():
    init_db()
    insert_calendar()
    insert_holidays()

    for day in [353,354,355,356,357,358,359,360,361,362,364,365,1,2,3,4,5,6,7,8,9,10,11,12,13]:
        load_holiday = select_holiday(day)
        # print(load_holiday)
        load_stars_5 = insert_reviews(str(load_holiday[0][0]),load_holiday[0][2],"5")
        load_stars_1 = insert_reviews(str(load_holiday[0][0]),load_holiday[0][2],"1")
    pass
