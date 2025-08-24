from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline,
    StableDiffusionControlNetPipeline,
    ControlNetModel,
    DPMSolverMultistepScheduler
)
from diffusers.utils import load_image
from transformers import CLIPTokenizer
from PIL import Image
import torch
import os
import cv2
import numpy as np

def truncate_prompt(prompt, max_length=77):
    """Trunca o prompt para o número máximo de tokens suportado pelo CLIP"""
    tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
    tokens = tokenizer.tokenize(prompt)
    
    if len(tokens) > max_length:
        print(f"[Aviso] O prompt foi truncado de {len(tokens)} para {max_length} tokens")
        truncated_tokens = tokens[:max_length]
        return tokenizer.convert_tokens_to_string(truncated_tokens)
    return prompt

def gerar_imagem(
    prompt,
    nome_arquivo="imagem_gerada.png",
    modo="text2img",  # modos: "text2img", "img2img", "controlnet"
    imagem_base_path=None
):
    # Configuração do dispositivo
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    print(f"[Modo selecionado] {modo}")

    # Garante que diretório exista
    os.makedirs("static/imagens", exist_ok=True)
    caminho_saida = os.path.join("static/imagens", nome_arquivo)

    # Trunca o prompt se for muito longo
    truncated_prompt = truncate_prompt(prompt)

    # ----------- MODO 1: TEXT TO IMAGE -----------
    if modo == "text2img":
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", torch_dtype=dtype
        ).to(device)
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.enable_attention_slicing()

        imagem = pipe(prompt=truncated_prompt, num_inference_steps=30).images[0]

    # ----------- MODO 2: IMAGE TO IMAGE -----------
    elif modo == "img2img":
        assert imagem_base_path, "Imagem base é obrigatória no modo img2img"

        imagem_base = Image.open(imagem_base_path).convert("RGB").resize((512, 512))

        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", torch_dtype=dtype
        ).to(device)
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.enable_attention_slicing()

        imagem = pipe(
            prompt=truncated_prompt,
            image=imagem_base,
            strength=0.75,
            guidance_scale=7.5,
            num_inference_steps=30
        ).images[0]

    # ----------- MODO 3: CONTROLNET (CANNY EDGE) -----------
    elif modo == "controlnet":
        assert imagem_base_path, "Imagem base é obrigatória no modo controlnet"

        imagem_base = load_image(imagem_base_path).resize((512, 512))

        # Detecta bordas com Canny
        np_image = np.array(imagem_base)
        edges = cv2.Canny(np_image, 100, 200)
        edges = Image.fromarray(edges).convert("RGB")

        controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-canny", torch_dtype=dtype
        )

        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=controlnet,
            torch_dtype=dtype
        ).to(device)

        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.enable_attention_slicing()

        imagem = pipe(
            prompt=truncated_prompt,
            image=edges,
            num_inference_steps=30,
            guidance_scale=7.5,
            controlnet_conditioning_scale=1.0
        ).images[0]

    else:
        raise ValueError("Modo inválido. Use 'text2img', 'img2img' ou 'controlnet'.")

    imagem.save(caminho_saida)
    print(f"[✅ Imagem salva em] {caminho_saida}")
