from flask import Flask,request,render_template
import Class
import Utils
app = Falsk(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/spider/dplp")
def dplp_spider():
    if request.method == 'POST':
        author_name = request.form['author_name']
        school = request.form['school']
        department = request.form['department']
        city = request.form['city']
        country = request.form['country']
        author = Class.Author(author_name, school, department, city, country)
        m = Utils.get_author_url(author)
        if  isinstance(m,str):
            P = Class.Papers(m,author.name)
            P.parse() 