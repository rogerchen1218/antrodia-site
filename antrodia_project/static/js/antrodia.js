let slideIndex = 0;
let slideInterval;

document.addEventListener('DOMContentLoaded', function () {
    console.log('Antrodia Frontend Loaded');
    showSlides(slideIndex);
    startAutoSlide();
    setupScrollAnimations();
});

function setupScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, {
        threshold: 0.1
    });

    const elements = document.querySelectorAll('.reveal-on-scroll');
    elements.forEach((el) => observer.observe(el));
}

function moveSlide(n) {
    showSlides(slideIndex += n);
    resetAutoSlide();
}

function currentSlide(n) {
    showSlides(slideIndex = n);
    resetAutoSlide();
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("carousel-slide");
    let dots = document.getElementsByClassName("dot");

    if (slides.length === 0) return;

    if (n >= slides.length) { slideIndex = 0 }
    if (n < 0) { slideIndex = slides.length - 1 }

    for (i = 0; i < slides.length; i++) {
        slides[i].className = slides[i].className.replace(" active", "");
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    if (slides[slideIndex]) slides[slideIndex].className += " active";
    if (dots[slideIndex]) dots[slideIndex].className += " active";
}

function startAutoSlide() {
    slideInterval = setInterval(function () {
        showSlides(slideIndex += 1);
    }, 5000);
}

function resetAutoSlide() {
    clearInterval(slideInterval);
    startAutoSlide();
}

window.moveSlide = moveSlide;
window.currentSlide = currentSlide;
