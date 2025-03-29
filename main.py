import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random
# Bot için niyetleri (intents) ayarlama
intents = discord.Intents.default()  # Varsayılan ayarların alınması
intents.messages = True              # Botun mesajları işlemesine izin verme
intents.message_content = True       # Botun mesaj içeriğini okumasına izin verme
intents.guilds = True                # Botun sunucularla (loncalar) çalışmasına izin verme

# Tanımlanmış bir komut önekine ve etkinleştirilmiş amaçlara sahip bir bot oluşturma
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot çalışmaya hazır olduğunda tetiklenen bir olay
@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  # Botun adını konsola çıktı olarak verir

# '!go' komutu
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Mesaj yazarının adını alma
    # Kullanıcının zaten bir Pokémon'u olup olmadığını kontrol edin. Eğer yoksa, o zaman...
    if author not in Pokemon.pokemons.keys():
        chance=random.randint(1,3)
        if chance==1:
            pokemon = Pokemon(author)  # Yeni bir Pokémon oluşturma
        if chance==2:
            pokemon = Wizard(author)  # Yeni bir Pokémon oluşturma
        if chance==3:
            pokemon = Fighter(author)  # Yeni bir Pokémon oluşturma
        await ctx.send(await pokemon.info())  # Pokémon hakkında bilgi gönderilmesi
        image_url = await pokemon.show_img()  # Pokémon resminin URL'sini alma
        if image_url:
            embed = discord.Embed()  # Gömülü mesajı oluşturma
            embed.set_image(url=image_url)  # Pokémon'un görüntüsünün ayarlanması
            await ctx.send(embed=embed)  # Görüntü içeren gömülü bir mesaj gönderme
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")  # Bir Pokémon'un daha önce yaratılıp yaratılmadığını gösteren bir mesaj




@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mesajda belirtilen kullanıcıyı alırız
    if target:  # Kullanıcının belirtilip belirtilmediğini kontrol ederiz
        # Hem saldırganın hem de hedefin Pokémon sahibi olup olmadığını kontrol ederiz
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]  # Hedefin Pokémon'unu alırız
            attacker = Pokemon.pokemons[ctx.author.name]  # Saldırganın Pokémon'unu alırız
            result = await attacker.attack(enemy)  # Saldırıyı gerçekleştirir ve sonucu alırız
            await ctx.send(result)  # Saldırı sonucunu göndeririz
        else:
            await ctx.send("Savaş için her iki tarafın da Pokémon'a sahip olması gerekir!")  # Katılımcılardan birinin Pokémon'u yoksa bilgilendiririz
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")  # Saldırmak için kullanıcıyı etiketleyerek belirtmesini isteriz


@bot.command
async def feed(ctx):
    author=ctx.author.name
    if author in Pokemon.pokemons:
        pokemon=Pokemon.pokemons[author]
        response=await pokemon.feed()
        await ctx.send(response)
    else:
        await ctx.send("Pokemonun yok, !go komutunu kullan ve yine gel")



@bot.command(name="kapat")
async def close_bot(ctx):
    await ctx.send("gg...")
    await bot.close()  # Gracefully closes the bot connection

    



@bot.command(name="aptal")
async def name(ctx):
    await ctx.send("Kusura bakma")

@bot.command(name="info")
async def name(ctx):
    if ctx.author.name in Pokemon.pokemons:
        pok = Pokemon.pokemons[ctx.author.name]
        await ctx.send()


# Botun çalıştırılması
bot.run(token)
