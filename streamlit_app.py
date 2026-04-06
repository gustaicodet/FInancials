import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sovereign Flow", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #000000; font-family: 'Inter', sans-serif; color: white; }
    #MainMenu, footer, header {visibility: hidden;}
    .game-container { border: 1px solid #1c1c1e; border-radius: 20px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-weight: 600; letter-spacing: -1px;'>Sovereign Flow v1.0</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8e8e93; font-size: 14px;'>Goal: Reach 100% Sovereignty. Use Arrow Keys or Mouse.</p>", unsafe_allow_html=True)

# --- THE GAME ENGINE (HTML/JS) ---
game_html = """
<div id="game-wrapper" style="display: flex; justify-content: center; align-items: center; background: #000;">
    <canvas id="gameCanvas" width="400" height="500" style="border-radius: 15px; cursor: none;"></canvas>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let score = 0;
let sovereignty = 0;
let gameOver = false;
let gameWon = false;

const player = { x: 200, y: 430, size: 20, color: '#ffffff' };
const items = [];
const particles = [];

function createItem() {
    const types = [
        { name: 'gold', color: '#FFD700', value: 5, chance: 0.4 },      // Wealth
        { name: 'skill', color: '#007AFF', value: 10, chance: 0.2 },    // Specialist Skills
        { name: 'tax', color: '#FF3B30', value: -15, chance: 0.3 },    // High Taxes
        { name: 'rain', color: '#48484A', value: -5, chance: 0.1 }     // Bad Weather
    ];
    
    const random = Math.random();
    let cumulative = 0;
    for (let type of types) {
        cumulative += type.chance;
        if (random < cumulative) {
            items.push({
                x: Math.random() * (canvas.width - 20),
                y: -20,
                size: type.name === 'tax' ? 18 : 12,
                speed: 3 + Math.random() * 3,
                ...type
            });
            break;
        }
    }
}

function update() {
    if (gameOver || gameWon) return;

    if (Math.random() < 0.05) createItem();

    items.forEach((item, index) => {
        item.y += item.speed;
        
        // Collision Detection
        const dx = player.x - item.x;
        const dy = player.y - item.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < player.size + item.size) {
            sovereignty += item.value;
            if (sovereignty < 0) sovereignty = 0;
            if (sovereignty >= 100) gameWon = true;
            items.splice(index, 1);
        }
    });

    // Cleanup off-screen items
    if (items.length > 50) items.shift();
}

function draw() {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Grid lines for "Engineer" look
    ctx.strokeStyle = '#1c1c1e';
    ctx.lineWidth = 1;
    for(let i=0; i<canvas.width; i+=40) {
        ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke();
    }
    for(let i=0; i<canvas.height; i+=40) {
        ctx.beginPath(); ctx.moveTo(0,i); ctx.lineTo(canvas.width,i); ctx.stroke();
    }

    // Items
    items.forEach(item => {
        ctx.fillStyle = item.color;
        if (item.name === 'tax') {
            ctx.fillRect(item.x, item.y, item.size, item.size);
        } else {
            ctx.beginPath();
            ctx.arc(item.x, item.y, item.size, 0, Math.PI * 2);
            ctx.fill();
        }
    });

    // Player
    ctx.fillStyle = player.color;
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#ffffff';
    ctx.beginPath();
    ctx.arc(player.x, player.y, player.size, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    // HUD
    ctx.fillStyle = '#ffffff';
    ctx.font = '600 16px Inter';
    ctx.fillText(`SOVEREIGNTY: ${Math.max(0, sovereignty)}%`, 20, 40);
    
    // Progress Bar
    ctx.fillStyle = '#1c1c1e';
    ctx.roundRect(20, 50, 360, 6, 3);
    ctx.fill();
    ctx.fillStyle = '#32D74B';
    ctx.roundRect(20, 50, (Math.min(sovereignty, 100) / 100) * 360, 6, 3);
    ctx.fill();

    if (gameWon) {
        ctx.fillStyle = 'rgba(0,0,0,0.8)';
        ctx.fillRect(0,0,canvas.width, canvas.height);
        ctx.fillStyle = '#32D74B';
        ctx.textAlign = 'center';
        ctx.font = '600 24px Inter';
        ctx.fillText('PASSPORT SECURED', canvas.width/2, canvas.height/2 - 20);
        ctx.fillStyle = '#ffffff';
        ctx.font = '400 16px Inter';
        ctx.fillText('Destination: Warm Country', canvas.width/2, canvas.height/2 + 10);
    }
}

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    player.x = e.clientX - rect.left;
});

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}
loop();
</script>
"""

# Render the game
components.html(game_html, height=550)

st.markdown("---")
st.write("### 🛠️ The Mechanics")
st.write(f"This game simulates your journey as a Water Engineer. You need to earn **$1500€** in passive value to reach full autonomy.")
