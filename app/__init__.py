from flask import Flask, render_template  # Додаємо імпорт render_template
from app.users.views import users_bp  # Імпортуємо блюпринт для користувачів

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Реєстрація блюпринта для користувачів
app.register_blueprint(users_bp, url_prefix='/users')

# Головний маршрут для сторінки
@app.route('/')
def home():
    return render_template('home.html')  # Головна сторінка

if __name__ == '__main__':
    app.run(debug=True)
