from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import subprocess
import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def listen_put(a, b):
    inp = b"0 "
    for i in range(361):
        if a[i] == '0':
            inp += b"-1 "
        if a[i] == 'X':
            inp += b"1 "
        if a[i] == ' ':
            inp += b"0 "
    inp += str.encode(b)
    args = ["/home/kirill/CLionProjects/XO4/cmake-build-debug/XO4"]
    args = ["venv/XO4"]
    result = subprocess.run(args, stdout=subprocess.PIPE, input=inp, shell=True, stderr=subprocess.STDOUT)
    s = result.stdout.decode('utf-8')
    s = s.split()
    ss = ""
    for i in range(361):
        if s[i] == '-1':
            ss += "0"
        if s[i] == '1':
            ss += "X"
        if s[i] == '0':
            ss += " "
    arr = [ss, s[361]]
    return arr


def listen_next_move(a):
    inp = b"1 "
    for i in range(361):
        if a[i] == '0':
            inp += b"-1 "
        if a[i] == 'X':
            inp += b"1 "
        if a[i] == ' ':
            inp += b"0 "
    args = ["/home/kirill/CLionProjects/XO4/cmake-build-debug/XO4"]
    result = subprocess.run(args, stdout=subprocess.PIPE, input=inp, shell=True, stderr=subprocess.STDOUT)
    s = result.stdout.decode('utf-8')
    return listen_put(a, s)


class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(361), nullable=False, default="")
    status = db.Column(db.Integer, default=2)

    def __repr__(self):
        return '<Field %r>' % self.id


@app.route('/index')
def game():
    return render_template("index.html")


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/multiplayer2/<int:id>', methods=['POST', 'GET'])
def multiplayer2(id):
    try:
        number = 2
        data = Field.query.get(id)
        temp = dt.datetime.now()
        strn = data.data
        status = data.status
        str2 = ""
        step = 1
        for i in range(361):
            str2 += strn[i]
            if strn[i] != " ":
                step += 1
        step = step % 2
    except:
        return "NO GAME"
    if request.method == "POST":
        try:
            index = int(request.form["name"])
            if strn[index] == " " and step == 0:
                iii = str(index // 19) + " " + str(index % 19)
                arr = listen_put(str2, iii)
                strn = arr[0]
                data.data = strn
                data.status = arr[1]
            else:
                print("aaaaa")
        except:
            a = 1
        try:
            clear = request.form["clear"]
            strn = 361 * " "
            data.data = strn
            data.status = 2
        except:
            a = 1
        try:
            db.session.commit()
            return redirect('/multiplayer2/' + str(id))
        except:
            return "ERROR"
    else:
        return render_template("multiplayer1.html", str=strn, status=status, temp=temp, id=id, step=step, number=number)


@app.route('/multiplayer1/<int:id>', methods=['POST', 'GET'])
def multiplayer1(id):
    try:
        number = 1
        data = Field.query.get(id)
        temp = dt.datetime.now()
        strn = data.data
        status = data.status
        str2 = ""
        step = 0
        for i in range(361):
            str2 += strn[i]
            if strn[i] != " ":
                step += 1
        step = step % 2
    except:
        return "NO GAME"
    if request.method == "POST":
        try:
            index = int(request.form["name"])
            if strn[index] == " " and step == 0:
                print(step)
                iii = str(index // 19) + " " + str(index % 19)
                arr = listen_put(str2, iii)
                strn = arr[0]
                data.data = strn
                data.status = arr[1]
        except:
            a = 1
        try:
            clear = request.form["clear"]
            strn = 361 * " "
            data.data = strn
            data.status = 2
        except:
            a = 1
        try:
            db.session.commit()
            return redirect('/multiplayer1/' + str(id))
        except:
            return "ERROR"
    else:
        return render_template("multiplayer1.html", str=strn, status=status, temp=temp, id=id, step=step, number=number)


@app.route('/play/<int:id>', methods=['POST', 'GET'])
def play_id(id):
    try:
        data = Field.query.get(id)
        temp = dt.datetime.now()
        strn = data.data
        status = data.status
    except:
        return "NO GAME"
    if request.method == "POST":
        str2 = ""
        for i in range(361):
            str2 += strn[i]
        try:
            index = int(request.form["name"])
            if strn[index] == " ":
                iii = str(index // 19) + " " + str(index % 19)
                arr = listen_put(str2, iii)
                strn = arr[0]
                data.data = strn
                data.status = arr[1]
        except:
            a = 1
        try:
            computer = request.form["computer"]
            arr = listen_next_move(str2)
            strn = arr[0]
            data.data = strn
            data.status = arr[1]
        except:
            a = 1
        try:
            clear = request.form["clear"]
            strn = 361 * " "
            data.data = strn
            data.status = 2
        except:
            a = 1
        try:
            db.session.commit()
            return redirect('/play/' + str(id))
        except:
            return "ERROR"
    else:
        return render_template("playid.html", str=strn, status=status, temp=temp, id=id)


@app.route('/newgamemlt')
def newgamemlt():
    field = Field.query.all()
    a = len(field)
    try:
        field = Field()
        field.data = 361 * " "
        db.session.add(field)
        db.session.commit()
        return redirect('/multiplayer1/' + str(a + 1))
    except:
        return "ERROR"

@app.route('/newgame')
def newgame():
    field = Field.query.all()
    a = len(field)
    try:
        field = Field()
        field.data = 361 * " "
        db.session.add(field)
        db.session.commit()
        return redirect('/play/' + str(a + 1))
    except:
        return "ERROR"


@app.route('/connect', methods=['POST', 'GET'])
def connect():
    if request.method == "POST":
        id = request.form['id']
        return redirect("multiplayer2/" + id)
    else:
        return render_template("connect.html")



if __name__ == '__main__':
    app.run(debug=True)
