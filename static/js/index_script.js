// 缓存元素引用
const nav = document.querySelector('.nav-f');
const btnPopup = document.querySelector('.btnLogin-popup');
const cards = document.querySelectorAll('.advantage-card');
const textElements = document.querySelectorAll('.advantage-card .advantage-text');

// 使用节流来限制滚动事件处理程序的执行频率
let ticking = false;
window.addEventListener('scroll', function () {
    if (!ticking) {
        window.requestAnimationFrame(function () {
            nav.classList.toggle('active', document.documentElement.scrollTop > 1);
            ticking = false;
        });

        ticking = true;
    }
});

// 点击按钮转到login
btnPopup.addEventListener('click', () => {
    window.location.href = "login";
});

// 为每个卡片添加点击事件监听器
cards.forEach((card, index) => {
    card.addEventListener('click', () => {
        card.classList.toggle('show-card');
        textElements[index].classList.toggle('show-text');
    });
});
