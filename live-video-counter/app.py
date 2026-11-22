
import streamlit as st
from collectors.tiktok import extrair_id_video, consultar_metricas
from datetime import datetime
from database import salvar_metricas, consultar_historico
import altair as alt
from pathlib import Path
import pandas as pd

ARQUIVO_INICIO_GRAFICO = Path(__file__).resolve().parent / "inicio_grafico.txt"

if not ARQUIVO_INICIO_GRAFICO.exists():
    ARQUIVO_INICIO_GRAFICO.write_text(
        datetime.now().isoformat(timespec="seconds"),
        encoding="utf-8"
    )

inicio_grafico = ARQUIVO_INICIO_GRAFICO.read_text(
    encoding="utf-8"
).strip()


st.set_page_config(
    page_title="Live Video Counter",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Live Video Counter")

st.write("Monitoramento de visualizações de vídeos")

st.subheader("🎵 TikTok")


url_video = st.text_input(
    "Link do vídeo do TikTok",
    placeholder="https://www.tiktok.com/@usuario/video/1234567890123456789"
)


if url_video:
    id_video = extrair_id_video(url_video)

    if id_video:
        st.success(f"ID do vídeo identificado: {id_video}")
    else:
        st.warning("Não foi possível identificar o ID do vídeo.")

# Atualização automática das métricas a cada 10 segundos

# Atualização automática das métricas a cada 10 segundos
@st.fragment(run_every="2m")
def atualizar_contador():

    if url_video and id_video:
        try:
            # 1. Consultar as métricas atuais
            metricas = consultar_metricas(id_video)

            st.caption(
                f"🕒 Última consulta: {datetime.now().strftime('%H:%M:%S')}"
            )

            if metricas.get("success"):

                # 2. Salvar as métricas no banco
                salvar_metricas(id_video, metricas)

                # 3. Exibir os contadores
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "👁️ Visualizações",
                        f"{metricas['viewCount']:,}"
                    )

                with col2:
                    st.metric(
                        "❤️ Curtidas",
                        f"{metricas['likeCount']:,}"
                    )

                with col3:
                    st.metric(
                        "💬 Comentários",
                        f"{metricas['commentCount']:,}"
                    )

                with col4:
                    st.metric(
                        "🔁 Compartilhamentos",
                        f"{metricas['shareCount']:,}"
                    )

            else:
                st.error("Não foi possível obter as métricas do vídeo.")

        except Exception as erro:
            st.error(f"Erro ao consultar o vídeo: {erro}")

        # 4. Consultar e exibir o histórico
        st.divider()
        st.subheader("📊 Histórico de visualizações")

        historico = consultar_historico(id_video)

        historico = [
            registro
            for registro in historico
            if registro[4] >= inicio_grafico
        ]

        st.write(
            f"Total de medições registradas: {len(historico)}"
        )

        if historico:
            
            menor_valor = min(registro[0] for registro in historico)
            maior_valor = max(registro[0] for registro in historico)

            grafico = alt.Chart(
                alt.Data(values=[
                    {
                        "Horário": registro[4],
                        "Visualizações": registro[0]
                    }
                    for registro in historico
                ])
            ).mark_line(point=True).encode(
                
                x=alt.X(
                    "Horário:T",
                    title="Horário",
                    axis=alt.Axis(
                        format="%H:%M",
                        tickCount=10,
                        labelAngle=0
                    )
                ),    
                y=alt.Y(
                    "Visualizações:Q",
                    title="Visualizações",
                    scale=alt.Scale(
                        domain=[menor_valor - 5, maior_valor + 5],
                        zero=False
                    )
                ),
                tooltip=[
                    alt.Tooltip("Horário:T", title="Data e hora"),
                    alt.Tooltip(
                        "Visualizações:Q",
                        title="Visualizações",
                        format=",d"
                    )
                ]
            )

            st.altair_chart(grafico, use_container_width=True)



atualizar_contador()
