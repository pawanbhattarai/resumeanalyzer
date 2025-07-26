/**
 * Resume-Job Compatibility Analyzer Frontend Script
 * Handles UI interactions, API calls, and result visualization
 */

class CompatibilityAnalyzer {
    constructor() {
        this.isAnalyzing = false;
        this.cache = new Map();
        this.debounceTimer = null;
        
        this.initializeElements();
        this.bindEvents();
        this.checkSystemHealth();
    }
    
    initializeElements() {
        // Input elements
        this.resumeTextarea = document.getElementById('resumeText');
        this.jobTextarea = document.getElementById('jobText');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.resumeCharCount = document.getElementById('resumeCharCount');
        this.jobCharCount = document.getElementById('jobCharCount');
        
        // Section elements
        this.inputSection = document.getElementById('inputSection');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        
        // Loading elements
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        
        // Results elements
        this.scoreValue = document.getElementById('scoreValue');
        this.scoreCircle = document.getElementById('scoreCircle');
        this.compatibilityLevel = document.getElementById('compatibilityLevel');
        this.improvementPotential = document.getElementById('improvementPotential');
        this.skillBreakdown = document.getElementById('skillBreakdown');
        this.matchBreakdown = document.getElementById('matchBreakdown');
        this.recommendationsList = document.getElementById('recommendationsList');
        
        // Action buttons
        this.newAnalysisBtn = document.getElementById('newAnalysisBtn');
        this.exportBtn = document.getElementById('exportBtn');
        this.retryBtn = document.getElementById('retryBtn');
        
        // Error elements
        this.errorMessage = document.getElementById('errorMessage');
    }
    
    bindEvents() {
        // Text input events
        this.resumeTextarea.addEventListener('input', () => this.updateCharCount(this.resumeTextarea, this.resumeCharCount));
        this.jobTextarea.addEventListener('input', () => this.updateCharCount(this.jobTextarea, this.jobCharCount));
        
        // Button events
        this.analyzeBtn.addEventListener('click', () => this.handleAnalyze());
        this.newAnalysisBtn.addEventListener('click', () => this.resetForm());
        this.exportBtn.addEventListener('click', () => this.exportResults());
        this.retryBtn.addEventListener('click', () => this.handleAnalyze());
        
        // Real-time validation with debouncing
        this.resumeTextarea.addEventListener('input', () => this.debounceValidation());
        this.jobTextarea.addEventListener('input', () => this.debounceValidation());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
    }
    
    updateCharCount(textarea, countElement) {
        const count = textarea.value.length;
        countElement.textContent = `${count} characters`;
        
        // Add visual feedback for minimum length
        if (count < 10 && count > 0) {
            countElement.style.color = 'var(--error-color)';
        } else if (count >= 10) {
            countElement.style.color = 'var(--success-color)';
        } else {
            countElement.style.color = 'var(--text-secondary)';
        }
    }
    
    debounceValidation() {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.validateInputs();
        }, 300);
    }
    
    validateInputs() {
        const resumeText = this.resumeTextarea.value.trim();
        const jobText = this.jobTextarea.value.trim();
        
        const isValid = resumeText.length >= 10 && jobText.length >= 10;
        
        this.analyzeBtn.disabled = !isValid || this.isAnalyzing;
        
        if (!isValid && (resumeText.length > 0 || jobText.length > 0)) {
            this.analyzeBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i><span>Need at least 10 characters in both fields</span>';
        } else if (isValid) {
            this.analyzeBtn.innerHTML = '<i class="fas fa-search"></i><span>Analyze Compatibility</span>';
        } else {
            this.analyzeBtn.innerHTML = '<i class="fas fa-search"></i><span>Analyze Compatibility</span>';
        }
    }
    
    async checkSystemHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (!response.ok) {
                console.warn('System health check failed:', data);
            } else {
                console.log('System healthy:', data);
            }
        } catch (error) {
            console.error('Health check error:', error);
        }
    }
    
    async handleAnalyze() {
        if (this.isAnalyzing) return;
        
        const resumeText = this.resumeTextarea.value.trim();
        const jobText = this.jobTextarea.value.trim();
        
        // Client-side validation
        if (!this.validateInputsForAnalysis(resumeText, jobText)) {
            return;
        }
        
        // Check cache
        const cacheKey = this.generateCacheKey(resumeText, jobText);
        if (this.cache.has(cacheKey)) {
            console.log('Using cached result');
            this.displayResults(this.cache.get(cacheKey));
            return;
        }
        
        await this.performAnalysis(resumeText, jobText, cacheKey);
    }
    
    validateInputsForAnalysis(resumeText, jobText) {
        if (resumeText.length < 10) {
            this.showError('Resume text must be at least 10 characters long.');
            return false;
        }
        
        if (jobText.length < 10) {
            this.showError('Job description must be at least 10 characters long.');
            return false;
        }
        
        if (resumeText.length > 10000) {
            this.showError('Resume text is too long (maximum 10,000 characters).');
            return false;
        }
        
        if (jobText.length > 10000) {
            this.showError('Job description is too long (maximum 10,000 characters).');
            return false;
        }
        
        return true;
    }
    
    generateCacheKey(resumeText, jobText) {
        return btoa(encodeURIComponent(resumeText + '|' + jobText)).slice(0, 32);
    }
    
    async performAnalysis(resumeText, jobText, cacheKey) {
        this.isAnalyzing = true;
        this.showLoadingState();
        
        try {
            const startTime = Date.now();
            
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    resume: resumeText,
                    job_description: jobText
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Analysis failed');
            }
            
            // Ensure minimum loading time for better UX
            const elapsedTime = Date.now() - startTime;
            const minLoadingTime = 1500;
            
            if (elapsedTime < minLoadingTime) {
                await new Promise(resolve => setTimeout(resolve, minLoadingTime - elapsedTime));
            }
            
            // Cache the result
            this.cache.set(cacheKey, data);
            
            this.displayResults(data);
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.showError(error.message || 'Failed to analyze compatibility. Please try again.');
        } finally {
            this.isAnalyzing = false;
        }
    }
    
    showLoadingState() {
        this.hideAllSections();
        this.loadingSection.style.display = 'block';
        this.loadingSection.classList.add('fade-in');
        
        // Animate progress bar
        this.animateProgress();
    }
    
    animateProgress() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 95) {
                progress = 95;
                clearInterval(interval);
            }
            
            this.progressFill.style.width = `${progress}%`;
            this.progressText.textContent = `${Math.round(progress)}%`;
        }, 200);
        
        // Store interval ID for cleanup
        this.progressInterval = interval;
    }
    
    displayResults(data) {
        this.hideAllSections();
        this.resultsSection.style.display = 'block';
        this.resultsSection.classList.add('slide-up');
        
        // Clear progress interval
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        // Display main score
        const scorePercentage = Math.round(data.compatibility_score * 100);
        this.scoreValue.textContent = `${scorePercentage}%`;
        this.compatibilityLevel.textContent = data.compatibility_level;
        this.improvementPotential.innerHTML = `<i class="fas fa-arrow-up"></i>Potential improvement: ${data.improvement_potential}`;
        
        // Animate score circle
        this.animateScoreCircle(scorePercentage);
        
        // Display detailed analysis
        this.displaySkillBreakdown(data.detailed_analysis.skill_matches);
        this.displayMatchBreakdown(data.detailed_analysis);
        this.displayRecommendations(data.recommendations);
        
        // Set compatibility level color
        this.setCompatibilityLevelColor(scorePercentage);
    }
    
    animateScoreCircle(percentage) {
        // Create animated circular progress
        const circumference = 2 * Math.PI * 90; // Assuming 90px radius
        const strokeDasharray = circumference;
        const strokeDashoffset = circumference - (percentage / 100) * circumference;
        
        // Apply gradient based on score
        let gradientColors;
        if (percentage >= 80) {
            gradientColors = 'from 0deg, #10b981 0%, #059669 100%';
        } else if (percentage >= 60) {
            gradientColors = 'from 0deg, #2563eb 0%, #1d4ed8 100%';
        } else if (percentage >= 40) {
            gradientColors = 'from 0deg, #f59e0b 0%, #d97706 100%';
        } else {
            gradientColors = 'from 0deg, #ef4444 0%, #dc2626 100%';
        }
        
        this.scoreCircle.style.background = `conic-gradient(${gradientColors})`;
    }
    
    setCompatibilityLevelColor(percentage) {
        let colorClass;
        if (percentage >= 80) {
            colorClass = 'var(--success-color)';
        } else if (percentage >= 60) {
            colorClass = 'var(--primary-color)';
        } else if (percentage >= 40) {
            colorClass = 'var(--warning-color)';
        } else {
            colorClass = 'var(--error-color)';
        }
        
        this.compatibilityLevel.style.color = colorClass;
    }
    
    displaySkillBreakdown(skillMatches) {
        this.skillBreakdown.innerHTML = '';
        
        for (const [category, percentage] of Object.entries(skillMatches)) {
            const skillItem = document.createElement('div');
            skillItem.className = 'skill-item';
            
            const numericPercentage = parseInt(percentage.replace('%', ''));
            let levelClass;
            if (numericPercentage >= 80) levelClass = 'excellent';
            else if (numericPercentage >= 60) levelClass = 'good';
            else if (numericPercentage >= 40) levelClass = 'fair';
            else levelClass = 'poor';
            
            skillItem.innerHTML = `
                <span class="skill-name">${category}</span>
                <span class="skill-percentage ${levelClass}">${percentage}</span>
            `;
            
            this.skillBreakdown.appendChild(skillItem);
        }
    }
    
    displayMatchBreakdown(detailedAnalysis) {
        const matchData = [
            { label: 'Experience Match', value: detailedAnalysis.experience_match, icon: 'fas fa-briefcase' },
            { label: 'Text Similarity', value: detailedAnalysis.text_similarity, icon: 'fas fa-align-left' }
        ];
        
        this.matchBreakdown.innerHTML = '';
        
        matchData.forEach(item => {
            const matchItem = document.createElement('div');
            matchItem.className = 'match-item';
            
            matchItem.innerHTML = `
                <span class="match-label">
                    <i class="${item.icon}"></i>
                    ${item.label}
                </span>
                <span class="match-value">${item.value}</span>
            `;
            
            this.matchBreakdown.appendChild(matchItem);
        });
    }
    
    displayRecommendations(recommendations) {
        this.recommendationsList.innerHTML = '';
        
        if (!recommendations || recommendations.length === 0) {
            this.recommendationsList.innerHTML = '<p class="text-center">No specific recommendations available.</p>';
            return;
        }
        
        recommendations.forEach(rec => {
            const recItem = document.createElement('div');
            recItem.className = `recommendation-item ${rec.priority.toLowerCase()}`;
            
            recItem.innerHTML = `
                <div class="recommendation-header">
                    <span class="recommendation-category">${rec.category}</span>
                    <span class="priority-badge ${rec.priority.toLowerCase()}">${rec.priority}</span>
                </div>
                <p class="recommendation-text">${rec.suggestion}</p>
                <p class="recommendation-impact">${rec.impact}</p>
            `;
            
            this.recommendationsList.appendChild(recItem);
        });
    }
    
    showError(message) {
        this.hideAllSections();
        this.errorSection.style.display = 'block';
        this.errorSection.classList.add('fade-in');
        this.errorMessage.textContent = message;
    }
    
    hideAllSections() {
        const sections = [this.loadingSection, this.resultsSection, this.errorSection];
        sections.forEach(section => {
            section.style.display = 'none';
            section.classList.remove('fade-in', 'slide-up');
        });
    }
    
    resetForm() {
        this.resumeTextarea.value = '';
        this.jobTextarea.value = '';
        this.updateCharCount(this.resumeTextarea, this.resumeCharCount);
        this.updateCharCount(this.jobTextarea, this.jobCharCount);
        this.hideAllSections();
        this.inputSection.scrollIntoView({ behavior: 'smooth' });
        this.validateInputs();
    }
    
    exportResults() {
        const results = this.getCurrentResults();
        if (!results) {
            alert('No results to export');
            return;
        }
        
        const exportData = {
            timestamp: new Date().toISOString(),
            resume_snippet: this.resumeTextarea.value.slice(0, 200) + '...',
            job_snippet: this.jobTextarea.value.slice(0, 200) + '...',
            ...results
        };
        
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `compatibility-analysis-${new Date().toISOString().slice(0, 10)}.json`;
        link.click();
    }
    
    getCurrentResults() {
        if (this.resultsSection.style.display === 'none') {
            return null;
        }
        
        return {
            compatibility_score: this.scoreValue.textContent,
            compatibility_level: this.compatibilityLevel.textContent,
            improvement_potential: this.improvementPotential.textContent
        };
    }
    
    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + Enter to analyze
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!this.isAnalyzing) {
                this.handleAnalyze();
            }
        }
        
        // Escape to reset
        if (e.key === 'Escape') {
            e.preventDefault();
            this.resetForm();
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const analyzer = new CompatibilityAnalyzer();
    
    // Global error handler
    window.addEventListener('error', (e) => {
        console.error('Global error:', e.error);
        analyzer.showError('An unexpected error occurred. Please refresh the page and try again.');
    });
    
    // Handle network errors
    window.addEventListener('online', () => {
        console.log('Connection restored');
    });
    
    window.addEventListener('offline', () => {
        analyzer.showError('Network connection lost. Please check your internet connection.');
    });
});
