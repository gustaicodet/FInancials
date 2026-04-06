import streamlit as st
import streamlit.components.v1 as components

# --- STABLE DESIGN & APPLE AESTHETIC ---
st.set_page_config(page_title="Sovereign HUD v2", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #000000; font-family: 'Inter', sans-serif; color: white; }
    #MainMenu, footer, header {visibility: hidden;}
    /* Clean container for the professional tool */
    .block-container { padding-top: 5rem; max-width: 500px; margin: auto; }
    .tool-title { text-align: center; font-weight: 500; font-size: 16px; color: #8e8e93; margin-bottom: 5px; }
    .tool-main { font-size: 56px; font-weight: 600; text-align: center; color: #ffffff; letter-spacing: -2px; margin: 0; line-height: 1; }
    .tool-status { text-align: center; font-size: 20px; font-weight: 500; margin-top: 5px; margin-bottom: 40px; color: #32d74b; }
    </style>
    """, unsafe_allow_html=True)

# --- UI LAYOUT ---
st.markdown('<p class="tool-title">HYDRODYNAMIC SPECIALIST TOOL V1</p>', unsafe_allow_html=True)
st.markdown('<p class="tool-main">Sovereign Flow</p>', unsafe_allow_html=True)
st.markdown('<p class="tool-status">ONLINE • DESIGN PHASE</p>', unsafe_allow_html=True)

# --- THE ENGINEERING ENGINE (HTML/JS) ---
engine_html = """
<div id="wrapper" style="display: flex; justify-content: center; align-items: center; background: #000; padding: 20px;">
    <canvas id="engineCanvas" width="400" height="500" style="border-radius: 15px; cursor: none;"></canvas>
</div>

<script>
const canvas = document.getElementById('engineCanvas');
const ctx = canvas.getContext('2d');

const gridWidth = 40;
const gridHeight = 50;
const cellSize = 10;
const grid = [];
const particles = [];
const particleRadius = 3;
const gravity = 0.5;
const smoothingLength = 12; // Radius of pressure interaction
const targetDensity = 10;
const pressureMultiplier = 2000;

// Initialize Grid & Boundaries
for (let y = 0; y < gridHeight; y++) {
    grid[y] = [];
    for (let x = 0; x < gridWidth; x++) {
        if (x === 0 || x === gridWidth - 1 || y === gridHeight - 1 || y === gridHeight - 2) {
            grid[y][x] = 1; // Wall block
        } else {
            grid[y][x] = 0; // Empty
        }
    }
}

// Minimal SPH Fluid Particle Class
class Particle {
    constructor(x, y) {
        this.x = x; this.y = y;
        this.vx = (Math.random() - 0.5) * 4; this.vy = gravity;
        this.density = 0; this.pressure = 0;
    }

    update() {
        this.vy += gravity; // Gravity always down

        // Pressure math: Push away from others
        let fx = 0, fy = 0;
        for (let other of particles) {
            if (this === other) continue;
            let d_vec_x = this.x - other.x;
            let d_vec_y = this.y - other.y;
            let d = Math.sqrt(d_vec_x * d_vec_x + d_vec_y * d_vec_y);
            
            if (d < smoothingLength && d > 0) {
                let diff = smoothingLength - d;
                let forceMag = (this.pressure + other.pressure) * diff * diff / d;
                fx += (d_vec_x / d) * forceMag;
                fy += (d_vec_y / d) * forceMag;
            }
        }

        this.vx += fx * 0.0001; // Integration scale
        this.vy += fy * 0.0001;
        this.x += this.vx; this.y += this.vy;

        // --- GRID COLLISION ---
        let gridX = Math.floor(this.x / cellSize);
        let gridY = Math.floor(this.y / cellSize);
        
        // Bounds & Block Interaction
        if (gridX < 0) { this.x = particleRadius; this.vx *= -0.5; }
        if (gridX >= gridWidth) { this.x = canvas.width - particleRadius; this.vx *= -0.5; }
        if (gridY < 0) { this.y = particleRadius; this.vy *= -0.5; }
        if (gridY >= gridHeight) { this.y = canvas.height - particleRadius; this.vy *= -0.5; }

        if (gridX >= 0 && gridX < gridWidth && gridY >= 0 && gridY < gridHeight) {
            if (grid[gridY][gridX] === 1) {
                // Determine collision direction based on center of grid cell
                let block_center_x = (gridX + 0.5) * cellSize;
                let block_center_y = (gridY + 0.5) * cellSize;
                
                if (Math.abs(this.x - block_center_x) > Math.abs(this.y - block_center_y)) {
                    this.x = (gridX * cellSize) + (this.x < block_center_x ? -particleRadius : cellSize + particleRadius);
                    this.vx *= -0.8; 
                } else {
                    this.y = (gridY * cellSize) + (this.y < block_center_y ? -particleRadius : cellSize + particleRadius);
                    this.vy *= -0.8;
                }
                
                // Add minor damping/friction
                this.vx *= 0.99;
                this.vy *= 0.99;
            }
        }
    }

    draw() {
        ctx.fillStyle = '#007AFF'; // Vibrant blue
        ctx.beginPath();
        ctx.arc(this.x, this.y, particleRadius, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Mouse for Interaction
canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    let gridX = Math.floor((e.clientX - rect.left) / cellSize);
    let gridY = Math.floor((e.clientY - rect.top) / cellSize);
    if (gridX >= 0 && gridX < gridWidth && gridY >= 0 && gridY < gridHeight) {
        if (grid[gridY][gridX] === 0) {
            grid[gridY][gridX] = 1; // Place block
        } else {
            grid[gridY][gridX] = 0; // Remove block
        }
    }
});

function draw() {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Grid lines for "Engineer" look
    ctx.strokeStyle = '#1c1c1e';
    ctx.lineWidth = 1;
    for(let i=0; i<canvas.width; i+=cellSize) {
        ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke();
    }
    for(let i=0; i<canvas.height; i+=cellSize) {
        ctx.beginPath(); ctx.moveTo(0,i); ctx.lineTo(canvas.width,i); ctx.stroke();
    }

    // Grid Blocks
    ctx.fillStyle = '#48484A'; // Gray blocks
    for (let y = 0; y < gridHeight; y++) {
        for (let x = 0; x < gridWidth; x++) {
            if (grid[y][x] === 1) {
                ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
            }
        }
    }

    // Simple Water Emitter
    if (Math.random() < 0.2 && particles.length < 300) {
        particles.push(new Particle(10 * cellSize, 5 * cellSize));
    }

    // SPH Simulation Loop
    for (let p of particles) {
        p.density = 0;
        for (let other of particles) {
            let d = Math.sqrt((p.x - other.x) ** 2 + (p.y - other.y) ** 2);
            if (d < smoothingLength) {
                let diff = smoothingLength - d;
                p.density += diff * diff * diff;
            }
        }
        p.pressure = (p.density - targetDensity) * pressureMultiplier;
    }

    // Update particles (in reverse)
    for (let i = particles.length - 1; i >= 0; i--) {
        particles[i].update();
        particles[i].draw();
    }
    
    // HUD element from sovereign HUD concept
    ctx.fillStyle = '#ffffff';
    ctx.font = '600 16px Inter';
    ctx.fillText(`STATUS: ONLINE • SPH v2`, 20, 40);
}

function loop() {
    draw();
    requestAnimationFrame(loop);
}
loop();
</script>
"""

# Render the engineering component
components.html(engine_html, height=550)

st.markdown("---")
st.write("### 🛠️ Hydrodynamic Engine Mechanics")
st.write(f"Click the grid to place/remove impenetrable **Concrete Blocks**. The water isn't a solid rectangle; it's thousands of individual particles calculating **Smoothed-Particle Hydrodynamics (SPH)**. Watch them pool, flow over your dam, and calculate pressure against boundaries.")
