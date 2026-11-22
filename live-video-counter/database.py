
import sqlite3
from pathlib import Path
from datetime import datetime

CAMINHO_BANCO = Path(__file__).resolve().parent / "historico.db"


def criar_banco():
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                visualizacoes INTEGER NOT NULL,
                curtidas INTEGER NOT NULL,
                comentarios INTEGER NOT NULL,
                compartilhamentos INTEGER NOT NULL,
                data_consulta TEXT NOT NULL
            )
        """)


def salvar_metricas(video_id, metricas):

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.execute("""
            INSERT INTO historico (
                video_id,
                visualizacoes,
                curtidas,
                comentarios,
                compartilhamentos,
                data_consulta
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            video_id,
            metricas["viewCount"],
            metricas["likeCount"],
            metricas["commentCount"],
            metricas["shareCount"],
            datetime.now().isoformat(timespec="seconds")
        ))


def consultar_historico(video_id):
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        cursor = conexao.execute("""
            SELECT
                visualizacoes,
                curtidas,
                comentarios,
                compartilhamentos,
                data_consulta
            FROM historico
            WHERE video_id = ?
            ORDER BY id ASC
        """, (video_id,))

        return cursor.fetchall()
