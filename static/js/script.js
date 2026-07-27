function typeEffect() {

    if(index < text.length) {

        document.getElementById("typing-text").innerHTML += text.charAt(index);

        index++;

        setTimeout(typeEffect, 80);

    }

}


window.onload = typeEffect;

const text = "Manage your tasks. Stay organized.";

let index = 0;

function typeEffect() {

    if (index < text.length) {

        document.getElementById("typing-text").innerHTML += text.charAt(index);

        index++;

        setTimeout(typeEffect, 80);

    }

}


window.onload = typeEffect;