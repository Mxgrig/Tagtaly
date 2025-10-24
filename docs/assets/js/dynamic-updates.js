/**
 * Tagtaly Dynamic Updates Module
 * Handles all dynamic content updates from data provider
 * Replaces hardcoded data with live-generated content
 */

/**
 * Update all date references on the page
 */
function updateDateReferences(dateStr) {
    try {
        const formattedDate = dataProvider.formatDate(dateStr);
        
        // Update main article headline date
        const headlineElement = document.getElementById('article-headline');
        if (headlineElement) {
            headlineElement.textContent = `${formattedDate}: Breaking Down the News Cycle`;
        }

        // Update article body date references
        const dateElements = document.querySelectorAll('[data-date-placeholder]');
        dateElements.forEach(el => {
            el.textContent = formattedDate;
        });

        console.log(`📅 Date references updated to: ${formattedDate}`);
    } catch (error) {
        console.error('Error updating date references:', error);
    }
}

/**
 * Update article headline with current date and trending topic
 */
function updateArticleHeadline(data) {
    try {
        const stats = dataProvider.calculateStatistics(data);
        const dateStr = dataProvider.formatDate(data.date);
        const topTopic = stats.topTopic || 'News';
        
        const headlineElement = document.getElementById('article-headline');
        if (headlineElement) {
            headlineElement.innerHTML = `${dateStr}: <span class="highlight-topic">${topTopic}</span> Dominates Today's News`;
        }

        console.log(`📰 Article headline updated`);
    } catch (error) {
        console.error('Error updating article headline:', error);
    }
}

/**
 * Update main article body paragraphs with live statistics
 */
function updateArticleBody(data) {
    try {
        const stats = dataProvider.calculateStatistics(data);
        const dateStr = dataProvider.formatDate(data.date);
        const topicTrend = dataProvider.getTopTopics(data, 3);

        // Update pipeline summary paragraph
        const summaryEl = document.getElementById('pipeline-summary');
        if (summaryEl) {
            summaryEl.innerHTML = `
                Tagtaly's news intelligence pipeline analyzed 
                <strong id="article-count">${stats.totalArticles}</strong> articles from
                <strong id="source-count">${stats.totalSources}</strong> major news sources
                across the UK and US on <strong id="article-date">${dateStr}</strong>.
                Here's what the data reveals about today's news cycle.
            `;
        }

        // Update sentiment summary
        const sentimentEl = document.getElementById('sentiment-summary');
        if (sentimentEl) {
            const sentiment = dataProvider.getSentimentTrend(data);
            const sentimentText = sentiment.current > 55 ? 'largely positive' 
                                 : sentiment.current > 45 ? 'mixed' 
                                 : 'cautious';
            sentimentEl.innerHTML = `
                Overall sentiment analysis shows <strong>${Math.round(sentiment.current)}% positive</strong> coverage,
                indicating a <strong>${sentimentText}</strong> tone across major outlets today.
            `;
        }

        // Update trending topics paragraph
        const topicsEl = document.getElementById('trending-topics');
        if (topicsEl && topicTrend.length > 0) {
            const topicsList = topicTrend.slice(0, 2)
                .map((t, i) => `<strong>${i + 1}. ${t.topic}</strong> (up ${t.change_pct}%)`)
                .join(' and ');
            topicsEl.innerHTML = `
                Today's dominant narrative centers on ${topicsList}.
                These topics are gaining significant coverage compared to yesterday's priorities.
            `;
        }

        console.log(`📝 Article body paragraphs updated`);
    } catch (error) {
        console.error('Error updating article body:', error);
    }
}

/**
 * Load and display live headlines feed from articles.json
 */
function loadLiveHeadlines(data) {
    try {
        const topArticles = dataProvider.getTopArticles(data, 5);
        const container = document.querySelector('[data-live-feed]');

        if (!container) {
            console.warn('⚠️ Live feed container not found');
            return;
        }

        if (topArticles.length === 0) {
            container.innerHTML = '<div class="headline-item"><span>No articles available</span></div>';
            return;
        }

        // Clear existing content
        container.innerHTML = '';

        // Populate with top articles
        topArticles.forEach(article => {
            const articleDate = dataProvider.formatDate(article.published_date || article.fetched_at);
            const sentiment = article.sentiment || 'neutral';
            const sentimentBadge = sentiment === 'positive' ? '😊' : sentiment === 'negative' ? '😞' : '😐';
            
            // Use display_topic if available (shows subcategory for "Other" category)
            const displayTopic = article.display_topic || article.topic || 'General';

            const element = document.createElement('div');
            element.className = 'headline-item';
            element.innerHTML = `
                <div class="headline-meta">
                    <span class="source">${article.source}</span>
                    <span class="date">${articleDate}</span>
                    <span class="sentiment-badge" title="${sentiment}">${sentimentBadge}</span>
                </div>
                <p class="headline-text">${article.headline}</p>
                <p class="headline-topic"><span class="topic-tag">${displayTopic}</span></p>
            `;
            container.appendChild(element);
        });

        console.log(`📰 Live feed updated with ${topArticles.length} articles`);
    } catch (error) {
        console.error('Error loading live headlines:', error);
    }
}

/**
 * Update all data-stat elements with current statistics
 */
function updateAllStatistics(data) {
    try {
        const stats = dataProvider.calculateStatistics(data);
        const sentiment = dataProvider.getSentimentTrend(data);

        // Define all statistics to update
        const updates = {
            'total-articles': stats.totalArticles.toString(),
            'uk-articles': stats.ukArticles.toString(),
            'us-articles': stats.usArticles.toString(),
            'positive-pct': stats.positivePct + '%',
            'neutral-pct': stats.neutralPct + '%',
            'negative-pct': stats.negativePct + '%',
            'top-topic-name': stats.topTopic,
            'top-topic-share': stats.topicShare + '%',
            'total-sources': stats.totalSources.toString(),
            'sentiment-mood': Math.round(sentiment.current) + '%',
            'sentiment-trend': sentiment.trend > 0 ? '↑ Improving' : sentiment.trend < 0 ? '↓ Declining' : '→ Stable'
        };

        // Apply updates to all data-stat elements
        Object.entries(updates).forEach(([key, value]) => {
            const elements = document.querySelectorAll(`[data-stat="${key}"]`);
            elements.forEach(el => {
                el.textContent = value;
                el.classList.add('updated'); // Add CSS class for animation
            });
        });

        console.log('✅ All statistics updated:', updates);
        return updates;
    } catch (error) {
        console.error('Error updating statistics:', error);
    }
}

/**
 * Render word cloud from keywords data
 */
function renderWordCloud(data) {
    try {
        const keywords = dataProvider.getKeywords(data, 50);
        const container = document.getElementById('wordcloud-container');

        if (!container || keywords.length === 0) {
            console.warn('⚠️ Word cloud container not found or no keywords');
            return;
        }

        // Calculate max frequency for scaling
        const maxFreq = keywords.length > 0 ? Math.max(...keywords.map(k => k.value)) : 1;

        // Clear existing content
        container.innerHTML = '';

        // Create word cloud elements
        keywords.forEach(keyword => {
            const scaleFactor = (keyword.value / maxFreq) * 0.8 + 0.5; // Scale between 0.5x and 1.3x
            const element = document.createElement('span');
            element.className = 'word-cloud-item';
            element.textContent = keyword.name;
            element.style.fontSize = (scaleFactor * 100) + '%';
            element.style.opacity = (keyword.value / maxFreq) * 0.7 + 0.3; // Opacity between 0.3 and 1.0
            element.title = `${keyword.value} mentions`;
            container.appendChild(element);
        });

        console.log(`☁️ Word cloud rendered with ${keywords.length} keywords`);
    } catch (error) {
        console.error('Error rendering word cloud:', error);
    }
}

/**
 * Update sentiment visualization data
 */
function updateSentimentCharts(data) {
    try {
        if (!data.sentiment || !data.sentiment.mood_scores) {
            console.warn('⚠️ No sentiment data available');
            return;
        }

        const sentiment = dataProvider.getSentimentTrend(data);
        
        // Update sentiment indicator
        const indicatorEl = document.getElementById('sentiment-indicator');
        if (indicatorEl) {
            const mood = sentiment.current;
            let moodClass = mood > 55 ? 'positive' : mood > 45 ? 'neutral' : 'negative';
            indicatorEl.className = `sentiment-indicator ${moodClass}`;
            indicatorEl.textContent = Math.round(mood) + '% Positive';
        }

        // Update sentiment trend
        const trendEl = document.getElementById('sentiment-trend');
        if (trendEl) {
            const trendText = sentiment.trend > 0 ? `📈 +${sentiment.trend.toFixed(1)}% (Improving)` 
                            : sentiment.trend < 0 ? `📉 ${sentiment.trend.toFixed(1)}% (Declining)` 
                            : `→ Stable`;
            trendEl.textContent = trendText;
        }

        console.log(`📊 Sentiment charts updated`);
    } catch (error) {
        console.error('Error updating sentiment charts:', error);
    }
}

/**
 * Update trending topics section
 */
function updateTrendingTopics(data) {
    try {
        const topTopics = dataProvider.getTopTopics(data, 5);
        const container = document.getElementById('trending-topics-list');

        if (!container || topTopics.length === 0) {
            console.warn('⚠️ Trending topics container not found');
            return;
        }

        container.innerHTML = '';

        topTopics.forEach((topic, index) => {
            const element = document.createElement('div');
            element.className = 'trending-topic-item';
            const trendIcon = topic.change_pct > 0 ? '📈' : '📉';
            const trendColor = topic.change_pct > 0 ? 'green' : 'red';
            
            element.innerHTML = `
                <div class="topic-rank">#${index + 1}</div>
                <div class="topic-info">
                    <div class="topic-name">${topic.topic}</div>
                    <div class="topic-change" style="color: ${trendColor}">
                        ${trendIcon} ${Math.abs(topic.change_pct)}% 
                        ${topic.change_pct > 0 ? 'increase' : 'decrease'}
                    </div>
                </div>
            `;
            container.appendChild(element);
        });

        console.log(`🔥 Trending topics updated`);
    } catch (error) {
        console.error('Error updating trending topics:', error);
    }
}

/**
 * Master update function - coordinates all dynamic updates
 */
async function updateAllPageContent() {
    try {
        console.log('🔄 Starting comprehensive page update...');
        const startTime = performance.now();

        // Load all data
        const data = await dataProvider.loadAllData();

        // Update all components in parallel where possible
        updateDateReferences(data.date);
        updateArticleHeadline(data);
        updateArticleBody(data);
        updateAllStatistics(data);
        loadLiveHeadlines(data);
        renderWordCloud(data);
        await renderOutletChart(data);
        updateSentimentCharts(data);
        updateTrendingTopics(data);

        const duration = performance.now() - startTime;
        console.log(`✅ Page update complete in ${duration.toFixed(0)}ms`);

        // Dispatch custom event for other modules to listen
        document.dispatchEvent(new CustomEvent('tagtaly-data-updated', { detail: data }));

    } catch (error) {
        console.error('❌ Error during page update:', error);
    }
}

/**
 * Render outlet/source productivity chart (async)
 */
async function renderOutletChart(data) {
    try {
        const container = document.getElementById('source-productivity-chart');
        if (!container) {
            console.warn('⚠️ Outlet chart container not found');
            return;
        }

        // Fetch outlet_sentiment.json
        const response = await fetch('assets/data/outlet_sentiment.json', { cache: 'no-store' });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const outletData = await response.json();

        if (!outletData.outlets || outletData.outlets.length === 0) {
            console.warn('⚠️ No outlet data available');
            container.innerHTML = '<div style="padding: 20px; color: #6b7280;">No outlet data available</div>';
            return;
        }

        // Clear container
        container.innerHTML = '';

        // Create chart data for top outlets
        const topOutlets = outletData.outlets.slice(0, 10);
        const chartContainer = document.createElement('div');
        chartContainer.style.cssText = 'padding: 20px; overflow-y: auto; height: 100%;';

        topOutlets.forEach((outlet, index) => {
            const row = document.createElement('div');
            row.style.cssText = `
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 0;
                border-bottom: 1px solid #e5e7eb;
                font-size: 14px;
            `;

            const barWidth = (outlet.articles / topOutlets[0].articles) * 100;
            const sentimentColor = outlet.positive_pct > 60 ? '#10b981' : outlet.positive_pct > 40 ? '#f59e0b' : '#ef4444';

            row.innerHTML = `
                <div style="width: 30%; font-weight: 600;">${outlet.outlet}</div>
                <div style="width: 50%;">
                    <div style="background: #e5e7eb; border-radius: 4px; overflow: hidden; height: 24px; position: relative;">
                        <div style="background: ${sentimentColor}; height: 100%; width: ${barWidth}%; transition: width 0.3s ease;"></div>
                        <span style="position: absolute; right: 8px; top: 50%; transform: translateY(-50%); font-weight: 600; color: ${barWidth > 50 ? 'white' : '#374151'}; font-size: 12px;">${outlet.articles}</span>
                    </div>
                </div>
                <div style="width: 20%; text-align: right; font-weight: 600; color: ${sentimentColor};">${outlet.positive_pct}%</div>
            `;
            chartContainer.appendChild(row);
        });

        container.appendChild(chartContainer);
        console.log(`📊 Outlet chart rendered with ${topOutlets.length} outlets`);
    } catch (error) {
        console.error('Error rendering outlet chart:', error);
        const container = document.getElementById('source-productivity-chart');
        if (container) {
            container.innerHTML = `<div style="padding: 20px; color: #ef4444;">Error loading outlet data: ${error.message}</div>`;
        }
    }
}

/**
 * Setup auto-refresh at specified interval (useful for live updates)
 */
function setupAutoRefresh(intervalMinutes = 30) {
    try {
        const intervalMs = intervalMinutes * 60 * 1000;
        
        setInterval(() => {
            console.log('🔄 Auto-refresh triggered');
            updateAllPageContent();
        }, intervalMs);

        console.log(`⏱️ Auto-refresh enabled every ${intervalMinutes} minutes`);
    } catch (error) {
        console.error('Error setting up auto-refresh:', error);
    }
}
