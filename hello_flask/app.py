
from flask import Flask,render_template, Response, url_for
import sys
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

#Debug logger
import logging 
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


def return_dict():
    #Dictionary to store music file information
    dict_here = [
        {'id': 1, 'name': 'We Don\'t Talk Anymore', 'link': "music/We Don't Talk Anymore.mp3", 'genre': 'Pop', 'rating': 5},
        {'id': 2, 'name': 'Counting Stars','link': 'music/Counting Stars.mp3', 'genre': 'Pop', 'rating': 5},
        {'id': 3, 'name': "Don't Let Me Down",'link': "music/Don't Let Me Down.mp3", 'genre': 'Electronic', 'rating': 5},
        {'id': 4, 'name': "Lean On",'link': "music/Lean On.mp3", 'genre': 'Electronic', 'rating': 5},
        {'id': 5, 'name': "In My Feelings",'link': "music/In My Feelings.mp3", 'genre': 'Hip-Hop/Rap', 'rating': 5},
        {'id': 6, 'name': "Uptown Funk",'link': "music/Uptown Funk.mp3", 'genre': 'Funk', 'rating': 5},
        {'id': 7, 'name': "Starboy",'link': "music/Starboy.mp3", 'genre': 'Contemporary R&B', 'rating': 5},
        {'id': 8, 'name': "See You Again",'link': "music/See You Again.mp3", 'genre': 'Hip-Hop/Rap', 'rating': 5}
        ]
    return dict_here
    

# Initialize Flask.
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base2.html")

@app.route("/ListenerLogin")
def enterpg():
    return render_template("enterpg.html")

@app.route("/ArtistLogin")
def enterpgArtist():
    return render_template("enterpgArtist.html")

#Route to render GUI
@app.route('/musicPlayer')
def show_entries():
    general_Data = {
        'title': 'Music Player'}
    print(return_dict())
    stream_entries = return_dict()
    return render_template('design.html', entries=stream_entries, **general_Data)

#Route to stream music
@app.route('/musicPlayer/<int:stream_id>')
def streammp3(stream_id):
    def generate():
        data = return_dict()
        count = 1
        for item in data:
            if item['id'] == stream_id:
                song = item['link']
        with open(song, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
                logging.debug('Music data fragment : ' + str(count))
                count += 1
                
    return Response(generate(), mimetype="audio/mp3")

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port)) #+ str(port)
    http_server.listen(port) #port
    IOLoop.instance().start()

'''

from flask import Flask,render_template,url_for
app = Flask(__name__) #references this file

@app.route("/")
def home():
    return render_template("base2.html")

@app.route("/ListenerLogin")
def enterpg():
    return render_template("enterpg.html")

@app.route("/ArtistLogin")
def enterpgArtist():
    return render_template("enterpgArtist.html")

if __name__ == "__main__":
    app.run(debug=True)
'''