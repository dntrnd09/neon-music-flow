
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NEON — Music Player</title>

<style>
:root {
    --accent: #a78bfa;
    --bg: #090711;
    --panel: rgba(255,255,255,.065);
}

* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    color: white;
    font-family: Inter, "Segoe UI", Arial, sans-serif;
    background:
        radial-gradient(ellipse at 15% 15%, #49218b55, transparent 45%),
        radial-gradient(ellipse at 85% 75%, #073c7355, transparent 45%),
        var(--bg);
    overflow-x: hidden;
}

.glow {
    position: fixed;
    width: 360px;
    height: 360px;
    border-radius: 50%;
    filter: blur(110px);
    opacity: .25;
    pointer-events: none;
    z-index: -1;
    animation: float 10s ease-in-out infinite alternate;
}

.glow.one { background: #923cff; top: 10%; left: -150px; }
.glow.two { background: #1877ff; right: -150px; bottom: 5%; animation-delay: -5s; }

@keyframes float {
    to { transform: translate(80px, 60px) scale(1.2); }
}

header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 23px 5%;
    border-bottom: 1px solid #ffffff12;
    backdrop-filter: blur(15px);
}

.logo {
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 3px;
}

.logo span {
    background: linear-gradient(90deg, #bd8cff, #59caff);
    color: transparent;
    background-clip: text;
}

.status {
    font-size: 11px;
    letter-spacing: 2px;
    color: #a9a0c7;
}

main {
    max-width: 1100px;
    margin: 45px auto;
    padding: 0 22px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.panel {
    background: var(--panel);
    border: 1px solid #ffffff12;
    border-radius: 24px;
    padding: 27px;
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 80px #00000020;
    min-width: 0;
}

.eyebrow {
    color: #b49aff;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: bold;
}

h1 {
    font-size: clamp(27px, 4vw, 43px);
    margin: 12px 0 5px;
    letter-spacing: -1.5px;
}

.muted { color: #9690aa; font-size: 13px; }

.art {
    width: min(100%, 285px);
    aspect-ratio: 1;
    margin: 25px auto;
    border-radius: 25px;
    position: relative;
    overflow: hidden;
    display: grid;
    place-items: center;
    background:
        radial-gradient(circle at 30% 25%, #e7c6ff, transparent 22%),
        radial-gradient(circle at 70% 75%, #168cff, transparent 35%),
        linear-gradient(135deg, #6129a8, #17152e 55%, #0b5e83);
    box-shadow: 0 15px 70px #723bda33;
}

.art::before, .art::after {
    content: "";
    position: absolute;
    border: 1px solid #ffffff40;
    border-radius: 50%;
    width: 75%;
    aspect-ratio: 1;
    transform: rotate(-25deg) scaleY(.48);
}

.art::after {
    width: 105%;
    transform: rotate(35deg) scaleY(.55);
    border-color: #9fe7ff70;
}

.disc {
    width: 46%;
    aspect-ratio: 1;
    border-radius: 50%;
    background: repeating-radial-gradient(
        circle, #14131e 0 3px, #28243a 4px 6px
    );
    border: 5px solid #302a47;
    box-shadow: 0 0 40px #a77bff55;
    display: grid;
    place-items: center;
    z-index: 1;
    animation: spin 8s linear infinite;
    animation-play-state: paused;
}

body.playing .disc { animation-play-state: running; }

.disc::after {
    content: "";
    width: 22%;
    aspect-ratio: 1;
    border-radius: 50%;
    background: linear-gradient(135deg, #e2aaff, #5f7aff);
    border: 4px solid #161324;
}

@keyframes spin { to { transform: rotate(360deg); } }

.track-title {
    font-size: 21px;
    font-weight: bold;
    overflow-wrap: anywhere;
}

.track-artist { margin-top: 5px; color: #a8a1bb; font-size: 13px; }

.progress-info {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #aaa2c2;
    margin: 23px 0 8px;
    font-variant-numeric: tabular-nums;
}

input[type=range] {
    width: 100%;
    accent-color: #b18aff;
    cursor: pointer;
}

.controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 23px;
    margin: 23px 0;
}

button {
    color: white;
    background: transparent;
    border: 0;
    cursor: pointer;
    transition: transform .2s, background .2s;
    font: inherit;
}

button:hover { transform: scale(1.08); }

.icon-btn { font-size: 24px; color: #c9c2df; }
.play-btn {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    color: #171023;
    font-size: 23px;
    background: linear-gradient(135deg, #e1b8ff, #79caff);
    box-shadow: 0 0 35px #a77bff45;
}

.volume-row {
    display: flex;
    gap: 12px;
    align-items: center;
    color: #aaa2c2;
    font-size: 13px;
}

.section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.section-title h2 { font-size: 18px; margin: 0; }

.small-btn {
    border: 1px solid #ffffff20;
    border-radius: 9px;
    padding: 9px 12px;
    font-size: 12px;
    color: #d3c5ff;
}

.file-label {
    display: block;
    border: 1px dashed #a58aff65;
    border-radius: 14px;
    padding: 17px;
    text-align: center;
    color: #c6b6ff;
    cursor: pointer;
    font-size: 13px;
    margin-bottom: 12px;
    background: #9a75ff08;
}

.file-label:hover { background: #9a75ff18; }

input[type=file] { display: none; }

.playlist {
    display: flex;
    flex-direction: column;
    gap: 7px;
    max-height: 245px;
    overflow-y: auto;
    margin-top: 15px;
}

.song {
    width: 100%;
    display: flex;
    align-items: center;
    text-align: left;
    gap: 12px;
    border-radius: 12px;
    padding: 12px;
    background: #ffffff05;
}

.song.active { background: linear-gradient(90deg, #9b70ff28, #49a9ff10); }
.song-num { color: #9489b5; font-size: 12px; width: 18px; }
.song-name { font-size: 13px; font-weight: 600; overflow-wrap: anywhere; }
.song-sub { color: #8f88a4; font-size: 11px; margin-top: 4px; }
.song-info { min-width: 0; flex: 1; }

.lyrics {
    height: 230px;
    overflow-y: auto;
    padding: 15px 5px;
    text-align: center;
    mask-image: linear-gradient(transparent, black 15%, black 85%, transparent);
}

.lyric-line {
    padding: 11px 4px;
    color: #706985;
    font-size: 14px;
    transition: .25s;
    overflow-wrap: anywhere;
}

.lyric-line.active {
    color: white;
    font-size: 19px;
    font-weight: bold;
    text-shadow: 0 0 20px #a78bfa70;
}

.lyric-editor {
    width: 100%;
    min-height: 90px;
    resize: vertical;
    border-radius: 12px;
    border: 1px solid #ffffff15;
    padding: 12px;
    background: #08071180;
    color: #ddd5f4;
    font: 12px/1.7 monospace;
}

.footer {
    color: #625b77;
    text-align: center;
    font-size: 11px;
    padding: 10px 20px 25px;
}

@media(max-width: 760px) {
    main { grid-template-columns: 1fr; margin-top: 22px; }
    header { padding: 20px; }
    .panel { padding: 21px; }
}
</style>
</head>

<body>
<div class="glow one"></div>
<div class="glow two"></div>

<header>
    <div class="logo">NEON<span> / MUSIC</span></div>
    <div class="status">PERSONAL PLAYER · 01</div>
</header>

<main>
<section class="panel">
    <div class="eyebrow">NOW PLAYING</div>
    <h1>Seu universo.<br>Sua música.</h1>
    <p class="muted">Uma experiência sonora do seu jeito.</p>

    <div class="art"><div class="disc"></div></div>

    <div class="track-title" id="title">Escolha uma música</div>
    <div class="track-artist" id="artist">Sua biblioteca pessoal</div>

    <div class="progress-info">
        <span id="current">0:00</span>
        <span id="duration">0:00</span>
    </div>
    <input id="seek" type="range" min="0" max="1000" value="0">

    <div class="controls">
        <button class="icon-btn" onclick="previous()" title="Anterior">⏮</button>
        <button class="play-btn" id="play" onclick="togglePlay()">▶</button>
        <button class="icon-btn" onclick="next()" title="Próxima">⏭</button>
    </div>

    <div class="volume-row">
        <span>VOL</span>
        <input id="volume" type="range" min="0" max="1" step="0.01" value="0.8">
        <span id="volText">80%</span>
    </div>

    <audio id="audio"></audio>
</section>

<section style="display:flex;flex-direction:column;gap:24px;min-width:0">
    <div class="panel">
        <div class="section-title">
            <h2>Biblioteca</h2>
            <span class="eyebrow" id="count">0 FAIXAS</span>
        </div>

        <label class="file-label" for="files">
            ＋ Adicionar músicas do computador
        </label>
        <input id="files" type="file" accept="audio/*" multiple>

        <div class="playlist" id="playlist">
            <p class="muted">Adicione arquivos MP3, WAV, OGG ou outros formatos compatíveis com seu navegador.</p>
        </div>
    </div>

    <div class="panel">
        <div class="section-title">
            <h2>✧ Letras</h2>
            <label class="small-btn" for="lrcFile">Abrir .LRC</label>
            <input id="lrcFile" type="file" accept=".lrc,.txt">
        </div>

        <div class="lyrics" id="lyrics">
            <div class="lyric-line active">Sua música, suas palavras.</div>
            <div class="lyric-line">Carregue um arquivo de letras .LRC</div>
            <div class="lyric-line">para acompanhar a reprodução.</div>
        </div>

        <p class="muted">Você também pode escrever suas letras abaixo.</p>
        <textarea class="lyric-editor" id="lyricEditor"
          placeholder="[00:00.00] Primeira linha&#10;[00:05.00] Segunda linha"></textarea>
        <button class="small-btn" onclick="applyLyrics()">Aplicar letras</button>
    </div>
</section>
</main>

<div class="footer">NEON MUSIC · FEITO PARA OUVIR DO SEU JEITO</div>

<script>
const audio = document.getElementById('audio');
const filesInput = document.getElementById('files');
const playlist = document.getElementById('playlist');
const seek = document.getElementById('seek');
const linesBox = document.getElementById('lyrics');

let songs = [];
let index = -1;
let lyrics = [];
let urls = [];

function timeText(seconds) {
    if (!Number.isFinite(seconds)) return '0:00';
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return m + ':' + String(s).padStart(2, '0');
}

function addSongs(files) {
    for (const file of files) {
        if (!file.type.startsWith('audio/') &&
            !/\.(mp3|wav|ogg|m4a|aac|flac|opus|webm)$/i.test(file.name)) continue;

        songs.push({
            name: file.name.replace(/\.[^.]+$/, ''),
            file,
            url: URL.createObjectURL(file)
        });
    }
    renderPlaylist();

    if (index === -1 && songs.length) loadSong(0);
}

filesInput.addEventListener('change', e => {
    addSongs(e.target.files);
    filesInput.value = '';
});

function renderPlaylist() {
    document.getElementById('count').textContent =
        songs.length + (songs.length === 1 ? ' FAIXA' : ' FAIXAS');

    playlist.innerHTML = '';

    if (!songs.length) {
        playlist.innerHTML = '<p class="muted">Sua biblioteca está vazia.</p>';
        return;
    }

    songs.forEach((song, i) => {
        const button = document.createElement('button');
        button.className = 'song' + (i === index ? ' active' : '');

        const number = document.createElement('span');
        number.className = 'song-num';
        number.textContent = String(i + 1).padStart(2, '0');

        const info = document.createElement('span');
        info.className = 'song-info';

        const name = document.createElement('div');
        name.className = 'song-name';
        name.textContent = song.name;

        const sub = document.createElement('div');
        sub.className = 'song-sub';
        sub.textContent = i === index && !audio.paused ? '▶ Tocando agora' : 'Sua biblioteca';

        info.append(name, sub);
        button.append(number, info);
        button.onclick = () => loadSong(i, true);
        playlist.append(button);
    });
}

function loadSong(i, autoplay = false) {
    if (!songs.length) return;
    index = (i + songs.length) % songs.length;

    audio.src = songs[index].url;
    document.getElementById('title').textContent = songs[index].name;
    document.getElementById('artist').textContent = 'Arquivo local · Seu dispositivo';
    seek.value = 0;
    document.getElementById('current').textContent = '0:00';
    document.getElementById('duration').textContent = '0:00';

    lyrics = [];
    renderLyrics();
    renderPlaylist();

    if (autoplay) audio.play().catch(() => {});
}

function togglePlay() {
    if (index === -1) {
        if (songs.length) loadSong(0, true);
        else filesInput.click();
        return;
    }

    if (audio.paused) audio.play().catch(() => {});
    else audio.pause();
}

function previous() {
    if (!songs.length) return;
    if (audio.currentTime > 3) {
        audio.currentTime = 0;
    } else {
        loadSong(index - 1, true);
    }
}

function next() {
    if (songs.length) loadSong(index + 1, true);
}

document.getElementById('play').addEventListener('click', () => {});

audio.addEventListener('play', () => {
    document.getElementById('play').textContent = 'Ⅱ';
    document.body.classList.add('playing');
    renderPlaylist();
});

audio.addEventListener('pause', () => {
    document.getElementById('play').textContent = '▶';
    document.body.classList.remove('playing');
    renderPlaylist();
});

audio.addEventListener('ended', next);

audio.addEventListener('loadedmetadata', () => {
    document.getElementById('duration').textContent = timeText(audio.duration);
});

audio.addEventListener('timeupdate', () => {
    document.getElementById('current').textContent = timeText(audio.currentTime);

    if (Number.isFinite(audio.duration) && audio.duration > 0) {
        seek.value = audio.currentTime / audio.duration * 1000;
    }

    updateActiveLyric();
});

seek.addEventListener('input', () => {
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
        audio.currentTime = seek.value / 1000 * audio.duration;
    }
});

document.getElementById('volume').addEventListener('input', e => {
    audio.volume = Number(e.target.value);
    document.getElementById('volText').textContent =
        Math.round(audio.volume * 100) + '%';
});

audio.volume = 0.8;

function parseLyrics(text) {
    return text.split(/\r?\n/).flatMap(line => {
        const matches = [...line.matchAll(/\[(\d{1,2}):(\d{2})(?:[.:](\d{1,3}))?\]/g)];
        const words = line.replace(/\[[^\]]+\]/g, '').trim();

        return matches.map(m => ({
            time: Number(m[1]) * 60 + Number(m[2]) +
                (m[3] ? Number('0.' + m[3]) : 0),
            text: words || '♪'
        }));
    }).sort((a, b) => a.time - b.time);
}

function applyLyrics() {
    lyrics = parseLyrics(document.getElementById('lyricEditor').value);
    renderLyrics();
}

document.getElementById('lrcFile').addEventListener('change', async e => {
    const file = e.target.files[0];
    if (!file) return;

    const text = await file.text();
    document.getElementById('lyricEditor').value = text;
    applyLyrics();
    e.target.value = '';
});

function renderLyrics() {
    linesBox.innerHTML = '';

    if (!lyrics.length) {
        const el = document.createElement('div');
        el.className = 'lyric-line active';
        el.textContent = 'Adicione letras sincronizadas no formato .LRC';
        linesBox.appendChild(el);
        return;
    }

    lyrics.forEach((lyric, i) => {
        const el = document.createElement('div');
        el.className = 'lyric-line';
        el.textContent = lyric.text;
        el.dataset.index = i;
        linesBox.appendChild(el);
    });
}

function updateActiveLyric() {
    if (!lyrics.length) return;

    let active = -1;
    for (let i = 0; i < lyrics.length; i++) {
        if (lyrics[i].time <= audio.currentTime) active = i;
        else break;
    }

    const elements = linesBox.querySelectorAll('.lyric-line');
    elements.forEach((el, i) => el.classList.toggle('active', i === active));

    if (active >= 0 && elements[active]) {
        elements[active].scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

renderPlaylist();
renderLyrics();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    print("=" * 36)
    print("  NEON MUSIC PLAYER")
    print("  http://127.0.0.1:5000")
    print("=" * 36)
    app.run(debug=False)
