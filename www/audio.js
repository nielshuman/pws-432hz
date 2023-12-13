let currentSong;
let song_order = [];
let votes = [];
const AMOUNT_OF_SONGS = 8;
const COLLECTION = 'votes';
let formLoads = 0;


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
    let shuffled = shuffle(audio.slice(0));
    // make sure the are no songs with the same title
    console.log(shuffled.length);
    shuffled = shuffled.filter((v, i, a) => a.findIndex(t => (t.title === v.title)) === i);
    console.log(shuffled.length);
    song_order = shuffled.slice(0, AMOUNT_OF_SONGS);
    switchSong(0);
});

function switchSong(n) {
    currentSong = n;
    try {$('#progress').MaterialProgress.setProgress(((currentSong) / song_order.length) * 100);} catch(e) {}   
    $('#audioa').dataset.url = song_order[currentSong].a.filename;
    $('#audiob').dataset.url = song_order[currentSong].b.filename;
    $('#progresstext').innerHTML = `${currentSong} / ${song_order.length}`;
    if (currentView != 0) refreshView();
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

function submitVote(v) {
    db.collection(COLLECTION).add({
        song_title: song_order[currentSong].title, 
        cat: song_order[currentSong].cat,
        cat2: song_order[currentSong].cat2,
        vote: v
    });
    nextSong();
}


$('#buttona').addEventListener('click', () => {
    submitVote(song_order[currentSong].a.cat);
});

$('#buttonb').addEventListener('click', () => {
    submitVote(song_order[currentSong].b.cat);
});

$('#buttonx').addEventListener('click', () => {
    submitVote('x');
});

$('#gform').addEventListener('load', (e) => {
    formLoads++;
    if (formLoads > 1) {
        nextView();
    }
});