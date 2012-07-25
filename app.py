import os
from datetime import datetime
from flask import Flask, render_template
from fisl_keynotes.datasource import GlobaisTalks

app = Flask(__name__)

@app.route('/')
def hello():
    all_talks = [talk for talk in GlobaisTalks().all_talks() if talk.date >= datetime.now()]
    return render_template('index.html', talks=all_talks)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
