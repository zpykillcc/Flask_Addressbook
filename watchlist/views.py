import os
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm

from watchlist import app, db
from watchlist.models import User, Movie



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        name = request.form['name']
        sex = request.form['sex']
        phone = request.form['phone']
        qq = request.form['qq']

        if not name or not sex:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(name=name, sex=sex, phone=phone, qq=qq)
        movie.user = current_user
        db.session.add(movie)
        db.session.commit()
        flash('创建联系人成功.')
        return redirect(url_for('index'))

    movies =[]
    if current_user.is_authenticated:
        user = current_user
        movies = Movie.query.filter_by(user_id=user.id).all()
    return render_template('index.html',user = current_user, movies=movies)


@app.route('/query', methods=['GET', 'POST'])
@login_required
def query():
    user = current_user
    movies = Movie.query.filter_by(user_id=user.id).all()
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        phone = request.form.get('phone')
        qq = request.form.get('qq')
        movies = Movie.query.filter_by(user_id=user.id,
        name=name if name else not None,
        sex=sex if sex else not None,
        phone=phone if phone else not None,
        qq=qq if qq else not None).all()
        query_dict = {
            'user_id': user.id,
            'name': name,
            'sex': sex,
            'phone': phone,
            'qq': qq
        }
        if not name:
            query_dict.pop('name')
        if not sex:
            query_dict.pop('sex')
        if not phone:
            query_dict.pop('phone')
        if not qq:
            query_dict.pop('qq')
        movies = Movie.query.filter_by(**query_dict).all()
        return render_template('index.html',user = current_user, movies=movies)
    return render_template('index.html',user = current_user, movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        phone = request.form['phone']
        qq = request.form['qq']

        if not name or not sex:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.name = name
        movie.sex = sex
        movie.phone = phone
        movie.qq = qq
        db.session.commit()
        flash('更新联系人成功.')
        return redirect(url_for('index'))

    return render_template('edit.html', user=current_user ,movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('删除联系人成功.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.filter_by(username=current_user.username).first()
        user.username = name
        db.session.commit()
        flash('设置更改成功.')
        return redirect(url_for('index'))

    return render_template('settings.html', user = current_user)

@app.route('/up_photo', methods=['POST'])
@login_required
def up_photo():
    from watchlist import allowed_file, random_string
    img = request.files.get('photo')
    if not img:
        flash("头像不能为空")
        return redirect(url_for('settings'))
    if not allowed_file(img.filename):
        flash("头像格式错误")
        return redirect(url_for('settings'))
    suffix = os.path.splitext(img.filename)[1]
    filename = random_string()+suffix
    file_path = app.config['UPLOAD_FOLDER']+filename
    img.save(file_path)
    user=current_user
    user.image_hash = filename
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        User.movies=[]
        if user and user.validate_password(password):
            login_user(user)
            flash('登陆成功.')
            return redirect(url_for('index'))

        flash('用户名错误或密码错误.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeatpassword = request.form['repeatpassword']
        if repeatpassword != password:
            flash('两次密码输入不同!')
            return redirect('register')
        if not User.query.filter_by(username=username).first() == None:
            flash('用户名已存在!')
            return redirect('register')
        user = User(username = username,)
        user.set_password(password)
        user.image_hash = 'default.png'
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('登陆成功.')
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        oldpassword = request.form['oldpassword']
        password = request.form['password']
        repeatpassword = request.form['repeatpassword']
        if repeatpassword != password:
            flash('两次密码输入不同!')
            return redirect('password')
        if not current_user.validate_password(oldpassword):
            flash('旧密码错误')
            return redirect('password')
        user = current_user
        user.set_password(password)
        db.session.commit()
        flash('密码修改成功.')
        return redirect(url_for('index'))
    return render_template('password.html',user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

