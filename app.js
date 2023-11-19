const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

let currentView = 0;
const views = $$('.view');
views[currentView].style.display = 'flex';
views[currentView].classList.add('active');


function nextView() {
    if (currentView < views.length - 1) {
        switchView(currentView + 1);
        return true;
    } else {
        return false;
    }
}

const switchView = (n) => {
    Essential_Audio.Stop()
    views[currentView].classList.remove('active');
    console.log(views[currentView].style.transition)
    setTimeout(() => {
        views[currentView].style.display = 'none';
        currentView = n;
        views[n].style.display = 'flex';
        setTimeout(() => {
            views[n].classList.add('active');
            Essential_Audio.init();
        }, 100);
    }, 400);
};

// nextView();