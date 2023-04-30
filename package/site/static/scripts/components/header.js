
// Declare elements
let timeContentEl = document.getElementById('time-content');
let dateContentEl = document.getElementById('date-content');
let hamburgerMenuContainer = document.querySelector('menu')
let hamburgerBtn = document.getElementById('hamburger_menu-btn');

hamburgerBtn.addEventListener('click', function() {
    hamburgerMenuContainer.toggleAttribute('data-open')
})
function toggleHamburgerMenu(state) {
    hamburgerMenuContainer.setAttribute('data-open', state);
}

async function setDatetime() {
    let response = await fetch(dtApiUrl);
    let datetime = await response.json();

    timeContentEl.innerText = datetime.time;
    dateContentEl.innerText = datetime.date;
}

// Intervals
setInterval(function () {
    setDatetime();
}, 250);
