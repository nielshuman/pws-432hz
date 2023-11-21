let currentSong = 0;
let song_order = [];
let votes = [];

const firebaseConfig = {
    apiKey: "AIzaSyDaf-ix7SOWU1hz3AMle-hK1NCU2e19TzU",
    authDomain: "pws432.firebaseapp.com",
    projectId: "pws432",
    storageBucket: "pws432.appspot.com",
    messagingSenderId: "596847777969",
    appId: "1:596847777969:web:0c874acbc548f3cbe62a90"
  };

firebase.initializeApp(firebaseConfig);

const db = firebase.firestore();

// add test item to firestore

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
    $('#progress').MaterialProgress.setProgress(((currentSong) / song_order.length) * 100);
    $('#progresstext').innerHTML = `${currentSong} / ${song_order.length}`;
    refreshView();
    return true;
}

function nextSong() {
    if (currentSong < song_order.length - 1) {
        switchSong(currentSong + 1);
        return true;
    } else {
        nextView();
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
    db.collection('votes').add({
        song_id: song_order[currentSong].id, 
        cat: song_order[currentSong].cat,
        vote: song_order[currentSong].a.cat
    });
    nextSong();
});

$('#buttonb').addEventListener('click', () => {
    db.collection('votes').add({
        song_id: song_order[currentSong].id, 
        cat: song_order[currentSong].cat,
        vote: song_order[currentSong].b.cat
    });
   nextSong();
});

