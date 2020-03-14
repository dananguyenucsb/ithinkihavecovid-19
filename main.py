from model import app, db
# from covidcases import app
# from covidcases.data.models import db
from sqlalchemy import exc
from flask import Blueprint, render_template, flash
from forms.entry_forms import CreateEntryForm
from model import User, db
from flask import current_app, redirect, request, url_for
import requests


# main = Blueprint('main', __name__, template_folder='templates')


@app.route('/')
def index():
    entries = [entry for entry in User.query.all()]
    current_app.logger.info("Displaying all entries.")

    return render_template("entries.htm", entries=entries)


@app.route('/create', methods=['GET', 'POST'])
def create_entry():
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

    if request.method == 'POST':

        print("HELLOS YOU DID A POST!!!")
        info = User(form.location.data, form.age.data, form.symptoms.data,
                    form.ip_address.data, form.travel_history.data)
        db.session.add(info)
        db.session.commit()
        return redirect('/')

    return render_template("create_entry.htm",
                           form=form)
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
