# 📈 Mutual Fund Analytics Platform

<div align="center">

### 🚀 End-to-End Financial Analytics Platform with Data Engineering, Portfolio Optimization & Automated Reporting

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-black?logo=github)
![Status](https://img.shields.io/badge/Project-Completed-success)

</div>

---

# 📌 Project Overview

The **Mutual Fund Analytics Platform** is a comprehensive financial analytics solution developed during the **Bluestock Data Analytics Internship**.

The platform demonstrates an end-to-end data analytics workflow—from data extraction and ETL to interactive dashboard visualization, portfolio optimization, and automated reporting.

The objective of this project is to simplify mutual fund analysis by providing investors with meaningful insights through interactive dashboards and intelligent portfolio recommendations.

---

# ✨ Key Features

- 📥 ETL Pipeline using Python
- 🧹 Data Cleaning & Validation
- 🗄 SQLite Relational Database
- 📊 Interactive Streamlit Dashboard
- 📈 Plotly Visualizations
- 📉 Mutual Fund Performance Analytics
- 💼 Portfolio Optimizer
- 🎲 Monte Carlo Simulation
- 📄 Weekly HTML Report Generation
- 📧 Gmail SMTP Email Automation
- ⏰ Windows Task Scheduler Automation
- 📚 SQL Schema & Data Dictionary
- 💻 GitHub Version Control

---

# 🏗 System Architecture

```text
                 Mutual Fund Data
                         │
                         ▼
                  Python ETL Pipeline
                         │
                         ▼
                  SQLite Database
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 Dashboard         Portfolio Optimizer   Reports
(Streamlit)      (Monte Carlo Model)    (HTML)
        │                                 │
        └───────────────┬─────────────────┘
                        ▼
                 Gmail SMTP Service
                        ▼
              Weekly Email Delivery
                        ▼
          Windows Task Scheduler
```

---

# 🗂 Project Structure

```text
MutualFundAnalytics/
│
├── dashboard/
│   ├── app.py
│   ├── portfolio_optimizer.py
│   ├── monte_carlo.py
│   ├── email_report.py
│
├── data/
│
├── db/
│
├── notebooks/
│
├── reports/
│   └── weekly_report.html
│
├── scripts/
│
├── sql/
│
├── docs/
│   ├── Final_Report.pdf
│   ├── Final_Report.docx
│   └── Presentation.pptx
│
├── README.md
├── requirements.txt
├── data_dictionary.md
└── .gitignore
```

---

# 🛠 Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Programming |
| Pandas | Data Cleaning & ETL |
| NumPy | Numerical Computation |
| SQLite | Database Management |
| Streamlit | Dashboard Development |
| Plotly | Interactive Charts |
| HTML & CSS | Report Generation |
| SMTP | Email Automation |
| Windows Task Scheduler | Scheduled Execution |
| Git & GitHub | Version Control |

---

# 📊 Dashboard Modules

### 📌 Industry Overview
- Mutual Fund Statistics
- NAV Summary
- Industry Insights

### 📌 Fund Performance
- Top Performing Funds
- Return Comparison
- Historical NAV Analysis

### 📌 Portfolio Optimizer
- Monte Carlo Simulation
- Efficient Frontier
- Optimal Asset Allocation
- Sharpe Ratio

### 📌 Weekly Reports
- Automated HTML Reports
- Professional Email Format

---

# 🎯 Portfolio Optimization

The project implements **Monte Carlo Simulation** to generate thousands of random portfolio combinations and identify the optimal allocation based on the **Sharpe Ratio**.

The optimizer provides:

- Expected Return
- Portfolio Risk
- Sharpe Ratio
- Efficient Frontier
- Recommended Fund Allocation

---

# 📧 Automated Reporting

The platform automatically:

- Generates Weekly HTML Reports
- Sends Reports using Gmail SMTP
- Schedules Execution using Windows Task Scheduler

This eliminates manual reporting and ensures timely updates.

---

## 📧 Email Configuration

To enable the automated email reporting feature, follow these steps:

### Step 1: Enable 2-Step Verification
Enable Two-Factor Authentication (2FA) on your Google account.

### Step 2: Generate a Gmail App Password
Generate a 16-character Gmail App Password from your Google Account.

### Step 3: Open the Email Configuration File

Navigate to:

```text
dashboard/email_report.py
```

### Step 4: Update Your Email Credentials

Replace the placeholder values with your own Gmail account details:

```python
sender_email = "your_sender_email@gmail.com"
sender_password = "your_16_character_app_password"
receiver_email = "receiver_email@gmail.com"
```

### Step 5: Save the File

Save the changes and run the application.

> **Note:** Never upload your real email address or App Password to GitHub. Always keep your credentials private.

### 🔗 Generate a Gmail App Password

If you don't already have an App Password, generate one from your Google Account:

https://myaccount.google.com/apppasswords

> **Security Notice:**  
> This project uses placeholder email credentials for security reasons. Before running the email automation module, replace them with your own Gmail address, App Password, and receiver email. Never commit or publish your actual credentials to a public repository.


# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/NeonLakshay/MutualFundAnalytics.git
```

Move into the project directory:

```bash
cd MutualFundAnalytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

---

# 📸 Dashboard Preview

> *(Replace these placeholders with your actual screenshots.)*

- 🏠 Dashboard Home
- 📈 Industry Overview
- 💼 Portfolio Optimizer
- 📊 Fund Performance
- 📧 Weekly Email Report

---

# 📚 Documentation

The complete project documentation is available in the **docs/** folder.

- 📄 Final Project Report (PDF)
- 📝 Final Project Report (DOCX)
- 📊 Project Presentation (PPTX)

---

# 🔮 Future Scope

- Live Mutual Fund API Integration
- AI-Based Investment Recommendation
- Cloud Deployment
- User Authentication
- Mobile Application
- Advanced Risk Analytics
- Real-Time Portfolio Tracking

---

# 👨‍💻 Author

## Lakshay Singh Negi

**B.Tech Computer Science Engineering (Artificial Intelligence & Machine Learning)**

Dronacharya College of Engineering

### Connect with me

- GitHub: https://github.com/NeonLakshay
- LinkedIn: *(Add your LinkedIn URL here)*

---

# ⭐ If you found this project useful, consider giving it a Star!
