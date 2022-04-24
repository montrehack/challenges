Reveal.initialize({
    hash: true,
    plugins: [
        RevealHighlight,
    ],
    transition: 'fade'
});

Reveal.on('slidechanged', event => {
    const currentSlide = event.currentSlide;
    const timer = currentSlide.querySelector('div.timer');

    if (!timer) {
        return;
    }

    let timelimit = timer.dataset.timelimit - 0;
    if (!timelimit) {
        return;
    }

    let interval = timer['timer_interval'];
    if (interval) {
        clearInterval(interval);
    }

    interval = setInterval(() => {
        const hours = Math.floor(timelimit / 3600);
        const minutes = Math.floor((timelimit % 3600) / 60);
        const seconds = Math.floor(timelimit % 60);

        timer.innerHTML = (
            (hours < 10 ? '0' : '') + hours + ' : ' +
            (minutes < 10 ? '0' : '') + minutes + ' : ' +
            (seconds < 10 ? '0' : '') + seconds
        );

        timelimit--;

        if (timelimit < 0) {
            clearInterval(interval);
        }
    }, 1000);

    timer.innerHTML = 'START!';
    timer['timer_interval'] = interval;
});

document.querySelectorAll('div.flags').forEach(e => {
    const countOn = e.dataset.on;
    const countOff = 10 - countOn;

    let html = '';
    for (let i = 0; i < countOn; i++) {
        html += '<img src="./images/flag-on.png">';
    }
    for (let i = 0; i < countOff; i++) {
        html += '<img src="./images/flag-off.png">';
    }

    e.innerHTML = html;
});
