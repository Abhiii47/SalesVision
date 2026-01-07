document.addEventListener('DOMContentLoaded', () => {
    // Set global Chart.js defaults for Light Theme
    Chart.defaults.color = '#64748b'; // Slate 500
    Chart.defaults.borderColor = '#e2e8f0'; // Slate 200
    Chart.defaults.font.family = "'Outfit', sans-serif";

    fetchData();
});

async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();

        updateMetrics(data);
        renderCharts(data);
        renderTable(data.negative_profit_orders);

        // Start polling activity
        fetchActivity();
        setInterval(fetchActivity, 2000);

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function fetchActivity() {
    try {
        const response = await fetch('/api/activity');
        const activities = await response.json();
        updateActivityFeed(activities);
    } catch (error) {
        console.error('Error fetching activity:', error);
    }
}

function updateActivityFeed(activities) {
    const feed = document.getElementById('activityFeed');
    feed.innerHTML = '';

    activities.forEach(item => {
        const div = document.createElement('div');
        const amountClass = parseFloat(item.amount) > 0 ? 'positive-amount' : (parseFloat(item.amount) < 0 ? 'negative-amount' : '');

        div.className = `activity-item ${amountClass}`;
        // Using toLocaleTimeString for better formatting
        const timeStr = new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

        div.innerHTML = `
            <strong>${item.user} <span style="color: #94a3b8; font-weight: 400;">${item.action}</span></strong>
            <div class="activity-meta">
                <span>${timeStr}</span>
                <span>${item.amount != 0 ? formatCurrency(item.amount) : ''}</span>
            </div>
        `;
        feed.appendChild(div);
    });
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
}

function updateMetrics(data) {
    document.getElementById('totalRevenue').textContent = formatCurrency(data.total_metrics.total_revenue);
    document.getElementById('totalProfit').textContent = formatCurrency(data.total_metrics.total_profit);
    document.getElementById('avgOrderValue').textContent = formatCurrency(data.avg_order_value);
    document.getElementById('lossOrdersCount').textContent = "View List";
}

function renderCharts(data) {
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: '#0f172a', font: { weight: 500 } }, // Darker legend
                position: 'top'
            }
        },
        scales: {
            y: {
                grid: { color: '#e2e8f0', borderDash: [4, 4] },
                ticks: { color: '#64748b' },
                beginAtZero: true
            },
            x: {
                grid: { display: false },
                ticks: { color: '#64748b' }
            }
        }
    };

    // 1. Revenue by Region - Bar Chart
    const regionCtx = document.getElementById('regionChart').getContext('2d');
    new Chart(regionCtx, {
        type: 'bar',
        data: {
            labels: data.revenue_by_region.map(d => d.Region),
            datasets: [{
                label: 'Revenue',
                data: data.revenue_by_region.map(d => d.revenue),
                backgroundColor: '#2563eb', // Blue 600
                borderRadius: 4,
                hoverBackgroundColor: '#1d4ed8'
            }]
        },
        options: commonOptions
    });

    // 2. Profit by Category - Doughnut
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    new Chart(categoryCtx, {
        type: 'doughnut',
        data: {
            labels: data.profit_by_category.map(d => d.Category),
            datasets: [{
                data: data.profit_by_category.map(d => d.profit),
                backgroundColor: ['#10b981', '#f59e0b', '#3b82f6', '#8b5cf6', '#ec4899'], // Emerald, Amber, Blue, Violet, Pink
                borderWidth: 1,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#0f172a', usePointStyle: true }
                }
            }
        }
    });

    // 3. Top Customers - Horizontal Bar
    // FIX: Ensure this renders correctly. Highlighting the container size issues.
    const customerCtx = document.getElementById('customerChart').getContext('2d');
    new Chart(customerCtx, {
        type: 'bar',
        data: {
            labels: data.top_customers.map(d => d.Customer_Name),
            datasets: [{
                label: 'Total Spent',
                data: data.top_customers.map(d => d.total_spent),
                backgroundColor: '#0f172a', // Slate 900 (Dark/Bold for contrast)
                borderRadius: 4
            }]
        },
        options: {
            ...commonOptions,
            indexAxis: 'y', // Horizontal
            scales: {
                x: {
                    grid: { color: '#e2e8f0', borderDash: [4, 4] },
                    ticks: { color: '#64748b' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#0f172a', font: { weight: 500 } } // Darker axis labels for names
                }
            }
        }
    });
}

function renderTable(orders) {
    const tbody = document.getElementById('lossTableBody');
    tbody.innerHTML = '';

    orders.forEach(order => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="font-family: monospace; color: #64748b;">${order.Order_ID}</td>
            <td>${formatCurrency(order.Sales)}</td>
            <td class="loss-val">${formatCurrency(order.Profit)}</td>
        `;
        tbody.appendChild(tr);
    });
}
