import asyncio
import aiohttp
import re


async def download_music(music_name):
    download_url = None
    async with aiohttp.ClientSession() as session:
        # Search for download link across multiple websites
        for i in range(1, 1001):
            url = f"https://example-website-{i}.com/search?q={music_name}"
            async with session.get(url) as response:
                html = await response.text()
                # Extract download link using regular expression
                match = re.search(r"https?://.*\.mp3", html)
                if match:
                    download_url = match.group()
                    break

    if download_url:
        # Download the music file
        print(f"Downloading music: {music_name}")
        with open(f"{music_name}.mp3", "wb") as f:
            async with session.get(download_url) as response:
                async for chunk in response.content.iter_chunks():
                    f.write(chunk)
        print(f"Music downloaded: {music_name}")
    else:
        print(f"Music not found: {music_name}")


async def main():
    music_name = input("Enter music name: ")
    tasks = []
    for i in range(10):  # Create 10 tasks to search different websites simultaneously
        tasks.append(asyncio.create_task(download_music(f"{music_name}-{i+1}")))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
