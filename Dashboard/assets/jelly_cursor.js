function setupFluid() {
    let canvas = null;
    let isActive = false;

    function initializeFluid() {
        if (!window.WebGLFluid || !canvas) return;
        
        try {
            // Define o tamanho inicial do buffer de desenho
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            window.WebGLFluid(canvas, {
                IMMEDIATE: true,
                TRIGGER: 'hover',
                SIM_RESOLUTION: 256,
                DYE_RESOLUTION: 1024,
                DENSITY_DISSIPATION: 0.95, // Quão rápido a tinta some (perto de 1 = demora mais)
                VELOCITY_DISSIPATION: 0.95,
                PRESSURE_ITERATIONS: 40,
                CURL: 30, // Quantidade de "redemoinhos" no fluido
                SPLAT_RADIUS: 0.28, // Tamanho do rastro do cursor (ideal para inverter texto de forma legível)
                SPLAT_FORCE: 6000, // Força com que a tinta é arrastada
                COLOR_PALETTE: ['#ffffff'], // Apenas branco para funcionar com o mix-blend-mode
                BACK_COLOR: '#000000', // O fundo do canvas preto fica invisível sob mix-blend-mode
                TRANSPARENT: true
            });
        } catch (e) {
            console.error("Erro ao inicializar o WebGL Fluid Simulation:", e);
        }
    }

    function checkAndRun() {
        const foundCanvas = document.getElementById('particleCanvas');
        
        // Se a landing page está ativa
        if (foundCanvas && !isActive) {
            isActive = true;
            
            // 1. Criar o canvas para o fluido WebGL
            if (!document.getElementById('fluid-canvas')) {
                canvas = document.createElement("canvas");
                canvas.setAttribute("id", "fluid-canvas");
                document.body.appendChild(canvas);
            } else {
                canvas = document.getElementById('fluid-canvas');
            }

            // 2. Carregar a biblioteca de simulação de fluidos se não carregada
            if (!window.WebGLFluid) {
                if (!document.getElementById('webgl-fluid-script')) {
                    const script = document.createElement("script");
                    script.id = "webgl-fluid-script";
                    script.src = "https://cdn.jsdelivr.net/npm/webgl-fluid@0.4.0/dist/webgl-fluid.umd.min.js";
                    script.onload = function() {
                        initializeFluid();
                    };
                    document.head.appendChild(script);
                }
            } else {
                initializeFluid();
            }
            
        } else if (!foundCanvas && isActive) {
            // Landing page inativa, limpar o canvas de fluido
            isActive = false;
            
            const existingCanvas = document.getElementById('fluid-canvas');
            if (existingCanvas && existingCanvas.parentNode) {
                existingCanvas.parentNode.removeChild(existingCanvas);
            }
            canvas = null;
        }
    }

    // Usar MutationObserver para páginas carregadas dinamicamente
    const observer = new MutationObserver(checkAndRun);
    observer.observe(document.body, { childList: true, subtree: true });

    // Executar imediatamente se já estiver na página
    checkAndRun();
}

// Inicializador robusto que suporta carregamento assíncrono do Dash
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupFluid);
} else {
    setupFluid();
}
