# Este é o arquivo de configuração do módulo tickets.
# Preencha este arquivo sem apagar os comentários, pois eles indicam,
# corretamente, qual valor deve ser atribuído a cada espaço de variável

# Cor do embed do canal de denúncias:
report_ticket_colour = 16711680 #ff0000

# Cor do embed do canal de dúvidas:
help_ticket_colour = 16776960 #ffff00

# Cor do embed do canal de bugs:
bugs_ticket_colour = 16747520 #ff8c00

# Cor do embed do canal de avaliação:
feedback_ticket_colour = 61680 #00ffff

# Cor do embed do canal de banimentos:
bans_ticket_colour = 16711680 #ff0000

# Cor do emebed do canal de inscrição:
staff_ticket_colour = 16776960 #ffff00

# IDs dos canais de ticket:
ticket_system_channels = [
    # [0] ID do canal de denúncias:
    777437928807858186,
    # [1] ID do canal de dúvidas:
    778034150212501506,
    # [2] ID do canal de bugs:
    778748532643070002,
    # [3] ID do canal de avaliação:
    778749045425569813,
    # [4] ID do canal de banimentos:
    780656872990048286,
    # [5] ID do canal de inscrição à Staff:
    800119421741039658
]

# IDs das categorias nas quais os canais de ticket serão criados:
ticket_system_categories = [
    # [0] Categoria de denúncias:
    777446415344861184,
    # [1] Categoria de dúvidas:
    778738025667887136,
    # [2] Categoria de bugs:
    778761253073977374,
    # [3] Categoria de avaliações:
    778761731873832967,
    # [4] Categoria de banimentos:
    780969736241807401
]

# IDs dos cargos que terão acesso aos canais de ticket específicos:
ticket_system_roles = [
    # [0] Administrador Chefe - Categorias denúncias, avaliações e banimentos:
    776946513208934430,
    # [1] Staff - Categoria dúvidas:
    777278739527893002,
    # [2] Programador - Categoria bugs:
    777301618654838805
]