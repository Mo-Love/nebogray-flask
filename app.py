import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

# --- ІМПОРТ Flask-Mail ---
from flask_mail import Mail, Message 
# ------------------------

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

# --- КОНФІГУРАЦІЯ FLASK-MAIL для GMAIL ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your_sending_email@gmail.com') # <<< ЗАМІНІТЬ: Ваша пошта для відправки
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your_app_password') # <<< ЗАМІНІТЬ: Пароль Додатку
app.config['MAIL_DEFAULT_SENDER'] = 'nebogray@gmail.com' # <<< Ваш цільовий email
# ---------------------------------------------

# Ініціалізуємо Flask-Mail
mail = Mail(app)


# --- 3. МАРШРУТИ ---

@app.route('/')
def index():
    form = ContactForm()
    return render_template('index.html', form=form)


@app.route('/contacts')
def contacts():
    form = ContactForm()
    return render_template('contacts.html', form=form)


@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Обробка відправки форми, включаючи надсилання email"""
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        message = form.message.data

        try:
            # --- ЛОГІКА НАДСИЛАННЯ EMAIL ---
            msg = Message(
                subject='🚀 НОВА ЗАЯВКА НА РЕМОНТ STARLINK (САЙТ)', 
                recipients=['nebogray@gmail.com'] # <<< Цільова пошта
            )
            
            msg.body = f"""
Нова заявка на ремонт Starlink:

Ім'я Клієнта: {name}
Контакт (Телефон/Telegram): {phone}
Опис проблеми:
------------------------------------------
{message}
------------------------------------------

Дата/Час відправки: {os.times().system}
            """
            
            mail.send(msg)
            
            flash('✅ Дякуємо! Вашу заявку прийнято. Ми зв\'яжемося з вами найближчим часом.', 'success')
            
        except Exception as e:
            print(f"Помилка при відправці email: {e}")
            flash('Помилка при надсиланні заявки. Спробуйте пізніше або зв\'яжіться з нами напряму.', 'danger')

        # Перенаправлення на головну сторінку
        return redirect(url_for('index'))
        
    else:
        # Помилка валідації (некоректно заповнені поля)
        flash('❌ Помилка валідації. Будь ласка, перевірте правильність заповнення полів.', 'danger')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
