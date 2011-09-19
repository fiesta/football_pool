import db
import fiesta
import settings
import user
import util

import sha, time

import flask
from flask import request, make_response, session, redirect
import decorator

app = flask.Flask('Football Pool Webserver')
app.secret_key = '# set the secret key.  keep this really secret:'

def do_login(requested_user, web_email, web_password):
    if not requested_user:
        return False

    if requested_user.password_hash != sha.sha(web_password).hexdigest():
        return False

    session['email'] = web_email
    return True


def _logged_in():
    if 'email' not in session:
        return None

    email = session['email']
    return user.User.from_email(email)


@decorator.decorator
def login_required(func, *args, **kwargs):
    """Require a logged in user."""
    user_obj = _logged_in()
    if not user_obj:
        return redirect("/login")

    flask.g.user_obj = user_obj
    return func(*args, **kwargs)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.ico')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        requested_user = user.User.from_email(email)

        if do_login(requested_user, email, password):
            return redirect('/homepage')
        else:
            return flask.render_template('login.html', error_msg='Could not login as %s' % (email))

    return flask.render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    return redirect('/login')


@app.route('/homepage')
@login_required
def homepage():
    user_obj = flask.g.user_obj
    return flask.render_template('homepage.html', username=user_obj.name, week=util.get_week())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return flask.render_template('register.html')

    email = request.form['email']
    password = request.form['password']
    confirmation = request.form['confirmation_password']
    league_password = request.form['league_password']

    if password != confirmation:
        return flask.render_template('register.html', error_msg='Your password did not match the confirmation')

    if league_password != settings.league_password:
        return flask.render_template('register.html', error_msg='Bad league password')

    session['email'] = email
    db.new_user(email, sha.sha(password).hexdigest(), email)
    if db.num_users() == 1:
        return redirect("https://fiesta.cc/authorize?state=create_group&response_type=code&client_id=%s&_register_email=%s" % (settings.client_id, email))
    else:
        fiesta.add_member(email)

    return redirect('/homepage')


@app.route('/fiesta_user_token')
def fiesta_user_token():
    if 'error' in request.args and request.args['error'] == 'access_denied':
        return flask.render_template('register.html', error_msg='access denied to create a list :(')

    grant_token = request.args['code']
    try:
        access_token = fiesta.get_user_token(grant_token)
    except Exception as inst:
        app.logger.debug(str(inst))
        return redirect('/register.html', error_msg='some weird problem :(')

    email = session['email']
    action = request.args['state']
    if action == 'create_group':
        response = fiesta.create_group(email, access_token)

    return redirect('/homepage')


if __name__ == '__main__':
    app.run(debug=True)
