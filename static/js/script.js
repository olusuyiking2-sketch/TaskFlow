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