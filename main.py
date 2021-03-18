import collections
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from data import CharCounter
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asfasfawfasfasfawf'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///history.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100))
    output_char = db.Column(db.String(100))
    count = db.Column(db.String(100))
    time = db.Column(db.String(20))
db.create_all()


@app.route('/', methods=["GET", "POST"])
def main():
    form = CharCounter()
    if form.validate_on_submit():
        word = form.word.data.lower()
        res = collections.Counter(word).most_common(2)
        try:
            for i in enumerate(word[::-1]):
                if i[1] == res[0][0]:
                    index1 = i[0]
                    break
            for i in enumerate(word[::-1]):
                if i[1] == res[1][0]:
                    index2 = i[0]
                    break
            if res[0][1] == res[1][1]:
                if index1 < index2:
                    res = res[0]
                else:
                    res = res[1]
            else:
                res = res[0]
        except IndexError:
            res = res[0]
        new_data = Data(
            word=form.word.data,
            output_char=res[0],
            count=res[1],
            time=datetime.now().strftime('%B/%D/%Y (%X)')
        )
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('data'))
    return render_template("main.html", form=form)

@app.route('/history')
def data():
    datas = Data.query.all()
    return render_template("data.html", datas=datas)



if __name__ == "__main__":
    app.run(debug=True)
