from model import app, db
# from covidcases import app
# from covidcases.data.models import db
from sqlalchemy import exc
from flask import Blueprint, render_template, flash
from forms.entry_forms import CreateEntryForm, CoronaSearchForm
from model import User, db
from flask import current_app, redirect, request, url_for
import requests


# main = Blueprint('main', __name__, template_folder='templates')


# @app.route('/')
# def index():
#     entries = [entry for entry in User.query.all()]
#     current_app.logger.info("Displaying all entries.")

#     return render_template("entries.htm", entries=entries)


@app.route('/', methods=['GET', 'POST'])
def create_entry():
    entries = [entry for entry in User.query.all()]
    form = CreateEntryForm()

    print("CREATE ENTRY REQ METHOD: " + request.method)
    # getting ip adress
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        # if behind a proxy
        ip_address = request.environ['HTTP_X_FORWARDED_FOR']

    try:
        resp = requests.get(
            'http://ip-api.com/json/{}'.format(ip_address)).json()
        if resp["status"] == "success":
            form.ip_address.data = resp["regionName"] + \
                ", "+resp["city"]+", "+resp["country"]
        else:
            form.ip_address.data = "CANT VERIFY"
    except Exception as e:
        form.ip_address.data = "CANT VERIFY"
    print("Going in")
    if request.method == 'POST' and form.validate_on_submit():
        print("IT WORKS")
        info = User(form.city.data.lower(), form.state.data.lower(), form.age.data,
                    str(form.symptoms.data), form.ip_address.data.lower(), form.tested.data)
        db.session.add(info)
        db.session.commit()
        return redirect('/')
    else:
        flash('Failed validation')
    return render_template("create_entry.htm",
                           form=form, entries=entries)


@app.route('/results', methods=['GET', 'POST'])
def do_search():
    search = CoronaSearchForm()
    if request.method == 'POST':
        results = []
        search_string = search.data['search'].lower()

        print(search_string)
        print(search.data['select'])
        if search.data['search'] != '':
            if search.data['select'] == 'City':
                qry = User.query.filter_by(city=search.data['search'])
                results = qry.all()
            elif search.data['select'] == 'State':
                qry = User.query.filter_by(state=search.data['search'])
                results = qry.all()
            elif search.data['select'] == 'Age':
                qry = User.query.filter_by(age=search.data['search'])
                results = qry.all()
        # display results
        return render_template('results.htm', results=results, form=search)
    return render_template("results.htm",
                           form=search, results=[])

    # form = CreateEntryForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     info = User(form.location.data, form.age.data, form.symptoms.data,
    #                 form.ip_address.data, form.travel_history.data)
    #     db.session.add(info)
    #     db.session.commit()
    #     flash('Entry successfully created.')

    #     return redirect(url_for('index'))

    # return render_template('create_entry.htm', form=form)


if __name__ == "__main__":
    app.run(port=8080)
