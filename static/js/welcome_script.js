
let time = 5;
function showTime() {

    time--;
    if (time <= 0) {
        //clearInterval(id);

        location.href = "http://www.baidu.com";
    }
    let sp = document.getElementById("time");
    sp.innerHTML = time;
}

let id = setInterval(showTime, 1000);