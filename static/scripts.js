function startTimer() {
    var start = Date.now(),
        diff,
        minutes,
        seconds,
        duration = (parseInt(($("#time").text().split(':')[0]),10) * 60) + parseInt(($("#time").text().split(':')[1]),10);
        console.log(duration);   // remaining on the clock
    function timer() {
        // get the number of seconds that have elapsed since
        // startTimer() was called

        diff = duration - (((Date.now() - start) / 1000) | 0);

        // does the same job as parseInt truncates the float
        minutes = (diff / 60) | 0;
        seconds = (diff % 60) | 0;

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        if (minutes == "00" && seconds == "00"){
            clearInterval(window.timerRunning);
            $(function() {
                $.ajax({
                    url: '/successlog',
                    type: 'GET',
                    success: function(type) {
                        console.log(type);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            });
        }
        else {}

        document.querySelector('#time').textContent = minutes + ":" + seconds;

        if (diff <= 0) {
            // add one second so that the count down starts at the full duration
            // example 05:00 not 04:59
            start = Date.now() + 1000;
        }
    }
    // we don't want to wait a full second before the timer starts
    timer();
    $(function() {
        $.ajax({
            url: '/startlog',
            type: 'GET',
            error: function(error) {
                console.log(error);
                }});
    });
    window.timerRunning = setInterval(timer, 1000);
}

function stopTimer() {
    clearInterval(window.timerRunning);
}


function getTime(){
    var duration = (parseInt(($("#time").text().split(':')[0]),10) * 60) + parseInt(($("#time").text().split(':')[1]),10);
    console.log(duration);
    console.log((parseInt(($("#time").text().split(':')[0]),10) * 60) + parseInt(($("#time").text().split(':')[1]),10));
    return duration;
}

function resetTimer(){
    stopTimer()
    document.querySelector('#time').textContent = "25:00";
}

