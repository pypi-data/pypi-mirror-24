from grazyna.utils import register


@register(reg=r'^[Ss]{4,}(?:!+|.+)$')
def creeper(bot):
    bot.kick(why='Alert!')
