// Chart.js Configuration for Tagtaly Dashboard
// Renders all charts using Chart.js library with data from JSON files

const chartInstances = {};

// Global Chart.js options
Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
Chart.defaults.plugins.legend.display = true;
Chart.defaults.plugins.legend.position = 'bottom';

// Color palette
const colors = {
    primary: '#3b82f6',
    secondary: '#1e293b',
    success: '#10b981',
    danger: '#ef4444',
    warning: '#f59e0b',
    neutral: {
        50: '#f9fafb',
        100: '#f3f4f6',
        200: '#e5e7eb',
        300: '#d1d5db',
        400: '#9ca3af',
        500: '#6b7280',
        600: '#4b5563',
        700: '#374151',
        800: '#1f2937',
        900: '#111827'
    }
};

// ============================================
// CHART 1: NEWS MOOD (Sentiment Tracker)
// ============================================
async function renderSentimentChart() {
    try {
        // Load sentiment data
        const response = await fetch('assets/data/sentiment_tracker.json', { cache: 'no-store' });
        const data = await response.json();

        const ctx = document.getElementById('sentiment-tracker-chart');
        if (!ctx) return;

        // Parse dates and scores
        const dates = data.dates || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        const scores = data.mood_scores || [42.5, 38.2, 45.8, 52.3, 48.9, 55.2, 50.1];

        // Create gradient
        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(139, 92, 246, 0.2)');
        gradient.addColorStop(1, 'rgba(139, 92, 246, 0)');

        chartInstances['sentiment'] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Mood Score',
                    data: scores,
                    borderColor: '#8b5cf6',
                    backgroundColor: gradient,
                    borderWidth: 3,
                    fill: true,
                    pointRadius: 6,
                    pointBackgroundColor: '#8b5cf6',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' }
                        },
                        grid: {
                            color: colors.neutral[200],
                            drawBorder: false
                        }
                    },
                    x: {
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' }
                        },
                        grid: {
                            display: false,
                            drawBorder: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering sentiment chart:', error);
    }
}

// ============================================
// CHART 2: TOPIC SURGES (Bar Chart)
// ============================================
async function renderSurgesChart() {
    try {
        const response = await fetch('assets/data/topic_surges.json', { cache: 'no-store' });
        const data = await response.json();

        const ctx = document.getElementById('topic-surges-chart');
        if (!ctx) return;

        const surges = data.surges || [];
        const labels = surges.map(s => s.topic);
        const changes = surges.map(s => s.change_pct);

        chartInstances['surges'] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Change %',
                    data: changes,
                    backgroundColor: changes.map(v => v > 0 ? colors.success : colors.danger),
                    borderRadius: 6,
                    borderSkipped: false
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        callbacks: {
                            label: function(context) {
                                return context.parsed.x.toFixed(1) + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' },
                            callback: function(value) {
                                return value + '%';
                            }
                        },
                        grid: {
                            color: colors.neutral[200],
                            drawBorder: false
                        }
                    },
                    y: {
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' }
                        },
                        grid: {
                            display: false,
                            drawBorder: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering surges chart:', error);
    }
}

// ============================================
// CHART 3: STORY CATEGORIES
// ============================================
async function renderCategoryChart() {
    try {
        const response = await fetch('assets/data/category_dominance.json', { cache: 'no-store' });
        const data = await response.json();

        const ctx = document.getElementById('category-dominance-chart');
        if (!ctx) return;

        const categories = data.categories || [
            { name: 'Tech', count: 234 },
            { name: 'Business', count: 187 },
            { name: 'Entertainment', count: 156 },
            { name: 'Health', count: 142 },
            { name: 'Politics', count: 131 }
        ];

        const categoryColors = [
            '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
            '#06b6d4', '#ec4899', '#84cc16', '#6366f1', '#14b8a6'
        ];

        chartInstances['categories'] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: categories.map(c => c.name || c.category),
                datasets: [{
                    data: categories.map(c => c.count || c.articles),
                    backgroundColor: categoryColors.slice(0, categories.length),
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: colors.neutral[700],
                            font: { weight: '600', size: 12 },
                            padding: 15
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return label + ': ' + value + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering category chart:', error);
    }
}

// ============================================
// CHART 4: SOURCE PRODUCTIVITY
// ============================================
async function renderSourceChart() {
    try {
        const response = await fetch('assets/data/source_productivity.json', { cache: 'no-store' });
        const data = await response.json();

        const ctx = document.getElementById('source-productivity-chart');
        if (!ctx) return;

        const sources = data.sources || [
            { source: 'BBC', articles: 87 },
            { source: 'Guardian', articles: 73 },
            { source: 'Sky News', articles: 65 },
            { source: 'Independent', articles: 54 },
            { source: 'Telegraph', articles: 48 }
        ];

        chartInstances['sources'] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sources.map(s => s.source),
                datasets: [{
                    label: 'Articles Published',
                    data: sources.map(s => s.articles),
                    backgroundColor: colors.primary,
                    borderRadius: 6,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' }
                        },
                        grid: {
                            color: colors.neutral[200],
                            drawBorder: false
                        }
                    },
                    x: {
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' }
                        },
                        grid: {
                            display: false,
                            drawBorder: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering source chart:', error);
    }
}

// ============================================
// CHART 5: OUTLET SENTIMENT
// ============================================
async function renderOutletChart() {
    try {
        const response = await fetch('assets/data/outlet_sentiment.json', { cache: 'no-store' });
        const data = await response.json();

        const ctx = document.getElementById('outlet-sentiment-chart');
        if (!ctx) return;

        const outlets = data.outlets || [
            { outlet: 'BBC', sentiment: 0.32 },
            { outlet: 'Guardian', sentiment: 0.28 },
            { outlet: 'Sky News', sentiment: 0.18 },
            { outlet: 'Independent', sentiment: 0.15 },
            { outlet: 'Telegraph', sentiment: -0.12 }
        ];

        chartInstances['outlets'] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: outlets.map(o => o.outlet),
                datasets: [{
                    label: 'Sentiment Score',
                    data: outlets.map(o => o.sentiment),
                    backgroundColor: outlets.map(o => o.sentiment > 0 ? colors.success : colors.danger),
                    borderRadius: 6,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        callbacks: {
                            label: function(context) {
                                const value = context.parsed.y;
                                return (value > 0 ? '+' : '') + value.toFixed(2);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' },
                            callback: function(value) {
                                return (value > 0 ? '+' : '') + value.toFixed(2);
                            }
                        },
                        grid: {
                            color: colors.neutral[200],
                            drawBorder: false
                        }
                    },
                    x: {
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' }
                        },
                        grid: {
                            display: false,
                            drawBorder: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering outlet chart:', error);
    }
}

// ============================================
// CHART 6: PUBLISHING RHYTHM
// ============================================
async function renderRhythmChart() {
    try {
        const response = await fetch('assets/data/publishing_rhythm.json', { cache: 'no-store' });
        const data = await response.json();

        const ctx = document.getElementById('publishing-rhythm-chart');
        if (!ctx) return;

        const rhythm = data.hourly || [];
        const hours = rhythm.map((_, i) => i + ':00');
        const articles = rhythm.map(h => h.articles || 0);

        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(59, 130, 246, 0.2)');
        gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');

        chartInstances['rhythm'] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Articles Published',
                    data: articles,
                    borderColor: colors.primary,
                    backgroundColor: gradient,
                    borderWidth: 3,
                    fill: true,
                    pointRadius: 4,
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' }
                        },
                        grid: {
                            color: colors.neutral[200],
                            drawBorder: false
                        }
                    },
                    x: {
                        ticks: {
                            color: colors.neutral[500],
                            font: { weight: '600' }
                        },
                        grid: {
                            display: false,
                            drawBorder: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering rhythm chart:', error);
    }
}

// ============================================
// INITIALIZE ALL CHARTS
// ============================================
function initializeCharts() {
    renderSentimentChart();
    renderSurgesChart();
    renderCategoryChart();
    renderSourceChart();
    renderOutletChart();
    renderRhythmChart();
}

// Run on document ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCharts);
} else {
    initializeCharts();
}
