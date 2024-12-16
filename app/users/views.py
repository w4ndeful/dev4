from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from datetime import timedelta

users_bp = Blueprint('users', __name__, template_folder='templates/users')

# Dummy user credentials
USER_CREDENTIALS = {"username": "admin", "password": "password"}

# Login page
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Authentication
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['user'] = username
            flash('Успішний вхід!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Невірний логін або пароль', 'danger')
            return redirect(url_for('users.login'))

    return render_template('login.html')

# Profile page
@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        flash('Спочатку увійдіть у систему.', 'danger')
        return redirect(url_for('users.login'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'logout':
            session.pop('user', None)
            flash('Ви вийшли із системи.', 'success')
            return redirect(url_for('users.login'))

        elif action == 'add_cookie':
            key = request.form.get('key')
            value = request.form.get('value')
            max_age = int(request.form.get('max_age', 0))
            resp = make_response(redirect(url_for('users.profile')))
            resp.set_cookie(key, value, max_age=max_age)
            flash(f'Кукі {key} додано.', 'success')
            return resp

        elif action == 'delete_cookie':
            key = request.form.get('key')
            resp = make_response(redirect(url_for('users.profile')))
            if key:
                resp.delete_cookie(key)
                flash(f'Кукі {key} видалено.', 'success')
            else:
                for cookie in request.cookies:
                    resp.delete_cookie(cookie)
                flash('Всі кукі видалено.', 'success')
            return resp

    cookies = request.cookies.items()
    return render_template('profile.html', username=session['user'], cookies=cookies)

# Change color scheme
@users_bp.route('/change-color/<color>')
def change_color(color):
    if 'user' not in session:
        flash('Спочатку увійдіть у систему.', 'danger')
        return redirect(url_for('users.login'))

    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie('color_scheme', color, max_age=30 * 24 * 60 * 60)  # 30 днів
    flash(f'Кольорова схема змінена на {color}.', 'success')
    return resp
