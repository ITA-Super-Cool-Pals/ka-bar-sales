import os, json, app_db
from flask import Flask, request, Response

app = Flask(__name__)

# Show result function, sorted by column order
def show_result(data, status=200):
    return Response(json.dumps(data, sort_keys=False), status=status, mimetype='application/json')

# Check if DB exists, if not create new DB
if not os.path.exists(app_db.db_path):
    print('bar sales db not found, creating new')
    app_db.db_create()
else:
    print(f'bar sales db found, using it at {app_db.db_path}')

# Routes
# Return all sales data
@app.route('/barsales')
def get_sales():
    sales = app_db.get_all()
    return show_result(sales)

app.run(host='0.0.0.0')
