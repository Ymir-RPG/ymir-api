from flask import Flask
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy

__version__ = '0.0.1'

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

import ymir.api


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
