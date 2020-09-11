from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/encode')
def encode():    
    return render_template('TripleDesEncode.html')

@app.route('/decode')
def decode():    
    return render_template('TripleDesDecode.html')

@app.route('/getdata', methods = ['GET', 'POST'])
def getdata():
    content = request.args.get('content')
    print(content)
    return content or 'None'


def run_app():
    app.run(host = '127.0.0.1', port = '8058', debug = True)

if __name__ == "__main__":
    run_app()