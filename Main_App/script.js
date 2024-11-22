document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;

    if (email && password && firstName && lastName) {
        window.location.href = 'signup2.html';
    } else {
        alert('Please fill in all fields.');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.navigate').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');

            fetch(href)
                .then(response => response.text())
                .then(html => {
                    // Parse the new HTML
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');

                    // Replace the entire document's html
                    document.documentElement.innerHTML = doc.documentElement.innerHTML;

                    // Scroll to the top of the page
                    window.scrollTo(0, 0);

                    // Scroll to the target section if specified in the link
                    const targetId = href.split('#')[1];
                    if (targetId) {
                        document.getElementById(targetId).scrollIntoView({
                            behavior: 'smooth'
                        });
                    }
                })
                .catch(error => console.error('Error fetching content:', error));
        });
    });
});
