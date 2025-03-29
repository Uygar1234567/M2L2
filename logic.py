import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.power=random.randint(1, 100)
        self.hp=random.randint(1, 1000)
        self.last_feed_time=datetime.now
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]
        

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['forms'][0]['name']  # Bir Pokémon'un adını döndürme
                else:
                    return "There is a problem"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"""Pokémonunuzun ismi: {self.name}
                Pokemon gucu {self.power}
                Pokemon HP {self.hp}"""  # Pokémon'un adını içeren dizeyi döndürür
    

    async def show_ability(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['abilities'][0]['ability']['name']  
                else:
                    return "kusura bakma"  # İstek başarısız olursa varsayılan adı döndürür

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémonun resmini almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    image_url=data['sprites']['front_default']
                    return image_url  # Bir Pokémon'un adını döndürme
                else:
                    return None  # İstek başarısız olursa varsayılan adı döndürür
                
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance=random.randint(1,5)
            if chance==1:
                return("sihirbaz pokeMON kAlKaN kullandi")
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu{enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"
        


    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon'un sağlığı geri yüklenir. Mevcut sağlık: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz: {current_time+delta_time}"





class Wizard(Pokemon):
    def feed(self):
        return super().feed(feed_interval=10)
    

class Fighter(Pokemon):
    async def attack(self, enemy):
        süper_güç = random.randint(5, 15)  
        self.güç += süper_güç
        sonuç = await super().attack(enemy)  
        self.güç -= süper_güç
        return sonuç + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {süper_güç}"
    
    def feed(self):
        return super().feed(hp_increase=20)



if __name__ == '__main__':
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    print(Wizard.info())
    print()
    print(Fighter.info())
    print()
    print(Fighter.attack(wizard))

