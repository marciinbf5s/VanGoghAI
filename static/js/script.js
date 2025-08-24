document.getElementById("btn-gerar-imagem").addEventListener("click", async () => {
    const prompt = document.getElementById("prompt").value;
    if (!prompt) {
        alert("Digite um prompt para gerar a imagem!");
        return;
    }

    // Abre modal de loading
    const modalLoading = new bootstrap.Modal(document.getElementById("modalLoading"));
    modalLoading.show();

    try {
        // Chama backend para gerar imagem
        const response = await fetch("/gerar-imagem", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt })
        });

        if (!response.ok) throw new Error("Erro ao gerar imagem");

        const data = await response.json();

        // Fecha modal de loading
        modalLoading.hide();

        // Preenche modal de resultado
        document.getElementById("imagemGerada").src = data.url;
        document.getElementById("btnDownload").href = data.url;

        // Abre modal de resultado
        const modalResultado = new bootstrap.Modal(document.getElementById("modalResultado"));
        modalResultado.show();

    } catch (error) {
        modalLoading.hide();
        alert("Erro: " + error.message);
    }
});
const textarea = document.getElementById('prompt');

textarea.addEventListener('input', () => {
  // Reseta a altura para calcular o scrollHeight corretamente
  textarea.style.height = 'auto';
  // Ajusta a altura para o conteúdo, respeitando max-height do CSS
  textarea.style.height = Math.min(textarea.scrollHeight, 192) + 'px'; // 192px = 12rem (aprox)
});


const toggleButton = document.getElementById('theme-toggle');
toggleButton.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  if (document.body.classList.contains('dark-mode')) {
    toggleButton.textContent = 'Modo Claro';
  } else {
    toggleButton.textContent = 'Modo Escuro';
  }
});