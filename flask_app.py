#!flask/bin/python
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'dons20!'

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://EricStauffer12:" \
                                        "testerman" \
                                        "@EricStauffer12.mysql.eu.pythonanywhere-services.com/" \
                                        "EricStauffer12$TheOffice"


from bs4 import BeautifulSoup
import re
import os


db = SQLAlchemy(app)
db.app = app


class Phrase(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    words = db.Column(db.String(500),nullable=False)
    startTime = db.Column(db.Integer,nullable=False)
    endTime = db.Column(db.Integer,nullable=False)
    season = db.Column(db.Integer,nullable=True)
    episode = db.Column(db.Integer,nullable=True)
    name = db.Column(db.String(500),nullable=False)
    show = db.Column(db.String(500),nullable=False)



    def __repr__(self):
        return {"season": self.season,"episode":self.episode,"startTime":self.startTime,"endTime":self.endTime,"name":self.name,"show":self.show}

    def as_json(self):
        return {"season": self.season,"episode":self.episode,"startTime":self.startTime,"endTime":self.endTime,"name":self.name,"show":self.show}


def toSeconds(time):
    return int(int(time[:len(time)-1])/10000000)


def init_db(directory):
    # db.drop_all()
    # db.create_all()
    show = directory
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        fileAndName = filename.split(" ",1)
        print(fileAndName)
        season = int(fileAndName[0][1])
        episode = int(fileAndName[0][3:])
        name = fileAndName[1]
        response = open(directory+"/" + file).read()
        soup = BeautifulSoup(response, "lxml")
        ptags = soup.find_all('p')
        words = ""
        for idx, tag in enumerate(ptags):
            if tag.string:
                if idx % 25 == 0 and idx != 0:
                    words = re.sub(r'[^\w\s]', "", words).lower()
                    item = Phrase(words=words, startTime=toSeconds(ptags[idx - 10]['begin']),
                                  endTime=toSeconds(tag['end']),
                                  season=season, episode=episode,name=name,show=show)
                    db.session.add(item)
                    words = ""
                else:
                    if words != "":
                        words += " "
                    words += tag.string
        db.session.commit()


def test(searchPhrase):
    phrases = Phrase.query.filter(Phrase.words.contains(searchPhrase))
    for phrase in phrases:
        print(phrase.season,phrase.episode)


def stripSearchString(searchString):
    searchString.islower()
    searchString = searchString.strip()
    searchString = re.sub(r'[^a-zA-Z0-9\s]',"",searchString)
    return searchString


def main(searchString,show):
    searchString = stripSearchString(searchString).lower()
    episodes = Phrase.query.filter(Phrase.show.contains(show)).filter(Phrase.words.contains(searchString))
    # episodes = Phrase.query.filter(Phrase.words.contains(searchString))
    episodeList = []
    for phrase in episodes:
        episodeList.append(phrase.as_json())
    return {"episode_number":len(episodeList),"episodes":episodeList}


def clear_the_template_cache():
    app.jinja_env.cache = {}

app.before_request(clear_the_template_cache)


@app.route('/search', methods=['POST'])
def search():
    search_input = request.json
    response = main(search_input["phrase"],search_input["show"])
    print(response["episode_number"])
    return response


@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
