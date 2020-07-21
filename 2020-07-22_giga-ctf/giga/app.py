from flask import Flask, flash, request, render_template, session, redirect, url_for, g
import os, sqlite3, time

app = Flask('giga')

DATABASE = 'db.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row 
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# aggressively rotate secret so that cookies from the disclosed pcap can't be reused
app.secret_key = os.urandom(50)

@app.route("/init")
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    flash("DB CREATED")
    return redirect(url_for('main'))

@app.route("/")
def main():
    if session:
        print('x')
    else:
        session['lockout_time'] = time.time();
    return render_template('main.html')

@app.route("/securityQuestion", methods=['GET','POST'])
def security():
    if session:
        if request.method == "POST":
            z = query_db('select email from user where id = ? and answer = ?',(session['id'], request.form['answer']))
            if z:
                session['email'] = z[0]['email']
                cur = get_db()
                cur.execute("UPDATE user set ip = ? where id = ?", (request.remote_addr, session['id']))
                cur.commit()
                return redirect(url_for('download'))
            else:
                return 'invalid'
        else:
            question = query_db('select question from user where id = ?',[session['id']])
            quest = question[0]['question']
            flash(quest)
            return render_template('questions.html')
    else:
        flash("Sorry, you must be logged in to view your downloads")
        return redirect(url_for('main'))

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        if 'lockout_time' in session:
                if time.time() - session['lockout_time'] < 0:
                    if session['email'] == request.form['email']:
                        return "This username is banned for " + str(session['lockout_time'] - time.time()) + 'seconds'
        
        email = request.form['email']
        password = request.form['pass']
        if email and password:
            user = query_db('select ip, id from user where email = ? and password = ?', (email, password))
            if user:
                if request.remote_addr == user[0]['ip']:
                    session['email'] = request.values['email']
                    session['id'] = user[0]['id']
                    return redirect(url_for('download'))
                else:
                    session['id'] = user[0]['id']
                    return redirect(url_for('security'))
            else:
                session['email'] = request.form['email']
                session['lockout_time'] = time.time() + 600
                flash("bad username or pass")
                return render_template("login.html")
        else:
            flash("bad username or pass")
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/contactus", methods=['GET','POST'])
def contact():
    if request.method == "POST":
        return "contact post"
    else:
        return "contact"

@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out")
    return redirect(url_for('main'))

@app.route("/download")
def download():
    if 'email' in session:
        links = query_db("SELECT id, name from downl where user_id = ?",[session['id']])
        return render_template('download.html', links = links)
    else:
        flash("Sorry, you must be logged in to view your downloads")
        return redirect(url_for('main'))

@app.route("/download/<x>")
def down(x):
    z = int(x)
    if 'email' in session:
        path = query_db('SELECT file_path from downl where id = ? and user_id = ?',(x, session['id']))
        if path:
            f = open(path[0]['file_path'])
            return f.read()
        else:
            flash("File not available")
            return redirect(url_for('download'))
    else:
        flash("Sorry, you must be logged in to view your download")
        return redirect(url_for('main'))
