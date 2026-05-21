document.addEventListener("DOMContentLoaded", function() {
    let container = null;
    let svgFilter = null;
    let isActive = false;
    let animationId = null;

    const mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    
    // Lista de blobs
    let blobs = [];

    function onMouseMove(e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    }

    function animate() {
        if (!isActive) return;

        // Atualiza a posição de cada blob
        for (let i = 0; i < blobs.length; i++) {
            const blob = blobs[i];
            const targetX = i === 0 ? mouse.x : blobs[i - 1].x;
            const targetY = i === 0 ? mouse.y : blobs[i - 1].y;

            // Easing / LERP
            // i === 0 é o principal, mais rápido. Os outros criam o rastro.
            const ease = i === 0 ? 0.28 : 0.22 - (i * 0.025);
            blob.x += (targetX - blob.x) * ease;
            blob.y += (targetY - blob.y) * ease;

            // Aplica no DOM usando transform para alta performance (Hardware Acceleration)
            blob.el.style.transform = `translate3d(${blob.x}px, ${blob.y}px, 0) translate(-50%, -50%)`;
        }

        animationId = requestAnimationFrame(animate);
    }

    // Handlers para hover em elementos interativos
    function handleMouseOver(e) {
        const target = e.target.closest('a, button, [role="button"], input, .glass-button, .upload-box, label, select');
        if (target && blobs.length > 0) {
            blobs[0].el.classList.add('jelly-hover');
        }
    }

    function handleMouseOut(e) {
        const target = e.target.closest('a, button, [role="button"], input, .glass-button, .upload-box, label, select');
        if (target && blobs.length > 0) {
            blobs[0].el.classList.remove('jelly-hover');
        }
    }

    const observer = new MutationObserver(function(mutations) {
        const foundCanvas = document.getElementById('particleCanvas');
        
        // Se a landing page está ativa (detectada pela presença do canvas de partículas)
        if (foundCanvas && !isActive) {
            isActive = true;
            
            // 1. Criar filtro SVG se não existir
            if (!document.getElementById('jelly-svg-filter')) {
                svgFilter = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                svgFilter.setAttribute("id", "jelly-svg-filter");
                svgFilter.style.display = "none";
                svgFilter.style.position = "absolute";
                svgFilter.innerHTML = `
                    <defs>
                        <filter id="goo">
                            <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
                            <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9" result="goo" />
                            <feComposite in="SourceGraphic" in2="goo" operator="atop" />
                        </filter>
                    </defs>
                `;
                document.body.appendChild(svgFilter);
            }

            // 2. Criar container do cursor se não existir
            if (!document.getElementById('jelly-cursor-container')) {
                container = document.createElement("div");
                container.setAttribute("id", "jelly-cursor-container");
                container.className = "jelly-container";
                
                // Criar 6 blobs para um rastro fluido e espesso
                const numBlobs = 6;
                blobs = [];
                for (let i = 0; i < numBlobs; i++) {
                    const el = document.createElement("div");
                    el.className = i === 0 ? "jelly-blob main-blob" : "jelly-blob trail-blob";
                    
                    // Adiciona o elemento interno para a animação de escala suave
                    const inner = document.createElement("div");
                    inner.className = "jelly-blob-inner";
                    el.appendChild(inner);
                    
                    container.appendChild(el);
                    
                    blobs.push({
                        el: el,
                        x: mouse.x,
                        y: mouse.y
                    });
                }
                
                document.body.appendChild(container);
            }
            
            window.addEventListener('mousemove', onMouseMove);
            window.addEventListener('mouseover', handleMouseOver);
            window.addEventListener('mouseout', handleMouseOut);
            animate();
            
        } else if (!foundCanvas && isActive) {
            // Landing page inativa, limpar elementos e listeners
            isActive = false;
            if (animationId) cancelAnimationFrame(animationId);
            window.removeEventListener('mousemove', onMouseMove);
            window.removeEventListener('mouseover', handleMouseOver);
            window.removeEventListener('mouseout', handleMouseOut);
            
            const existingContainer = document.getElementById('jelly-cursor-container');
            if (existingContainer && existingContainer.parentNode) {
                existingContainer.parentNode.removeChild(existingContainer);
            }
            
            const existingFilter = document.getElementById('jelly-svg-filter');
            if (existingFilter && existingFilter.parentNode) {
                existingFilter.parentNode.removeChild(existingFilter);
            }
            
            container = null;
            svgFilter = null;
            blobs = [];
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
