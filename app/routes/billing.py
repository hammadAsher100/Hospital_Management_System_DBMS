from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required
from app import db
from app.models.billing import Bill, BillItem
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.utils import role_required
from datetime import datetime
import csv
import io

billing_bp = Blueprint('billing', __name__)


@billing_bp.route('/')
@login_required
def list_bills():
    status_filter = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)

    query = Bill.query.join(Patient)
    if status_filter:
        query = query.filter(Bill.status == status_filter)

    bills = query.order_by(Bill.bill_date.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('billing/list.html', bills=bills, status_filter=status_filter)


@billing_bp.route('/generate', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'billing')
def generate_bill():
    if request.method == 'POST':
        try:
            patient_id = int(request.form['patient_id'])
            appointment_id = request.form.get('appointment_id') or None
            payment_method = request.form.get('payment_method', '')

            descriptions = request.form.getlist('description[]')
            quantities = request.form.getlist('quantity[]')
            unit_prices = request.form.getlist('unit_price[]')

            if not descriptions or not descriptions[0]:
                flash('Please add at least one item.', 'danger')
                raise ValueError("No items")

            bill = Bill(
                patient_id=patient_id,
                appointment_id=int(appointment_id) if appointment_id else None,
                payment_method=payment_method,
                status='pending'
            )
            db.session.add(bill)
            db.session.flush()

            total = 0
            for desc, qty, price in zip(descriptions, quantities, unit_prices):
                if desc.strip():
                    qty_int = int(qty) if qty else 1
                    price_float = float(price) if price else 0
                    item_total = qty_int * price_float
                    total += item_total
                    item = BillItem(
                        bill_id=bill.bill_id,
                        description=desc,
                        quantity=qty_int,
                        unit_price=price_float,
                        total_price=item_total
                    )
                    db.session.add(item)

            bill.total_amount = total
            bill.update_status()
            db.session.commit()
            flash('Bill generated successfully!', 'success')
            return redirect(url_for('billing.view_bill', id=bill.bill_id))

        except Exception as e:
            db.session.rollback()
            if str(e) != "No items":
                flash(f'Error generating bill: {str(e)}', 'danger')

    patients = Patient.query.order_by(Patient.last_name).all()
    appointments = Appointment.query.filter_by(status='completed').order_by(
        Appointment.appointment_date.desc()
    ).all()
    preselect = request.args.get('patient_id', type=int)
    return render_template('billing/generate.html', patients=patients,
                           appointments=appointments, preselect=preselect)


@billing_bp.route('/<int:id>')
@login_required
def view_bill(id):
    bill = Bill.query.get_or_404(id)
    return render_template('billing/view.html', bill=bill)


@billing_bp.route('/<int:id>/print')
@login_required
def print_bill(id):
    bill = Bill.query.get_or_404(id)
    return render_template('billing/invoice.html', bill=bill)


@billing_bp.route('/<int:id>/payment', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'billing')
def record_payment(id):
    bill = Bill.query.get_or_404(id)

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            method = request.form['payment_method']

            if amount <= 0:
                flash('Payment amount must be positive.', 'danger')
            elif amount > bill.get_balance():
                flash(f'Amount exceeds balance of Rs. {bill.get_balance():.2f}.', 'danger')
            else:
                bill.record_payment(amount, method)
                flash(f'Payment of Rs. {amount:.2f} recorded.', 'success')
                return redirect(url_for('billing.view_bill', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error recording payment: {str(e)}', 'danger')

    return render_template('billing/payment.html', bill=bill)


@billing_bp.route('/patient/<int:patient_id>/bills')
@login_required
def patient_bills(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    bills = Bill.query.filter_by(patient_id=patient_id).order_by(Bill.bill_date.desc()).all()
    return render_template('billing/patient_bills.html', patient=patient, bills=bills)


@billing_bp.route('/export')
@login_required
@role_required('admin', 'billing')
def export_bills():
    bills = Bill.query.join(Patient).order_by(Bill.bill_date.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Bill ID', 'Patient', 'Date', 'Total', 'Paid', 'Balance', 'Status'])

    for b in bills:
        writer.writerow([
            b.bill_id, b.patient.full_name,
            b.bill_date.strftime('%Y-%m-%d'),
            float(b.total_amount), float(b.paid_amount),
            b.get_balance(), b.status
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=bills_export.csv'}
    )
