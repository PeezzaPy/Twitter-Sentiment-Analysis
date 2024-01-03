function setActiveLink(linkId) {
    // Remove active class from all links
    document.querySelectorAll('.nav-links a').forEach(function(link) {
        link.classList.remove('active');
    })

    // Add active class to the current page link
    document.getElementById(linkId).classList.add('active');
}