
import sqlite3, os

DB = 'stockwise.db'

def init_db():
    if os.path.exists(DB):
        return
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT,
            cost_price REAL DEFAULT 0,
            selling_price REAL DEFAULT 0,
            quantity INTEGER DEFAULT 0
        );
    ''')
    c.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            change_qty INTEGER,
            note TEXT,
            timestamp TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        );
    ''')

    products = [
        ("Bokomo Weet-Bix 500g", "BM-WBX500", 35.0, 55.0, 120),
        ("Bokomo Weet-Bix 1kg", "BM-WBX1KG", 65.0, 95.0, 100),
        ("Bokomo Weet-Bix 1.5kg Family Pack", "BM-WBX15KG", 90.0, 135.0, 80),
        ("Bokomo Corn Flakes 500g", "BM-CF500", 30.0, 50.0, 150),
        ("Bokomo Corn Flakes 750g", "BM-CF750", 45.0, 70.0, 140),
        ("Bokomo Corn Flakes 1.2kg", "BM-CF12KG", 70.0, 110.0, 100),
        ("Bokomo Oats 500g", "BM-OATS500", 25.0, 40.0, 130),
        ("Bokomo Oats 1kg", "BM-OATS1KG", 45.0, 70.0, 120),
        ("Bokomo Oats Instant Sachets Variety Pack", "BM-OATSVAR", 55.0, 85.0, 90),
        ("Bokomo ProNutro Original 500g", "BM-PRO500", 50.0, 80.0, 110),
        ("Bokomo ProNutro Original 1kg", "BM-PRO1KG", 95.0, 140.0, 80),
        ("Bokomo ProNutro Chocolate 500g", "BM-PRCH500", 55.0, 85.0, 100),
        ("Bokomo ProNutro Chocolate 1kg", "BM-PRCH1KG", 100.0, 150.0, 75),
        ("Bokomo ProNutro Strawberry 500g", "BM-PRST500", 55.0, 85.0, 100),
        ("Bokomo Bran Flakes 500g", "BM-BRAN500", 35.0, 55.0, 100),
        ("Bokomo Bran Flakes 750g", "BM-BRAN750", 50.0, 80.0, 90),
        ("Bokomo Swiss Muesli 750g", "BM-MUS750", 85.0, 120.0, 60),
        ("Bokomo Tropical Muesli 750g", "BM-MUSTROP750", 85.0, 120.0, 60),
        ("Bokomo Crunchy Granola 750g", "BM-GRAN750", 95.0, 140.0, 70),
        ("Bokomo Honey & Nut Granola 750g", "BM-GRANHN750", 100.0, 150.0, 70),
    ]
    c.executemany("INSERT INTO products (name, sku, cost_price, selling_price, quantity) VALUES (?,?,?,?,?)", products)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
