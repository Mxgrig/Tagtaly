# viral_viz.py
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
import numpy as np

class ViralChartMaker:
    """Create charts designed to stop the scroll"""

    def __init__(self):
        # BOLD social media color palette
        self.colors = {
            'surge': '#FF3B30',      # Dramatic red
            'drop': '#34C759',       # Fresh green
            'neutral': '#8E8E93',    # Grey
            'highlight': '#FF9500',  # Orange
            'background': '#000000', # Black (or white)
            'text': '#FFFFFF'        # White (or black)
        }

        # Mobile-first sizing
        self.fig_size = (1080/100, 1350/100)  # Instagram portrait
        self.dpi = 100

    def create_surge_alert(self, story_data):
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

        # Dramatic title
        ax.text(0.5, 1.15, story_data['headline'].upper(),
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

        # Branding
        ax.text(0.98, 0.02, 'Tagtaly | @tagtaly',
               transform=ax.transAxes,
               fontsize=10, ha='right',
               color=self.colors['neutral'])

        plt.tight_layout()
        return fig

    def create_politician_race(self, story_data):
        """Horse race chart for political mentions"""

        fig, ax = plt.subplots(figsize=self.fig_size, facecolor=self.colors['background'])
        ax.set_facecolor(self.colors['background'])

        mentions = sorted(story_data['data'].items(), key=lambda x: x[1], reverse=True)
        names = [m[0] for m in mentions]
        counts = [m[1] for m in mentions]

        # Create bars
        bars = ax.barh(names, counts, color=self.colors['highlight'])

        # Add mention counts on bars
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(count + max(counts)*0.02, i, f"{count} mentions",
                   va='center', fontsize=18, fontweight='bold',
                   color=self.colors['text'])

        # Title
        ax.text(0.5, 1.12, story_data['headline'].upper(),
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

    def create_record_highlight(self, story_data):
        """Spotlight a record-breaking number"""

        if not story_data['data']:
            return None

        fig, ax = plt.subplots(figsize=self.fig_size, facecolor='#FF3B30')
        ax.axis('off')

        record = story_data['data'][0]

        # Extract the key number from headline
        import re
        numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', record['headline'])
        big_number = numbers[0] if numbers else "NEW"

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
               color='rgba(255,255,255,0.7)')

        # Branding
        ax.text(0.5, 0.05, 'Tagtaly',
               transform=ax.transAxes,
               fontsize=14, ha='center',
               color='white', fontweight='bold')

        return fig
