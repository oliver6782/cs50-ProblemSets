
from numpy_financial import irr
from scipy.optimize import newton
from scipy.optimize import fsolve

def calculate_npv_irr(capacity,year,epc,maintenance_fee,absorption_rate,avg_price,fy_decay,linear_decay,first_year_electricity,coal_rate,discount_rate):
    annual_electricity = [0] * year
    revenue = [0] * year
    maintenance = [0] * year
    ebit = [0] * year
    income_tax = [0] * year
    cash_flow_after_tax = [0] * year
    npv = [0] * year
    aggregate_npv = [0] * year
    decay = [0] * year
    
    decay[0] = 1 - fy_decay
    i = 1
    while i < year:
        decay[i] = decay[i-1] - linear_decay
        i = i + 1

    aggregate_npv = - epc * capacity * 1000000

    for y in range(year):
        annual_electricity[y] = decay[y] * first_year_electricity * capacity * 1000000
        
        revenue[y] = absorption_rate * annual_electricity[y] * avg_price
        + (1 - absorption_rate) * annual_electricity[y] * coal_rate
        
        maintenance[y] = maintenance_fee * capacity * 1000000
        ebit[y] = revenue[y] - maintenance[y] - epc * capacity * 1000000 / year

        if y < 3:
            income_tax[y] = 0
        elif 3 <= y < 6:
            income_tax[y] = 0.125 * ebit[y]
        else:
            income_tax[y] = 0.25 * ebit[y]

        cash_flow_after_tax[y] = ebit[y] - income_tax[y] + epc * capacity * 1000000 / year
        npv[y] = cash_flow_after_tax[y] / (1 + discount_rate) ** (y + 1)
        aggregate_npv += npv[y]
    
    
    cash_flow_final = [0] * (year + 1)
    cash_flow_final[0] = - epc * capacity * 1000000
    k = 1
    while k < year + 1:
        cash_flow_final[k] = cash_flow_after_tax[k - 1]
        k += 1
    internal_return = irr(cash_flow_final)
    return internal_return, aggregate_npv


def find_unit_price(capacity,year,epc,maintenance_fee,absorption_rate,fy_decay,linear_decay,first_year_electricity,coal_rate,discount_rate):
    
    npv_function = lambda x: calculate_npv_irr(capacity,year,epc,maintenance_fee,absorption_rate,x,fy_decay,linear_decay,first_year_electricity,coal_rate,discount_rate)[1]
    
    initial_guess = 0.4  
    unit_price = newton(npv_function, initial_guess,tol=1e-5)
    
    return unit_price


def percentage(value):
    return f"{100*value:,.2f}%"

def rmb(value):
    return f"￥{value:,.2f}"