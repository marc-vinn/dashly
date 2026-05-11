
Este documento detalha a nova arquitetura visual e as instruções de implementação para o **Dashly**, focando em uma experiência de usuário moderna, fluida e de alta performance.

## 1. Landing Page (Experiência Imersiva)

A porta de entrada do sistema foi redesenhada para transmitir sofisticação e clareza.

### Estética e Identidade
- **Cor de Fundo:** `#ececec` (Cinza Leve/Off-white).
- **Tipografia:** SF Pro (San Francisco). - Pode ser encontrada na pasta "assets" como SF-Pro.dmg -- SFProDisplay.ttf 
- **Mensagem Principal:** *"Entenda seus dados como nunca e tome as melhores decisões com Dashly"*

### Efeito de Partículas (AntiGravity Mouse)
Um fundo interativo que reage ao movimento do mouse, criando uma sensação de profundidade.

**Especificações Técnicas:**
- **Opacidade:** Partículas sutis com `rgba(255, 255, 255, 0.3)`.
- **Performance:** Renderização via `Canvas API` utilizando `requestAnimationFrame` para manter 60fps estáveis.
- **Responsividade:** Listener de `resize` acoplado para recalcular as dimensões do canvas dinamicamente.

A transição entre a Landing Page e o Dashboard deve ser feita via troca de rotas (ou alteração de estado no Dash/Flutter), garantindo que o efeito de partículas seja pausado para economizar recursos de hardware enquanto o usuário estiver no Dashboard.

```javascript
// Lógica de Redimensionamento
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    init(); // Reinicializa partículas para preencher o novo espaço
});

Botão "Iniciar Análise" (Liquid Glass)
Logo abaixo do texto principal, encontra-se o botão de ação principal.

Efeito Liquid Glass: O botão utiliza um fundo semi-transparente com backdrop-filter: blur(15px), bordas finas esbranquiçadas e uma animação de "onda" interna que simula líquido sob o vidro ao interagir com o mouse.

O Dashboard será uma aplicação web que deve iniciar em uma landing page com tema Claro, em um tom de cinza leve #ececec e um texto Na fonte SF Pro, dizendo algo como "Entenda seus dados como nunca e tome as melhores decisões com Dashly" e ao fundo um efeito de particulas no mouse que siga uma logica como essa: /* Configuração do Fundo */



body {

    margin: 0;

    padding: 0;

    overflow: hidden; /* Evita scroll durante a interação */

    background-color: #0b0e14; /* Tom escuro profundo */

    font-family: 'Inter', sans-serif;

    color: #ffffff;

}



#particleCanvas {

    position: fixed;

    top: 0;

    left: 0;

    width: 100%;

    height: 100%;

    z-index: -1; /* Mantém atrás do texto */

    pointer-events: none; /* Garante que cliques passem para os botões */

}



.content {

    position: relative;

    z-index: 1;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    height: 100vh;

    text-align: center;

    pointer-events: auto;

}



/* Tipografia Estilo AntiGravity */

h1 {

    font-size: 3rem;

    font-weight: 300;

    letter-spacing: -1px;

    background: linear-gradient(to bottom, #fff, #888);

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

}

const canvas = document.getElementById('particleCanvas');

const ctx = canvas.getContext('2d');



let particles = [];

const mouse = { x: null, y: null, radius: 150 };



window.addEventListener('mousemove', (event) => {

    mouse.x = event.x;

    mouse.y = event.y;

});



class Particle {

    constructor(x, y) {

        this.x = x;

        this.y = y;

        this.size = Math.random() * 2 + 1;

        this.baseX = this.x;

        this.baseY = this.y;

        this.density = (Math.random() * 30) + 1;

    }



    draw() {

        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';

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

    canvas.width = window.innerWidth;

    canvas.height = window.innerHeight;

    particles = [];

    for (let i = 0; i < 150; i++) {

        let x = Math.random() * canvas.width;

        let y = Math.random() * canvas.height;

        particles.push(new Particle(x, y));

    }

}



function animate() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < particles.length; i++) {

        particles[i].draw();

        particles[i].update();

    }

    requestAnimationFrame(animate);

}



init();

animate();

Opacidade: Mantenha as partículas sutis (rgba(255,255,255, 0.3)) para não distrair da leitura.

Performance: Use requestAnimationFrame para garantir que o efeito rode a 60fps sem sobrecarregar a CPU.

Responsividade: Recalcule o tamanho do canvas no evento resize da janela.



e logo abaixo um botao com o efeito de liquid glass animado ao passar o mouse escrito "Iniciar analise" - Utilize o agente de design para isso, ele saberá o que fazer



----



Ao clicar no botão o usuario será levado para a pagina do dashboard que deixará de ter o design atual e pasará a ter algo parecido com isso: {

  "themeName": "ProductSalesDashboardTheme",

  "version": "1.0",

  "description": "A clean, modern, light-themed dashboard UI guide with a focus on neon-lime accents and soft glassmorphism.",

  "globalStyles": {

    "backgroundColor": "#F4F5F7",

    "fontFamily": "San Francisco, Helvetica Neue, Helvetica, Arial, sans-serif",

    "mainTextColor": "#1A1D21",

    "secondaryTextColor": "#717680",

    "accentColor": "#A1E63D",

    "borderRadius": "24px"

  },

  "buttons": {

    "default": {

      "design": {

        "backgroundColor": "#FFFFFF",

        "textColor": "#1A1D21",

        "borderRadius": "20px",

        "padding": "12px 20px",

        "fontSize": "14px",

        "fontWeight": "medium",

        "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.05)",

        "transition": "all 0.2s ease"

      },

      "interactions": {

        "hover": {

          "backgroundColor": "#F9FAFB"

        }

      }

    },

    "primary": {

      "design": {

        "backgroundColor": "#1A1D21",

        "textColor": "#FFFFFF",

        "borderRadius": "20px",

        "padding": "12px 20px"

      },

      "examples": ["'Dashboard' tab", "'Create a report'"]

    },

    "icon": {

      "design": {

        "backgroundColor": "#FFFFFF",

        "color": "#1A1D21",

        "borderRadius": "50%",

        "padding": "10px",

        "display": "flex",

        "alignItems": "center",

        "justifyContent": "center"

      },

      "examples": ["Sidebar icons", "Search icon", "Settings icons in card headers", "Card expansion arrows"]

    },

    "iconPrimary": {

      "design": {

        "backgroundColor": "#1A1D21",

        "color": "#FFFFFF",

        "borderRadius": "50%"

      },

      "examples": ["Sidebar top star icon", "Header datepicker icon"]

    },

    "pillTag": {

      "design": {

        "backgroundColor": "#A1E63D",

        "textColor": "#1A1D21",

        "borderRadius": "12px",

        "padding": "4px 8px",

        "fontSize": "11px",

        "fontWeight": "semibold"

      },

      "examples": ["Positive growth percentage (+9%) in revenue chart"]

    },

    "glassCardButton": {

      "design": {

        "backgroundColor": "rgba(255, 255, 255, 0.15)",

        "backdropFilter": "blur(10px)",

        "borderRadius": "12px",

        "border": "1px solid rgba(255, 255, 255, 0.3)"

      },

      "examples": ["'Advantages' section close button (top right cross)", "'Advantages' go-to arrow"]

    }

  },

  "labelsAndCharts": {

    "general": {

      "titleTextColor": "#1A1D21",

      "valueTextColor": "#1A1D21",

      "subtitleTextColor": "#717680",

      "dataValueFontWeight": "bold"

    },

    "activityChart": {

      "type": "Bar Chart (Monochrome)",

      "bars": {

        "fill": "#EBECEF"

      },

      "highlightedValue": {

        "textColor": "#1A1D21",

        "backgroundColor": "#A1E63D",

        "borderRadius": "8px",

        "padding": "2px 6px",

        "fontWeight": "semibold"

      },

      "axes": {

        "labelTextColor": "#C1C4CC",

        "fontSize": "11px"

      }

    },

    "revenueChart": {

      "type": "Area Chart (Multi-line)",

      "primaryLine": {

        "stroke": "#A1E63D",

        "strokeWidth": "2px",

        "fill": "url(#greenGradient)"

      },

      "secondaryLine": {

        "stroke": "#D0D5DD",

        "strokeWidth": "1.5px",

        "strokeDasharray": "4 4",

        "fill": "url(#greyGradient)"

      },

      "growthLabel": {

        "backgroundColor": "#A1E63D",

        "textColor": "#1A1D21",

        "borderRadius": "12px",

        "padding": "4px 8px"

      },

      "annotations": {

        "textColor": "#C1C4CC",

        "fontSize": "11px"

      }

    },

    "advantagesCards": {

      "type": "Bar Charts (Accent Color)",

      "bars": {

        "fill": "#A1E63D",

        "borderRadius": "8px 8px 0 0"

      },

      "valueLabels": {

        "title": {

          "fontSize": "11px",

          "fontWeight": "medium"

        },

        "subtitle": {

          "fontSize": "20px",

          "fontWeight": "bold"

        }

      },

      "tagLabels": {

        "textColor": "#1A1D21",

        "backgroundColor": "#A1E63D",

        "borderRadius": "8px",

        "fontWeight": "semibold"

      }

    },

    "totalSpendChart": {

      "type": "Line Chart with Points",

      "line": {

        "stroke": "#1A1D21",

        "strokeWidth": "1.5px"

      },

      "points": {

        "fill": "#1A1D21",

        "stroke": "#FFFFFF",

        "strokeWidth": "1px"

      },

      "highlightedValue": {

        "backgroundColor": "#A1E63D",

        "textColor": "#1A1D21",

        "borderRadius": "12px",

        "fontWeight": "semibold"

      },

      "axes": {

        "textColor": "#C1C4CC"

      }

    }

  },

  "assets": {

    "icons": [

      {

        "name": "Dashboard logo",

        "type": "SVG",

        "color": "#1A1D21"

      }

    ]

  }

}



Ignore os nomes descritos e substitua pelos que ja estao sendo usados.