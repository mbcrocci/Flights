from flask import Flask, render_template, request, flash, redirect, url_for
from flask.ext.pymongo import PyMongo
from wtforms import Form, validators, TextField


app = Flask(__name__)
mongo = PyMongo(app)

app.secret_key = 'maurizio'

class Flight:

    def __init__(self, number, company, desteny, hour, minutes):
        self.number = number
        self.company = company
        self.desteny = desteny
        self.hour = hour
        self.minutes = minutes

    def __repr__(self):
        return '<Flight %s %s %s %s %s %s' % (self.number, self.company,
                                              self.desteny, self.hour,
                                              self.minutes)


class New_flight_form(Form):
    number = TextField('Number', [validators.Length(min=3, max=9)])
    company = TextField('Company', [validators.Length(max=20)])
    desteny = TextField('Desteny', [validators.Length(max=20)])
    hour = TextField('Hour', [validators.Length(max=3)])
    minutes = TextField('Minutes', [validators.Length(max=3)])


@app.route("/")
def home_page():
    flights = mongo.db.flights
    return render_template('index.html', flights=flights)


@app.route("/new_flight", methods=["GET", "POST"])
def new_flight():
    form = New_flight_form(request.form)
    if request.method == "POST" and form.validate():
        flight = Flight(form.number.data, form.company.data,
                        form.desteny.data, form.hour.data,
                        form.minutes.data)

        mongo.db.flights.insert(flight.__dict__)
        flash('New flight added')
        return redirect(url_for('home_page'))

    return render_template('new_flight.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
