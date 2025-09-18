
# StockWise Inventory Prototype (Render-ready)

Lightweight Flask app for inventory management with preloaded Bokomo products.

## Features
- Add/edit products
- Adjust stock in/out
- View transaction reports
- Preloaded with 20 Bokomo items (Weet-Bix, ProNutro, Oats, Corn Flakes, Muesli, Granola)

## Running Locally
```bash
pip install -r requirements.txt
python init_db.py
python app.py
```
Visit http://localhost:5000

## Deploying to Render
1. Push this repo to GitHub
2. On Render, create a new Web Service from this repo
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Render will give you a live URL
