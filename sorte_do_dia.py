import streamlit as st
import random
import requests
from datetime import datetime, date

# 🎨 Lista de nomes de cores possíveis
cores_disponiveis = ["Azul Cósmico", "Verde Esperança", "Vermelho Paixão", "Roxo Místico"]

# 🔁 Converter nome de cor em hexadecimal
def cor_para_hex(cor_nome):
    mapa_cores = {
        "Azul Cósmico": "#5DADE2",
        "Verde Esperança": "#58D68D",
        "Vermelho Paixão": "#EC7063",
        "Roxo Místico": "#AF7AC5"
    }
    return mapa_cores.get(cor_nome, "#FFFFFF")  # branco por padrão

# 🔮 Descobrir signo com base na data
def descobrir_signo(data_nascimento):
    dia = data_nascimento.day
    mes = data_nascimento.month
    signos = [
        ((1, 20), (2, 18), "Aquário"),
        ((2, 19), (3, 20), "Peixes"),
        ((3, 21), (4, 19), "Áries"),
        ((4, 20), (5, 20), "Touro"),
        ((5, 21), (6, 20), "Gêmeos"),
        ((6, 21), (7, 22), "Câncer"),
        ((7, 23), (8, 22), "Leão"),
        ((8, 23), (9, 22), "Virgem"),
        ((9, 23), (10, 22), "Libra"),
        ((10, 23), (11, 21), "Escorpião"),
        ((11, 22), (12, 21), "Sagitário"),
        ((12, 22), (1, 19), "Capricórnio")
    ]
    for inicio, fim, signo in signos:
        if (mes == inicio[0] and dia >= inicio[1]) or (mes == fim[0] and dia <= fim[1]):
            return signo.lower()
    return "desconhecido"

# 🌐 API Aztro via RapidAPI
def buscar_horoscopo_rapidapi(signo):
    url = f"https://aztro.p.rapidapi.com/?sign={signo}&day=today"
    headers = {
        "X-RapidAPI-Key": "9f4022a5b4msh9d032fc15f14369p17ccb7jsnf5de31614759",  # 🔁 Sua chave
        "X-RapidAPI-Host": "aztro.p.rapidapi.com"
    }

    try:
        response = requests.post(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "description": data.get("description", "Hoje os astros estão ocultos."),
                "mood": data.get("mood", "neutro"),
                "lucky_number": data.get("lucky_number", "0"),
                "color": data.get("color", "Roxo Místico"),
                "tema": "geral"
            }
        else:
            return None
    except Exception as e:
        print("Erro na API:", e)
        return None

# 🔁 Fallback: horóscopo fake
def buscar_horoscopo_fake(signo):
    humores = ["happy", "sad", "angry", "excited", "bored", "content", "neutral"]
    frases_base = {
        "love": [
            f"Talvez hoje seja o dia que você finalmente pare de stalkear o crush, {signo.capitalize()}. Ou não.",
            f"Amor no ar? Talvez. Mas pode ser só alergia mesmo, {signo.capitalize()}."
        ],
        "money": [
            f"{signo.capitalize()}, hoje você vai pensar duas vezes antes de pedir delivery. Boa escolha.",
            f"Seu saldo pode não estar positivo, mas sua vibe tá. Mais ou menos."
        ],
        "health": [
            f"Cuidado com as costas, {signo.capitalize()}. Ou com o coração. Ou com o que sobrou do seu sono.",
            f"Hoje é um ótimo dia pra começar a dieta… ou só pensar nela."
        ],
        "career": [
            f"Aviso do universo: não aceite convites pra reuniões que poderiam ser e-mails.",
            f"{signo.capitalize()}, talvez seja um bom momento pra *parecer* produtivo. O resto a gente finge."
        ]
    }

    tema = random.choice(list(frases_base.keys()))
    frase_escolhida = random.choice(frases_base[tema])
    humor = random.choice(humores)

    return {
        "description": frase_escolhida,
        "mood": humor,
        "lucky_number": str(random.randint(1, 99)),
        "color": random.choice(cores_disponiveis),
        "tema": tema
    }

# 💬 Mensagem por humor
def mensagem_por_humor(humor, nome):
    humor = humor.lower()
    respostas = {
        "happy": f"😄 {nome}, tá tudo fluindo! Aproveita e espalha essa vibe, mas sem esfregar na cara dos outros, né?",
        "sad": f"😢 {nome}, hoje talvez seja melhor evitar filmes tristes e chamadas de vídeo com o ex.",
        "angry": f"😠 {nome}, respira fundo. Nem todo mundo merece um textão... mas alguns talvez mereçam sim.",
        "excited": f"🤩 {nome}, canaliza essa energia! Só cuidado pra não sair marcando reunião às 22h por empolgação.",
        "bored": f"😐 {nome}, o tédio bateu? Vai que hoje o destino te surpreende... ou não.",
        "content": f"🙂 {nome}, tá de boas? Ótimo. Mas não abaixa a guarda, Mercúrio ainda tá retrógrado.",
        "neutral": f"😶 {nome}, seu dia tá tipo arroz branco: neutro, mas alimenta.",
    }
    return respostas.get(humor, f"🔮 {nome}, hoje o universo tá misterioso... e você também.")

# 🧙 Interface principal
st.title("🔮 Sua sorte do dia - Astrologia Mística")

# Inputs
data_padrao = date(1900, 1, 1)
nome = st.text_input("Qual o seu nome?")
data_nasc = st.date_input("Sua data de nascimento", value=data_padrao, min_value=data_padrao, max_value=date.today())

# Quando dados forem preenchidos
if nome and data_nasc != data_padrao:
    clicou = st.button("✨ Ver minha sorte do dia")

    if clicou:
        signo = descobrir_signo(data_nasc)
        dados = buscar_horoscopo_rapidapi(signo)

        if dados is None:
            st.warning("⚠️ API oficial do universo indisponível. Consultando os astros manualmente...")
            dados = buscar_horoscopo_fake(signo)

        if dados:
            data_nasc_formatada = data_nasc.strftime('%d/%m/%Y')
            data_hoje_formatada = date.today().strftime('%d/%m/%Y')
            cor_fundo = cor_para_hex(dados['color'])

            # Altera fundo
            st.markdown(
                f"""
                <style>
                    .stApp {{
                        background-color: {cor_fundo};
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )

            # Exibição
            st.subheader(f"Olá, {nome}! Seu signo é **{signo.capitalize()}**")
            st.markdown(f"📅 Nascimento: **{data_nasc_formatada}**")
            st.markdown(f"📆 Sorte do dia: **{data_hoje_formatada}**")
            st.markdown(f"### 🔮 Tema do dia: **{dados.get('tema', 'Amor').capitalize()}**")
            st.write(f"**Resumo do dia:** {dados['description']}")
            st.markdown(f"### 🪐 Humor do dia: **{dados['mood']}**")
            st.write(f"**Número da sorte:** {dados['lucky_number']}")
            st.write(f"**Cor do dia:** {dados['color']}")

            st.markdown("---")
            mensagem = mensagem_por_humor(dados['mood'], nome)
            st.success(mensagem)
        else:
            st.error("Não conseguimos consultar os astros hoje. Tente novamente mais tarde.")