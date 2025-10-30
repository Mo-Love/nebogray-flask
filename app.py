import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

# --- 1. ВИЗНАЧЕННЯ ФОРМИ (Flask-WTF) ---
class ContactForm(FlaskForm):
    """Форма зворотного зв'язку для контакту"""
    name = StringField('Ваше Ім\'я', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Телефон або Telegram ID', validators=[DataRequired(), Length(min=5, max=50)])
    message = TextAreaField('Опис Проблеми', validators=[Length(max=500)])


# --- 2. ІНІЦІАЛІЗАЦІЯ ДОДАТКУ ТА КОНФІГУРАЦІЯ ---
app = Flask(__name__)

# ВИКОРИСТАННЯ ЗМІННОЇ СЕРЕДОВИЩА для SECRET_KEY (КРИТИЧНО)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key-must-be-changed-in-production')
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com' 
# ... інші налаштування Flask-Mail, якщо використовуєте ...


# --- 3. МАРШРУТИ ---

@app.route('/')
def index():
    """Головна сторінка"""
    form = ContactForm()
    return render_template('index.html', form=form)


@app.route('/contacts')
def contacts():
    """Сторінка контактів"""
    form = ContactForm()
    return render_template('contacts.html', form=form)


@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Обробка відправки форми з головної сторінки та сторінки контактів"""
    form = ContactForm()
    
    # Перевіряємо валідацію Flask-WTF
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        message = form.message.data

        # ----------------------------------------------------------------------
        #  ТУТ МАЄ БУТИ ВАША ЛОГІКА НАДСИЛАННЯ EMAIL (Flask-Mail) 
        #  АБО ЗБЕРЕЖЕННЯ ЗАЯВКИ
        # ----------------------------------------------------------------------
        
        # Для прикладу:
        print(f"Нова Заявка: Ім'я: {name}, Телефон: {phone}, Проблема: {message}") 

        flash('Дякуємо! Вашу заявку прийнято. Ми зв\'яжемося з вами найближчим часом.', 'success')
        
        # Перенаправлення на головну сторінку
        return redirect(url_for('index'))
        
    else:
        # Помилка валідації
        flash('Помилка валідації. Будь ласка, перевірте правильність заповнення полів.', 'danger')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
