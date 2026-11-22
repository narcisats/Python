
import re
import yt_dlp


def extrair_id_video(url):
    resultado = re.search(r"/video/(\d+)", url)

    if resultado:
        return resultado.group(1)

    return None


def consultar_metricas(id_video):
    url = f"https://www.tiktok.com/@gmmtvofficial/video/{id_video}"

    opcoes = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        dados = ydl.extract_info(url, download=False)

    if not dados:
        raise ValueError("O TikTok não retornou dados do vídeo.")

    return {
        "success": True,
        "viewCount": dados.get("view_count") or 0,
        "likeCount": dados.get("like_count") or 0,
        "commentCount": dados.get("comment_count") or 0,
        "shareCount": dados.get("repost_count") or 0,
    }
