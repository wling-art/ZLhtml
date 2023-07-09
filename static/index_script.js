// 缓存元素引用
const nav = document.querySelector('.nav-f');

// 使用 requestAnimationFrame
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

const btnPopup = document.querySelector('.btnLogin-popup');

//点击按钮转到login
btnPopup.addEventListener('click', () => {
    window.location.href = "login";
});