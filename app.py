import os
import psycopg2
from flask import Flask, render_template_string, request, redirect
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_NAME = os.environ.get('POSTGRES_DB', 'taxidb')
DB_USER = os.environ.get('POSTGRES_USER', 'taxiuser')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'adminpass123')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                pickup_location VARCHAR(200) NOT NULL,
                dropoff_location VARCHAR(200) NOT NULL,
                status VARCHAR(50) DEFAULT 'Đang chờ'
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Loi khoi tao CSDL: {e}")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Hệ Thống Đặt Xe - Taxi Booking</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 30px; background-color: #eef2f5; }
        .container { width: 92%; max-width: 1400px; margin: 0 auto; background: white; padding: 35px 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 8px; font-size: 32px; }
        .student-info { text-align: center; color: #7f8c8d; font-size: 17px; margin-bottom: 30px; }
        .form-group { background: #f8f9fa; padding: 25px 30px; border-radius: 10px; margin-bottom: 35px; border: 1px solid #e9ecef; }
        form { display: flex; flex-direction: column; gap: 15px; }
        input { padding: 14px 18px; border: 1px solid #ced4da; border-radius: 8px; font-size: 16px; outline: none; }
        button { padding: 15px; background-color: #27ae60; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 18px; cursor: pointer; }
        button:hover { background-color: #219150; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 16px; }
        th, td { border: 1px solid #dee2e6; padding: 14px 18px; text-align: left; }
        th { background-color: #34495e; color: white; font-weight: 600; font-size: 17px; }
        tr:nth-child(even) { background-color: #f8f9fa; }
        .status { font-weight: bold; color: #e67e22; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚕 HỆ THỐNG ĐẶT XE TAXI ONLINE</h1>
        <div class="student-info"><b>Sinh viên thực hiện:</b> Hoàng Ngọc Huy - Lớp CNTT K23C (Đề 22)</div>
        
        <div class="form-group">
            <h3 style="margin-top:0; color: #2c3e50; font-size: 22px;">Đặt chuyến xe mới</h3>
            <form action="/add" method="POST">
                <input type="text" name="customer_name" placeholder="Tên khách hàng" required>
                <input type="text" name="pickup_location" placeholder="Điểm đón" required>
                <input type="text" name="dropoff_location" placeholder="Điểm đến" required>
                <button type="submit">Xác Nhận Đặt Xe</button>
            </form>
        </div>

        <h3 style="color: #2c3e50; font-size: 22px;">Danh sách chuyến đi</h3>
        <table>
            <tr>
                <th style="width: 8%;">ID</th>
                <th style="width: 25%;">Khách hàng</th>
                <th style="width: 28%;">Điểm đón</th>
                <th style="width: 28%;">Điểm đến</th>
                <th style="width: 11%;">Trạng thái</th>
            </tr>
            {% for b in bookings %}
            <tr>
                <td>{{ b[0] }}</td>
                <td>{{ b[1] }}</td>
                <td>{{ b[2] }}</td>
                <td>{{ b[3] }}</td>
                <td class="status">{{ b[4] }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    init_db()
    bookings = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, customer_name, pickup_location, dropoff_location, status FROM bookings ORDER BY id DESC;')
        bookings = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Loi lay du lieu: {e}")
    return render_template_string(HTML_TEMPLATE, bookings=bookings)

@app.route('/add', methods=['POST'])
def add_booking():
    init_db()
    name = request.form.get('customer_name')
    pickup = request.form.get('pickup_location')
    dropoff = request.form.get('dropoff_location')
    
    if name and pickup and dropoff:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO bookings (customer_name, pickup_location, dropoff_location) VALUES (%s, %s, %s);',
                (name, pickup, dropoff)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Loi them du lieu: {e}")
        
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
