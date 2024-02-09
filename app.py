from cs50 import SQL
from flask import Flask, request, flash, render_template, redirect,jsonify
from helpers import calculate_npv_irr, find_unit_price, percentage, rmb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bella'
app.jinja_env.filters["percentage"] = percentage
app.jinja_env.filters["rmb"] = rmb
db = SQL("sqlite:///finance.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ownership", methods=["GET", "POST"])
def ownership():
    discount_rate = 0.05
    if request.method == "POST":
        province = request.form.get("province")
        city = request.form.get("city")
        first_year_electricity_result = db.execute(
            "SELECT first_year_electricity FROM light WHERE province = ? AND city = ?", province, city
        )
        coal_rate_result = db.execute(
            "SELECT coal_rate FROM light WHERE province = ? AND city = ?", province, city
        )
        if first_year_electricity_result and coal_rate_result:
            first_year_electricity = first_year_electricity_result[0]['first_year_electricity']
            coal_rate = coal_rate_result[0]['coal_rate']
        else:
            flash("Error retrieving data from the database!")
            return render_template("ownership.html", provinces=db.execute("SELECT province FROM light GROUP BY province"))
        
        capacity = request.form.get("capacity")
        year = request.form.get("运行年限")
        epc = request.form.get("EPC单价")
        maintenance_fee = request.form.get("运维费用")
        absorption_rate = request.form.get("消纳比")
        avg_price = request.form.get("平均电价")
        fy_decay = request.form.get("首年衰减")
        linear_decay = request.form.get("线性衰减")
    

        if not capacity or not year or not epc or not absorption_rate or not avg_price:
            flash("Invalid Input!")
            return render_template("ownership.html",provinces=db.execute("SELECT province FROM light GROUP BY province"))
        
        capacity = float(request.form.get("capacity"))
        year = int(request.form.get("运行年限"))
        epc = float(request.form.get("EPC单价"))
        maintenance_fee = float(request.form.get("运维费用"))
        absorption_rate = float(request.form.get("消纳比"))/100
        avg_price = float(request.form.get("平均电价"))
        fy_decay = float(request.form.get("首年衰减"))/100
        linear_decay = float(request.form.get("线性衰减"))/100

        internal_return = calculate_npv_irr(capacity,year,epc,maintenance_fee,absorption_rate,avg_price,fy_decay,linear_decay,first_year_electricity,coal_rate,discount_rate)[0]
        if not 0 < internal_return < 1:
            return render_template("investment_plan.html",page_name="error")
        else:
            return render_template("investment_plan.html",page_name="ownership",internal_return=internal_return)

    
    else:
        provinces = db.execute("SELECT province FROM light GROUP BY province")
        return render_template("ownership.html",  provinces=provinces)
    

@app.route("/non_ownership", methods=["GET", "POST"])
def non_ownership():
    if request.method == "POST":
        province = request.form.get("province")
        city = request.form.get("city")
        first_year_electricity_result = db.execute(
            "SELECT first_year_electricity FROM light WHERE province = ? AND city = ?", province, city
        )
        coal_rate_result = db.execute(
            "SELECT coal_rate FROM light WHERE province = ? AND city = ?", province, city
        )
        if first_year_electricity_result and coal_rate_result:
            first_year_electricity = first_year_electricity_result[0]['first_year_electricity']
            coal_rate = coal_rate_result[0]['coal_rate']
        else:
            flash("Error retrieving data from the database!")
            return render_template("non_ownership.html", provinces=db.execute("SELECT province FROM light GROUP BY province"))
        
        capacity = request.form.get("capacity")
        year = request.form.get("运行年限")
        epc = request.form.get("EPC单价")
        maintenance_fee = request.form.get("运维费用")
        absorption_rate = request.form.get("消纳比")
        discount_rate = request.form.get("收益率")
        fy_decay = request.form.get("首年衰减")
        linear_decay = request.form.get("线性衰减")
    
    
        if not capacity or not year or not epc or not absorption_rate:
            flash("Invalid Input!")
            return render_template("non_ownership.html",provinces=db.execute("SELECT province FROM light GROUP BY province"))
        
        capacity = float(request.form.get("capacity"))
        year = int(request.form.get("运行年限"))
        epc = float(request.form.get("EPC单价"))
        maintenance_fee = float(request.form.get("运维费用"))
        absorption_rate = float(request.form.get("消纳比"))/100
        discount_rate = float(request.form.get("收益率"))/100
        fy_decay = float(request.form.get("首年衰减"))/100
        linear_decay = float(request.form.get("线性衰减"))/100

        unit_price = find_unit_price(capacity,year,epc,maintenance_fee,absorption_rate,fy_decay,linear_decay,first_year_electricity,coal_rate,discount_rate)
        if not unit_price:
            return render_template("investment_plan.html", page_name="error")
        else:
            return render_template("investment_plan.html", page_name="non_ownership", unit_price=unit_price)
    
    else:
        provinces = db.execute("SELECT province FROM light GROUP BY province")
        return render_template("non_ownership.html", provinces=provinces)


@app.route("/investment_plan")
def plan():
    return render_template("investment_plan.html")

@app.route('/get_cities/<selected_province>')
def get_cities(selected_province):
    cities = db.execute("SELECT city FROM light WHERE province = ? GROUP BY city", selected_province)
    city_names = []
    for city in cities:
        city_names.append(city['city'])
    return jsonify(city_names)

    




