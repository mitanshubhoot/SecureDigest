/**
 * Radar Chart Utilities for SecureDaily
 * Provides reusable radar chart components using Chart.js
 */

/**
 * Create a security posture radar chart
 * @param {string} canvasId - ID of the canvas element
 * @param {Object} data - Chart data with labels and values
 */
function createSecurityRadarChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const chartData = {
        labels: data.labels || ['Access Control', 'Data Protection', 'Network Security', 'Incident Response', 'Compliance', 'Security Awareness'],
        datasets: [{
            label: 'Your Score',
            data: data.scores || [0, 0, 0, 0, 0, 0],
            fill: true,
            backgroundColor: 'rgba(15, 76, 129, 0.2)',
            borderColor: 'rgb(15, 76, 129)',
            pointBackgroundColor: 'rgb(15, 76, 129)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(15, 76, 129)'
        }]
    };

    // Add benchmark data if provided
    if (data.benchmark) {
        chartData.datasets.push({
            label: 'Industry Average',
            data: data.benchmark,
            fill: true,
            backgroundColor: 'rgba(100, 100, 100, 0.1)',
            borderColor: 'rgb(150, 150, 150)',
            borderDash: [5, 5],
            pointBackgroundColor: 'rgb(150, 150, 150)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(150, 150, 150)'
        });
    }

    new Chart(ctx, {
        type: 'radar',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    angleLines: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    pointLabels: {
                        color: '#fff',
                        font: {
                            size: 12,
                            family: "'Inter', sans-serif"
                        }
                    },
                    ticks: {
                        display: false,
                        stepSize: 20
                    },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#fff',
                        font: {
                            size: 14,
                            family: "'Inter', sans-serif"
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgb(15, 76, 129)',
                    borderWidth: 1
                }
            }
        }
    });
}

/**
 * Create a tool comparison radar chart
 * @param {string} canvasId - ID of the canvas element
 * @param {Array} tools - Array of tool objects with capabilities
 */
function createToolComparisonChart(canvasId, tools) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const labels = ['Scanning', 'Manual Testing', 'Automation', 'Reporting', 'Ease of Use'];
    const colors = [
        'rgba(15, 76, 129, 0.6)',
        'rgba(34, 197, 94, 0.6)',
        'rgba(251, 146, 60, 0.6)',
        'rgba(168, 85, 247, 0.6)',
        'rgba(236, 72, 153, 0.6)'
    ];

    const datasets = tools.map((tool, index) => ({
        label: tool.name,
        data: [
            tool.capabilities.scanning || 0,
            tool.capabilities.manual_testing || 0,
            tool.capabilities.automation || 0,
            tool.capabilities.reporting || 0,
            tool.capabilities.ease_of_use || 0
        ],
        fill: true,
        backgroundColor: colors[index % colors.length].replace('0.6', '0.2'),
        borderColor: colors[index % colors.length],
        pointBackgroundColor: colors[index % colors.length],
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: colors[index % colors.length]
    }));

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    angleLines: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    pointLabels: {
                        color: '#fff',
                        font: {
                            size: 12,
                            family: "'Inter', sans-serif"
                        }
                    },
                    ticks: {
                        display: false,
                        stepSize: 2
                    },
                    suggestedMin: 0,
                    suggestedMax: 10
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#fff',
                        font: {
                            size: 14,
                            family: "'Inter', sans-serif"
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgb(15, 76, 129)',
                    borderWidth: 1
                }
            }
        }
    });
}

/**
 * Create a threat distribution radar chart
 * @param {string} canvasId - ID of the canvas element
 * @param {Object} data - Threat distribution data
 */
function createThreatDistributionChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: data.labels || ['Web Application', 'Network', 'Authentication', 'Privilege Escalation', 'Code Execution', 'Data Exposure'],
            datasets: [{
                label: 'Threat Count',
                data: data.data || [0, 0, 0, 0, 0, 0],
                fill: true,
                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                borderColor: 'rgb(239, 68, 68)',
                pointBackgroundColor: 'rgb(239, 68, 68)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(239, 68, 68)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    angleLines: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    pointLabels: {
                        color: '#fff',
                        font: {
                            size: 11,
                            family: "'Inter', sans-serif"
                        }
                    },
                    ticks: {
                        display: false
                    },
                    suggestedMin: 0
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgb(239, 68, 68)',
                    borderWidth: 1
                }
            }
        }
    });
}

/**
 * Create a severity distribution doughnut chart
 * @param {string} canvasId - ID of the canvas element
 * @param {Object} data - Severity distribution data
 */
function createSeverityChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels || ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                data: data.data || [0, 0, 0, 0],
                backgroundColor: [
                    'rgba(220, 38, 38, 0.8)',   // Critical - Red
                    'rgba(251, 146, 60, 0.8)',  // High - Orange
                    'rgba(250, 204, 21, 0.8)',  // Medium - Yellow
                    'rgba(34, 197, 94, 0.8)'    // Low - Green
                ],
                borderColor: [
                    'rgb(220, 38, 38)',
                    'rgb(251, 146, 60)',
                    'rgb(250, 204, 21)',
                    'rgb(34, 197, 94)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#fff',
                        font: {
                            size: 12,
                            family: "'Inter', sans-serif"
                        },
                        padding: 15
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgb(15, 76, 129)',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;

                            // Calculate percentage client-side based on the actual rendered data
                            const dataset = context.dataset;
                            const total = dataset.data.reduce((acc, current) => acc + Number(current), 0);
                            const percentage = total > 0 ? Math.round((value / total) * 100) : 0;

                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create a timeline chart for CVE trends
 * @param {string} canvasId - ID of the canvas element
 * @param {Object} data - Timeline data
 */
function createTimelineChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: [{
                label: 'CVEs Published',
                data: data.data || [],
                fill: true,
                backgroundColor: 'rgba(15, 76, 129, 0.2)',
                borderColor: 'rgb(15, 76, 129)',
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#fff',
                        font: {
                            size: 14,
                            family: "'Inter', sans-serif"
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgb(15, 76, 129)',
                    borderWidth: 1
                }
            }
        }
    });
}
