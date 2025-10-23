document.addEventListener('DOMContentLoaded', () => {
    // Initialize all 5 charts with dual-chart hover support
    initEmotionalRollercoaster();
    initWeeklyWinner();
    initSurgeAlert();
    initMediaDivide();
    initSentimentShowdown();
});

const ECHART_TEXT_STYLE = {
    fontFamily: 'Inter, sans-serif',
    fontWeight: 600,
    color: 'hsl(0 0% 45.1%)'
};

// Mock data fallbacks when actual data is not available
const MOCK_DATA = {
    emotional: {
        headline: "📊 Emotional Rollercoaster - Sentiment Trend",
        dates: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        scores: [42.5, 38.2, 45.8, 52.3, 48.9]
    },
    surge: {
        headline: "🚨 Topic Surge Alert",
        data: [
            ['Technology', 67.5],
            ['Health', 45.2],
            ['Politics', 38.8],
            ['Climate', 22.3],
            ['Entertainment', 18.5]
        ]
    },
    mediaDivide: {
        headline: "📰 Media Divide - Outlet Sentiment",
        positive_outlets: [
            { source: 'BBC', mood_score: 8 },
            { source: 'Guardian', mood_score: 12 }
        ],
        negative_outlets: [
            { source: 'Daily Mail', mood_score: -15 },
            { source: 'Telegraph', mood_score: -9 }
        ]
    },
    sentiment: {
        headline: "Sentiment Showdown - BBC vs Daily Mail",
        positive: { source: 'BBC', mood_score: 24 },
        negative: { source: 'Daily Mail', mood_score: 31 }
    }
};

/**
 * Create dual-chart card with hover switching
 * Loads both primary and alternate chart JSON and toggles on hover
 */
function createDualChartCard(containerId, primaryFile, alternateFile, initFunction) {
    const container = document.getElementById(containerId);

    if (!container) {
        console.error(`Container not found: ${containerId}`);
        return;
    }

    // Add data attributes for hover tracking
    container.dataset.isPrimary = 'true';
    container.dataset.primaryFile = primaryFile;
    container.dataset.alternateFile = alternateFile;

    // Load both variants (corrected paths for root index.html)
    Promise.all([
        fetch(`assets/data/${primaryFile}`).then(r => r.json()),
        fetch(`assets/data/${alternateFile}`).then(r => r.json())
    ]).then(([primaryData, alternateData]) => {
        // Store both data sets on the container
        container.dataset.primaryData = JSON.stringify(primaryData);
        container.dataset.alternateData = JSON.stringify(alternateData);

        // Initialize with primary chart
        let chartInstance = echarts.init(container.parentElement.querySelector('.chart-content') || container);
        initFunction(primaryData, chartInstance);
        container.dataset.chartInstance = chartInstance;

        // Add hover listeners to parent card
        const chartCard = container.closest('.chart-card');
        if (chartCard) {
            let isHovering = false;

            chartCard.addEventListener('mouseenter', () => {
                isHovering = true;
                setTimeout(() => {
                    if (isHovering) {
                        // Switch to alternate
                        container.dataset.isPrimary = 'false';
                        const altData = JSON.parse(container.dataset.alternateData);
                        initFunction(altData, chartInstance);
                    }
                }, 300);
            });

            chartCard.addEventListener('mouseleave', () => {
                isHovering = false;
                // Switch back to primary
                container.dataset.isPrimary = 'true';
                const primData = JSON.parse(container.dataset.primaryData);
                initFunction(primData, chartInstance);
            });
        }

        // Handle window resize
        window.addEventListener('resize', () => chartInstance.resize());
    }).catch(error => {
        console.error(`Dual Chart Error for ${containerId}:`, error);
        // Use mock data on error
        let chartInstance = echarts.init(container);
        let mockData = MOCK_DATA[containerId.replace('-chart', '').replace('emotional-rollercoaster', 'emotional').replace('surge-alert', 'surge').replace('media-divide', 'mediaDivide').replace('sentiment-showdown', 'sentiment')];
        if (mockData) {
            initFunction(mockData, chartInstance);
        }
    });
}

// --- CHART 1: EMOTIONAL ROLLERCOASTER (Line Chart) ---
function initEmotionalRollercoaster() {
    const chartDom = document.getElementById('emotional-rollercoaster-chart');
    const initFunc = (content, myChart) => {
        document.getElementById('rollercoaster-title').textContent = content.headline || MOCK_DATA.emotional.headline;

        // Handle both actual data structure and mock data
        const dates = content.dates || MOCK_DATA.emotional.dates;
        const scores = content.scores || MOCK_DATA.emotional.scores;

        const option = {
            tooltip: { trigger: 'axis' },
            grid: { left: '3%', right: '10%', bottom: '3%', top: '15%', containLabel: true },
            xAxis: { type: 'category', data: dates, axisLabel: { ...ECHART_TEXT_STYLE } },
            yAxis: { type: 'value', name: 'Mood Score', nameTextStyle: { ...ECHART_TEXT_STYLE }, axisLabel: { ...ECHART_TEXT_STYLE } },
            series: [{
                name: 'Mood Score',
                type: 'line',
                data: scores,
                smooth: true,
                symbol: 'circle',
                symbolSize: 8,
                lineStyle: { color: '#8b5cf6', width: 3 },
                itemStyle: { color: '#8b5cf6' },
                areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(139, 92, 246, 0.2)' }, { offset: 1, color: 'rgba(139, 92, 246, 0)' }]) }
            }]
        };
        myChart.setOption(option);
    };

    createDualChartCard(
        'emotional-rollercoaster-chart',
        'chart_1_primary.json',
        'chart_1_alternate.json',
        initFunc
    );
}

// --- CHART 2: WEEKLY WINNER (Custom HTML) ---
function initWeeklyWinner() {
    fetch('assets/data/social_weekly_winner.json')
        .then(response => response.json())
        .then(content => {
            const chartDom = document.getElementById('weekly-winner-chart');
            const topic = content.topic || 'Technology';
            const count = content.count || 127;
            chartDom.innerHTML = `
                <div class="winner-card">
                    <div class="winner-topic">${topic}</div>
                    <div class="winner-count">${count}</div>
                    <div class="winner-subtitle">articles</div>
                </div>
            `;
        }).catch(error => {
            console.error('Weekly Winner Error:', error);
            const chartDom = document.getElementById('weekly-winner-chart');
            chartDom.innerHTML = `
                <div class="winner-card">
                    <div class="winner-topic">Technology</div>
                    <div class="winner-count">127</div>
                    <div class="winner-subtitle">articles</div>
                </div>
            `;
        });
}

// --- CHART 3: SURGE ALERT (Bar Chart) with Dual-Chart Hover ---
function initSurgeAlert() {
    const chartDom = document.getElementById('surge-alert-chart');
    const initFunc = (content, myChart) => {
        document.getElementById('surge-alert-title').textContent = content.headline || MOCK_DATA.surge.headline;

        // Handle actual data or use mock
        const chartData = (content.data && Array.isArray(content.data)) ? content.data : MOCK_DATA.surge.data;

        const option = {
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            grid: { left: '3%', right: '10%', bottom: '3%', containLabel: true },
            xAxis: { type: 'value', boundaryGap: [0, 0.01], axisLabel: { ...ECHART_TEXT_STYLE } },
            yAxis: {
                type: 'category',
                data: chartData.map(item => item[0]).reverse(),
                axisLabel: { ...ECHART_TEXT_STYLE, fontWeight: 'bold' }
            },
            series: [{
                name: 'Surge Score',
                type: 'bar',
                data: chartData.map(item => item[1]).reverse(),
                itemStyle: { color: '#ef4444', borderRadius: [0, 4, 4, 0] },
                label: { show: true, position: 'right', fontWeight: 'bold', formatter: '{c}%' }
            }]
        };
        myChart.setOption(option);
    };

    createDualChartCard(
        'surge-alert-chart',
        'chart_2_primary.json',
        'chart_2_alternate.json',
        initFunc
    );
}

// --- CHART 4: MEDIA DIVIDE (Horizontal Bar Chart) with Dual-Chart Hover ---
function initMediaDivide() {
    const chartDom = document.getElementById('media-divide-chart');
    const initFunc = (content, myChart) => {
        document.getElementById('media-divide-title').textContent = content.headline || MOCK_DATA.mediaDivide.headline;

        // Handle actual structure or use mock
        const positiveOutlets = content.positive_outlets || MOCK_DATA.mediaDivide.positive_outlets;
        const negativeOutlets = content.negative_outlets || MOCK_DATA.mediaDivide.negative_outlets;
        const allOutlets = [...positiveOutlets, ...negativeOutlets];
        const sortedOutlets = allOutlets.sort((a, b) => a.mood_score - b.mood_score);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' },
                formatter: (params) => `${params[0].name}: <strong>Mood Score ${params[0].value > 0 ? '+' : ''}${params[0].value}</strong>`
            },
            grid: { left: '3%', right: '10%', bottom: '3%', top: '10%', containLabel: true },
            xAxis: {
                type: 'value',
                position: 'top',
                splitLine: { lineStyle: { type: 'dashed' } },
                axisLabel: { ...ECHART_TEXT_STYLE, formatter: '{value}' }
            },
            yAxis: {
                type: 'category',
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: { ...ECHART_TEXT_STYLE, fontWeight: 'bold' },
                data: sortedOutlets.map(o => o.source)
            },
            series: [{
                name: 'Mood Score',
                type: 'bar',
                label: { show: false },
                data: sortedOutlets.map(outlet => ({
                    value: outlet.mood_score,
                    itemStyle: {
                        color: outlet.mood_score > 0 ? '#22c55e' : '#ef4444'
                    }
                }))
            }]
        };

        myChart.setOption(option);
    };

    createDualChartCard(
        'media-divide-chart',
        'chart_3_primary.json',
        'chart_3_alternate.json',
        initFunc
    );
}

// --- CHART 5: SENTIMENT SHOWDOWN (Diverging Bar) with Dual-Chart Hover ---
function initSentimentShowdown() {
    const chartDom = document.getElementById('sentiment-showdown-chart');
    const initFunc = (content, myChart) => {
        document.getElementById('sentiment-showdown-title').textContent = content.headline || MOCK_DATA.sentiment.headline;

        // Handle actual structure or use mock
        const pos = content.positive || MOCK_DATA.sentiment.positive;
        const neg = content.negative || MOCK_DATA.sentiment.negative;

        const option = {
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            grid: { left: '3%', right: '3%', bottom: '3%', containLabel: true },
            xAxis: { type: 'value', show: false },
            yAxis: { type: 'category', data: [''], show: false },
            series: [
                {
                    name: pos.source,
                    type: 'bar',
                    stack: 'Showdown',
                    data: [pos.mood_score],
                    itemStyle: { color: '#22c55e' },
                    label: { show: true, position: 'insideLeft', formatter: `${pos.source}\n+${pos.mood_score}`, fontWeight: 'bold', fontSize: 14, color: '#fff' }
                },
                {
                    name: neg.source,
                    type: 'bar',
                    stack: 'Showdown',
                    data: [-neg.mood_score],
                    itemStyle: { color: '#ef4444' },
                    label: { show: true, position: 'insideRight', formatter: `${neg.source}\n${neg.mood_score}`, fontWeight: 'bold', fontSize: 14, color: '#fff' }
                }
            ]
        };
        myChart.setOption(option);
    };

    createDualChartCard(
        'sentiment-showdown-chart',
        'chart_4_primary.json',
        'chart_4_alternate.json',
        initFunc
    );
}
