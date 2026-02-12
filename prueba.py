from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'colonias.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    edo = request.args.get('edo', '')
    id_param = request.args.get('id', '')
    return render_template('index.html', edo=edo, id_param=id_param)

@app.route('/api/municipios/<estado>')
def get_municipios(estado):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT mun, no_contesto 
            FROM colonias 
            WHERE edo = ? 
            ORDER BY mun
        """, (estado,))
        municipios = [{"nombre": row['mun'], "no_contesto": row['no_contesto']} 
                     for row in cursor.fetchall()]
        conn.close()
        return jsonify(municipios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/colonias/<estado>/<municipio>')
def get_colonias(estado, municipio):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT colonias, campo_colonias 
            FROM colonias 
            WHERE edo = ? AND mun = ?
            ORDER BY colonias
        """, (estado, municipio))
        colonias = [{"nombre": row['colonias'], "valor": row['campo_colonias']} 
                   for row in cursor.fetchall()]
        conn.close()
        return jsonify(colonias)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
