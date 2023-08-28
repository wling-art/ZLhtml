const loginLink = document.querySelector(".login-link");
const registerLink = document.querySelector(".register-link");

registerLink.addEventListener("click", () => {
  wrapper.classList.add("active");
});

loginLink.addEventListener("click", () => {
  wrapper.classList.remove("active");
});

// 等待网页加载完执行wrapper.classList.add('active-popup');
window.onload = function () {
  wrapper.classList.add("active-popup");
};
