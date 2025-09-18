
import os
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

DB = 'stockwise.db'

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.secret_key = 'dev-key-change-me'

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    total_value = sum([p['quantity'] * p['cost_price'] for p in products])
    conn.close()
    return render_template('index.html', products=products, total_value=total_value)

@app.route('/product/add', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name'].strip()
        sku = request.form['sku'].strip()
        cost_price = float(request.form['cost_price'] or 0)
        selling_price = float(request.form['selling_price'] or 0)
        quantity = int(request.form['quantity'] or 0)
        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, sku, cost_price, selling_price, quantity) VALUES (?,?,?,?,?)', 
                     (name, sku, cost_price, selling_price, quantity))
        conn.commit()
        conn.close()
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/product/<int:pid>/adjust', methods=['GET','POST'])
def adjust_stock(pid):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id=?', (pid,)).fetchone()
    if not product:
        conn.close()
        flash('Product not found', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        change = int(request.form['change'] or 0)
        note = request.form.get('note','').strip()
        new_qty = product['quantity'] + change
        conn.execute('UPDATE products SET quantity=? WHERE id=?', (new_qty, pid))
        conn.execute('INSERT INTO transactions (product_id, change_qty, note, timestamp) VALUES (?,?,?,?)',
                     (pid, change, note, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        flash('Stock adjusted.', 'success')
        return redirect(url_for('index'))
    conn.close()
    return render_template('adjust_stock.html', product=product)

@app.route('/reports/transactions')
def transactions():
    conn = get_db_connection()
    txs = conn.execute('SELECT t.*, p.name as product_name, p.sku as sku FROM transactions t JOIN products p ON p.id=t.product_id ORDER BY t.timestamp DESC').fetchall()
    conn.close()
    return render_template('transactions.html', transactions=txs)

if __name__ == '__main__':
    import init_db
    init_db.init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
