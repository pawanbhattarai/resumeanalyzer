/**
 * Charts and Visual Components for Resume-Job Compatibility Analyzer
 * Handles animated progress bars, circular progress indicators, and visual feedback
 */

class ChartComponents {
    constructor() {
        this.animationDuration = 1000;
        this.easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
    }
    
    /**
     * Animate a circular progress indicator
     * @param {HTMLElement} element - The circle element
     * @param {number} percentage - Target percentage (0-100)
     * @param {string} color - Color for the progress
     */
    animateCircularProgress(element, percentage, color = '#2563eb') {
        if (!element) return;
        
        const radius = 90;
        const circumference = 2 * Math.PI * radius;
        const strokeDasharray = circumference;
        const targetOffset = circumference - (percentage / 100) * circumference;
        
        // Create or update SVG
        let svg = element.querySelector('svg');
        if (!svg) {
            svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', '200');
            svg.setAttribute('height', '200');
            svg.style.position = 'absolute';
            svg.style.top = '0';
            svg.style.left = '0';
            svg.style.transform = 'rotate(-90deg)';
            
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', '100');
            circle.setAttribute('cy', '100');
            circle.setAttribute('r', radius);
            circle.setAttribute('fill', 'none');
            circle.setAttribute('stroke', color);
            circle.setAttribute('stroke-width', '8');
            circle.setAttribute('stroke-linecap', 'round');
            circle.setAttribute('stroke-dasharray', strokeDasharray);
            circle.setAttribute('stroke-dashoffset', circumference);
            
            svg.appendChild(circle);
            element.appendChild(svg);
        }
        
        const circle = svg.querySelector('circle');
        this.animateStrokeDashoffset(circle, circumference, targetOffset);
    }
    
    /**
     * Animate stroke-dashoffset for smooth progress animation
     */
    animateStrokeDashoffset(element, startOffset, targetOffset) {
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / this.animationDuration, 1);
            const easedProgress = this.easeOutCubic(progress);
            
            const currentOffset = startOffset - (startOffset - targetOffset) * easedProgress;
            element.setAttribute('stroke-dashoffset', currentOffset);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    /**
     * Create an animated horizontal progress bar
     * @param {HTMLElement} container - Container element
     * @param {number} percentage - Target percentage (0-100)
     * @param {string} color - Progress bar color
     * @param {string} label - Optional label
     */
    createHorizontalProgressBar(container, percentage, color = '#2563eb', label = '') {
        const progressBar = document.createElement('div');
        progressBar.className = 'horizontal-progress-bar';
        progressBar.style.cssText = `
            width: 100%;
            height: 12px;
            background-color: #f3f4f6;
            border-radius: 6px;
            overflow: hidden;
            position: relative;
            margin: 8px 0;
        `;
        
        const progressFill = document.createElement('div');
        progressFill.className = 'progress-fill';
        progressFill.style.cssText = `
            height: 100%;
            background-color: ${color};
            width: 0%;
            border-radius: 6px;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        `;
        
        // Add shimmer effect
        const shimmer = document.createElement('div');
        shimmer.style.cssText = `
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 1.5s infinite;
        `;
        
        progressFill.appendChild(shimmer);
        progressBar.appendChild(progressFill);
        
        if (label) {
            const labelElement = document.createElement('div');
            labelElement.textContent = label;
            labelElement.style.cssText = `
                font-size: 0.875rem;
                font-weight: 500;
                color: #374151;
                margin-bottom: 4px;
            `;
            container.appendChild(labelElement);
        }
        
        container.appendChild(progressBar);
        
        // Animate the progress bar
        setTimeout(() => {
            progressFill.style.width = `${percentage}%`;
        }, 100);
        
        return progressBar;
    }
    
    /**
     * Create a skill radar chart using CSS
     * @param {HTMLElement} container - Container element
     * @param {Object} skills - Skills data {category: percentage}
     */
    createSkillRadarChart(container, skills) {
        const radarContainer = document.createElement('div');
        radarContainer.className = 'radar-chart';
        radarContainer.style.cssText = `
            position: relative;
            width: 300px;
            height: 300px;
            margin: 0 auto;
        `;
        
        // Create radar background
        const radarBg = document.createElement('div');
        radarBg.style.cssText = `
            position: absolute;
            width: 100%;
            height: 100%;
            border: 2px solid #e5e7eb;
            border-radius: 50%;
            opacity: 0.3;
        `;
        radarContainer.appendChild(radarBg);
        
        // Add concentric circles
        for (let i = 1; i <= 4; i++) {
            const circle = document.createElement('div');
            const size = (i * 25);
            circle.style.cssText = `
                position: absolute;
                width: ${size}%;
                height: ${size}%;
                border: 1px solid #d1d5db;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                opacity: 0.2;
            `;
            radarContainer.appendChild(circle);
        }
        
        // Create skill points
        const skillEntries = Object.entries(skills);
        const angleStep = (2 * Math.PI) / skillEntries.length;
        
        skillEntries.forEach(([skill, percentage], index) => {
            const angle = index * angleStep - Math.PI / 2;
            const numericPercentage = typeof percentage === 'string' ? 
                parseInt(percentage.replace('%', '')) : percentage;
            const radius = (numericPercentage / 100) * 120; // Max radius 120px
            
            const x = 150 + radius * Math.cos(angle);
            const y = 150 + radius * Math.sin(angle);
            
            const point = document.createElement('div');
            point.style.cssText = `
                position: absolute;
                width: 12px;
                height: 12px;
                background-color: #2563eb;
                border: 2px solid white;
                border-radius: 50%;
                left: ${x - 6}px;
                top: ${y - 6}px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            `;
            
            // Add skill label
            const label = document.createElement('div');
            const labelRadius = 140;
            const labelX = 150 + labelRadius * Math.cos(angle);
            const labelY = 150 + labelRadius * Math.sin(angle);
            
            label.textContent = skill;
            label.style.cssText = `
                position: absolute;
                left: ${labelX}px;
                top: ${labelY}px;
                transform: translate(-50%, -50%);
                font-size: 0.75rem;
                font-weight: 500;
                color: #374151;
                white-space: nowrap;
            `;
            
            radarContainer.appendChild(point);
            radarContainer.appendChild(label);
            
            // Animate point appearance
            point.style.transform = 'scale(0)';
            setTimeout(() => {
                point.style.transform = 'scale(1)';
            }, index * 100);
        });
        
        container.appendChild(radarContainer);
        return radarContainer;
    }
    
    /**
     * Create animated counter for numbers
     * @param {HTMLElement} element - Target element
     * @param {number} targetValue - Target number
     * @param {number} duration - Animation duration in ms
     * @param {string} suffix - Optional suffix (e.g., '%')
     */
    animateCounter(element, targetValue, duration = 1000, suffix = '') {
        const startValue = 0;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = this.easeOutCubic(progress);
            
            const currentValue = Math.round(startValue + (targetValue - startValue) * easedProgress);
            element.textContent = currentValue + suffix;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    /**
     * Create a compatibility meter gauge
     * @param {HTMLElement} container - Container element
     * @param {number} percentage - Compatibility percentage (0-100)
     */
    createCompatibilityGauge(container, percentage) {
        const gauge = document.createElement('div');
        gauge.className = 'compatibility-gauge';
        gauge.style.cssText = `
            position: relative;
            width: 200px;
            height: 100px;
            margin: 0 auto;
            overflow: hidden;
        `;
        
        // Create gauge background
        const gaugeBg = document.createElement('div');
        gaugeBg.style.cssText = `
            width: 200px;
            height: 200px;
            border: 20px solid #f3f4f6;
            border-radius: 50%;
            border-bottom-color: transparent;
            position: absolute;
            top: 0;
            left: 0;
        `;
        
        // Create gauge fill
        const gaugeFill = document.createElement('div');
        const rotation = (percentage / 100) * 180;
        gaugeFill.style.cssText = `
            width: 200px;
            height: 200px;
            border: 20px solid #2563eb;
            border-radius: 50%;
            border-right-color: transparent;
            border-bottom-color: transparent;
            position: absolute;
            top: 0;
            left: 0;
            transform: rotate(${rotation}deg);
            transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
        `;
        
        // Create needle
        const needle = document.createElement('div');
        needle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 80px;
            background-color: #1f2937;
            left: 50%;
            bottom: 0;
            transform-origin: bottom center;
            transform: translateX(-50%) rotate(${rotation - 90}deg);
            transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
        `;
        
        // Create center dot
        const centerDot = document.createElement('div');
        centerDot.style.cssText = `
            position: absolute;
            width: 12px;
            height: 12px;
            background-color: #1f2937;
            border-radius: 50%;
            left: 50%;
            bottom: -6px;
            transform: translateX(-50%);
        `;
        
        gauge.appendChild(gaugeBg);
        gauge.appendChild(gaugeFill);
        gauge.appendChild(needle);
        gauge.appendChild(centerDot);
        
        container.appendChild(gauge);
        return gauge;
    }
    
    /**
     * Add CSS animations for shimmer effect
     */
    injectAnimationStyles() {
        if (document.getElementById('chart-animations')) return;
        
        const style = document.createElement('style');
        style.id = 'chart-animations';
        style.textContent = `
            @keyframes shimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            @keyframes bounceIn {
                0% { transform: scale(0.3); opacity: 0; }
                50% { transform: scale(1.05); }
                70% { transform: scale(0.9); }
                100% { transform: scale(1); opacity: 1; }
            }
            
            .chart-animate-in {
                animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            }
        `;
        
        document.head.appendChild(style);
    }
}

// Initialize chart components when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const chartComponents = new ChartComponents();
    chartComponents.injectAnimationStyles();
    
    // Make chartComponents globally available
    window.chartComponents = chartComponents;
});
