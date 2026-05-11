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
        rgba(152, 88, 241, 0.4) 0%,
        rgba(152, 88, 241, 0.1) 30%,
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

  // Observer is needed because Dash renders components dynamically
  const observer = new MutationObserver(function(mutations) {
      const dynamicGlassElements = document.querySelectorAll('.glass-button');
      dynamicGlassElements.forEach(element => {
        if (!element.dataset.glassInited) {
            element.addEventListener('mousemove', handleMouseMove);
            element.addEventListener('mouseleave', handleMouseLeave);
            element.dataset.glassInited = 'true';
        }
      });
  });

  observer.observe(document.body, { childList: true, subtree: true });
});
