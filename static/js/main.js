// ==================== PROGRESS TRACKING ====================

/**
 * Toggle step completion status via AJAX
 */
function toggleStepProgress(stepId, checkbox) {
    fetch(`/user/progress/${stepId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update progress bar
                const progressBar = document.querySelector('.progress-bar');
                const progressText = document.querySelector('.progress-text');

                if (progressBar) {
                    progressBar.style.width = data.progress + '%';
                }

                if (progressText) {
                    progressText.textContent = data.progress + '%';
                }

                // Update step item styling
                const stepItem = checkbox.closest('.step-item');
                if (data.completed) {
                    stepItem.classList.add('completed');
                } else {
                    stepItem.classList.remove('completed');
                }

                // Show toast notification
                showToast(
                    data.completed ? 'Step completed! 🎉' : 'Step marked as incomplete',
                    data.completed ? 'success' : 'info'
                );
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Failed to update progress. Please try again.', 'danger');
            // Revert checkbox state
            checkbox.checked = !checkbox.checked;
        });
}

// ==================== TOAST NOTIFICATIONS ====================

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Remove existing toasts
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    // Add styles
    Object.assign(toast.style, {
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        padding: '1rem 1.5rem',
        borderRadius: '12px',
        color: '#fff',
        fontWeight: '600',
        zIndex: '9999',
        animation: 'slideInRight 0.3s ease',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)'
    });

    // Set background based on type
    const backgrounds = {
        success: 'linear-gradient(135deg, #00FF94, #00D9FF)',
        danger: 'linear-gradient(135deg, #FF3366, #FF1744)',
        info: 'linear-gradient(135deg, #00D9FF, #B026FF)',
        warning: 'linear-gradient(135deg, #FFB800, #FF6B00)'
    };
    toast.style.background = backgrounds[type] || backgrounds.info;

    // Add to document
    document.body.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== CONFIRMATION DIALOGS ====================

/**
 * Show confirmation dialog before delete actions
 */
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this? This action cannot be undone.');
}

// ==================== SMOOTH SCROLL ====================

/**
 * Smooth scroll to element
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// ==================== SEARCH & FILTER ====================

/**
 * Filter roadmaps by category
 */
function filterByCategory(category) {
    const url = new URL(window.location);
    url.searchParams.set('category', category);
    window.location.href = url.toString();
}

/**
 * Search roadmaps
 */
function searchRoadmaps(query) {
    const url = new URL(window.location);
    if (query) {
        url.searchParams.set('search', query);
    } else {
        url.searchParams.delete('search');
    }
    window.location.href = url.toString();
}

// ==================== FORM VALIDATION ====================

/**
 * Validate form before submission
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = '#FF3366';
        } else {
            input.style.borderColor = '';
        }
    });

    if (!isValid) {
        showToast('Please fill in all required fields', 'danger');
    }

    return isValid;
}

// ==================== DYNAMIC STEP MANAGEMENT ====================

let stepCounter = 0;

/**
 * Add new step input fields (for admin roadmap creation)
 */
function addStepField() {
    stepCounter++;
    const container = document.getElementById('steps-container');
    if (!container) return;

    const stepDiv = document.createElement('div');
    stepDiv.className = 'step-field card mb-3';
    stepDiv.id = `step-${stepCounter}`;
    stepDiv.innerHTML = `
        <div class="card-header flex-between">
            <h5>Step ${stepCounter}</h5>
            <button type="button" class="btn btn-danger btn-sm" onclick="removeStepField(${stepCounter})">
                Remove
            </button>
        </div>
        <div class="card-body">
            <div class="form-group">
                <label class="form-label">Step Title *</label>
                <input type="text" name="step_title_${stepCounter}" class="form-control" required>
            </div>
            <div class="form-group">
                <label class="form-label">Step Description *</label>
                <textarea name="step_description_${stepCounter}" class="form-control" rows="3" required></textarea>
            </div>
            <div class="form-group">
                <label class="form-label">Resources (one per line)</label>
                <textarea name="step_resources_${stepCounter}" class="form-control" rows="2"></textarea>
            </div>
        </div>
    `;

    container.appendChild(stepDiv);
}

/**
 * Remove step input field
 */
function removeStepField(stepId) {
    const stepDiv = document.getElementById(`step-${stepId}`);
    if (stepDiv) {
        stepDiv.remove();
    }
}

// ==================== AUTO-DISMISS ALERTS ====================

/**
 * Auto-dismiss flash messages after 5 seconds
 */
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Add slideOut animation
const slideOutStyle = document.createElement('style');
slideOutStyle.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(-100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(slideOutStyle);

// ==================== ACTIVE NAV LINK ====================

/**
 * Highlight active navigation link
 */
document.addEventListener('DOMContentLoaded', function () {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// ==================== PROGRESS BAR ANIMATION ====================

/**
 * Animate progress bars on page load
 */
document.addEventListener('DOMContentLoaded', function () {
    const progressBars = document.querySelectorAll('.progress-bar');

    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';

        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 100);
    });
});

// ==================== COPY TO CLIPBOARD ====================

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy', 'danger');
    });
}

// ==================== KEYBOARD SHORTCUTS ====================

/**
 * Handle keyboard shortcuts
 */
document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + K for search focus
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// ==================== EXPORT FUNCTIONS ====================

// Make functions available globally
window.toggleStepProgress = toggleStepProgress;
window.showToast = showToast;
window.confirmDelete = confirmDelete;
window.smoothScrollTo = smoothScrollTo;
window.filterByCategory = filterByCategory;
window.searchRoadmaps = searchRoadmaps;
window.validateForm = validateForm;
window.addStepField = addStepField;
window.removeStepField = removeStepField;
window.copyToClipboard = copyToClipboard;

console.log('🚀 Learn with AK - JavaScript loaded successfully!');
