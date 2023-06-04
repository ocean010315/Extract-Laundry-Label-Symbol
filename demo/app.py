from flask import Flask,request, render_template
from routes.welcome_route import bp

app = Flask(__name__)
app.register_blueprint(bp)

# @app.route('/')
# def hello():
#     return 'Hello, My First Flask!'
@app.route('/')
def index():
    return render_template('index.html' )

@app.route('/result' , methods=['POST'])
def sample2():
    if request.method=='POST':
        id = request.form['text']
        return render_template('html_sample2.html') , 200
    else:
        return render_template('html_sample2.html') , 200

@app.route('/user/<username>')
def name_print(username):
    return f"hello {username}" , 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)