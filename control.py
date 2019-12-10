from flask import Flask, render_template, request, redirect
import sqlite3
# from datetime import datetime
from model import *

app = Flask(__name__)
DBNAME = "HolidayReviews.db"

@app.route('/reviews/<day>/<rating>',methods=['GET','POST'])
def reviews(day="1",rating="1"):

    choose_holiday = select_holiday(day)
    if len(select_reviews(day,rating)) > 0:
        review = select_reviews(day,rating)
    else:
        stars_5 = insert_reviews(str(choose_holiday[0][0]),choose_holiday[0][2],"5")
        stars_1 = insert_reviews(str(choose_holiday[0][0]),choose_holiday[0][2],"1")
        review = select_reviews(day,rating)

    if request.method == 'POST':
        if request.form['nav'] == "Next":
            base = "/reviews/"
            if day == "365":
                day_str = "1"
            else:
                day_str = str(int(day) + 1)
            rating = "/"+rating
            new_url = base+day_str+rating
            return redirect(new_url)

        elif request.form['nav'] == "Prior":
            base = "/reviews/"
            if day == "1":
                day_str = "365"
            else:
                day_str = str(int(day) - 1)
            rating = "/"+rating
            new_url = base+day_str+rating
            return redirect(new_url)

        elif request.form['nav'] == "5Star":
            base = "/reviews/"
            day_str = day
            rating = "/5"
            new_url = base+day_str+rating
            return redirect(new_url)

        elif request.form['nav'] == "1Star":
            base = "/reviews/"
            day_str = day
            rating = "/1"
            new_url = base+day_str+rating
            return redirect(new_url)
    else:
        pass

    if len(review) > 0:
        return render_template("index.html",holiday=review[0][0],datestring=review[0][1],review=review[0][2],rating=rating,href=review[0][4],recipe=review[0][5],error=False)
    else:
        return render_template("index.html",holiday=choose_holiday[0][4],datestring=choose_holiday[0][3],rating=rating,error=True)

if __name__ == '__main__':
    init_all()
    app.run(debug=True)
