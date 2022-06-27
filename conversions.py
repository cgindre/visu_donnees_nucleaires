# -*- coding: utf-8 -*-

AVOGADRO = 6.02214e23
NUMBER_OF_DIGITS = 4


def convertit_temps(old_value, old_unit, new_unit):
    """Renvoie new_value en accord avec la nouvelle unitée désirée"""
    old_value = float(old_value)

    if(old_unit == new_unit):
        return old_value

    elif(old_unit == 's'):
        if(new_unit == 'mn'):
            new_value = old_value / 60
        if (new_unit == 'h'):
            new_value = old_value / (60 * 60)
        if (new_unit == 'j'):
            new_value = old_value / (60 * 60 * 24)
        if (new_unit == 'an'):
            new_value = old_value / (60 * 60 * 24 * 365)

    elif (old_unit == 'mn'):
        if (new_unit == 's'):
            new_value = old_value * 60
        if (new_unit == 'h'):
            new_value = old_value / 60
        if (new_unit == 'j'):
            new_value = old_value / (60 * 24)
        if (new_unit == 'an'):
            new_value = old_value / (60 * 24 * 365)

    elif (old_unit == 'h'):
        if (new_unit == 's'):
            new_value = old_value * (60 * 60)
        if (new_unit == 'mn'):
            new_value = old_value * 60
        if (new_unit == 'j'):
            new_value = old_value / 24
        if (new_unit == 'an'):
            new_value = old_value / (24 * 365)

    elif (old_unit == 'j'):
        if (new_unit == 's'):
            new_value = old_value * (24 * 60 * 60)
        if (new_unit == 'mn'):
            new_value = old_value * (24 * 60)
        if (new_unit == 'h'):
            new_value = old_value * 24
        if (new_unit == 'an'):
            new_value = old_value / 365

    elif (old_unit == 'an'):
        if (new_unit == 's'):
            new_value = old_value * (365 * 24 * 60 * 60)
        if (new_unit == 'mn'):
            new_value = old_value * (365 * 24 * 60)
        if (new_unit == 'h'):
            new_value = old_value * (365 * 24)
        if (new_unit == 'j'):
            new_value = old_value * 365

    else : return -1

    return new_value

def scientific_notation(number):
    """renvoie string de number en notation scientifique. N, nombre de digits après vrigule """
    number = float(number)
    expr = "{:." + str(NUMBER_OF_DIGITS) + "e}"
    scientific_notation = expr.format(number)
    return scientific_notation

def verifie_ligne_decoupage_temps(t1, t2, N):
    if(verifie_saisi_instant(t1) and verifie_saisi_instant(t2) and verifie_N(N)):
        return True
    else:
        return False

def verifie_N(N):
    if N.isdigit() and int(N) != 0:
        return True
    else:
        return False

def verifie_saisi_instant(tx):
    """verifie la saisie d'un instant tx (e.g. : "1.3mn") dans tableau decoupage automatique"""
    delim=0
    if tx[-2:] in ['mn','an']:
        delim=-2
    elif tx[-1:] in ['s','j','h']:
        delim=-1
    else:
        print("Unknown unit")
        return False
    return verifie_valeur(tx[0:delim])

def verifie_valeur(valeur_saisie):
    """vérifie que la valeur saisie soit bien un nombre positif"""
    try:
        Ts=float(valeur_saisie)
        if Ts >= 0:
            return True
        else:
            print("must be >= 0")
            return False
    except:
        print("could not convert to float ... ")
        return False



if __name__ == "__main__":
    #mon_nombre = 123453
    mon_nombre = 17.78603
    print("scientific_notation of ", mon_nombre, " is : ", scientific_notation(mon_nombre))

    t1 = "1.4mn"
    print(verifie_saisi_instant(t1))
    t2 = "12a"
    print(verifie_saisi_instant(t2))
    t3 = "1an"
    print(verifie_saisi_instant(t3))
    t4 = "-1an"
    print(verifie_saisi_instant(t4))

    first_test = verifie_ligne_decoupage_temps("1mn", "5mn", "3")
    print("first_test = ", first_test)

    second_test = verifie_ligne_decoupage_temps("1.4mn", "1.4mn", "-5")
    print("second_test = ", second_test)