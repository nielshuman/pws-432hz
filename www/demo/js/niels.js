let numEl = document.getElementById('num');
let num = 432;
let audio = [];
let currentVariant = 432;

let DELAY = 50

let currentSong = {};
let songIndex = -1;
let el432 = new Audio();
let el440 = new Audio();

function change_text(target, interval) {
  numEl.innerHTML = num + ' Hz';
  if (num == target) return;
  if (num < target) {
    num++;
    setTimeout(change_text, interval, target, interval*1.3);
  }
  else {
    num--;
    setTimeout(change_text, interval, target, interval*1.3);
  }
}

function to432() {
    if (currentVariant == 432) return;
    if (num != currentVariant) return;
    currentVariant = 432;

    el440.pause();
    el432.currentTime = el440.currentTime * (el432.duration / el440.duration);
    el432.play();

    change_text(432, DELAY);
    setTimeout(start, 0);
  }
  
  function to440() {
    if (currentVariant == 440) return;
    if (num != currentVariant) return;
    currentVariant = 440;

    el432.pause();
    el440.currentTime = el432.currentTime * (el440.duration / el432.duration);
    el440.play();

    change_text(440, 75);
    stop();
  }

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array
}

fetch('/audio.yml').then(r=>r.text()).then(t => {
    audio = shuffle(jsyaml.load(t));
    nextSong();
});

function nextSong() {
  el432.pause();
  el440.pause();
  if (songIndex < audio.length - 1) {
      songIndex++;
      currentSong = audio[songIndex];
  }

  if (currentSong.cat != '440-432') return nextSong();

  if (currentSong.a.cat == '432') {
    el432 = new Audio('/' + currentSong.a.filename);
    el440 = new Audio('/' + currentSong.b.filename);
  } else if (currentSong.b.cat == '432') {
    el432 = new Audio('/' + currentSong.b.filename);
    el440 = new Audio('/' + currentSong.a.filename);
  }

  play()
}

function play() {
  if (currentVariant == 432) {
    el432.play();
  } else {
    el440.play();
  }
}

// add key event listeners, l for 432, h for 440, space for next song
document.addEventListener('keydown', function(event) {
  if (event.key === 'l') {
    to432();
  }
  else if (event.key === 'h') {
    to440();
  }
  else if (event.key === ' ') {
    nextSong();
  }
});