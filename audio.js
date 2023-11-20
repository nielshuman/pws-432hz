let currentSong = 0;
let song_order = [];
let votes = [];

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      let j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array
  }

fetch('/audio.yml').then(r=>r.text()).then(t => {
    const audio = jsyaml.load(t);
    song_order = shuffle(audio.slice(0)).slice(0, 20);

    $('#audioa').dataset.url = song_order[currentSong].a.filename;
    $('#audiob').dataset.url = song_order[currentSong].b.filename;

});

function switchSong(n) {
    currentSong = n;
    $('#audioa').dataset.url = song_order[currentSong].a.filename;
    $('#audiob').dataset.url = song_order[currentSong].b.filename;
    refreshView();
    return true;
}

function nextSong() {
    if (currentSong < song_order.length - 1) {
        switchSong(currentSong + 1);
        return true;
    } else {
        return false;
    }
}

function previousSong() {
    if (currentSong > 0) {
        switchSong(currentSong - 1);
        return true;
    } else {
        return false;
    }
}

$('#buttona').addEventListener('click', () => {
    votes[currentSong] = {
         song: song_order[currentSong],
         vote: song_order[currentSong].a
    }
    nextSong();
});

$('#buttonb').addEventListener('click', () => {
    votes[currentSong] = {
        song: song_order[currentSong],
        vote: song_order[currentSong].b
   }
   nextSong();
});