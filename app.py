from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Дані для шаблону (можна замінити на БД)
    stats = {'reobladnano': 150, 'vidremontovano': 300}  # Оновив нулі на реалістичні
    services = [
        {
            'title': 'Переобладнання StarLink V2 для авто',
            'description': 'Комплект: водостійкий корпус, 4 неодимові магніти, PoE інжектор, мікротік.',
            'details': ['Водостійкий корпус', '4 неодимові магніти', 'PoE інжектор', 'Мікротік']
        },
        {
            'title': 'Ремонт та модернізація',
            'description': 'Заміна корпусу, ремонт плати, переробка розʼєму під RJ 45, переробка роутера.',
            'details': ['Заміна корпусу', 'Ремонт плати', 'Переробка розʼєму RJ 45', 'Переробка роутера']
        }
    ]
    poe_injectors = [
        {'model': 'YSNEPPU15001A', 'power': '15W', 'ports': '1x Gigabit', 'price': '500 грн'},
        {'model': 'YSNEPPU32010A', 'power': '32W', 'ports': '1x Gigabit', 'price': '700 грн'},
        {'model': 'YSNEAPL12001A', 'power': '12W', 'ports': '1x Fast Ethernet', 'price': '400 грн'}
    ]
    cable = {'model': 'YSNEACSLDV21A', 'length': '2m', 'type': 'Cat6', 'price': '200 грн'}
    reviews = [
        {'author': 'Іван Кривоніс', 'text': 'Швидкий ремонт, все працює ідеально!'},
        {'author': 'Петро Качур', 'text': 'Переобладнання для авто – топ, рекомендую!'},
        {'author': 'Лілія Степанко', 'text': 'Якісний сервіс, дякую Небограю!'}
    ]
    return render_template('index.html', stats=stats, services=services, poe_injectors=poe_injectors, 
                           cable=cable, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)