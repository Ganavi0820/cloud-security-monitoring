# Cloud Security Monitoring Dashboard

A production-ready web application for scanning and visualizing AWS security misconfigurations. Built with Python, Flask, Boto3, SQLite, and Bootstrap.

## Features
- **AWS Service Scanning**: Checks IAM, S3, and EC2 for common misconfigurations (e.g., missing MFA, public buckets, open security groups).
- **Interactive Dashboard**: Visualizes high, medium, and low severity findings with Chart.js.
- **Historical Tracking**: Stores scan results in SQLite to track security posture over time.
- **Export Reports**: Generate downloadable CSV and PDF reports.
- **Mock Data Mode**: If AWS credentials are not configured, the app seamlessly falls back to generating realistic mock data, making it perfect for portfolio demonstrations and testing.
- **Responsive UI**: Built with Bootstrap 5 using a premium dark-mode aesthetic.

## Prerequisites
- Python 3.8+
- (Optional) AWS Credentials configured via `aws configure` or `~/.aws/credentials`.

## Installation & Setup

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd "cloud security monitoring"
   ```

2. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the Dashboard:**
   Open your browser and navigate to `http://127.0.0.1:5000/`.

## Usage
- Click **"Run Scan"** in the top navigation bar.
- If your machine has active AWS credentials, it will perform a live scan of your AWS account.
- If no credentials are found, it will generate sample mock findings so you can preview the dashboard's capabilities.
- Navigate to the **Findings** tab to view detailed remediation steps.
- Click **Export CSV** or **Export PDF** on the dashboard to download reports.

## Project Structure
- `app.py`: Main Flask application.
- `database/`: SQLite database initialization.
- `scanner/`: Modules for interacting with AWS services via Boto3 (and the mock data generator).
- `utils/`: Report generation utilities (CSV/PDF).
- `templates/`: HTML templates.
- `static/`: Custom CSS and JavaScript.

## License
MIT License
