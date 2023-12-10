const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

let currentView = 0;

const views = $$('.view');
views[currentView].style.display = 'flex';
views[currentView].classList.add('active');

const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
if (!isSafari) {
    let scriptEle = document.createElement("script");
    scriptEle.setAttribute("src", "https://code.getmdl.io/1.3.0/material.min.js");
    document.body.appendChild(scriptEle);
    $('#audioa').dataset.preload = true;
    $('#audiob').dataset.preload = true;
}

if (isSafari) {
    $('progress').style.display = 'none';
}
    

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

function refreshView() {
    switchView(currentView);
}

// switchView(0);

// nextView();