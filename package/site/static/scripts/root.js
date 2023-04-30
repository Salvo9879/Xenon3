// Declare elements
let dataRedirectEnabled = document.querySelectorAll('[data-redirect-enabled]');

for (var i = 0; i < dataRedirectEnabled.length; i++) {
    e = dataRedirectEnabled[i]
    e.addEventListener('click', function() {
        window.location.href = this.getAttribute('data-redirection_url')
    });
}