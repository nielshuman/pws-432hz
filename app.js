const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);


const views = $$('.view');

let currentView = 0;
function nextView() {
    if (currentView < views.length - 1) {
        switchView(currentView + 1);
    }
}

switchView = (n) => {
    views[currentView].classList.remove('active');
    console.log(views[currentView].style.transition)
    setTimeout(() => {
        views[currentView].style.display = 'none';
        currentView = n;
        views[n].style.display = 'block';
        setTimeout(() => {
            views[n].classList.add('active');
        }, 100);
    }, 400);
};

// nextView();