from flask import Flask, render_template, request, jsonify, redirect, url_for
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# تهيئة Supabase
supabase_url = os.getenv('https://bxqamnrnxjyuwdqxyyps.supabase.co')
supabase_key = os.getenv('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ4cWFtbnJueGp5dXdkcXh5eXBzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIxNjE4MzksImV4cCI6MjA3NzczNzgzOX0.C-b7v5w5Ld545TvhYXV12447YpybweUS0_bB7_SlTC8')
supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        # الحصول على البيانات من النموذج
        data = {
            'temperature': float(request.form['temperature']),
            'moisture': float(request.form['moisture']),
            'rainfall': float(request.form['rainfall']),
            'ph': float(request.form['ph']),
            'nitrogen': float(request.form['nitrogen']),
            'phosphorous': float(request.form['phosphorous']),
            'potassium': float(request.form['potassium']),
            'carbon': float(request.form['carbon']),
            'soil': request.form['soil'],
            'crop': request.form['crop'],
            'fertilizer': request.form['fertilizer'],
            'water_ph': float(request.form['water_ph']),
            'water_level': float(request.form['water_level']),
            'turbidity': float(request.form['turbidity'])
        }
        
        # إدخال البيانات إلى Supabase
        response = supabase.table('sensor_data').insert(data).execute()
        
        return jsonify({
            'success': True,
            'message': 'تم إدخال البيانات بنجاح!',
            'data': response.data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في إدخال البيانات: {str(e)}'
        }), 400

@app.route('/data')
def view_data():
    try:
        # جلب البيانات من Supabase
        response = supabase.table('sensor_data').select('*').execute()
        return render_template('data.html', data=response.data)
    except Exception as e:
        return f'خطأ في جلب البيانات: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
