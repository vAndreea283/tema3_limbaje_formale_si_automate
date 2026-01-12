def citeste_TA(fisier='TA.txt'):
    TA = {}
    with open(fisier, 'r') as f:
        for linie in f:
            parts = linie.strip().split()
            if len(parts) == 3:
                stare, simbol, actiune = parts
                TA[(int(stare), simbol)] = actiune
    return TA

def citeste_TS(fisier='TS.txt'):
    TS = {}
    with open(fisier, 'r') as f:
        for linie in f:
            parts = linie.strip().split()
            if len(parts) == 3:
                stare, neterminal, stare_noua = parts
                TS[(int(stare), neterminal)] = int(stare_noua)
    return TS

def verifica_TA_asteptata():
    TA_asteptata = {
        (0, 'a'): 'd5', (0, '('): 'd4',
        (1, '+'): 'd6', (1, '$'): 'acc',
        (2, '+'): 'r2', (2, '*'): 'd7', (2, ')'): 'r2', (2, '$'): 'r2',
        (3, '+'): 'r4', (3, '*'): 'r4', (3, ')'): 'r4', (3, '$'): 'r4',
        (4, 'a'): 'd5', (4, '('): 'd4',
        (5, '+'): 'r6', (5, '*'): 'r6', (5, ')'): 'r6', (5, '$'): 'r6',
        (6, 'a'): 'd5', (6, '('): 'd4',
        (7, 'a'): 'd5', (7, '('): 'd4',
        (8, '+'): 'd6', (8, ')'): 'd11',
        (9, '+'): 'r1', (9, '*'): 'd7', (9, ')'): 'r1', (9, '$'): 'r1',
        (10, '+'): 'r3', (10, '*'): 'r3', (10, ')'): 'r3', (10, '$'): 'r3',
        (11, '+'): 'r5', (11, '*'): 'r5', (11, ')'): 'r5', (11, '$'): 'r5',
    }
    return TA_asteptata

def verifica_TS_asteptata():
    TS_asteptata = {
        (0, 'E'): 1, (0, 'T'): 2, (0, 'F'): 3,
        (4, 'E'): 8, (4, 'T'): 2, (4, 'F'): 3,
        (6, 'T'): 9, (6, 'F'): 3,
        (7, 'F'): 10,
    }
    return TS_asteptata

def compara_tabele():
    print("=" * 60)
    print("VERIFICARE TABELE GENERATE")
    print("=" * 60)

    try:
        TA_generata = citeste_TA('TA.txt')
        TS_generata = citeste_TS('TS.txt')
    except FileNotFoundError as e:
        print(f"\nEROARE: {e}")
        print("Ruleaza mai intai 'python generator_lr1.py'")
        return False

    TA_asteptata = verifica_TA_asteptata()
    TS_asteptata = verifica_TS_asteptata()

    # Verificare TA
    print("\nVERIFICARE TABELA DE ACTIUNI (TA)")
    print("-" * 60)

    erori_TA = 0
    for cheie, valoare_asteptata in TA_asteptata.items():
        valoare_generata = TA_generata.get(cheie, 'LIPSA')

        if valoare_generata == valoare_asteptata:
            status = "✓"
        else:
            status = "✗"
            erori_TA += 1

        stare, simbol = cheie
        print(f"{status} TA[{stare}, '{simbol}'] = {valoare_generata:5s} "
              f"(așteptat: {valoare_asteptata})")

    # Intrari extra in TA generata
    extra_TA = set(TA_generata.keys()) - set(TA_asteptata.keys())
    if extra_TA:
        print(f"\n! Intrari EXTRA in TA generata: {len(extra_TA)}")
        for cheie in sorted(extra_TA):
            print(f"   TA[{cheie[0]}, '{cheie[1]}'] = {TA_generata[cheie]}")

    # Verificare TS
    print("\nVERIFICARE TABELA DE SALT (TS)")
    print("-" * 60)

    erori_TS = 0
    for cheie, valoare_asteptata in TS_asteptata.items():
        valoare_generata = TS_generata.get(cheie, 'LIPSA')

        if valoare_generata == valoare_asteptata:
            status = "✓"
        else:
            status = "✗"
            erori_TS += 1

        stare, neterminal = cheie
        print(f"{status} TS[{stare}, '{neterminal}'] = {valoare_generata:3} "
              f"(așteptat: {valoare_asteptata})")

    # Intrari extra in TS generata
    extra_TS = set(TS_generata.keys()) - set(TS_asteptata.keys())
    if extra_TS:
        print(f"\nIntrari EXTRA in TS generata: {len(extra_TS)}")
        for cheie in sorted(extra_TS):
            print(f"   TS[{cheie[0]}, '{cheie[1]}'] = {TS_generata[cheie]}")

    # Rezultat final
    print("\n" + "=" * 60)
    print("REZULTAT FINAL")
    print("=" * 60)

    if erori_TA == 0 and erori_TS == 0:
        print("✓ TOATE TESTELE AU TRECUT!")
        print(f"   TA: {len(TA_asteptata)} intrari corecte")
        print(f"   TS: {len(TS_asteptata)} intrari corecte")

        if extra_TA or extra_TS:
            print(f"\n!  Nota: Exista {len(extra_TA) + len(extra_TS)} "
                  "intrari extra (posibil din stari redundante)")

        return True
    else:
        print(f"TESTELE AU EȘUAT!")
        print(f"   Erori in TA: {erori_TA}")
        print(f"   Erori in TS: {erori_TS}")
        return False

def test_parsare_sir():
    """Testează un șir simplu: a+a*a"""
    print("\n" + "=" * 60)
    print("TEST PARSARE ȘIR: a+a*a")
    print("=" * 60)

    print("\nPașii așteptați pentru șirul 'a+a*a':")
    print("1. Stiva: 0 | Intrare: a+a*a$ | Acțiune: d5 (shift)")
    print("2. Stiva: 0a5 | Intrare: +a*a$ | Acțiune: r6 (reduce F->a)")
    print("3. Stiva: 0F3 | Intrare: +a*a$ | Acțiune: r4 (reduce T->F)")
    print("4. Stiva: 0T2 | Intrare: +a*a$ | Acțiune: r2 (reduce E->T)")
    print("5. Stiva: 0E1 | Intrare: +a*a$ | Acțiune: d6 (shift)")
    print("6. ...")
    print("N. Stiva: 0E1 | Intrare: $ | Acțiune: acc (ACCEPTAT)")

    print("\n💡 Pentru test complet, rulează programul C++ cu TA.txt și TS.txt")

if __name__ == "__main__":
    print("\n🔍 SCRIPT DE TESTARE - GENERATOR LR(1)\n")

    succes = compara_tabele()
    test_parsare_sir()

    print("\n" + "=" * 60)
    if succes:
        print("✅ Tabelele sunt CORECTE și pot fi folosite în C++!")
    else:
        print("⚠️  Verifică implementarea generatorului")
    print("=" * 60 + "\n")