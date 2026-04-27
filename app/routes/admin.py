from flask import Blueprint, render_template, request, Response
from flask_login import login_required
from app import db
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.billing import Bill
from app.models.pharmacy import Medicine
from app.models.doctor import Doctor
from app.models.admission import Admission
from app.utils import admin_required
from datetime import datetime, date, timedelta
from sqlalchemy import func, cast, Date
import csv, io

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
def dashboard():
    today = date.today()
    month_start = today.replace(day=1)

    total_patients = Patient.query.count()
    today_appointments = Appointment.query.filter_by(appointment_date=today).count()
    active_admissions = Admission.query.filter_by(discharge_date=None).count()
    low_stock_count = Medicine.query.filter(
        Medicine.stock_quantity <= Medicine.reorder_level
    ).count()

    monthly_revenue = db.session.query(func.sum(Bill.paid_amount)).filter(
        Bill.bill_date >= month_start
    ).scalar() or 0

    pending_bills_count = Bill.query.filter_by(status='pending').count()

    # Today's appointments for quick view
    todays_appts = Appointment.query.filter_by(
        appointment_date=today
    ).order_by(Appointment.appointment_time).limit(5).all()

    # Recent patients
    recent_patients = Patient.query.order_by(
        Patient.registration_date.desc()
    ).limit(5).all()

    # Revenue last 7 days for mini chart
    revenue_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        rev = db.session.query(func.sum(Bill.paid_amount)).filter(
            cast(Bill.bill_date, Date) == d
        ).scalar() or 0
        revenue_data.append({'date': d.strftime('%b %d'), 'amount': float(rev)})

    return render_template('dashboard/admin_dashboard.html',
                           total_patients=total_patients,
                           today_appointments=today_appointments,
                           active_admissions=active_admissions,
                           low_stock_count=low_stock_count,
                           monthly_revenue=monthly_revenue,
                           pending_bills_count=pending_bills_count,
                           todays_appts=todays_appts,
                           recent_patients=recent_patients,
                           revenue_data=revenue_data)


@admin_bp.route('/reports/patients')
@login_required
def report_patients():
    total = Patient.query.count()
    by_gender = db.session.query(Patient.gender, func.count()).group_by(Patient.gender).all()
    by_blood = db.session.query(Patient.blood_group, func.count()).group_by(Patient.blood_group).all()

    monthly_reg = db.session.query(
        func.year(Patient.registration_date).label('yr'),
        func.month(Patient.registration_date).label('mo'),
        func.count().label('cnt')
    ).group_by('yr', 'mo').order_by('yr', 'mo').limit(12).all()

    return render_template('admin/report_patients.html',
                           total=total, by_gender=by_gender,
                           by_blood=by_blood, monthly_reg=monthly_reg)


@admin_bp.route('/reports/revenue')
@login_required
def report_revenue():
    period = request.args.get('period', 'monthly')
    today = date.today()

    if period == 'daily':
        start = today - timedelta(days=30)
        data = db.session.query(
            cast(Bill.bill_date, Date).label('period'),
            func.sum(Bill.total_amount).label('total'),
            func.sum(Bill.paid_amount).label('paid')
        ).filter(cast(Bill.bill_date, Date) >= start).group_by('period').order_by('period').all()
    elif period == 'weekly':
        start = today - timedelta(weeks=12)
        data = db.session.query(
            func.datepart(db.text('iso_week'), Bill.bill_date).label('period'),
            func.sum(Bill.total_amount).label('total'),
            func.sum(Bill.paid_amount).label('paid')
        ).filter(Bill.bill_date >= start).group_by('period').order_by('period').all()
    else:
        data = db.session.query(
            func.year(Bill.bill_date).label('yr'),
            func.month(Bill.bill_date).label('mo'),
            func.sum(Bill.total_amount).label('total'),
            func.sum(Bill.paid_amount).label('paid')
        ).group_by('yr', 'mo').order_by('yr', 'mo').limit(12).all()

    total_revenue = db.session.query(func.sum(Bill.paid_amount)).scalar() or 0
    total_pending = db.session.query(
        func.sum(Bill.total_amount - Bill.paid_amount)
    ).filter(Bill.status != 'paid').scalar() or 0

    return render_template('admin/report_revenue.html',
                           data=data, period=period,
                           total_revenue=total_revenue,
                           total_pending=total_pending)


@admin_bp.route('/reports/inventory')
@login_required
def report_inventory():
    all_meds = Medicine.query.order_by(Medicine.stock_quantity).all()
    low_stock = [m for m in all_meds if m.is_low_stock()]
    by_category = db.session.query(
        Medicine.category, func.count(), func.sum(Medicine.stock_quantity)
    ).group_by(Medicine.category).all()
    total_value = db.session.query(
        func.sum(Medicine.unit_price * Medicine.stock_quantity)
    ).scalar() or 0

    return render_template('admin/report_inventory.html',
                           all_meds=all_meds, low_stock=low_stock,
                           by_category=by_category, total_value=total_value)


@admin_bp.route('/reports/appointments')
@login_required
def report_appointments():
    by_status = db.session.query(
        Appointment.status, func.count()
    ).group_by(Appointment.status).all()

    by_doctor = db.session.query(
        Doctor.first_name, Doctor.last_name, func.count(Appointment.appointment_id)
    ).join(Appointment).group_by(Doctor.doctor_id, Doctor.first_name, Doctor.last_name).all()

    return render_template('admin/report_appointments.html',
                           by_status=by_status, by_doctor=by_doctor)
