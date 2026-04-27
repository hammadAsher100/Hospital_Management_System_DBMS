from app import db
from datetime import datetime, date


class Patient(db.Model):
    __tablename__ = 'Patients'

    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(100))
    blood_group = db.Column(db.String(5))
    allergies = db.Column(db.Text)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', back_populates='patient', lazy='dynamic')
    admissions = db.relationship('Admission', back_populates='patient', lazy='dynamic')
    bills = db.relationship('Bill', back_populates='patient', lazy='dynamic')
    prescriptions = db.relationship('Prescription', back_populates='patient', lazy='dynamic')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        return today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )

    def __repr__(self):
        return f'<Patient {self.full_name}>'
