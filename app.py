from flask import Flask, render_template, request, jsonify, send_file
import os

from database.db import init_db, save_scan_results, get_latest_findings, get_historical_summary
from scanner.aws_auth import get_boto3_session
from scanner.iam_scanner import scan_iam
from scanner.s3_scanner import scan_s3
from scanner.ec2_scanner import scan_ec2
from scanner.mock_data import generate_mock_findings
from utils.report_gen import generate_csv_report, generate_pdf_report

app = Flask(__name__)

# Initialize database
init_db()

@app.route('/')
def dashboard():
    history = get_historical_summary()
    latest_findings = get_latest_findings()
    
    # Calculate current severity counts
    severity_counts = {'High': 0, 'Medium': 0, 'Low': 0}
    for f in latest_findings:
        sev = f.get('severity', 'Low')
        if sev in severity_counts:
            severity_counts[sev] += 1
            
    return render_template('dashboard.html', history=history, severity_counts=severity_counts)

@app.route('/findings')
def findings():
    latest_findings = get_latest_findings()
    return render_template('findings.html', findings=latest_findings)

@app.route('/api/scan', methods=['POST'])
def trigger_scan():
    session = get_boto3_session()
    all_findings = []
    
    if session:
        print("AWS session established. Running live scan...")
        all_findings.extend(scan_iam(session))
        all_findings.extend(scan_s3(session))
        all_findings.extend(scan_ec2(session))
    else:
        print("No AWS session. Falling back to mock data...")
        all_findings = generate_mock_findings()
        
    scan_id = save_scan_results(all_findings)
    
    return jsonify({
        'status': 'success',
        'message': 'Scan completed successfully',
        'scan_id': scan_id,
        'findings_count': len(all_findings),
        'is_mock': session is None
    })

@app.route('/download/csv')
def download_csv():
    findings = get_latest_findings()
    filepath = generate_csv_report(findings)
    if filepath and os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name='security_report.csv')
    return "Error generating CSV", 500

@app.route('/download/pdf')
def download_pdf():
    findings = get_latest_findings()
    filepath = generate_pdf_report(findings)
    if filepath and os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name='security_report.pdf')
    return "Error generating PDF", 500

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
