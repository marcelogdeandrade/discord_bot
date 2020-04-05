from discord.ext import commands
from marcelo_bot.youtube_downloader import YoutubeDownloader
from marcelo_bot.message_formater import MessageFormater
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.songs_queue = []
        self.now_playing = None

    def _next_song(self, ctx):
        """Go to next song on queue"""
        self.now_playing = None
        if self.songs_queue:
            self._play_song(ctx)
            asyncio.run_coroutine_threadsafe(self.queue(ctx),
                                                 self.bot.loop)
        else:
            ctx.send("Song queue ended.")

    def _play_song(self, ctx):
        """Streams a song from Youtube"""
        yt_downloader = self.songs_queue.pop(0) 
        self.now_playing = yt_downloader  
        player = yt_downloader.get_player()
        ctx.voice_client.play(player, after = lambda err: self._next_song(ctx))

    @commands.command()
    async def play(self, ctx, *, url):
        """Adds a song to queue and play it"""
        print(url)
        yt_downloader = YoutubeDownloader(url)
        self.songs_queue.append(yt_downloader)
        if not self.now_playing:
            self._play_song(ctx)
        self.queue(ctx)

    @commands.command()
    async def queue(self, ctx):
        """Sends message with current queue"""
        await ctx.send(MessageFormater.queue_message(self.songs_queue, self.now_playing))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
    
    @commands.command()
    async def skip(self, ctx):
        """Skips current song on the queue"""
        if self.songs_queue:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            self._next_song(ctx)
        else:
            await ctx.send("There's no song to be skipped")
    
    @commands.command()
    async def clear(self, ctx):
        """Clears song queue"""
        self.songs_queue = []
        await ctx.send("Queue cleared.")

    
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")