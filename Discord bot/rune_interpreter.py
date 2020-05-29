def rune_convertor(rune):
    rune = rune.replace(' ', '_')
    rune = rune.replace(':', '')
    rune = rune.replace('\'', '')
    rune = rune.lower()
    return rune
