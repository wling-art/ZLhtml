
let time = 5;
function showTime() {

    time--;
    if (time <= 0) {
        //clearInterval(id);

        location.href = "index";
    }
    const sp = document.getElementById("time");
    sp.innerHTML = time;
}

setInterval(showTime, 1000);