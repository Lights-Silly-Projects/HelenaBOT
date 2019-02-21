import discord

servants = {
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "40",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "50",
    "51",
    "52",
    "53",
    "54",
    "55",
    "56",
    "57",
    "58",
    "59",
    "60",
    "61",
    "62",
    "63",
    "64",
    "65",
    "66",
    "67",
    "68",
    "69",
    "70",
    "71",
    "72",
    "73",
    "74",
    "75",
    "76",
    "77",
    "78",
    "79",
    "80",
    "81",
    "82",
    "83",
    "84",
    "85",
    "86",
    "87",
    "88",
    "89",
    "90",
    "91",
    "92",
    "93",
    "94",
    "95",
    "96",
    "97",
    "98",
    "99",
    "100",
    "101",
    "102",
    "103",
    "104",
    "105",
    "106",
    "107",
    "108",
    "109",
    "110",
    "111",
    "112",
    "113",
    "114",
    "115",
    "116",
    "117",
    "118",
    "119",
    "120",
    "121",
    "122",
    "123",
    "124",
    "125",
    "126",
    "127",
    "128",
    "129",
    "130",
    "131",
    "132",
    "133",
    "134",
    "135",
    "136",
    "137",
    "138",
    "139",
    "140",
    "141",
    "142",
    "143",
    "144",
    "145",
    "146",
    "147",
    "148",
    "149",
    "150",
    "151",
    "152",
    "153",
    "154",
    "155",
}

# TO-DO: add powerMod and superEffective variables

def calc_dmg(name, atk, maxAtk, atkMod, defMod, cardMod, npDamageMod, atkModLow, defModLow, cardModLow, npDamageModLow, atkModMax, defModMax, cardModMax, npDamageModMax, dmgPlusAdd=0, npDamageMultiplier1=0, npDamageMultiplier2=0, npDamageMultiplier3=0, npDamageMultiplier4=0, npDamageMultiplier5=0, NP="1", offensiveNP=True, class_bonus=True, random=True, grailed=False, buffed="Max", servantClass="Saber", npCardType="Buster"):
    if offensiveNP is True:
        if grailed:
            servantAtk = maxAtk
        else:
            servantAtk = atk

        isNP = 1

        if npCardType is "Buster":
            cardDamageValue = 1.5
        elif npCardType is "Arts":
            cardDamageValue = 1
        else:
            cardDamageValue = 0.8

        if buffed is "None":
            atkMod = atkModLow
            defMod = defModLow
            cardMod = cardModLow
            npDamageMod = npDamageModLow
        elif buffed is "Medium":
            atkMod = atkMod
            defMod = defMod
            cardMod = cardMod
            npDamageMod = npDamageMod
        else:
            atkMod = atkModMax
            defMod = defModMax
            cardMod = cardModMax
            npDamageMod = npDamageModMax


        if servantClass is "Berserker" or "Ruler" or "Avenger":
            classAtkBonus = 1.1
        elif servantClass is "Lancer":
            classAtkBonus = 1.05
        elif servantClass is "Archer":
            classAtkBonus = 0.95
        elif servantClass is "Caster" or "Assassin":
            classAtkBonus = 0.9

        if servantClass is "Berserker":
            triangleModifier = 1.5
        elif class_bonus:
            triangleModifier = 2
        else:
            triangleModifier = 1

        if NP == 2:
            npDamageMultiplier = npDamageMultiplier2
        elif NP == 3:
            npDamageMultiplier = npDamageMultiplier3
        elif NP == 4:
            npDamageMultiplier = npDamageMultiplier4
        elif NP == 5:
            npDamageMultiplier = npDamageMultiplier5
        else: 
            npDamageMultiplier = npDamageMultiplier1

        if random:
            randomModifier = random.uniform(0.9, 1.1)
        else:
            randomModifier = 1

        dmg = servantAtk * npDamageMultiplier * (cardDamageValue * (1 + cardMod)) * classAtkBonus * triangleModifier * randomModifier * 0.23 * (1 + atkMod - defMod) * {1 + (npDamageMod * isNP)} + dmgPlusAdd
    else:
        ctx.channel.send('This Servant does not have an offensive-type Noble Phantasm.')  