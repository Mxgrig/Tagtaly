# viral_viz.py
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
import numpy as np
import sys
import os

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.countries import get_country_config

class ViralChartMaker:
    """Create charts designed to stop the scroll"""

    def __init__(self):
        # BOLD social media color palette
        self.colors = {
            'surge': '#FF3B30',      # Dramatic red
            'drop': '#34C759',       # Fresh green
            'neutral': '#8E8E93',    # Grey
            'highlight': '#FF9500',  # Orange
            'background': '#000000', # Black
            'text': '#FFFFFF'        # White
        }

        # Mobile-first sizing (Instagram portrait)
        self.fig_size = (1080/100, 1350/100)
        self.dpi = 100

    def create_surge_alert(self, story_data, country=None):
        """Dramatic week-over-week comparison"""

        fig, ax = plt.subplots(figsize=self.fig_size, facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        data = story_data['data'].nlargest(5, 'pct_change')

        # Horizontal bars with dramatic colors
        bars = ax.barh(data['topic'], data['pct_change'])

        # Color code by change
        for i, (bar, pct) in enumerate(zip(bars, data['pct_change'])):
            bar.set_color(self.colors['surge'] if pct > 0 else self.colors['drop'])
            bar.set_edgecolor(self.colors['text'])
            bar.set_linewidth(2)

            # Add percentage labels
            ax.text(pct + 5, i, f"+{pct:.0f}%",
                   va='center', fontsize=20, fontweight='bold',
                   color=self.colors['text'])

        # Dramatic title with country flag
        title = story_data.get('headline', 'NEWS SURGE').upper()
        ax.text(0.5, 1.15, title,
               transform=ax.transAxes,
               fontsize=24, fontweight='bold',
               ha='center', color=self.colors['text'],
               wrap=True)

        # Subtitle context
        ax.text(0.5, 1.08, 'vs last week',
               transform=ax.transAxes,
               fontsize=14, ha='center',
               color=self.colors['neutral'])

        # Style cleanup
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(self.colors['text'])
        ax.spines['left'].set_color(self.colors['text'])
        ax.tick_params(colors=self.colors['text'], labelsize=16)
        ax.set_xlabel('')

        # Updated branding (not "UK News in Charts")
        ax.text(0.98, 0.02, 'Tagtaly',
               transform=ax.transAxes,
               fontsize=10, ha='right',
               color=self.colors['neutral'])

        plt.tight_layout()
        return fig

    def create_viral_people_race(self, story_data, country=None):
        """Horse race chart for viral people mentions (politicians, celebs, tech CEOs)"""

        fig, ax = plt.subplots(figsize=self.fig_size, facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        mentions = sorted(story_data['data'].items(), key=lambda x: x[1], reverse=True)[:8]
        names = [m[0] for m in mentions]
        counts = [m[1] for m in mentions]

        # Create bars
        bars = ax.barh(names, counts, color=self.colors['highlight'])

        # Add mention counts on bars
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(count + max(counts)*0.02, i, f"{count} mentions",
                   va='center', fontsize=18, fontweight='bold',
                   color=self.colors['text'])

        # Title with country flag
        title = story_data.get('headline', 'VIRAL PEOPLE SCORECARD').upper()
        ax.text(0.5, 1.12, title,
               transform=ax.transAxes,
               fontsize=22, fontweight='bold',
               ha='center', color=self.colors['text'],
               wrap=True)

        # Clean up
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_color(self.colors['text'])
        ax.tick_params(colors=self.colors['text'], labelsize=16)
        ax.set_xticks([])

        # Branding
        ax.text(0.98, 0.02, 'Tagtaly',
               transform=ax.transAxes,
               fontsize=10, ha='right',
               color=self.colors['neutral'])

        plt.tight_layout()
        return fig

    def create_record_highlight(self, story_data, country=None):
        """Spotlight a record-breaking number"""

        if not story_data.get('data'):
            return None

        fig, ax = plt.subplots(figsize=self.fig_size, facecolor='#FF3B30')
        ax.axis('off')

        record = story_data['data'][0]

        # Extract the key number from headline
        import re
        numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', record['headline'])
        big_number = numbers[0] if numbers else "NEW"

        # Add country flag at top if provided
        if country:
            config = get_country_config(country)
            if config:
                ax.text(0.5, 0.95, config['flag'],
                       transform=ax.transAxes,
                       fontsize=48, ha='center',
                       color='white')

        # Giant number in center
        ax.text(0.5, 0.55, big_number,
               transform=ax.transAxes,
               fontsize=120, fontweight='bold',
               ha='center', va='center',
               color='white')

        # Headline above
        ax.text(0.5, 0.85, "RECORD HIGH" if 'high' in record['headline'].lower() else "RECORD LOW",
               transform=ax.transAxes,
               fontsize=32, fontweight='bold',
               ha='center', color='white')

        # Context below
        ax.text(0.5, 0.35, record['headline'][:80],
               transform=ax.transAxes,
               fontsize=18, ha='center',
               color='white', wrap=True)

        # Source
        ax.text(0.5, 0.20, f"Source: {record['source']}",
               transform=ax.transAxes,
               fontsize=12, ha='center',
               color='white', alpha=0.7)

        # Branding
        ax.text(0.5, 0.05, 'Tagtaly',
               transform=ax.transAxes,
               fontsize=14, ha='center',
               color='white', fontweight='bold')

        return fig

    def create_sentiment_shift(self, story_data, country=None):
        """Show mood changes in coverage"""

        if story_data.get('data') is None or (hasattr(story_data['data'], 'empty') and story_data['data'].empty):
            return None

        fig, ax = plt.subplots(figsize=self.fig_size, facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        data = story_data['data'].nlargest(5, 'abs_change')

        # Horizontal bars showing sentiment change
        bars = ax.barh(data['topic'], data['sentiment_change'])

        # Color code by direction
        for i, (bar, change) in enumerate(zip(bars, data['sentiment_change'])):
            bar.set_color(self.colors['drop'] if change > 0 else self.colors['surge'])
            bar.set_edgecolor(self.colors['text'])
            bar.set_linewidth(2)

            # Add labels
            direction = "+" if change > 0 else ""
            ax.text(change + 0.05, i, f"{direction}{change:.2f}",
                   va='center', fontsize=18, fontweight='bold',
                   color=self.colors['text'])

        # Title with country flag
        title = story_data.get('headline', 'MOOD SHIFT').upper()
        ax.text(0.5, 1.15, title,
               transform=ax.transAxes,
               fontsize=24, fontweight='bold',
               ha='center', color=self.colors['text'],
               wrap=True)

        # Subtitle
        ax.text(0.5, 1.08, 'Sentiment change (-1 to +1 scale)',
               transform=ax.transAxes,
               fontsize=12, ha='center',
               color=self.colors['neutral'])

        # Style
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(self.colors['text'])
        ax.spines['left'].set_color(self.colors['text'])
        ax.tick_params(colors=self.colors['text'], labelsize=16)

        # Branding
        ax.text(0.98, 0.02, 'Tagtaly',
               transform=ax.transAxes,
               fontsize=10, ha='right',
               color=self.colors['neutral'])

        plt.tight_layout()
        return fig

    def create_media_bias_chart(self, story_data, country=None):
        """Show what each outlet focuses on"""

        if story_data.get('data') is None or (hasattr(story_data['data'], 'empty') and story_data['data'].empty):
            return None

        fig, ax = plt.subplots(figsize=self.fig_size, facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        data = story_data['data']

        # Create bars
        bars = ax.barh(data['source'], data['count'], color=self.colors['highlight'])

        # Add topic labels on bars
        for i, (bar, topic) in enumerate(zip(bars, data['topic'])):
            ax.text(bar.get_width() / 2, i, topic,
                   va='center', ha='center', fontsize=16, fontweight='bold',
                   color=self.colors['background'])

        # Title with country flag
        title = story_data.get('headline', 'MEDIA FOCUS').upper()
        ax.text(0.5, 1.12, title,
               transform=ax.transAxes,
               fontsize=22, fontweight='bold',
               ha='center', color=self.colors['text'],
               wrap=True)

        # Clean up
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_color(self.colors['text'])
        ax.tick_params(colors=self.colors['text'], labelsize=14)
        ax.set_xticks([])

        # Branding
        ax.text(0.98, 0.02, 'Tagtaly',
               transform=ax.transAxes,
               fontsize=10, ha='right',
               color=self.colors['neutral'])

        plt.tight_layout()
        return fig

    def create_comparison_chart(self, uk_data, us_data, topic):
        """NEW: Create UK vs US comparison chart"""

        fig, ax = plt.subplots(figsize=self.fig_size, facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        countries = ['🇬🇧 UK', '🇺🇸 US']
        values = [uk_data, us_data]

        # Create bars
        bars = ax.bar(countries, values, color=[self.colors['surge'], self.colors['highlight']])

        # Add value labels
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                   f"{val:.0f}",
                   ha='center', fontsize=32, fontweight='bold',
                   color=self.colors['text'])

        # Title
        ax.text(0.5, 1.12, f"🌍 {topic.upper()}: UK vs US",
               transform=ax.transAxes,
               fontsize=24, fontweight='bold',
               ha='center', color=self.colors['text'])

        # Style
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(self.colors['text'])
        ax.spines['left'].set_color(self.colors['text'])
        ax.tick_params(colors=self.colors['text'], labelsize=18)
        ax.set_ylabel('')

        # Branding
        ax.text(0.98, 0.02, 'Tagtaly',
               transform=ax.transAxes,
               fontsize=10, ha='right',
               color=self.colors['neutral'])

        plt.tight_layout()
        return fig

if __name__ == "__main__":
    # Test chart creation
    print("Viral chart maker ready")
