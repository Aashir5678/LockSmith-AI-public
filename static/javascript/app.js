document.addEventListener("DOMContentLoaded", () => {
    // Typing effect for input placeholders
    const textBoxes = document.querySelectorAll(".input-box");
    const placeholderTexts = {
        username: "Enter the username/email you want to evaluate ...",
        password: "Enter your password used with that username/email for evaluation.....",
    };
    let typingInterval;

    const startTypingEffect = (textBox, placeholderText) => {
        let currentText = "";
        let index = 0;

        clearInterval(typingInterval);

        typingInterval = setInterval(() => {
            if (index < placeholderText.length) {
                currentText += placeholderText[index];
                textBox.setAttribute("placeholder", currentText);
                index++;
            } else {
                clearInterval(typingInterval);
            }
        }, 100);
    };

    textBoxes.forEach((textBox) => {
        textBox.addEventListener("focus", () => {
            textBox.setAttribute("placeholder", "");
            const placeholderText = textBox.name === "password" ? placeholderTexts.password : placeholderTexts.username;
            startTypingEffect(textBox, placeholderText);
        });

        textBox.addEventListener("blur", () => {
            const placeholderText = textBox.name === "password" ? placeholderTexts.password : placeholderTexts.username;
            textBox.setAttribute("placeholder", placeholderText);
            clearInterval(typingInterval);
        });
    });

    // Submit button interaction
    const submitButton = document.querySelector(".submit-btn-custom");
    if (submitButton) {
        submitButton.addEventListener("click", (e) => {
            e.preventDefault();
            console.log("Form Submitted!");
        });
    }

    // Lock animation functionality
    const lockStatic = document.getElementById("lock-static");
    const lockGif = document.getElementById("lock-gif");
    const surveyButton = document.getElementById("survey-button");

    // Unlock sound
    const unlockSound = new Audio();
    unlockSound.src = "/static/sounds/unlock.mp3"; // Path to your sound file
    unlockSound.load(); // Preload the sound
    unlockSound.volume = 1.0; // Set volume to full

    // Lock click event
    lockStatic.addEventListener("click", () => {
        // Hide the static lock
        lockStatic.classList.add("hidden");

        // Show the unlocking animation
        lockGif.classList.remove("hidden");

        // Play the unlocking sound
        unlockSound
            .play()
            .then(() => {
                console.log("Audio playback started successfully.");
            })
            .catch((err) => console.error("Audio playback failed:", err));

        // Reveal the survey button after the animation completes
        setTimeout(() => {
            lockGif.classList.add("hidden");
            surveyButton.style.display = "inline-block";
        }, 5000); // Matches the duration of your unlocking GIF
    });

    // Survey button hover effect
    if (surveyButton) {
        surveyButton.addEventListener("mouseover", () => {
            surveyButton.style.transform = "scale(1.1)";
            surveyButton.style.transition = "transform 0.3s ease";
        });

        surveyButton.addEventListener("mouseout", () => {
            surveyButton.style.transform = "scale(1)";
        });
    }
});

