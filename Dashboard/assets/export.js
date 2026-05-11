/**
 * exportDashboardToPDF — Gera um PDF limpo com logo + gráficos
 * Usa jsPDF + html2canvas (carregados via CDN no app.py)
 */
window.exportDashboardToPDF = async function () {
    console.log("Iniciando exportação para PDF...");
    try {
        if (!window.jspdf) {
            console.error("jsPDF não carregado na window.");
            alert("Erro: biblioteca jsPDF não carregada. Verifique sua conexão ou recarregue a página.");
            return;
        }
        
        // Exibir um alerta ou indicador de carregamento
        const shareBtn = document.getElementById('btn-share-pdf');
        const oldContent = shareBtn.innerHTML;
        shareBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });

        const pageWidth  = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        const margin     = 14;
        let cursorY      = margin;

        // 1. Logo no canto superior esquerdo
        const logoImg = document.querySelector('.header-logo');
        if (logoImg) {
            try {
                const logoCanvas = await html2canvas(logoImg, { scale: 2, backgroundColor: null });
                const logoData   = logoCanvas.toDataURL('image/png');
                const logoH      = 10;
                const logoW      = (logoCanvas.width / logoCanvas.height) * logoH;
                pdf.addImage(logoData, 'PNG', margin, cursorY, logoW, logoH);
                cursorY += logoH + 8;
            } catch (e) { console.warn('Logo não carregada:', e); }
        }

        // Linha separadora
        pdf.setDrawColor(200, 200, 200);
        pdf.line(margin, cursorY, pageWidth - margin, cursorY);
        cursorY += 6;

        // 2. Captura cada bloco individualmente (card inteiro: título, moda, média e gráfico)
        const graphEls = document.querySelectorAll('.glass-card');
        
        if (graphEls.length === 0) {
            console.warn("Nenhum gráfico encontrado na tela para exportar.");
            alert("Nenhum gráfico encontrado para exportar.");
            shareBtn.innerHTML = oldContent;
            return;
        }

        for (const el of graphEls) {
            try {
                // Captura o card inteiro mas ignora os botões de 3 pontinhos (card-actions)
                const canvas  = await html2canvas(el, { 
                    scale: 1.5, 
                    backgroundColor: '#ffffff',
                    ignoreElements: function(element) {
                        return element.classList && element.classList.contains('card-actions');
                    }
                });
                const imgData = canvas.toDataURL('image/png');

                const imgW = pageWidth - margin * 2;
                const imgH = (canvas.height / canvas.width) * imgW;

                if (cursorY + imgH > pageHeight - margin) {
                    pdf.addPage();
                    cursorY = margin;
                }

                pdf.addImage(imgData, 'PNG', margin, cursorY, imgW, imgH);
                cursorY += imgH + 8;
            } catch (e) { console.warn('Erro ao capturar gráfico:', e); }
        }

        pdf.save('dashly-relatorio.pdf');
        
        // Restaura botão
        shareBtn.innerHTML = oldContent;
        console.log("PDF gerado com sucesso.");

    } catch (err) {
        console.error("Erro fatal na exportação PDF:", err);
        alert("Ocorreu um erro ao gerar o PDF. Verifique o console.");
        const shareBtn = document.getElementById('btn-share-pdf');
        if(shareBtn) shareBtn.innerHTML = '<i class="fa-solid fa-share-nodes"></i>';
    }
};

/**
 * Download PNG individual de um bloco de gráfico.
 * Acionado pelo botão "Baixar como PNG" do DropdownMenu de cada card.
 */
document.addEventListener('click', async function (e) {
    const btn = e.target.closest('.dropdown-item-download');
    if (!btn) return;
    
    e.preventDefault();

    // Sobe até o .glass-card e encontra o gráfico
    const card   = btn.closest('.glass-card');
    const graph  = card ? card.querySelector('.js-plotly-plot') : null;
    const titulo = card ? card.querySelector('.card-header span')?.innerText || 'grafico' : 'grafico';

    if (!graph) {
        console.warn("Gráfico não encontrado no card.");
        return;
    }

    try {
        const canvas  = await html2canvas(graph, { scale: 2, backgroundColor: '#ffffff' });
        const link    = document.createElement('a');
        link.download  = `${titulo}.png`;
        link.href      = canvas.toDataURL('image/png');
        link.click();
    } catch (e) { console.error('Erro ao exportar PNG:', e); }
});
