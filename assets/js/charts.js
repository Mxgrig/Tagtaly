// Tagtaly ECharts-based Chart Renderers with Dual-Chart Hover
// Modern, polished charts with smooth animations and professional styling

const chartInstances = {};

// Ensure ECharts is loaded
if (typeof echarts === 'undefined') {
    console.error('ERROR: ECharts library not loaded. Charts will not render.');
}

// Color palette matching Tagtaly brand
const COLORS = {
    primary: '#3b82f6',
    secondary: '#1e293b',
    success: '#10b981',
    danger: '#ef4444',
    warning: '#f59e0b',
    purple: '#8b5cf6',
    cyan: '#06b6d4',
    pink: '#ec4899',
    lime: '#84cc16',
    indigo: '#6366f1',
    teal: '#14b8a6',
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

// Text styling for charts
const TEXT_STYLE = {
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    fontSize: 12,
    fontWeight: 500,
    color: COLORS.neutral[600]
};

// ============================================
// CHART 1: SENTIMENT TRACKER (Line Chart)
// ============================================
async function renderSentimentChart() {
    try {
        const response = await fetch('assets/data/sentiment_tracker.json', { cache: 'no-store' });
        const data = await response.json();

        const ctx = document.getElementById('sentiment-tracker-chart');
        if (!ctx) return;

        // Convert canvas to div for ECharts
        const container = ctx.parentElement;
        container.innerHTML = '<div id="sentiment-chart-echarts" style="width:100%; height:400px;"></div>';
        const echartsDiv = document.getElementById('sentiment-chart-echarts');

        const dates = data.dates || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        const scores = data.mood_scores || [42.5, 38.2, 45.8, 52.3, 48.9, 55.2, 50.1];

        const chart = echarts.init(echartsDiv);
        chartInstances['sentiment'] = chart;

        const primaryOption = {
            tooltip: {
                trigger: 'axis',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                borderColor: '#fff',
                textStyle: { color: '#fff', fontSize: 13, fontWeight: 500 }
            },
            grid: { left: '5%', right: '5%', bottom: '10%', top: '15%', containLabel: true },
            xAxis: {
                type: 'category',
                data: dates,
                axisLine: { lineStyle: { color: COLORS.neutral[200] } },
                axisLabel: { ...TEXT_STYLE, color: COLORS.neutral[500] },
                splitLine: { show: false }
            },
            yAxis: {
                type: 'value',
                name: 'Mood Score',
                min: 0,
                max: 100,
                axisLine: { show: false },
                axisLabel: { ...TEXT_STYLE, color: COLORS.neutral[500] },
                splitLine: { lineStyle: { color: COLORS.neutral[100], type: 'dashed' } }
            },
            series: [{
                name: 'Mood Score',
                type: 'line',
                data: scores,
                smooth: true,
                symbol: 'circle',
                symbolSize: 8,
                itemStyle: { color: COLORS.purple, borderWidth: 2, borderColor: '#fff' },
                lineStyle: { color: COLORS.purple, width: 3 },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(139, 92, 246, 0.3)' },
                        { offset: 1, color: 'rgba(139, 92, 246, 0.01)' }
                    ])
                },
                emphasis: { itemStyle: { borderWidth: 3 } }
            }]
        };

        const alternateOption = {
            ...primaryOption,
            series: [{
                ...primaryOption.series[0],
                name: '7-Day Average',
                itemStyle: { color: COLORS.cyan, borderWidth: 2, borderColor: '#fff' },
                lineStyle: { color: COLORS.cyan, width: 3 },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(6, 182, 212, 0.3)' },
                        { offset: 1, color: 'rgba(6, 182, 212, 0.01)' }
                    ])
                }
            }]
        };

        chart.setOption(primaryOption);
        setupDualChartHover('sentiment-tracker-chart', chart, primaryOption, alternateOption);
        window.addEventListener('resize', () => chart.resize());

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

        const container = ctx.parentElement;
        container.innerHTML = '<div id="surges-chart-echarts" style="width:100%; height:400px;"></div>';
        const echartsDiv = document.getElementById('surges-chart-echarts');

        const surges = data.surges || [];
        const topics = surges.map(s => s.topic);
        const changes = surges.map(s => s.change_pct);
        const colors = changes.map(v => v > 0 ? COLORS.success : COLORS.danger);

        const chart = echarts.init(echartsDiv);
        chartInstances['surges'] = chart;

        const primaryOption = {
            tooltip: {
                trigger: 'axis',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                textStyle: { color: '#fff' },
                formatter: (params) => {
                    if (params.length > 0) {
                        const value = params[0].value;
                        return `${params[0].name}<br/><strong>${value > 0 ? '+' : ''}${value.toFixed(1)}%</strong>`;
                    }
                    return '';
                }
            },
            grid: { left: '5%', right: '10%', bottom: '5%', top: '10%', containLabel: true },
            xAxis: {
                type: 'value',
                axisLine: { show: false },
                axisLabel: { ...TEXT_STYLE, color: COLORS.neutral[500], formatter: '{value}%' },
                splitLine: { lineStyle: { color: COLORS.neutral[100], type: 'dashed' } }
            },
            yAxis: {
                type: 'category',
                data: topics,
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: { ...TEXT_STYLE, fontWeight: 600, color: COLORS.neutral[700] }
            },
            series: [{
                name: 'Change %',
                type: 'bar',
                data: changes.map((v, i) => ({ value: v, itemStyle: { color: colors[i] } })),
                itemStyle: { borderRadius: [0, 6, 6, 0] },
                label: { show: true, position: 'right', formatter: '{c}%', fontWeight: 'bold' }
            }]
        };

        const alternateOption = {
            ...primaryOption,
            series: [{
                ...primaryOption.series[0],
                name: 'Yesterday vs Today',
                type: 'bar',
                label: { show: true, position: 'right', formatter: (params) => {
                    const idx = topics.indexOf(params.name);
                    return surges[idx] ? `${surges[idx].today} articles` : '';
                }, fontWeight: 'bold' }
            }]
        };

        chart.setOption(primaryOption);
        setupDualChartHover('topic-surges-chart', chart, primaryOption, alternateOption);
        window.addEventListener('resize', () => chart.resize());

    } catch (error) {
        console.error('Error rendering surges chart:', error);
    }
}

// ============================================
// CHART 3: CATEGORY DOMINANCE (Doughnut)
// ============================================
async function renderCategoryChart() {
    try {
        const response = await fetch('assets/data/category_dominance.json', { cache: 'no-store' });
        const data = await response.json();

        const ctx = document.getElementById('category-dominance-chart');
        if (!ctx) return;

        const container = ctx.parentElement;
        container.innerHTML = '<div id="category-chart-echarts" style="width:100%; height:400px;"></div>';
        const echartsDiv = document.getElementById('category-chart-echarts');

        const categories = data.categories || [
            { name: 'Tech', count: 234 },
            { name: 'Business', count: 187 },
            { name: 'Entertainment', count: 156 }
        ];

        const categoryColors = [
            COLORS.primary, COLORS.success, COLORS.warning,
            COLORS.danger, COLORS.purple, COLORS.cyan
        ];

        const chart = echarts.init(echartsDiv);
        chartInstances['categories'] = chart;

        const seriesData = categories.map((c, i) => ({
            value: c.count || c.articles,
            name: c.name || c.category,
            itemStyle: { color: categoryColors[i % categoryColors.length] }
        }));

        const primaryOption = {
            tooltip: {
                trigger: 'item',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                formatter: (params) => {
                    if (params.value) {
                        const total = seriesData.reduce((a, b) => a + b.value, 0);
                        const pct = ((params.value / total) * 100).toFixed(1);
                        return `${params.name}<br/><strong>${params.value}</strong> (${pct}%)`;
                    }
                    return '';
                }
            },
            legend: { bottom: 10, textStyle: { ...TEXT_STYLE, color: COLORS.neutral[700] } },
            series: [{
                name: 'Articles',
                type: 'pie',
                radius: ['40%', '70%'],
                data: seriesData,
                emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
            }]
        };

        const alternateOption = {
            ...primaryOption,
            series: [{
                ...primaryOption.series[0],
                radius: ['30%', '80%']
            }]
        };

        chart.setOption(primaryOption);
        setupDualChartHover('category-dominance-chart', chart, primaryOption, alternateOption);
        window.addEventListener('resize', () => chart.resize());

    } catch (error) {
        console.error('Error rendering category chart:', error);
    }
}

// ============================================
// CHART 4: SOURCE PRODUCTIVITY (Bar)
// ============================================
async function renderSourceChart() {
    try {
        const response = await fetch('assets/data/source_productivity.json', { cache: 'no-store' });
        const data = await response.json();

        const ctx = document.getElementById('source-productivity-chart');
        if (!ctx) return;

        const container = ctx.parentElement;
        container.innerHTML = '<div id="source-chart-echarts" style="width:100%; height:400px;"></div>';
        const echartsDiv = document.getElementById('source-chart-echarts');

        const sources = data.sources || [
            { source: 'BBC', articles: 87 },
            { source: 'Guardian', articles: 73 }
        ];

        const chart = echarts.init(echartsDiv);
        chartInstances['sources'] = chart;

        const primaryOption = {
            tooltip: {
                trigger: 'axis',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                formatter: (params) => {
                    if (params.length) {
                        return `${params[0].name}<br/><strong>${params[0].value} articles</strong>`;
                    }
                    return '';
                }
            },
            grid: { left: '5%', right: '5%', bottom: '10%', top: '10%', containLabel: true },
            xAxis: {
                type: 'category',
                data: sources.map(s => s.source),
                axisLine: { lineStyle: { color: COLORS.neutral[200] } },
                axisLabel: { ...TEXT_STYLE, color: COLORS.neutral[600] }
            },
            yAxis: {
                type: 'value',
                axisLine: { show: false },
                axisLabel: { ...TEXT_STYLE, color: COLORS.neutral[500] },
                splitLine: { lineStyle: { color: COLORS.neutral[100], type: 'dashed' } }
            },
            series: [{
                name: 'Articles',
                type: 'bar',
                data: sources.map(s => ({ value: s.articles, itemStyle: { color: COLORS.primary } })),
                itemStyle: { borderRadius: [6, 6, 0, 0] },
                label: { show: true, position: 'top', fontWeight: 'bold' }
            }]
        };

        const alternateOption = {
            ...primaryOption,
            series: [{
                ...primaryOption.series[0],
                itemStyle: { color: COLORS.cyan, borderRadius: [6, 6, 0, 0] }
            }]
        };

        chart.setOption(primaryOption);
        setupDualChartHover('source-productivity-chart', chart, primaryOption, alternateOption);
        window.addEventListener('resize', () => chart.resize());

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

        const container = ctx.parentElement;
        container.innerHTML = '<div id="outlet-chart-echarts" style="width:100%; height:400px;"></div>';
        const echartsDiv = document.getElementById('outlet-chart-echarts');

        const outlets = data.outlets || [
            { outlet: 'BBC', sentiment: 0.32 },
            { outlet: 'Guardian', sentiment: 0.28 }
        ];

        const chart = echarts.init(echartsDiv);
        chartInstances['outlets'] = chart;

        const primaryOption = {
            tooltip: {
                trigger: 'axis',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                formatter: (params) => {
                    if (params.length) {
                        const v = params[0].value;
                        return `${params[0].name}<br/><strong>${v > 0 ? '+' : ''}${v.toFixed(2)}</strong>`;
                    }
                    return '';
                }
            },
            grid: { left: '5%', right: '5%', bottom: '10%', top: '10%', containLabel: true },
            xAxis: {
                type: 'category',
                data: outlets.map(o => o.outlet),
                axisLine: { lineStyle: { color: COLORS.neutral[200] } },
                axisLabel: { ...TEXT_STYLE, color: COLORS.neutral[600] }
            },
            yAxis: {
                type: 'value',
                axisLine: { show: false },
                axisLabel: { ...TEXT_STYLE, color: COLORS.neutral[500], formatter: (v) => (v > 0 ? '+' : '') + v.toFixed(1) },
                splitLine: { lineStyle: { color: COLORS.neutral[100], type: 'dashed' } }
            },
            series: [{
                name: 'Sentiment Score',
                type: 'bar',
                data: outlets.map((o, i) => ({
                    value: o.sentiment,
                    itemStyle: { color: o.sentiment > 0 ? COLORS.success : COLORS.danger }
                })),
                itemStyle: { borderRadius: [6, 6, 0, 0] },
                label: { show: true, position: 'top', fontWeight: 'bold' }
            }]
        };

        const alternateOption = {
            ...primaryOption,
            series: [{
                ...primaryOption.series[0],
                name: 'Media Bias',
                label: { show: true, position: 'top', formatter: (params) => outlets[params.dataIndex].outlet }
            }]
        };

        chart.setOption(primaryOption);
        setupDualChartHover('outlet-sentiment-chart', chart, primaryOption, alternateOption);
        window.addEventListener('resize', () => chart.resize());

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

        const container = ctx.parentElement;
        container.innerHTML = '<div id="rhythm-chart-echarts" style="width:100%; height:400px;"></div>';
        const echartsDiv = document.getElementById('rhythm-chart-echarts');

        const rhythm = data.hourly || [];
        const hours = rhythm.map((_, i) => i + ':00');
        const articles = rhythm.map(h => h.articles || 0);

        const chart = echarts.init(echartsDiv);
        chartInstances['rhythm'] = chart;

        const primaryOption = {
            tooltip: {
                trigger: 'axis',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                formatter: (params) => {
                    if (params.length) {
                        return `${params[0].name}<br/><strong>${params[0].value} articles</strong>`;
                    }
                    return '';
                }
            },
            grid: { left: '5%', right: '5%', bottom: '10%', top: '10%', containLabel: true },
            xAxis: {
                type: 'category',
                data: hours,
                axisLine: { lineStyle: { color: COLORS.neutral[200] } },
                axisLabel: { ...TEXT_STYLE, color: COLORS.neutral[500], rotate: 45 }
            },
            yAxis: {
                type: 'value',
                axisLine: { show: false },
                axisLabel: { ...TEXT_STYLE, color: COLORS.neutral[500] },
                splitLine: { lineStyle: { color: COLORS.neutral[100], type: 'dashed' } }
            },
            series: [{
                name: 'Articles Published',
                type: 'line',
                data: articles,
                smooth: true,
                symbol: 'circle',
                symbolSize: 6,
                itemStyle: { color: COLORS.primary, borderWidth: 2, borderColor: '#fff' },
                lineStyle: { color: COLORS.primary, width: 2.5 },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
                        { offset: 1, color: 'rgba(59, 130, 246, 0.01)' }
                    ])
                }
            }]
        };

        const alternateOption = {
            ...primaryOption,
            series: [{
                ...primaryOption.series[0],
                name: 'Peak Hours',
                itemStyle: { color: COLORS.warning, borderWidth: 2, borderColor: '#fff' },
                lineStyle: { color: COLORS.warning, width: 2.5 },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(245, 158, 11, 0.3)' },
                        { offset: 1, color: 'rgba(245, 158, 11, 0.01)' }
                    ])
                }
            }]
        };

        chart.setOption(primaryOption);
        setupDualChartHover('publishing-rhythm-chart', chart, primaryOption, alternateOption);
        window.addEventListener('resize', () => chart.resize());

    } catch (error) {
        console.error('Error rendering rhythm chart:', error);
    }
}

// ============================================
// DUAL-CHART HOVER FUNCTIONALITY
// ============================================
function setupDualChartHover(containerId, chartInstance, primaryOption, alternateOption) {
    const container = document.getElementById(containerId)?.parentElement;
    if (!container) return;

    const card = container.closest('.chart-card');
    if (!card) return;

    let isPrimary = true;
    let hoverTimeout;

    card.addEventListener('mouseenter', () => {
        hoverTimeout = setTimeout(() => {
            if (isPrimary) {
                isPrimary = false;
                chartInstance.setOption(alternateOption, true);
            }
        }, 200);
    });

    card.addEventListener('mouseleave', () => {
        clearTimeout(hoverTimeout);
        if (!isPrimary) {
            isPrimary = true;
            chartInstance.setOption(primaryOption, true);
        }
    });
}

// ============================================
// INITIALIZE ALL CHARTS
// ============================================
function initializeCharts() {
    if (typeof echarts === 'undefined') {
        console.error('ECharts not loaded. Please ensure echarts.min.js is loaded before this script.');
        return;
    }

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
