from flask import render_template, flash, redirect, jsonify, request
from app import app, db, models
from .forms import LoginForm, SearchForm, ResultsForm
import json, html
from sqlalchemy import distinct

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/Results', methods=['GET', 'POST'])
def Results():
    page = 1
    form = ResultsForm()
    offense = "test"
    if form.validate_on_submit():
        offense = form.category.data
        page = form.page.data

#    Defendants = models.Defendant.query.limit(50).all()
#    Defendants = models.Charge.query.filter(models.Charge.Offense == offense).join(models.Defendant, models.Defendant.defendant_id == 1)
    Defendants = models.Defendant.query.join(models.Case_Info,(models.Case_Info.defendant_id == models.Defendant.defendant_id)).join(models.Charge, (models.Charge.Case_Number == models.Case_Info.Case_Number)).filter(models.Charge.Offense == offense).paginate(page, 15, False)
 #   Defendants = models.Charge.query.filter(models.Charge.Offense == offense, models.Charge.Case.Defendant.Sex == 'M')

    defendantList = json.dumps(
        [
        {
            'defendant_id' : d.defendant_id,
            'Name_Full': html.escape(d.Name_Full),
            'Sex' : html.escape(d.Sex),
            'Race' : html.escape(d.Race)
        }
        for d in Defendants.items])
    return render_template('results.html',
                            defendants=defendantList,
                            Defendants = Defendants,
                            category=offense,
                            page=page,
                            form = form
                            )

@app.route('/Search', methods=['GET', 'POST'])
def Search():
    form = ResultsForm()
    Offenses = db.session.query(models.Charge.Offense).distinct()
    offenseList = ""
    for o in Offenses:
        oStr = html.escape(str(o).replace('(','').replace(')','').replace("'", "").replace(",","%2"))
        k = oStr.rfind("%2") #we want the last comma to be a comma to separate values
        new_string = oStr[:k] + "," + oStr[k+2:]
        offenseList = offenseList + new_string
    return render_template('search.html',
                            offenses=offenseList,
                            form = form
                            )

@app.route('/Person/<ID>')
def Person(ID):
    Charges = models.Charge.query.join(models.Case_Info, (models.Case_Info.Case_Number == models.Charge.Case_Number)).join(models.Defendant, (models.Defendant.defendant_id == models.Case_Info.defendant_id)).filter(models.Defendant.defendant_id == ID)
    Defendant = models.Defendant.query.filter(models.Defendant.defendant_id == ID)

    if Defendant.count() == 1:
        Defendant = Defendant[0]

    chargeList = json.dumps(
    [
    {
        'Offense' : c.Offense,
        'Offense_Date' : c.Offense_Date,
        'Disposition' : c.Disposition,
        'Disposition_Date' : c.Disposition_Date
    }
    for c in Charges]
    )

    return render_template('defendant.html',
                            charges = chargeList,
                            defendant = Defendant
                            )

@app.errorhandler(404)
def not_found(error):

    if "person" in request.url.lower():
        new_url = request.url.replace("person", "Person")
        return redirect(new_url)
    if "results" in request.url.lower():
        new_url = request.url.replace("results","Results")
        return redirect(new_url)

    return render_template('error.html'), 404