document.addEventListener("DOMContentLoaded", function () {
    let canvas = null;
    let ctx = null;
    let particles = [];
    let animationId = null;
    let isActive = false;

    const mouse = { x: null, y: null, radius: 150 };

    window.addEventListener('mousemove', (event) => {
        mouse.x = event.x;
        mouse.y = event.y;
    });

    class Particle {
        constructor(x, y, cWidth, cHeight) {
            this.x = x;
            this.y = y;
            this.size = Math.random() * 2 + 1;
            this.baseX = this.x;
            this.baseY = this.y;
            this.density = (Math.random() * 30) + 1;
        }

        draw() {
            // Partículas com cor escura já que o fundo agora é claro (#ececec)
            // A instrução dizia opacidade sutil (rgba(255,255,255, 0.3)), mas como o fundo
            // mudou para branco/cinza, o branco não vai aparecer. Vou usar cinza/preto com opacidade sutil.
            ctx.fillStyle = 'rgba(207, 11, 210, 0.41)';
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.closePath();
            ctx.fill();
        }

        update() {
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            let forceDirectionX = dx / distance;
            let forceDirectionY = dy / distance;
            let maxDistance = mouse.radius;
            let force = (maxDistance - distance) / maxDistance;
            let directionX = forceDirectionX * force * this.density;
            let directionY = forceDirectionY * force * this.density;

            if (distance < mouse.radius) {
                this.x -= directionX;
                this.y -= directionY;
            } else {
                if (this.x !== this.baseX) {
                    let dx = this.x - this.baseX;
                    this.x -= dx / 10;
                }
                if (this.y !== this.baseY) {
                    let dy = this.y - this.baseY;
                    this.y -= dy / 10;
                }
            }
        }
    }

    function init() {
        if (!canvas) return;
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        particles = [];
        for (let i = 0; i < 150; i++) {
            let x = Math.random() * canvas.width;
            let y = Math.random() * canvas.height;
            particles.push(new Particle(x, y, canvas.width, canvas.height));
        }
    }

    function animate() {
        if (!isActive || !ctx) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < particles.length; i++) {
            particles[i].draw();
            particles[i].update();
        }
        animationId = requestAnimationFrame(animate);
    }

    // Observador para iniciar/parar a animação dependendo da presença do canvas
    const observer = new MutationObserver(function (mutations) {
        const foundCanvas = document.getElementById('particleCanvas');
        if (foundCanvas && !isActive) {
            canvas = foundCanvas;
            ctx = canvas.getContext('2d');
            isActive = true;
            document.body.classList.add('landing-body');

            window.addEventListener('resize', init);
            init();
            animate();
        } else if (!foundCanvas && isActive) {
            isActive = false;
            if (animationId) cancelAnimationFrame(animationId);
            window.removeEventListener('resize', init);
            document.body.classList.remove('landing-body');
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
