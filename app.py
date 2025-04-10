from flask import Flask, render_template, request, send_file, redirect, url_for, session
import os
import shutil
import subprocess
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Input_Images'
app.secret_key = os.environ.get('SECRET_KEY')

# Gmail SMTP credentials (replace these with your real Gmail credentials)
GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_PASS = os.environ.get('GMAIL_PASS')  # Use an App Password, not your actual Gmail password

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_images():
    try:
        input_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(input_folder, exist_ok=True)

        files = request.files.getlist('images')
        if not files or all(file.filename == '' for file in files):
            return "No files uploaded."

        for file in files:
            if file.filename:
                file.save(os.path.join(input_folder, file.filename))

        subprocess.run(["python", "Master_Script.py", input_folder], check=True)

        pdf_path = "Quality-Report.pdf"
        if not os.path.exists(pdf_path):
            raise FileNotFoundError("PDF report not generated.")

        static_pdf_path = os.path.join("static", "Quality-Report.pdf")
        shutil.move(pdf_path, static_pdf_path)

        emails_input = request.form.get("emails", "").strip()
        if emails_input:
            session['emails'] = emails_input
            send_email_with_report(emails_input)

        return redirect(url_for('result'))

    except Exception as e:
        return f"Error during processing: {str(e)}"

@app.route('/result')
def result():
    return render_template("result.html")

@app.route('/download')
def download_pdf():
    pdf_path = os.path.join("static", "Quality-Report.pdf")
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name="Quality-Report.pdf")
    return "PDF not found", 404

def send_email_with_report(emails_input):
    recipients = [email.strip() for email in emails_input.split(',') if email.strip()]
    pdf_path = "static/Quality-Report.pdf"

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()


    try:
        msg = EmailMessage()
        msg['Subject'] = 'Your PDF Report is Ready!'
        msg['From'] = GMAIL_USER
        msg['To'] = ', '.join(recipients)
        msg.set_content("Hello,\n\nYour report is ready. Please find the PDF attached.\n\nRegards,\nImage Processing System")
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='Quality-Report.pdf')

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)

        print(f"✅ Email sent to {', '.join(recipients)}")
    except Exception as e:
        print(f"❌ Failed to send email to : {e}")

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
