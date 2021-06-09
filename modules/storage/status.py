# Este arquivo armazena as configurações do módulo status
# activity() e status() são listas de strings que armazenam os status
# que serão utilizados no ciclo do BOT.

from itertools import cycle

status_delay = 5

activity = cycle([
    "Jailbreak on-line em ip.fenbrasil:27050",
    "Jailbreak offline.",
    "Jailbreak em manutenção.",
    "Jailbreak reiniciando.",
    "Zombie Plague on-line em ip.fenbrasil:27016",
    "Zombie Plague offline.",
    "Zombie Plague em manutenção.",
    "Zombie Plague reiniciando.",
    "TTT on-line em ip.fenbrasil:27015",
    "TTT offline.",
    "TTT em manutenção.",
    "TTT reiniciando."
])

statuses = cycle([
    'discord.Status.online',
    'discord.Status.dnd',
    'discord.Status.dnd',
    'discord.Status.idle',
])