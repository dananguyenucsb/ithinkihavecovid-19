from sqlalchemy import exc
from flask import Blueprint, render_template, flash
from forms.entry_forms import CreateEntryForm
from model import User, db
from flask import current_app, redirect, request, url_for


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    entries = [entry for entry in User.query.all()]
    current_app.logger.info("Displaying all entries.")

    return render_template("entries.htm", entries=entries)


@main.route('/create', methods=['GET', 'POST'])
def create_entry():
    form = CreateEntryForm()
    if request.method == 'POST' and form.validate():
        info = User(form.location.data, form.age.data, form.symptoms.data,
                    form.ip_address.data, form.travel_history.data)
        db.session.add(info)
        db.session.commit()
        flash('Entry successfully created.')

        return redirect(url_for('main.index'))

    return render_template('create_entry.htm', form=form)
