# SalesVision Dashboard 🚀

**SalesVision** is a modern, real-time sales analytics dashboard built with **Flask** and **Vanilla JS**. It visualizes sales data from a SQLite database and features a simulated live activity feed.

![SalesVision Dashboard](https://via.placeholder.com/1200x600.png?text=SalesVision+Dashboard+Preview)
*(Replace with your actual screenshot)*

## ✨ Features

- **Real-Time Activity Feed**: Simulates live sales events (Orders, Payments, Signups) using serverless-friendly on-the-fly generation.
- **Interactive Charts**:
    - Revenue by Region (Bar Chart)
    - Profit by Category (Doughnut Chart)
    - Top 10 Customers (Horizontal Bar Chart)
- **Key Metrics**: Instant view of Total Revenue, Profit, and Average Order Value.
- **Alert System**: Highlights loss-making orders for immediate attention.
- **Premium UI**: "Shadcn" inspired design with a clean light theme, glass-like elements, and responsive layout.

## 🛠️ Tech Stack

- **Backend**: Python (Flask), SQLite
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Visualization**: Chart.js
- **Deployment**: Vercel Ready (Serverless)

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Git

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Abhiii47/SalesVision.git
    cd SalesVision
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Seed the Database**:
    ```bash
    python seed_data.py
    ```
    *This creates `sales.db` with dummy data.*

4.  **Run the Application**:
    ```bash
    python app.py
    ```

5.  **Open in Browser**:
    Visit `http://127.0.0.1:5000`

## ☁️ Deployment (Vercel)

This project is configured for **Vercel** serverless deployment.

1.  Push your code to GitHub.
2.  Import the repository into Vercel.
3.  Vercel will automatically detect `vercel.json` and deploy.

> **Note**: On Vercel, the SQLite database (`sales.db`) is **read-only**. The live activity feed generates mock data dynamically to work around serverless filesystem limitations.

## 📂 Project Structure

```
SalesVision/
├── app.py              # Flask Application (API & Serverless Logic)
├── seed_data.py        # Database Seeding Script
├── sales.db            # SQLite Database (Auto-generated)
├── analysis.sql        # Reference SQL Queries
├── activity.csv        # (Removed in Serverless version)
├── templates/
│   └── index.html      # Dashboard HTML
├── static/
│   ├── style.css       # Premium Styling (Shadcn Theme)
│   └── script.js       # Frontend Logic & Charts
├── requirements.txt    # Python Dependencies
└── vercel.json         # Vercel Configuration
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ by [Abhiii47](https://github.com/Abhiii47)
