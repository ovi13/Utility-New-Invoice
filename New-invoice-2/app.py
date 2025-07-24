from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Fixed data for predefined users
users = {
    "Mridul Kanti Dey": {"consumer_id": "41793600", "meter_number": "250145"},
    "Rita Dey": {"consumer_id": "41569338", "meter_number": "094222"},
    "Pijush Kanti Dey": {"consumer_id": "41019683", "meter_number": "27023"},
    "Angshu Debray": {"consumer_id": "41569323", "meter_number": "094221"},
    "Mridul Kanti Dey & Rita Dey (Motor Bill Shared)": {"consumer_id": "41771313", "meter_number": "10501785"},
    "Mridul Kanti Dey, Rita Dey, Pijush Kanti Dey, Pappu Dey (Gas Bill Shared)": {"consumer_id": "240101995",
                                                                                  "meter_number": None},
    # Gas bill has no meter number
}


# Function to calculate the total bill and balance
def calculate_invoice(gas, electricity, motor, bkash_charge, paid):
    total_bill = gas + electricity + motor + bkash_charge
    balance = paid - total_bill
    return total_bill, balance


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_user = request.form['selected_user']

        if selected_user in users:
            name = selected_user
            consumer_id = users[selected_user]["consumer_id"]
            meter_number = users[selected_user]["meter_number"]
        else:
            name = request.form['name']
            consumer_id = request.form['consumer_id']
            meter_number = request.form['meter_number']

        billing_month = request.form['billing_month']
        gas_bill = float(request.form['gas_bill'])
        electricity_bill = float(request.form['electricity_bill'])
        motor_bill = float(request.form['motor_bill'])
        bkash_charge = float(request.form['bkash_charge'])
        bkash_transaction_id = request.form['bkash_transaction_id']
        total_paid = float(request.form['total_paid'])

        total_bill, balance = calculate_invoice(gas_bill, electricity_bill, motor_bill, bkash_charge, total_paid)

        if balance < 0:
            balance_status = f"Balance Due: ৳{-balance}"
        else:
            balance_status = f"Balance Returned: ৳{balance}"

        special_note = "This is a computer programming generated invoice, does not require any signature."

        current_datetime = datetime.now()
        billing_date = current_datetime.strftime("%Y-%m-%d")
        billing_time = current_datetime.strftime("%I:%M %p")

        return render_template('invoice.html', name=name, billing_month=billing_month, consumer_id=consumer_id,
                               meter_number=meter_number, gas_bill=gas_bill, electricity_bill=electricity_bill,
                               motor_bill=motor_bill, bkash_charge=bkash_charge,
                               bkash_transaction_id=bkash_transaction_id,
                               total_paid=total_paid, total_bill=total_bill, balance_status=balance_status,
                               special_note=special_note, billing_date=billing_date, billing_time=billing_time)

    return render_template('index.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
