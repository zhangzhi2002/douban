import re

from flask import Blueprint, request, redirect, render_template, session
from .utils import query
from .utils.getHomeData import *

blue = Blueprint('blue', __name__)


@blue.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat, request.path):
        return
    if request.path == '/login':
        return
    if request.path == '/register':
        return

    if session.get('email'):
        return
    return redirect('/login')


@blue.route('/')
def index():
    return render_template('start/login.html')


@blue.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'GET':
        return render_template('start/login.html')
    elif request.method == 'POST':
        def filter_fn(item):
            return request.form['email'] == item[1] and request.form['password'] == item[2]

        users = query.querys('select * from user', [], 'select')
        filter_users = list(filter(filter_fn, users))
        session['email'] = request.form['email']
        if filter_users:
            return redirect('/home')
        else:
            return render_template('start/error.html', message='邮箱或密码错误')


@blue.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@blue.route('/register', methods=['GET', 'POST'])
def register():  # put application's code here
    if request.method == 'GET':
        return render_template('start/register.html')
    elif request.method == 'POST':
        if request.form['password'] == request.form['passwordChecked']:
            print('password matched')
        else:
            return render_template('start/error.html', message='两次密码不匹配')

        def filter_fn(item):
            return request.form['email'] == item[1]

        users = query.querys('select * from user ', [], type='select')
        filter_user = list(filter(filter_fn, users))
        print(filter_user)
        if filter_user:
            return render_template('start/error.html', message='邮箱已被注册')
        else:
            query.querys('insert into user (email,password) values (%s,%s)',
                         [request.form['email'], request.form['password']])
            return redirect('/login')


@blue.route('/home', methods=['GET', 'POST'])
def home():
    maxMovieLen, maxRate, strActors, strActorsNumber, strCountry, maxTypeLen, strLanguage = getHomeData()
    movieType = getTypesEcharDate()
    x, y = getRatesEcharDate()
    email = session.get('email')
    return render_template('top/index.html', email=email, maxMovieLen=maxMovieLen, maxRate=maxRate, strActors=strActors,
                           strActorsNumber=strActorsNumber,
                           strCountry=strCountry, maxTypeLen=maxTypeLen, strLanguage=strLanguage, movieType=movieType,
                           x=x,
                           y=y)


@blue.route('/detail')
def detail():
    email = session.get('email')
    tableData = getTableData()
    return render_template('top/detail.html', email=email, tableData=tableData)


@blue.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        searchMovies = searchMovie()
        return render_template('top/search.html', searchMovies=searchMovies)
    else:
        searchWord = request.form['movie_name']
        searchMovies = searchMovieByWord(searchWord)
        return (render_template('top/search.html', searchMovies=searchMovies))


@blue.route('/time', methods=['GET', 'POST'])
def time():
    movieLength = getLength()
    x, y = getTime()
    print(x, y)
    email = session.get('email')
    return render_template('charts/time.html', x=x, y=y, movieLength=movieLength, email=email)


@blue.route('/rate', methods=['GET', 'POST'])
@blue.route('/rate/<movie_type>', methods=['GET', 'POST'])
def rate(movie_type=None):
    email = session.get('email')
    movieType = getmovieType()
    movie_name, RateLevels = getRateLevel('长津湖')
    x2, y2 = getYearRate()
    if movie_type is not None:
        # 如果提供了电影类型，可以根据电影类型获取相关信息
        x, y = searchMovieByType(movie_type)
    # movieType = movie_type  # 假设这个函数返回电影类型的名称
    else:
        x, y = getRatesEcharDate()
    if request.method == 'POST':
        keyword = request.form['电影名称']
        movie_name,RateLevels=getRateLevel(keyword)
        print(movie_name,RateLevels)
    return render_template('charts/rate.html', movieType=movieType, email=email, x=x, y=y, movie_name=movie_name, RateLevels=RateLevels, x2=x2, y2=y2)


@blue.route('/', methods=['GET', 'POST'])
def allRequest():
    return redirect('/login')
