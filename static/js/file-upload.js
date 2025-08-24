document.addEventListener('DOMContentLoaded', function() {
    const imagemBaseInput = document.getElementById('imagem-base');
    const containerArquivos = document.getElementById('container-arquivos');
    const nomeArquivoBase = document.getElementById('nome-arquivo-base');
    const previewImagem = document.getElementById('preview-imagem'); // ← miniatura
    const btnGerar = document.getElementById('btn-gerar-imagem');

    // Objeto para armazenar os arquivos
    const arquivos = {
        base: null
    };

    // Gerenciar upload da imagem base
    imagemBaseInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            arquivos.base = e.target.files[0];
            nomeArquivoBase.textContent = arquivos.base.name;
            containerArquivos.style.display = 'block';

            // Mostrar preview da imagem
            const reader = new FileReader();
            reader.onload = function(event) {
                previewImagem.src = event.target.result;
                previewImagem.style.display = 'block';
            };
            reader.readAsDataURL(arquivos.base);
        }
    });

    // Remover arquivos
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-remover')) {
            const tipo = e.target.getAttribute('data-tipo');

            if (tipo === 'base') {
                arquivos.base = null;
                imagemBaseInput.value = '';
                nomeArquivoBase.textContent = '';
                containerArquivos.style.display = 'none';

                // Esconder preview da imagem
                previewImagem.src = '';
                previewImagem.style.display = 'none';
            }
        }
    });

    // Enviar formulário
    btnGerar.addEventListener('click', async function() {
        const prompt = document.getElementById('prompt').value.trim();

        if (!prompt) {
            alert('Por favor, insira um prompt de texto.');
            return;
        }

        const formData = new FormData();
        formData.append('prompt', prompt);

        if (arquivos.base) {
            formData.append('imagem_base', arquivos.base);
        }

        // Mostrar loading
        const modalLoading = new bootstrap.Modal(document.getElementById('modalLoading'));
        modalLoading.show();

        try {
            const response = await fetch('/gerar-imagem', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                // Mostrar imagem gerada
                const modalResultado = new bootstrap.Modal(document.getElementById('modalResultado'));
                const imgResultado = document.getElementById('imagemGerada');
                const btnDownload = document.getElementById('btnDownload');

                // Adiciona timestamp para evitar cache
                const timestamp = new Date().getTime();
                const urlComTimestamp = `${data.url}?t=${timestamp}`;

                imgResultado.src = urlComTimestamp;
                btnDownload.href = urlComTimestamp;

                modalLoading.hide();
                modalResultado.show();
            } else {
                throw new Error(data.error || 'Erro ao gerar imagem');
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao processar sua solicitação: ' + error.message);
            modalLoading.hide();
        }
    });
});
