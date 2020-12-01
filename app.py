from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(361), nullable=False, default="")
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Field %r>' % self.id


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intro = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/index')
def game():
    return render_template("index.html")


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/play/<int:id>', methods=['POST', 'GET'])
def play_id(id):
    try:
        data = Field.query.get(id)
        strn = data.data
        print(strn)
    except:
        return "NO GAME"
    if request.method == "POST":
        try:
            ii = int(request.form["ii"])
            jj = int(request.form["jj"])
        except:
            return render_template("playid.html", str=strn)
        str2 = ""
        for i in range(361):
            if i != ii * 19 + jj:
                str2 += strn[i]
            else:
                str2 += "x"
        strn = str2
        data.data = strn
        try:
            db.session.commit()
            return render_template("playid.html", str=strn)
        except:
            return "ERROR"
    else:
        return render_template("playid.html", str=strn)


@app.route('/play', methods=['POST', 'GET'])
def play():
    if request.method == "POST":
        try:
            ii = request.form["ii"]
            jj = request.form["jj"]
            try:
                send = request.form["send"]
            except:
                render_template("play.html")
            print(ii, jj)
            return render_template("play.html")
        except:
            return "ERROR"
    else:
        return render_template("play.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "ERROR"


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR"
    else:
        return render_template("create-article.html")


@app.route('/newgame')
def newgame():
    field = Field.query.all()
    print(len(field))
    a = len(field)
    try:
        field = Field()
        field.data = 361 * " "
        db.session.add(field)
        db.session.commit()
        return redirect('/play/' + str(a + 1))
    except:
        return "ERROR"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR"
    else:
        return render_template("post_update.html", article=article)


if __name__ == '__main__':
    app.run(debug=True)
