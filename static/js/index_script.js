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

// 获取所有的 advantage-card 元素
const cards = document.querySelectorAll('.advantage-card');

// 为每个卡片添加点击事件监听器
cards.forEach(card => {
    card.addEventListener('click', () => {
        // 获取当前卡片下的 advantage-text 元素
        const textElement = card.querySelector('.advantage-text');

        // 切换显示状态
        card.classList.toggle('show-card');
        textElement.classList.toggle('show-text');
    });
});

