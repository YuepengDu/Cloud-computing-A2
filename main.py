from flask import Flask,render_template,url_for,flash,redirect,request,session
from forms import LoginForm, RegistrationForm, SearchForm
import boto3
from boto3.dynamodb.conditions import Key
import helpers
from flask_paginate import get_page_args, Pagination
import databaseLoad

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    if session.get('user') is None:
        return redirect(url_for('login'))
    form = SearchForm()
    results = helpers.get_all_music()
    emp= ""
    if form.validate_on_submit():
        if form.title.data is emp and form.year.data is emp:
            results = helpers.query_music_by_artist(form.artist.data)
        elif form.artist.data is emp and form.year.data is emp:
            results = helpers.query_music_by_title(form.title.data)
        elif form.year.data is emp:
            results = helpers.query_music_by_title_artist(form.title.data,form.artist.data)
        elif form.artist.data is emp and form.title.data is emp:
            results = helpers.query_music_by_year(form.year.data)
        elif form.artist.data is emp:
            results = helpers.query_music_by_year_title(form.title.data,form.year.data)
        elif form.title.data is emp:  
            results = helpers.query_music_by_year_artist(form.artist.data, form.year.data)
        elif form.title.data and form.year.data and form.artist.data: 
            results = helpers.query_music_by_all_three(form.title.data,form.artist.data,form.year.data) 
        if len(results) == 0:
            flash('No result is retrieved. Please query again!','danger')
        return render_template('home.html', form=form, results = results, Pagination=None)
    page, per_page, offset = get_page_args(page_parameter = 'page', per_page_parameter = 'per_page')
    final = helpers.music_index(offset = offset, per_page = per_page)
    amount = len(list(results))
    paging = Pagination(page = page, per_page = per_page, total = amount,css_frameword= "bootstrap4")
    return render_template('home.html', form=form, results = final, page = page, per_page = per_page, Pagination = paging)

@app.route("/subscription/<string:title>", methods=['GET', 'POST'])
def unsubscribe(title):
    helpers.delete_sub(session['user'], title)
    subscriptions = helpers.query_all_sub(session['user'])
    flash('Unsubscribe successful', 'success')
    return render_template('subscription.html',subscriptions = subscriptions )
    
@app.route("/subscription", methods=['GET', 'POST'])
def display_sub():
    subscriptions = helpers.query_all_sub(session['user'])
    return render_template('subscription.html', subscriptions = subscriptions )

@app.route("/home/<string:title>+<string:artist>+<string:year>", methods=['GET', 'POST'])
def subscribe(title,artist,year):
    results = helpers.get_all_music()
    if helpers.check_sub(session['user'], title):
        flash('You have subscribed this music', 'danger') 
    else:
        databaseLoad.put_sub(session['user'], title, artist , year)
        flash('Subscribe successful', 'success')
    return redirect(url_for('home'))

@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('user') is not None:
        flash('You have already logged in', 'danger')
    form = LoginForm(next=request.args.get('next'))
    if form.validate_on_submit():
        results = helpers.scan_user(form.email.data,form.password.data)
        if results:
            session['user'] = form.email.data
            for result in results:
                session['username'] = result['user_name']
            flash('You have been loggin in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsucceessful. Please check username or password', 'danger')       
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        result = helpers.scan_for_duplicate(form.email.data)
        name_check = helpers.scan_duplicate_username(form.user_name.data)
        if result:
            flash('The email already exists, please try again!', 'danger')
        elif name_check:
            flash('The user_name already exists, please try again!', 'danger')
        else:
            helpers.create_user(form.email.data,form.user_name.data,form.password.data)
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    session.pop('user',None)
    session.pop('username',None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
