from model import app, db
# from covidcases import app
# from covidcases.data.models import db
from sqlalchemy import exc, func
from flask import Blueprint, render_template, flash
from forms.entry_forms import CreateEntryForm, CoronaSearchForm
from model import User, db
from flask import current_app, redirect, request, url_for
from flask_paginate import Pagination, get_page_args

import requests


# main = Blueprint('main', __name__, template_folder='templates')


# @app.route('/')
# def index():
#     entries = [entry for entry in User.query.all()]
#     current_app.logger.info("Displaying all entries.")

#     return render_template("entries.htm", entries=entries)

def get_entries(offset=0, per_page=10):
    return User.query.order_by(User.id.desc()).offset(offset).limit(per_page)


def get_results(qry, offset=0, per_page=10):
    return qry.order_by(User.id.desc()).offset(offset).limit(per_page)


@app.route('/', methods=['GET', 'POST'])
def create_entry():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = User.query.count()
    pagination_entries = get_entries(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

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

    if request.method == 'POST':
        if form.validate():
            print("IT WORKS")
            info = User(form.city.data.lower(), form.state.data.lower(), form.age.data,
                        str(form.symptoms.data), form.ip_address.data.lower(), form.tested.data, form.in_contact.data)
            db.session.add(info)
            db.session.commit()
            return redirect('/')
        else:
            flash('Failed to post. Try to submit info again.')
    return render_template("create_entry.htm",
                           form=form,
                           entries=pagination_entries,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,)


@app.route('/results', methods=['GET', 'POST'])
def do_search():
    search = CoronaSearchForm()

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination = Pagination(page=page, per_page=per_page, total=0,
                            css_framework='bootstrap4')

    if request.method == 'POST':
        results = []
        search_string = search.data['search'].lower()

        # print(search_string)
        # print(search.data['select'])
        if search.data['search'] != '':
            if search.data['select'] == 'City':
                qry = User.query.filter_by(city=search.data['search'].lower())
                # results = qry.all()
                total = qry.count()
                pagination_results = get_results(
                    qry, offset=offset, per_page=per_page)
                pagination = Pagination(page=page, per_page=per_page, total=total,
                                        css_framework='bootstrap4')
            elif search.data['select'] == 'State':
                qry = User.query.filter_by(state=search.data['search'].lower())
                total = qry.count()
                pagination_results = get_results(
                    qry, offset=offset, per_page=per_page)
                pagination = Pagination(page=page, per_page=per_page, total=total,
                                        css_framework='bootstrap4')
            elif search.data['select'] == 'Age':
                qry = User.query.filter_by(age=search.data['search'].lower())
                total = qry.count()
                pagination_results = get_results(
                    qry, offset=offset, per_page=per_page)
                pagination = Pagination(page=page, per_page=per_page, total=total,
                                        css_framework='bootstrap4')
        # display results
        return render_template('results.htm',
                               results=pagination_results,
                               form=search,
                               page=page,
                               per_page=per_page,
                               pagination=pagination)
    return render_template("results.htm",
                           form=search, results=[], page=page,
                           per_page=per_page,
                           pagination=pagination)

    # form = CreateEntryForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     info = User(form.location.data, form.age.data, form.symptoms.data,
    #                 form.ip_address.data, form.travel_history.data)
    #     db.session.add(info)
    #     db.session.commit()
    #     flash('Entry successfully created.')

    #     return redirect(url_for('index'))

    # return render_template('create_entry.htm', form=form)


# @app.route('/static/resources.htm')
# def get_resources():
#     return
if __name__ == "__main__":
    app.run(port=80, host='0.0.0.0')
