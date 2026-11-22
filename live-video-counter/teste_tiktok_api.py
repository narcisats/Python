
import asyncio
from TikTokApi import TikTokApi


async def testar_api():
    async with TikTokApi() as api:
        await api.create_sessions(
            num_sessions=1,
            sleep_after=3,
            browser="chromium"
        )

        video = api.video(
            url="https://www.tiktok.com/@lolennn_/video/7708092046451543303")
        dados = await video.info()

        print("Dados recebidos:")
        print(dados.get("stats", {}))
        print("Estatísticas detalhadas:", dados.get("statsV2", {}))


asyncio.run(testar_api())
