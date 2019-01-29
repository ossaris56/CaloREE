from caloree import app

if __name__ == '__main__':
    app.run(debug=True, port=8234, ssl_context='adhoc', host="0.0.0.0")
