from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from flask import send_from_directory
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'peekway-traders-secret-key-2026'

COMPANY_DETAILS = {
    "name": "Peekway Traders & Scraps",
    "short_name": "Peekway",
    "address": "1/274/T, Thrithala, Palakkad - 679534, Kerala",
    "promoter": "Dr. Khalid A",
    "mobile": "+91 90616 95008",
    "landline": "0466 2080083",
    "email": "Peekwaytrd@gmail.com"
}
# Flask-Mail Configuration (Example using Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'peekwaytrd@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('hdcbajmxrpmtoovw')
app.config['MAIL_DEFAULT_SENDER'] = 'peekwaytrd@gmail.com'
mail = Mail(app)
@app.context_processor
def inject_company_info():
    return dict(company=COMPANY_DETAILS)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        service = request.form.get('service', 'General Consultation')
        message_body = request.form.get('message')

        # Send Email Notification
        msg = Message(
            subject=f"New Booking Request: {service.title()} - {first_name} {last_name}",
            recipients=['peekwaytrd@gmail.com'], # Destination email address
            body=f"""
New consultation request received!

Selected Service: {service.title()}
Name: {first_name} {last_name}
Email: {email}

Message:
{message_body}
            """
        )
        
        try:
            mail.send(msg)
            flash(f"Thank you, {first_name}! Your booking request for '{service.title()}' has been submitted successfully.", "success")
        except Exception as e:
            flash("There was an error sending your booking request. Please try again later.", "danger")

        return redirect(url_for('book', service=service))

    # GET Request: Fetch selected service from URL query params (e.g. /book?service=executive)
    selected_service = request.args.get('service', 'discovery')
    return render_template('booking.html', selected_service=selected_service)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        flash(f"Thank you, {first_name}! Your message has been received.", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=9000)