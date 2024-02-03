function showContent(contentId) {
    const containers = document.querySelectorAll('.container');
    containers.forEach(container => {
        container.classList.remove('active-container');
    });
    document.getElementById(contentId).classList.add('active-container');
}

// Add an event listener to show the "Home" page by default
document.addEventListener('DOMContentLoaded', function() {
    showContent('info');
});