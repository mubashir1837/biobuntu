// BioBuntu Web Dashboard JavaScript

let currentView = 'dashboard';
let refreshInterval;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    startAutoRefresh();
});

function initializeApp() {
    showLoading('Loading dashboard...');
    loadWorkflows();
    loadProjects();
    loadStatus();
    loadRemoteJobs();
    hideLoading();
}

function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const view = this.dataset.view;
            switchView(view);
        });
    });

    // Modal close on outside click
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            hideAllModals();
        }
    });

    // File input change
    document.getElementById('file-input').addEventListener('change', handleFileSelection);

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'r':
                    e.preventDefault();
                    refreshAll();
                    break;
                case 'n':
                    e.preventDefault();
                    showCreateProject();
                    break;
            }
        }
    });
}

function startAutoRefresh() {
    refreshInterval = setInterval(() => {
        if (currentView === 'dashboard' || currentView === 'jobs') {
            loadRemoteJobs();
        }
    }, 5000);
}

function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
}

function switchView(view) {
    currentView = view;

    // Update navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-view="${view}"]`).classList.add('active');

    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });

    // Show selected section
    const targetSection = document.getElementById(`${view}-section`);
    if (targetSection) {
        targetSection.style.display = 'block';
    }

    // Load view-specific data
    switch(view) {
        case 'projects':
            loadProjects();
            break;
        case 'workflows':
            loadWorkflows();
            break;
        case 'jobs':
            loadRemoteJobs();
            break;
        case 'dashboard':
            loadAllData();
            break;
    }
}

function loadAllData() {
    loadWorkflows();
    loadProjects();
    loadStatus();
    loadRemoteJobs();
}

function refreshAll() {
    showLoading('Refreshing...');
    loadAllData();
    setTimeout(hideLoading, 500);
}

function showLoading(message = 'Loading...') {
    const loading = document.getElementById('loading-overlay') || createLoadingOverlay();
    loading.querySelector('.loading-text').textContent = message;
    loading.style.display = 'flex';
}

function hideLoading() {
    const loading = document.getElementById('loading-overlay');
    if (loading) {
        loading.style.display = 'none';
    }
}

function createLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <span class="loading-text">Loading...</span>
        </div>
    `;
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;
    document.body.appendChild(overlay);
    return overlay;
}

function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="btn-small">×</button>
    `;

    const container = document.querySelector('.container');
    container.insertBefore(alert, container.firstChild);

    setTimeout(() => {
        if (alert.parentElement) {
            alert.remove();
        }
    }, 5000);
}

async function loadWorkflows() {
    try {
        const response = await fetch('/api/workflows');
        const data = await response.json();

        const workflowsDiv = document.getElementById('workflows-list');
        const select = document.getElementById('workflow-select');

        if (!workflowsDiv || !select) return;

        workflowsDiv.innerHTML = '';
        select.innerHTML = '<option value="">Select Workflow</option>';

        if (data.length === 0) {
            workflowsDiv.innerHTML = '<p class="text-center">No workflows available</p>';
            return;
        }

        data.forEach(workflow => {
            // Display list
            const div = document.createElement('div');
            div.className = 'workflow-item';
            div.innerHTML = `
                <div class="workflow-name">${workflow.name}</div>
                <div class="workflow-description">${workflow.description || 'No description available'}</div>
                <div class="mt-1">
                    <button class="btn btn-small" onclick="viewWorkflowDetails('${workflow.file}')">View Details</button>
                </div>
            `;
            workflowsDiv.appendChild(div);

            // Populate select
            const option = document.createElement('option');
            option.value = workflow.file;
            option.textContent = workflow.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading workflows:', error);
        showAlert('Failed to load workflows', 'error');
    }
}

async function loadProjects() {
    try {
        const response = await fetch('/api/projects');
        const data = await response.json();

        const projectsDiv = document.getElementById('projects-list');
        const select = document.getElementById('project-select');

        if (!projectsDiv || !select) return;

        projectsDiv.innerHTML = '';
        select.innerHTML = '<option value="">Select Project</option>';

        if (data.length === 0) {
            projectsDiv.innerHTML = '<p class="text-center">No projects found. <button class="btn btn-small" onclick="showCreateProject()">Create your first project</button></p>';
            return;
        }

        data.forEach(project => {
            // Display list
            const div = document.createElement('div');
            div.className = 'project-item';
            div.innerHTML = `
                <div class="project-header">
                    <div>
                        <div class="project-name">${project.name}</div>
                        <div class="project-description">${project.description || 'No description'}</div>
                    </div>
                    <div class="flex gap-2">
                        <button class="btn btn-small btn-secondary" onclick="viewProjectDetails('${project.name}')">View</button>
                        <button class="btn btn-small btn-danger" onclick="deleteProject('${project.name}')">Delete</button>
                    </div>
                </div>
            `;
            projectsDiv.appendChild(div);

            // Populate select
            const option = document.createElement('option');
            option.value = project.name;
            option.textContent = project.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading projects:', error);
        showAlert('Failed to load projects', 'error');
    }
}

async function loadStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        const statusDiv = document.getElementById('status-content');
        if (statusDiv) {
            statusDiv.innerHTML = `
                <div class="mb-2"><strong>Status:</strong> <span class="status-${data.status || 'unknown'}">${data.status || 'Unknown'}</span></div>
                <div class="mb-2"><strong>Version:</strong> ${data.version || 'Unknown'}</div>
                <div class="mb-2"><strong>Python:</strong> ${data.python_version || 'Unknown'}</div>
                <div><strong>Uptime:</strong> ${data.uptime || 'Unknown'}</div>
            `;
        }
    } catch (error) {
        console.error('Error loading status:', error);
        showAlert('Failed to load system status', 'error');
    }
}

async function loadRemoteJobs() {
    try {
        const response = await fetch('/api/remote/jobs');
        const data = await response.json();

        const jobsDiv = document.getElementById('remote-jobs-list');
        if (!jobsDiv) return;

        jobsDiv.innerHTML = '';

        if (data.length === 0) {
            jobsDiv.innerHTML = '<p class="text-center">No remote jobs found</p>';
            return;
        }

        data.forEach(job => {
            const div = document.createElement('div');
            div.className = 'job-item';
            div.innerHTML = `
                <div class="job-header">
                    <div>
                        <div class="project-name">Job ID: ${job.job_id || 'N/A'}</div>
                        <div class="project-description">
                            Workflow: ${job.workflow} | Project: ${job.project}
                        </div>
                    </div>
                    <span class="status status-${job.status || 'unknown'}">${job.status || 'Unknown'}</span>
                </div>
                ${job.progress !== undefined ? `
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${job.progress}%"></div>
                    </div>
                    <div class="text-right">${job.progress}% complete</div>
                ` : ''}
                ${job.error ? `<div class="alert alert-error mt-1">${job.error}</div>` : ''}
                ${job.started_at ? `<div class="mt-1"><small>Started: ${new Date(job.started_at).toLocaleString()}</small></div>` : ''}
                ${job.completed_at ? `<div class="mt-1"><small>Completed: ${new Date(job.completed_at).toLocaleString()}</small></div>` : ''}
                <div class="mt-1">
                    <button class="btn btn-small" onclick="viewJobDetails('${job.job_id}')">Details</button>
                    ${job.status === 'running' ? '<button class="btn btn-small btn-warning" onclick="cancelJob(\'' + job.job_id + '\')">Cancel</button>' : ''}
                </div>
            `;
            jobsDiv.appendChild(div);
        });
    } catch (error) {
        console.error('Error loading remote jobs:', error);
        showAlert('Failed to load remote jobs', 'error');
    }
}

async function runPipeline() {
    const project = document.getElementById('project-select').value;
    const workflow = document.getElementById('workflow-select').value;
    const files = document.getElementById('file-input').files;

    if (!project || !workflow) {
        showAlert('Please select both project and workflow', 'warning');
        return;
    }

    const btn = document.querySelector('button[onclick="runPipeline()"]');
    const originalText = btn.textContent;
    btn.textContent = 'Running...';
    btn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('project', project);
        formData.append('workflow', workflow);
        for (let file of files) {
            formData.append('input_files', file);
        }

        const response = await fetch('/api/run', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(data.message || 'Pipeline started successfully', 'success');
            loadRemoteJobs();
        } else {
            showAlert(data.error || 'Failed to start pipeline', 'error');
        }
    } catch (error) {
        console.error('Error running pipeline:', error);
        showAlert('Failed to start pipeline', 'error');
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
}

async function runRemotePipeline() {
    const project = document.getElementById('project-select').value;
    const workflow = document.getElementById('workflow-select').value;
    const callbackUrl = document.getElementById('callback-url').value;

    if (!project || !workflow) {
        showAlert('Please select both project and workflow', 'warning');
        return;
    }

    const btn = document.querySelector('button[onclick="runRemotePipeline()"]');
    const originalText = btn.textContent;
    btn.textContent = 'Submitting...';
    btn.disabled = true;

    try {
        const response = await fetch('/api/remote/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                project: project,
                workflow: workflow,
                callback_url: callbackUrl || undefined
            })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(data.message || 'Remote job submitted successfully', 'success');
            loadRemoteJobs();
        } else {
            showAlert(data.error || 'Failed to submit remote job', 'error');
        }
    } catch (error) {
        console.error('Error submitting remote job:', error);
        showAlert('Failed to submit remote job', 'error');
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
}

function handleFileSelection(e) {
    const files = e.target.files;
    const fileList = document.getElementById('file-list');

    if (fileList) {
        fileList.innerHTML = '';
        for (let file of files) {
            const li = document.createElement('li');
            li.textContent = `${file.name} (${formatFileSize(file.size)})`;
            fileList.appendChild(li);
        }
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showCreateProject() {
    document.getElementById('create-project-modal').style.display = 'flex';
    document.getElementById('project-name').focus();
}

function hideCreateProject() {
    document.getElementById('create-project-modal').style.display = 'none';
    document.getElementById('project-name').value = '';
    document.getElementById('project-desc').value = '';
}

function hideAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

async function createProject() {
    const name = document.getElementById('project-name').value.trim();
    const desc = document.getElementById('project-desc').value.trim();

    if (!name) {
        showAlert('Project name is required', 'warning');
        return;
    }

    const btn = document.querySelector('#create-project-modal .btn:not(.btn-secondary)');
    const originalText = btn.textContent;
    btn.textContent = 'Creating...';
    btn.disabled = true;

    try {
        const response = await fetch('/api/projects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                description: desc
            })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(data.message || 'Project created successfully', 'success');
            hideCreateProject();
            loadProjects();
        } else {
            showAlert(data.error || 'Failed to create project', 'error');
        }
    } catch (error) {
        console.error('Error creating project:', error);
        showAlert('Failed to create project', 'error');
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
}

async function deleteProject(name) {
    if (!confirm(`Are you sure you want to delete project "${name}"? This action cannot be undone.`)) {
        return;
    }

    try {
        const response = await fetch(`/api/projects/${name}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(data.message || 'Project deleted successfully', 'success');
            loadProjects();
        } else {
            showAlert(data.error || 'Failed to delete project', 'error');
        }
    } catch (error) {
        console.error('Error deleting project:', error);
        showAlert('Failed to delete project', 'error');
    }
}

function viewProjectDetails(name) {
    // TODO: Implement project details view
    showAlert('Project details view coming soon!', 'info');
}

function viewWorkflowDetails(filename) {
    // TODO: Implement workflow details view
    showAlert('Workflow details view coming soon!', 'info');
}

function viewJobDetails(jobId) {
    // TODO: Implement job details view
    showAlert('Job details view coming soon!', 'info');
}

function cancelJob(jobId) {
    // TODO: Implement job cancellation
    showAlert('Job cancellation coming soon!', 'info');
}

// Keyboard shortcuts help
function showKeyboardShortcuts() {
    const shortcuts = `
        <h4>Keyboard Shortcuts</h4>
        <ul>
            <li><kbd>Ctrl+R</kbd> - Refresh all data</li>
            <li><kbd>Ctrl+N</kbd> - Create new project</li>
            <li><kbd>Esc</kbd> - Close modals</li>
        </ul>
    `;

    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h3>Keyboard Shortcuts</h3>
            ${shortcuts}
            <div class="text-center mt-2">
                <button class="btn" onclick="this.closest('.modal').remove()">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    modal.style.display = 'flex';
}

// Add ESC key handler
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        hideAllModals();
    }
});