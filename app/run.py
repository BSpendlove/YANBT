from flask import Flask

app = Flask(__name__)

from views import index

if __name__ == "__main__":
    app.register_blueprint(index.bp)
    app.run(host="0.0.0.0", port=5006, debug=True)