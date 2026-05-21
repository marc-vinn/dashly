/**
 * WebGL Fluid Simulation — Efeito de rastro líquido na Landing Page
 *
 * PROBLEMA RESOLVIDO:
 * O canvas precisa de `pointer-events: none` no CSS para que cliques
 * alcancem o botão de upload por baixo. Porém a biblioteca WebGLFluid
 * escuta mousemove/mousedown/mouseup diretamente no canvas.
 *
 * SOLUÇÃO:
 * Capturamos os eventos de mouse no `window` e despachamos cópias
 * sintéticas diretamente no canvas, fazendo o fluido reagir ao cursor
 * sem bloquear a interação com os elementos por baixo.
 */
function setupFluid() {
    let canvas = null;
    let isActive = false;
    let forwarding = false;

    // ── Reencaminhamento de eventos do mouse para o canvas ──────────
    function forwardMouseEvent(e) {
        if (!canvas || !isActive) return;
        // Cria um evento sintético idêntico e despacha no canvas
        const syntheticEvent = new MouseEvent(e.type, {
            clientX: e.clientX,
            clientY: e.clientY,
            screenX: e.screenX,
            screenY: e.screenY,
            movementX: e.movementX,
            movementY: e.movementY,
            button: e.button,
            buttons: e.buttons,
            bubbles: false,      // Não propagar de volta para o window
            cancelable: true
        });
        canvas.dispatchEvent(syntheticEvent);
    }

    function startForwarding() {
        if (forwarding) return;
        forwarding = true;
        ['mousemove', 'mousedown', 'mouseup'].forEach(function(type) {
            window.addEventListener(type, forwardMouseEvent, { passive: true });
        });
    }

    function stopForwarding() {
        if (!forwarding) return;
        forwarding = false;
        ['mousemove', 'mousedown', 'mouseup'].forEach(function(type) {
            window.removeEventListener(type, forwardMouseEvent);
        });
    }

    // ── Resize handler ─────────────────────────────────────────────
    function handleResize() {
        if (!canvas) return;
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    // ── Inicializador da simulação ─────────────────────────────────
    function initializeFluid() {
        if (!window.WebGLFluid || !canvas) return;

        try {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            window.WebGLFluid(canvas, {
                IMMEDIATE: true,
                TRIGGER: 'hover',
                SIM_RESOLUTION: 256,
                DYE_RESOLUTION: 1024,
                DENSITY_DISSIPATION: 0.95,
                VELOCITY_DISSIPATION: 0.95,
                PRESSURE_ITERATIONS: 40,
                CURL: 30,
                SPLAT_RADIUS: 0.28,
                SPLAT_FORCE: 6000,
                COLOR_PALETTE: ['#ffffff'],
                BACK_COLOR: '#000000',
                TRANSPARENT: true
            });

            // Inicia o reencaminhamento APÓS a biblioteca registrar seus listeners
            startForwarding();
            window.addEventListener('resize', handleResize);

        } catch (e) {
            console.error("Erro ao inicializar o WebGL Fluid Simulation:", e);
        }
    }

    // ── Observer para ciclo de vida da landing page ─────────────────
    function checkAndRun() {
        var foundLanding = document.getElementById('particleCanvas');

        if (foundLanding && !isActive) {
            isActive = true;

            // 1. Criar o canvas para o fluido WebGL
            if (!document.getElementById('fluid-canvas')) {
                canvas = document.createElement("canvas");
                canvas.setAttribute("id", "fluid-canvas");
                document.body.appendChild(canvas);
            } else {
                canvas = document.getElementById('fluid-canvas');
            }

            // 2. Carregar a biblioteca se necessário
            if (!window.WebGLFluid) {
                if (!document.getElementById('webgl-fluid-script')) {
                    var script = document.createElement("script");
                    script.id = "webgl-fluid-script";
                    script.src = "https://cdn.jsdelivr.net/npm/webgl-fluid@0.4/dist/webgl-fluid.umd.min.js";
                    script.onload = function() {
                        initializeFluid();
                    };
                    script.onerror = function() {
                        console.error("Falha ao carregar webgl-fluid CDN");
                    };
                    document.head.appendChild(script);
                }
            } else {
                initializeFluid();
            }

        } else if (!foundLanding && isActive) {
            // Fora da landing — limpar tudo
            isActive = false;
            stopForwarding();
            window.removeEventListener('resize', handleResize);

            var existingCanvas = document.getElementById('fluid-canvas');
            if (existingCanvas && existingCanvas.parentNode) {
                existingCanvas.parentNode.removeChild(existingCanvas);
            }
            canvas = null;
        }
    }

    // MutationObserver para detectar navegação dinâmica do Dash
    var observer = new MutationObserver(checkAndRun);
    observer.observe(document.body, { childList: true, subtree: true });

    // Executar imediatamente caso já esteja na landing
    checkAndRun();
}

// Inicializador robusto — funciona mesmo se o DOM já estiver pronto
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupFluid);
} else {
    setupFluid();
}
