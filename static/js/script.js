const text = "Manage Your Tasks Smarter";

let index = 0;

function typeEffect() {

    const element = document.getElementById("typing-text");

    if (!element) return;

    if (index < text.length) {

        element.textContent += text.charAt(index);

        index++;

        setTimeout(typeEffect, 80);

    } else {

        element.classList.add("finished");

    }

}

window.addEventListener("load", () => {

    const element = document.getElementById("typing-text");

    if (element) {

        element.textContent = "";

        typeEffect();

    }

});

const particlesContainer = document.querySelector(".particles");


for (let i = 0; i < 40; i++) {

    const particle = document.createElement("span");

    particle.classList.add("particle");


    particle.style.left = Math.random() * 100 + "%";

    particle.style.animationDuration =
        Math.random() * 10 + 5 + "s";


    particle.style.animationDelay =
        Math.random() * 5 + "s";


    particlesContainer.appendChild(particle);

}