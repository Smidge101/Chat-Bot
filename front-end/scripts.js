const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const botResponse = document.getElementById("bot-response");

sendBtn.addEventListener("click", async () => {
    const question = userInput.value.trim();
    if (!question) return;

    // show user's message
    chatBox.innerHTML += `<div class="user-msg">${question}</div>`;

    // show "Thinking..."
    botResponse.innerText = "Thinking...";

    try {
        const response = await fetch("http://127.0.0.1:8000/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        // extract text safely
        let answerText = "";
        if (data.answer && data.answer.parts && data.answer.parts.length > 0) {
            answerText = data.answer.parts.map(p => p.text).join("\n");
        } else {
            answerText = "No response from Virtual Eddie.";
        }

        botResponse.innerText = answerText;

    } catch (err) {
        console.error(err);
        botResponse.innerText = "Error connecting to Virtual Eddie.";
    }

    userInput.value = "";
});