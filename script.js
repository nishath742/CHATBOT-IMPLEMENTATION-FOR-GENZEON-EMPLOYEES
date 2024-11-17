// Canvas and Particle Animation Code
const canvas = document.getElementById('galaxyCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    const size = Math.min(window.innerWidth, window.innerHeight) * 0.5;
    canvas.width = size;
    canvas.height = size;
    init();
}

window.addEventListener('resize', resizeCanvas);

let particles = [];
let waveRadius = 0;
let waveGrowing = false;

function Particle(x, y) {
    this.x = x;
    this.y = y;
    this.size = Math.random() * 3;
    this.speedX = Math.random() * 0.4 - 0.2;
    this.speedY = Math.random() * 0.4 - 0.2;
    this.opacity = Math.random();
}

Particle.prototype.update = function() {
    this.x += this.speedX;
    this.y += this.speedY;

    if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
        this.x = canvas.width / 2;
        this.y = canvas.height / 2;
    }
};

Particle.prototype.draw = function() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
    ctx.shadowColor = 'white';
    ctx.shadowBlur = 10;
    ctx.fill();
};

function init() {
    particles = [];
    for (let i = 0; i < 200; i++) { // Number of particles
        particles.push(new Particle(canvas.width / 2, canvas.height / 2));
    }
}

function drawWave() {
    if (waveGrowing) {
        waveRadius += 2;
    } else {
        waveRadius = 0;
    }
    
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, waveRadius, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)';
    ctx.lineWidth = 3;
    ctx.shadowColor = 'aqua';
    ctx.shadowBlur = 20;
    ctx.stroke();

    if (waveRadius > canvas.width / 2) {
        waveGrowing = false;
        waveRadius = 0;
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, canvas.width / 2, 0, Math.PI * 2);
    ctx.clip();

    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    drawBlinkingDot();
    drawWave();

    ctx.restore();
    requestAnimationFrame(animate);
}

let blinkState = true;
let blinkCounter = 0;

function drawBlinkingDot() {
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const dotSize = 5;

    ctx.beginPath();
    ctx.arc(centerX, centerY, dotSize, 0, Math.PI * 2);
    ctx.fillStyle = blinkState ? 'aqua' : 'transparent';
    ctx.fill();
    ctx.shadowColor = 'aqua';
    ctx.shadowBlur = 20;

    if (blinkCounter % 30 === 0) { // Blink every 30 frames
        blinkState = !blinkState;
        if (blinkState) {
            waveGrowing = true;
        }
    }
    blinkCounter++;
}

resizeCanvas(); // Initial call to set canvas size
init();
animate();

// Initialize Speech Recognition
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.continuous = true; // Allow continuous speech recognition

let isListening = false;

function updateListeningStatus() {
    if (isListening) {
        addMessage('system', 'Listening...');
    } else {
        addMessage('system', 'Recognizing...');
    }
}

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('chat-input').value = transcript;
    addMessage('user', transcript);
    recognition.stop(); // Stop recognition after result is received
    document.getElementById('send-button').click(); // Automatically send the voice input
    isListening = false;
    updateListeningStatus(); // Update status after receiving result
};

recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    recognition.stop();
    isListening = false;
    updateListeningStatus(); // Update status on error
};

document.getElementById('send-button').addEventListener('click', () => {
    const input = document.getElementById('chat-input');
    const message = input.value;
    if (message.trim() !== '') {
        addMessage('user', message);
        input.value = '';
        eel.process_query(message)((response) => {
            addMessage('Gen-Z', response);
        });
    }
});

document.getElementById('voice-button').addEventListener('click', () => {
    isListening = true;
    updateListeningStatus(); // Update status when starting speech recognition
    recognition.start(); // Start speech recognition when button is clicked
});

// Handle Enter key press
document.getElementById('chat-input').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevents the default action of Enter key
        document.getElementById('send-button').click(); // Simulate button click
    }
});
eel.expose(redirectToBlank);

function addMessage(sender, text) {
    const messages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.className = 'message';

    const label = document.createElement('div');
    label.className = 'label';
    label.textContent = sender === 'user' ? 'USER' : sender === 'Gen-Z' ? 'Gen-Z' : 'SYSTEM';
    
    const messageText = document.createElement('div');
    messageText.className = 'text';
    messageText.textContent = text;

    messageElement.appendChild(label);
    messageElement.appendChild(messageText);
    messages.appendChild(messageElement);
    messages.scrollTop = messages.scrollHeight; // Auto-scroll to the bottom
}
