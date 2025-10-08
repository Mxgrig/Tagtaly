// Tagtaly Website JavaScript

// Mobile menu toggle (for future implementation)
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

// Chart loading functionality (will be enhanced with actual data)
function loadLatestCharts() {
    // Placeholder for dynamic chart loading
    // Future: Fetch from GitHub API or JSON manifest
    console.log('Charts loading...');
}

// Filter functionality for archive page
function applyFilters() {
    const topicFilter = document.getElementById('topic-filter')?.value;
    const typeFilter = document.getElementById('type-filter')?.value;
    const dateFilter = document.getElementById('date-filter')?.value;

    console.log('Filters:', { topicFilter, typeFilter, dateFilter });
    // Future: Implement actual filtering logic
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Tagtaly website loaded');

    // Add any initialization code here
    loadLatestCharts();
});
