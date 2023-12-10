const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
if (!isSafari) {
    let scriptEle = document.createElement("script");
    scriptEle.setAttribute("src", "https://code.getmdl.io/1.3.0/material.min.js");
    document.body.appendChild(scriptEle);
    $('#audioa').dataset.preload = true;
    $('#audiob').dataset.preload = true;
}
