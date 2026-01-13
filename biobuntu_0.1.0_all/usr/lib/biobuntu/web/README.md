# BioBuntu Web Interface

The BioBuntu web dashboard provides a modern, responsive interface for managing bioinformatics workflows and projects.

## Features

### 🎨 Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark/Light Theme Support**: Automatic theme detection
- **Professional Styling**: Clean, modern interface with consistent branding
- **Loading States**: Visual feedback for all operations
- **Error Handling**: User-friendly error messages and alerts

### 🧭 Navigation
- **Tabbed Interface**: Easy switching between different sections
- **Breadcrumb Navigation**: Clear indication of current location
- **Keyboard Shortcuts**: Quick access to common actions
- **Contextual Actions**: Relevant buttons based on current view

### 📊 Dashboard
- **System Overview**: Real-time status and system information
- **Quick Actions**: Fast access to common tasks
- **Recent Activity**: Latest projects and jobs
- **Statistics**: Usage metrics and system health

### 📁 Project Management
- **Project Creation**: Easy project setup with validation
- **Project Listing**: Overview of all projects with status
- **Project Details**: Comprehensive project information
- **Bulk Operations**: Manage multiple projects efficiently

### ⚙️ Workflow Management
- **Workflow Browser**: Explore available analysis pipelines
- **Workflow Details**: Step-by-step workflow information
- **Validation**: Check workflow compatibility
- **Favorites**: Save frequently used workflows

### ▶️ Pipeline Execution
- **Local Execution**: Run pipelines directly on the server
- **Remote Execution**: Submit jobs to distributed workers
- **File Upload**: Drag-and-drop file selection
- **Progress Tracking**: Real-time execution monitoring
- **Callback Integration**: Webhook notifications for job completion

### 🔄 Job Monitoring
- **Job Queue**: View all active and completed jobs
- **Status Updates**: Live status changes
- **Progress Bars**: Visual progress indication
- **Error Reporting**: Detailed error information
- **Job History**: Complete execution history

### ℹ️ System Status
- **Health Checks**: System component status
- **Resource Usage**: CPU, memory, and disk monitoring
- **Version Information**: Software versions and updates
- **Configuration**: Current system settings

## Keyboard Shortcuts

- `Ctrl+R` / `Cmd+R`: Refresh all data
- `Ctrl+N` / `Cmd+N`: Create new project
- `Esc`: Close modals and dialogs

## Browser Support

- **Chrome/Edge**: Full support (recommended)
- **Firefox**: Full support
- **Safari**: Full support
- **Mobile Browsers**: Responsive design support

## API Integration

The web interface communicates with the BioBuntu REST API:

```javascript
// Example: Create a project
fetch('/api/projects', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'myproject',
        description: 'Analysis project'
    })
});
```

## Customization

### Themes
The interface supports custom themes through CSS variables:

```css
:root {
    --primary-color: #your-color;
    --background-color: #your-bg;
    /* ... other variables */
}
```

### Branding
Replace the logo and favicon in `/static/images/` to customize branding.

## Troubleshooting

### Common Issues

**Interface not loading**: Check network connectivity and API availability
**Buttons not working**: Ensure JavaScript is enabled
**Styling issues**: Clear browser cache
**Mobile display problems**: Check viewport meta tag

### Debug Mode
Enable debug mode in the browser console for detailed logging:

```javascript
localStorage.setItem('debug', 'true');
```

## Contributing

To contribute to the web interface:

1. Follow the existing CSS architecture
2. Use semantic HTML and ARIA attributes
3. Test on multiple browsers and devices
4. Maintain accessibility standards
5. Document new features in this README