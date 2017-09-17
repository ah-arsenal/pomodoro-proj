function startTimer() {
    var start = Date.now(),
        diff,
        minutes,
        seconds,
        duration = (parseInt(($("#time").text().split(':')[0]),10) * 60) + parseInt(($("#time").text().split(':')[1]),10);
        console.log(duration);        //parseInt((document.querySelector('#time').split(',')[0]),10) * 60 + parseInt((document.querySelector('#time').split(',')[0]),10); // remaining on the clock
    function timer() {
        // get the number of seconds that have elapsed since
        // startTimer() was called

        diff = duration - (((Date.now() - start) / 1000) | 0);

        // does the same job as parseInt truncates the float
        minutes = (diff / 60) | 0;
        seconds = (diff % 60) | 0;

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        document.querySelector('#time').textContent = minutes + ":" + seconds;

        if (diff <= 0) {
            // add one second so that the count down starts at the full duration
            // example 05:00 not 04:59
            start = Date.now() + 1000;
        }
    }
    // we don't want to wait a full second before the timer starts
    timer();
    setInterval(timer, 1000);
}

function stopTimer() {

}


function getTime(){
    var duration = (parseInt(($("#time").text().split(':')[0]),10) * 60) + parseInt(($("#time").text().split(':')[1]),10);
    console.log(duration);
    console.log((parseInt(($("#time").text().split(':')[0]),10) * 60) + parseInt(($("#time").text().split(':')[1]),10));
    return duration;
}

// window.onload = function () {
//         setTimeout(function(){
//             getTime();
//         }, 1000);
// };

