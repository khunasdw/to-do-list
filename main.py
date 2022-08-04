from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to-do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_do = db.Column(db.String(250), unique=False, nullable=False)
    finished = db.Column(db.Boolean, nullable=False)


db.create_all()
db.session.commit()


@app.route("/", methods=["POST", "GET"])
def to_do():
    to_do_list = Todolist.query.all()
    if request.method == "POST":
        data = request.form
        my_to_do = data["to-do"]
        new_to_do_list = Todolist(to_do=my_to_do,
                                  finished=False
                                  )
        db.session.add(new_to_do_list)
        db.session.commit()
        return redirect(url_for('to_do'))
    return render_template("index.html", to_do_list=to_do_list)


@app.route("/delete")
def delete():
    my_to_do = request.args.get("id")
    my_to_do_to_delete = Todolist.query.get(my_to_do)
    db.session.delete(my_to_do_to_delete)
    db.session.commit()
    return redirect(url_for('to_do'))


@app.route("/check")
def change_status():
    to_do_list = request.args.get("id")
    my_to_do = Todolist.query.get(to_do_list)
    if my_to_do.finished:
        my_to_do.finished = 0
    else:
        my_to_do.finished = 1
    db.session.commit()
    return redirect(url_for('to_do'))


if __name__ == "__main__":
    app.run(debug=True)
