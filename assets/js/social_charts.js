document.addEventListener('DOMContentLoaded', () => {
    // Ensure all container elements have proper sizing before chart init
    const containers = document.querySelectorAll('.chart-container');
    containers.forEach(container => {
        if (!container.style.height && !container.style.minHeight) {
            container.style.height = '400px';
        }
    });

    // Initialize all charts
    initEmotionalRollercoaster();
    initWeeklyWinner();
    initSurgeAlert();
    initMediaDivide();
    initSentimentShowdown();
    initCategoryDominance();
    initSourceProductivity();
    initPublishingRhythm();
    initWordcloud();
    initCrossSourceStories();
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
    },
    categories: {
        labels: ['Technology', 'Politics', 'Health', 'Business', 'Entertainment'],
        data: [35, 25, 18, 15, 7]
    },
    sources: {
        labels: ['BBC', 'Guardian', 'Sky News', 'Independent', 'Telegraph'],
        data: [45, 38, 32, 28, 22]
    },
    rhythm: {
        labels: ['6AM', '9AM', '12PM', '3PM', '6PM', '9PM', '12AM'],
        data: [12, 28, 42, 35, 38, 25, 18]
    }
};

// --- CHART 1: EMOTIONAL ROLLERCOASTER (Line Chart) ---
function initEmotionalRollercoaster() {
    const chartDom = document.getElementById('emotional-rollercoaster-chart');
    if (!chartDom) {
        console.warn('emotional-rollercoaster-chart not found');
        return;
    }
    console.log('Initializing Emotional Rollercoaster chart');

    fetch('assets/data/sentiment_tracker.json')
        .then(r => r.json())
        .then(data => {
            const myChart = echarts.init(chartDom);
            const titleEl = document.getElementById('rollercoaster-title');
            
            // Convert dates to short format (Mon, Tue, etc)
            const dates = (data.dates || []).map(d => {
                const date = new Date(d);
                return date.toLocaleDateString('en-GB', { weekday: 'short' });
            });
            const scores = data.mood_scores || MOCK_DATA.emotional.scores;

            if (titleEl) titleEl.textContent = "📊 Emotional Rollercoaster - Sentiment Trend";

            const option = {
                tooltip: { trigger: 'axis' },
                grid: { left: '3%', right: '10%', bottom: '3%', top: '15%', containLabel: true },
                xAxis: { type: 'category', data: dates.length > 0 ? dates : MOCK_DATA.emotional.dates, axisLabel: { ...ECHART_TEXT_STYLE } },
                yAxis: { type: 'value', name: 'Mood Score', nameTextStyle: { ...ECHART_TEXT_STYLE }, axisLabel: { ...ECHART_TEXT_STYLE } },
                series: [{
                    name: 'Mood Score',
                    type: 'line',
                    data: scores.length > 0 ? scores : MOCK_DATA.emotional.scores,
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 8,
                    lineStyle: { color: '#8b5cf6', width: 3 },
                    itemStyle: { color: '#8b5cf6' },
                    areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(139, 92, 246, 0.2)' }, { offset: 1, color: 'rgba(139, 92, 246, 0)' }]) }
                }]
            };
            myChart.setOption(option);
            window.addEventListener('resize', () => myChart.resize());
        })
        .catch(error => {
            console.warn('Sentiment tracker error:', error);
            const myChart = echarts.init(chartDom);
            const titleEl = document.getElementById('rollercoaster-title');
            if (titleEl) titleEl.textContent = "📊 Emotional Rollercoaster - Sentiment Trend";

            const option = {
                tooltip: { trigger: 'axis' },
                grid: { left: '3%', right: '10%', bottom: '3%', top: '15%', containLabel: true },
                xAxis: { type: 'category', data: MOCK_DATA.emotional.dates, axisLabel: { ...ECHART_TEXT_STYLE } },
                yAxis: { type: 'value', name: 'Mood Score', nameTextStyle: { ...ECHART_TEXT_STYLE }, axisLabel: { ...ECHART_TEXT_STYLE } },
                series: [{
                    name: 'Mood Score',
                    type: 'line',
                    data: MOCK_DATA.emotional.scores,
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 8,
                    lineStyle: { color: '#8b5cf6', width: 3 },
                    itemStyle: { color: '#8b5cf6' },
                    areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(139, 92, 246, 0.2)' }, { offset: 1, color: 'rgba(139, 92, 246, 0)' }]) }
                }]
            };
            myChart.setOption(option);
        });
}

// --- CHART 2: WEEKLY WINNER (Custom HTML) ---
function initWeeklyWinner() {
    const chartDom = document.getElementById('weekly-winner-chart');
    if (!chartDom) return;

    fetch('assets/data/dashboard_config.json')
        .then(response => response.json())
        .then(content => {
            // Extract top topic from sections or use config
            let topic = 'Technology';
            let count = 127;
            
            if (content.top_topic) {
                topic = content.top_topic;
                count = content.top_topic_count || 127;
            } else if (content.sections && Array.isArray(content.sections)) {
                // Parse from sections structure
                const glance = content.sections.find(s => s.id === 'at-a-glance');
                if (glance && glance.charts) {
                    const dominant = glance.charts.find(c => c.id === 'record-breakers-chart');
                    if (dominant) topic = dominant.title || 'Technology';
                }
            }
            
            chartDom.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; gap: 20px; padding: 20px;">
                    <div style="font-size: 2.5rem; font-weight: 800; color: #3b82f6;">${topic}</div>
                    <div style="font-size: 1rem; color: #6b7280;"><strong>${count}</strong> articles this week</div>
                </div>
            `;
        }).catch(error => {
            console.warn('Weekly Winner Error:', error);
            chartDom.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; gap: 20px; padding: 20px;">
                    <div style="font-size: 2.5rem; font-weight: 800; color: #3b82f6;">Technology</div>
                    <div style="font-size: 1rem; color: #6b7280;"><strong>127</strong> articles this week</div>
                </div>
            `;
        });
}

// --- CHART 3: SURGE ALERT (Bar Chart) ---
function initSurgeAlert() {
    const chartDom = document.getElementById('surge-alert-chart');
    if (!chartDom) return;

    fetch('assets/data/topic_surges.json')
        .then(r => r.json())
        .then(data => {
            const myChart = echarts.init(chartDom);
            const titleEl = document.getElementById('surge-alert-title');
            
            // Transform surges data - show most volatile topics (highest absolute change)
            const surges = data.surges || [];
            const chartData = surges
                .filter(s => Math.abs(s.change_pct) > 0) // Filter out zero change
                .sort((a, b) => Math.abs(b.change_pct) - Math.abs(a.change_pct)) // Sort by absolute change
                .slice(0, 5)
                .map(s => [s.topic, Math.abs(s.change_pct)]);

            if (titleEl) titleEl.textContent = "🚨 Topic Volatility - Most changed topics from yesterday";

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
                    label: { show: true, position: 'right', fontWeight: 'bold', formatter: (v) => Math.abs(v) + '%' }
                }]
            };
            myChart.setOption(option);
            window.addEventListener('resize', () => myChart.resize());
        })
        .catch(error => {
            console.warn('Surge Alert Error:', error);
            const myChart = echarts.init(chartDom);
            const titleEl = document.getElementById('surge-alert-title');
            if (titleEl) titleEl.textContent = "🚨 Topic Surge Alert - What's trending more than yesterday";

            const chartData = MOCK_DATA.surge.data;
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
        });
}

// --- CHART 4: MEDIA DIVIDE (Horizontal Bar Chart) ---
function initMediaDivide() {
    const chartDom = document.getElementById('media-divide-chart');
    if (!chartDom) return;

    fetch('assets/data/outlet_sentiment.json')
        .then(r => r.json())
        .then(data => {
            const myChart = echarts.init(chartDom);
            const titleEl = document.getElementById('media-divide-title');
            
            // Transform outlet sentiment data
            const outlets = (data.top_10 || []).map(o => ({
                source: o.source,
                sentiment_score: o.mood_score
            }));
            const sortedOutlets = outlets.sort((a, b) => a.sentiment_score - b.sentiment_score);

            if (titleEl) titleEl.textContent = "📰 Media Divide - Comparing outlet sentiment";

            const option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: { type: 'shadow' },
                    formatter: (params) => `${params[0].name}: <strong>${params[0].value > 0 ? '+' : ''}${params[0].value.toFixed(1)}</strong>`
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
                    name: 'Sentiment',
                    type: 'bar',
                    label: { show: false },
                    data: sortedOutlets.map(outlet => ({
                        value: outlet.sentiment_score || 0,
                        itemStyle: {
                            color: (outlet.sentiment_score || 0) > 0 ? '#22c55e' : '#ef4444'
                        }
                    }))
                }]
            };

            myChart.setOption(option);
            window.addEventListener('resize', () => myChart.resize());
        })
        .catch(error => {
            console.warn('Media Divide Error:', error);
            const myChart = echarts.init(chartDom);
            const titleEl = document.getElementById('media-divide-title');
            if (titleEl) titleEl.textContent = "📰 Media Divide - Comparing outlet sentiment";

            const positiveOutlets = MOCK_DATA.mediaDivide.positive_outlets;
            const negativeOutlets = MOCK_DATA.mediaDivide.negative_outlets;
            const allOutlets = [...positiveOutlets, ...negativeOutlets];
            const sortedOutlets = allOutlets.sort((a, b) => a.mood_score - b.mood_score);

            const option = {
                tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                grid: { left: '3%', right: '10%', bottom: '3%', top: '10%', containLabel: true },
                xAxis: {
                    type: 'value',
                    position: 'top',
                    splitLine: { lineStyle: { type: 'dashed' } },
                    axisLabel: { ...ECHART_TEXT_STYLE }
                },
                yAxis: {
                    type: 'category',
                    axisLine: { show: false },
                    axisTick: { show: false },
                    axisLabel: { ...ECHART_TEXT_STYLE, fontWeight: 'bold' },
                    data: sortedOutlets.map(o => o.source)
                },
                series: [{
                    name: 'Sentiment',
                    type: 'bar',
                    label: { show: false },
                    data: sortedOutlets.map(outlet => ({
                        value: outlet.mood_score,
                        itemStyle: { color: outlet.mood_score > 0 ? '#22c55e' : '#ef4444' }
                    }))
                }]
            };
            myChart.setOption(option);
        });
}

// --- CHART 5: SENTIMENT SHOWDOWN (Diverging Bar) ---
function initSentimentShowdown() {
    const chartDom = document.getElementById('sentiment-showdown-chart');
    if (!chartDom) return;

    fetch('assets/data/outlet_sentiment.json')
        .then(r => r.json())
        .then(data => {
            const myChart = echarts.init(chartDom);
            const titleEl = document.getElementById('sentiment-showdown-title');
            
            // Get top positive and negative outlets
            const outlets = (data.top_10 || []).map(o => ({
                outlet: o.source,
                sentiment_score: o.mood_score
            }));
            const positive = outlets.filter(o => (o.sentiment_score || 0) > 0).sort((a, b) => b.sentiment_score - a.sentiment_score)[0];
            const negative = outlets.filter(o => (o.sentiment_score || 0) < 0).sort((a, b) => a.sentiment_score - b.sentiment_score)[0];

            const pos = positive || MOCK_DATA.sentiment.positive;
            const neg = negative || MOCK_DATA.sentiment.negative;

            if (titleEl) titleEl.textContent = `Sentiment Showdown - ${pos.outlet || pos.source} vs ${neg.outlet || neg.source}`;

            const option = {
                tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                grid: { left: '3%', right: '3%', bottom: '3%', containLabel: true },
                xAxis: { type: 'value', show: false },
                yAxis: { type: 'category', data: [''], show: false },
                series: [
                    {
                        name: pos.outlet || pos.source,
                        type: 'bar',
                        stack: 'Showdown',
                        data: [pos.sentiment_score || pos.mood_score],
                        itemStyle: { color: '#22c55e' },
                        label: { show: true, position: 'insideLeft', formatter: `${pos.outlet || pos.source}\n+${(pos.sentiment_score || pos.mood_score).toFixed(1)}`, fontWeight: 'bold', fontSize: 14, color: '#fff' }
                    },
                    {
                        name: neg.outlet || neg.source,
                        type: 'bar',
                        stack: 'Showdown',
                        data: [-(neg.sentiment_score || neg.mood_score)],
                        itemStyle: { color: '#ef4444' },
                        label: { show: true, position: 'insideRight', formatter: `${neg.outlet || neg.source}\n${(neg.sentiment_score || neg.mood_score).toFixed(1)}`, fontWeight: 'bold', fontSize: 14, color: '#fff' }
                    }
                ]
            };
            myChart.setOption(option);
            window.addEventListener('resize', () => myChart.resize());
        })
        .catch(error => {
            console.warn('Sentiment Showdown Error:', error);
            const myChart = echarts.init(chartDom);
            const titleEl = document.getElementById('sentiment-showdown-title');
            if (titleEl) titleEl.textContent = `Sentiment Showdown - BBC vs Daily Mail`;

            const pos = MOCK_DATA.sentiment.positive;
            const neg = MOCK_DATA.sentiment.negative;

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
        });
}

// --- CHART 6: CATEGORY DOMINANCE (Doughnut) ---
function initCategoryDominance() {
    const canvas = document.getElementById('category-dominance-chart');
    if (!canvas) return;

    fetch('assets/data/category_dominance.json')
        .then(r => r.json())
        .then(data => {
            const categories = data.categories || [];
            const labels = categories.map(c => c.name || 'Unknown');
            const values = categories.map(c => c.value || 0);
            
            new Chart(canvas, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6'],
                        borderColor: '#ffffff',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { font: { family: 'Inter, sans-serif', size: 13 }, padding: 15 }
                        }
                    }
                }
            });
        })
        .catch(() => {
            new Chart(canvas, {
                type: 'doughnut',
                data: {
                    labels: MOCK_DATA.categories.labels,
                    datasets: [{
                        data: MOCK_DATA.categories.data,
                        backgroundColor: ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6'],
                        borderColor: '#ffffff',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { font: { family: 'Inter, sans-serif', size: 13 }, padding: 15 }
                        }
                    }
                }
            });
        });
}

// --- CHART 7: SOURCE PRODUCTIVITY (Horizontal Bar) ---
function initSourceProductivity() {
    const canvas = document.getElementById('source-productivity-chart');
    if (!canvas) return;

    fetch('assets/data/source_productivity.json')
        .then(r => r.json())
        .then(data => {
            const sources = (data.top_sources || []).slice(0, 8);
            const labels = sources.map(s => s.source || 'Unknown');
            const values = sources.map(s => s.count || 0);
            
            new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Articles Published',
                        data: values,
                        backgroundColor: '#3b82f6',
                        borderRadius: 4,
                        borderSkipped: false
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { beginAtZero: true }
                    }
                }
            });
        })
        .catch(() => {
            new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: MOCK_DATA.sources.labels,
                    datasets: [{
                        label: 'Articles Published',
                        data: MOCK_DATA.sources.data,
                        backgroundColor: '#3b82f6',
                        borderRadius: 4,
                        borderSkipped: false
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { beginAtZero: true }
                    }
                }
            });
        });
}

// --- CHART 8: PUBLISHING RHYTHM (Line/Area) ---
function initPublishingRhythm() {
    const canvas = document.getElementById('publishing-rhythm-chart');
    if (!canvas) return;

    fetch('assets/data/publishing_rhythm.json')
        .then(r => r.json())
        .then(data => {
            const hourlyData = data.hourly_counts || [];
            const labels = hourlyData.map((_, i) => `${i}:00`);
            
            new Chart(canvas, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Articles',
                        data: hourlyData,
                        fill: true,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        pointBackgroundColor: '#3b82f6',
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        })
        .catch(() => {
            new Chart(canvas, {
                type: 'line',
                data: {
                    labels: MOCK_DATA.rhythm.labels,
                    datasets: [{
                        label: 'Articles',
                        data: MOCK_DATA.rhythm.data,
                        fill: true,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        pointBackgroundColor: '#3b82f6',
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        });
}

// --- CHART 9: WORDCLOUD ---
function initWordcloud() {
    const container = document.getElementById('wordcloud-chart');
    if (!container) return;

    fetch('assets/data/wordcloud.json')
        .then(r => r.json())
        .then(data => {
            if (!window.echarts) {
                console.error('ECharts not loaded');
                return;
            }

            // Transform keywords to wordcloud format - filter HTML artifacts and stop words
            const stopWords = new Set(['href', 'https', 'http', 'apos', 'quot', 'nbsp', 'amp', 'lt', 'gt', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'that', 'this', 'is', 'are', 'was', 'were', 'be', 'have', 'has', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'her', 'his', 'their', 'he', 'she', 'it', 'you', 'me', 'we']);
            const wordData = (data.keywords || [])
                .filter(k => k.name && k.value && k.name.length > 2 && !stopWords.has(k.name.toLowerCase())) // Filter out stop words and short keywords
                .slice(0, 40)
                .map(k => ({ name: k.name, value: k.value }));

            if (wordData.length === 0) {
                wordData.push(...[
                    { name: 'Technology', value: 450 },
                    { name: 'News', value: 380 },
                    { name: 'Politics', value: 320 }
                ]);
            }

            const chart = echarts.init(container);
            const option = {
                tooltip: {},
                series: [{
                    type: 'wordCloud',
                    shape: 'circle',
                    left: 'center',
                    top: 'center',
                    width: '100%',
                    height: '100%',
                    right: null,
                    bottom: null,
                    sizeRange: [12, 48],
                    rotationRange: [-45, 45],
                    emphasis: {
                        focus: 'self',
                        textStyle: {
                            textShadowColor: 'rgba(0, 0, 0, 0.5)',
                            textShadowBlur: 10
                        }
                    },
                    textStyle: {
                        color: () => {
                            return 'rgb(' + [
                                Math.round(Math.random() * 200 + 30),
                                Math.round(Math.random() * 200 + 30),
                                Math.round(Math.random() * 200 + 30)
                            ].join(',') + ')';
                        },
                        fontFamily: 'Inter, sans-serif',
                        fontWeight: 'bold'
                    },
                    data: wordData
                }]
            };
            chart.setOption(option);
            window.addEventListener('resize', () => chart.resize());
        })
        .catch(error => {
            console.warn('Wordcloud Error:', error);
            const chart = echarts.init(container);
            const mockWords = [
                { name: 'Technology', value: 450 },
                { name: 'News', value: 380 },
                { name: 'Politics', value: 320 },
                { name: 'Health', value: 280 },
                { name: 'Business', value: 250 },
                { name: 'Climate', value: 200 },
                { name: 'Entertainment', value: 180 },
                { name: 'Sports', value: 160 }
            ];
            
            const option = {
                tooltip: {},
                series: [{
                    type: 'wordCloud',
                    shape: 'circle',
                    left: 'center',
                    top: 'center',
                    width: '100%',
                    height: '100%',
                    right: null,
                    bottom: null,
                    sizeRange: [12, 48],
                    rotationRange: [-45, 45],
                    emphasis: {
                        focus: 'self',
                        textStyle: {
                            textShadowColor: 'rgba(0, 0, 0, 0.5)',
                            textShadowBlur: 10
                        }
                    },
                    textStyle: {
                        color: () => {
                            return 'rgb(' + [
                                Math.round(Math.random() * 200 + 30),
                                Math.round(Math.random() * 200 + 30),
                                Math.round(Math.random() * 200 + 30)
                            ].join(',') + ')';
                        },
                        fontFamily: 'Inter, sans-serif',
                        fontWeight: 'bold'
                    },
                    data: mockWords
                }]
            };
            chart.setOption(option);
        });
}

// --- CHART 10: CROSS-SOURCE STORIES ---
function initCrossSourceStories() {
    const container = document.getElementById('cross-source-container');
    if (!container) return;

    fetch('assets/data/cross_source_stories.json')
        .then(r => r.json())
        .then(data => {
            const stories = data.stories || [];
            
            if (stories.length === 0) {
                container.innerHTML = '<p style="color: #9ca3af; padding: 20px; text-align: center;">No cross-source stories available yet</p>';
                return;
            }

            let html = '';
            stories.slice(0, 10).forEach(story => {
                const outlets = story.sources || story.outlets || [];
                html += `
                    <div style="padding: 16px; border-bottom: 1px solid #e5e7eb; cursor: pointer; transition: background 0.2s;">
                        <div style="font-weight: 600; color: #0f172a; margin-bottom: 8px; line-height: 1.5;">${story.headline || 'Untitled'}</div>
                        <div style="font-size: 0.875rem; color: #6b7280;">
                            <strong>${outlets.length}</strong> outlets: ${outlets.slice(0, 3).join(', ')}${outlets.length > 3 ? '...' : ''}
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        })
        .catch(error => {
            console.warn('Cross-source Error:', error);
            container.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #9ca3af;">
                    <p>No cross-source data available. Check back after the pipeline runs.</p>
                </div>
            `;
        });
}
