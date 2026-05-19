HTML code: <!-- SVG Filter for Glass Distortion -->
<svg style="display: none">
  <filter id="glass-distortion">
    <feTurbulence type="turbulence" baseFrequency="0.008" numOctaves="2" result="noise" />
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="77" />
  </filter>
</svg>

<button class="glass-button">
  <div class="glass-filter"></div>
  <div class="glass-overlay"></div>
  <div class="glass-specular"></div>
  <div class="glass-content">
    <span>Liquid Glass Button</span>
  </div>
</button>

Css: 
/* Glass Button Container */
.glass-button {
  --bg-color: rgba(255, 255, 255, 0.25);
  --highlight: rgba(255, 255, 255, 0.75);
  --text: #ffffff;
  
  position: relative;
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  overflow: hidden;
  background: transparent;
  transition: transform 0.2s ease;
  outline: none;
}

.glass-button:hover {
  transform: scale(1.05);
}

.glass-button:active {
  transform: scale(0.95);
}

.glass-filter,
.glass-overlay,
.glass-specular {
  position: absolute;
  inset: 0;
  border-radius: inherit;
}

.glass-filter {
  z-index: 1;
  backdrop-filter: blur(4px);
  filter: url(#glass-distortion) saturate(120%) brightness(1.15);
}

.glass-overlay {
  z-index: 2;
  background: var(--bg-color);
}

.glass-specular {
  z-index: 3;
  box-shadow: inset 1px 1px 1px var(--highlight);
}

.glass-content {
  position: relative;
  z-index: 4;
  color: var(--text);
  font-weight: 500;
  font-size: 16px;
}

/* Dark mode styles */
@media (prefers-color-scheme: dark) {
  .glass-button {
    --bg-color: rgba(0, 0, 0, 0.25);
    --highlight: rgba(255, 255, 255, 0.15);
  }
}

JS

// Add mouse movement interactivity to glass button
document.addEventListener('DOMContentLoaded', function() {
  // Get all glass elements
  const glassElements = document.querySelectorAll('.glass-button');
  
  // Add mousemove effect for each glass element
  glassElements.forEach(element => {
    element.addEventListener('mousemove', handleMouseMove);
    element.addEventListener('mouseleave', handleMouseLeave);
  });
  
  // Handle mouse movement over glass elements
  function handleMouseMove(e) {
    const rect = this.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    
    // Add highlight effect
    const specular = this.querySelector('.glass-specular');
    if (specular) {
      specular.style.background = `radial-gradient(
        circle at ${x}px ${y}px,
        rgba(255,255,255,0.15) 0%,
        rgba(255,255,255,0.05) 30%,
        rgba(255,255,255,0) 60%
      )`;
    }
  }
  
  // Reset effects when mouse leaves
  function handleMouseLeave() {
    const filter = document.querySelector('#glass-distortion feDisplacementMap');
    if (filter) {
      filter.setAttribute('scale', '77');
    }
    
    const specular = this.querySelector('.glass-specular');
    if (specular) {
      specular.style.background = 'none';
    }
  }
});
