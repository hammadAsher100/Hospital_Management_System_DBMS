from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app import db
from app.models.patient import Patient
from app.utils import role_required
from datetime import datetime

patients_bp = Blueprint('patients', __name__)


@patients_bp.route('/')
@login_required
def list_patients():
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)

    query = Patient.query
    if search:
        query = query.filter(
            db.or_(
                Patient.first_name.ilike(f'%{search}%'),
                Patient.last_name.ilike(f'%{search}%'),
                Patient.phone.ilike(f'%{search}%'),
                Patient.email.ilike(f'%{search}%')
            )
        )

    patients = query.order_by(Patient.registration_date.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    return render_template('patients/list.html', patients=patients, search=search)


@patients_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'doctor', 'nurse')
def add_patient():
    if request.method == 'POST':
        try:
            patient = Patient(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                dob=datetime.strptime(request.form['dob'], '%Y-%m-%d').date(),
                gender=request.form['gender'],
                phone=request.form['phone'],
                email=request.form.get('email'),
                address=request.form.get('address'),
                emergency_contact=request.form.get('emergency_contact'),
                blood_group=request.form.get('blood_group'),
                allergies=request.form.get('allergies'),
            )
            db.session.add(patient)
            db.session.commit()
            flash(f'Patient {patient.full_name} registered successfully.', 'success')
            return redirect(url_for('patients.view_patient', id=patient.patient_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error registering patient: {str(e)}', 'danger')

    return render_template('patients/form.html', patient=None, action='Add')


@patients_bp.route('/<int:id>')
@login_required
def view_patient(id):
    patient = Patient.query.get_or_404(id)
    tab = request.args.get('tab', 'info')
    return render_template('patients/view.html', patient=patient, tab=tab)


@patients_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'doctor', 'nurse')
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        try:
            patient.first_name = request.form['first_name']
            patient.last_name = request.form['last_name']
            patient.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
            patient.gender = request.form['gender']
            patient.phone = request.form['phone']
            patient.email = request.form.get('email')
            patient.address = request.form.get('address')
            patient.emergency_contact = request.form.get('emergency_contact')
            patient.blood_group = request.form.get('blood_group')
            patient.allergies = request.form.get('allergies')
            db.session.commit()
            flash('Patient information updated.', 'success')
            return redirect(url_for('patients.view_patient', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating patient: {str(e)}', 'danger')

    return render_template('patients/form.html', patient=patient, action='Edit')


@patients_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    try:
        db.session.delete(patient)
        db.session.commit()
        flash('Patient record deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Cannot delete patient: {str(e)}', 'danger')
    return redirect(url_for('patients.list_patients'))
