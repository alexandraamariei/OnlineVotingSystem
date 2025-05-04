import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime

# Listele de candidați și voturi
candidati = ["Elena Lasconi", "Marcel Ciolacu", "Nicolae Ciuca"]
voturi = [0, 0, 0]
votanti_verificati = []
votat_deja = {}

# Variabile pentru câmpurile de input
entry_cnp = None
entry_judet = None
fereastra_login = None

# Listele județelor pentru validarea CNP-ului
judete = {
    "01": "Alba", "02": "Arad", "03": "Arges", "04": "Bacau", "05": "Bihor", "06": "Bistrita-Nasaud",
    "07": "Botosani", "08": "Brasov", "09": "Braila", "10": "Buzau", "11": "Caras-Severin", "12": "Calarasi",
    "13": "Cluj", "14": "Constanta", "15": "Covasna", "16": "Dambovita", "17": "Dolj", "18": "Galati",
    "19": "Giurgiu", "20": "Gorj", "21": "Harghita", "22": "Hunedoara", "23": "Ialomita", "24": "Iasi",
    "25": "Ilfov", "26": "Maramures", "27": "Mehedinti", "28": "Mures", "29": "Neamt", "30": "Olt",
    "31": "Prahova", "32": "Salaj", "33": "Sibiu", "34": "Suceava", "35": "Teleorman", "36": "Timis",
    "37": "Tulcea", "38": "Valcea", "39": "Vrancea", "40": "Bucuresti", "41": "Sector 1", "42": "Sector 2",
    "43": "Sector 3", "44": "Sector 4", "45": "Sector 5", "46": "Sector 6", "51": "Calarasi", "52": "Giurgiu"
}

# Funcție pentru a verifica vârsta pe baza CNP-ului (doar secolul 21)
def verifica_varsta(cnp):
    data_nasterii = cnp[1:3] + cnp[3:5] + cnp[5:7]
    ziua = int(data_nasterii[:2])
    luna = int(data_nasterii[2:4])
    anul = int(data_nasterii[4:8])

    data_curenta = datetime.now()
    varsta = data_curenta.year - anul - ((data_curenta.month, data_curenta.day) < (luna, ziua))
    return varsta

# Funcție pentru validarea cifrei de control a CNP-ului
def validare_control(cnp):
    control = "279146358279"
    suma = 0
    for i in range(12):
        suma += int(cnp[i]) * int(control[i])
    rest = suma % 11
    if rest < 10:
        cifra_control = str(rest)
    else:
        cifra_control = "1"
    return cnp[12] == cifra_control

# Funcție pentru validarea CNP-ului (doar secolul 21)
def validare_cnp_partial(cnp):
    if len(cnp) != 13 or not cnp.isdigit():
        messagebox.showerror("Eroare", "CNP-ul trebuie să aibă exact 13 caractere numerice!")
        return False

    if cnp[0] not in ['5', '6']:
        messagebox.showerror("Eroare", "Primul caracter din CNP trebuie să fie 5 sau 6 (secolul 21)!")
        return False

    an_nastere = int(cnp[1:3])
    luna_nastere = int(cnp[3:5])
    ziua_nastere = int(cnp[5:7])

    if luna_nastere < 1 or luna_nastere > 12:
        messagebox.showerror("Eroare", "Luna din CNP este invalidă!")
        return False
    if ziua_nastere < 1 or ziua_nastere > 31:
        messagebox.showerror("Eroare", "Ziua din CNP este invalidă!")
        return False

    if an_nastere < 0 or an_nastere > 99:
        messagebox.showerror("Eroare", "Anul din CNP este invalid!")
        return False

    varsta = verifica_varsta(cnp)
    if varsta < 18:
        messagebox.showerror("Eroare", "Trebuie să ai cel puțin 18 ani pentru a vota!")
        return False

    if not validare_control(cnp):
        messagebox.showerror("Eroare", "Cifra de control din CNP este invalidă!")
        return False

    return True

# Funcție pentru a verifica județul sau sectorul doar pe baza input-ului
def verifica_judet_sector(judet_input):
    return judet_input in list(judete.values())

# Funcție de validare a votantului și deschiderea ferestrei de vot
def validare_votant():
    global entry_cnp, entry_judet, fereastra_login

    cnp = entry_cnp.get()
    judet_input = entry_judet.get()

    if cnp == "" or judet_input == "":
        messagebox.showerror("Eroare", "Te rugăm să completezi atât CNP-ul cât și județul!")
        return

    if validare_cnp_partial(cnp):
        if cnp not in votanti_verificati:
            if verifica_judet_sector(judet_input):
                votanti_verificati.append(cnp)
                votat_deja[cnp] = False
                messagebox.showinfo("Aprobare", "Verificat și aprobat! Poți vota acum.")
                fereastra_login.destroy()
                afiseaza_fereastra_candidati(cnp)
            else:
                messagebox.showerror("Eroare", "Județul specificat este invalid!")
        else:
            messagebox.showinfo("Eroare", "Ai votat deja cu acest CNP!")
    else:
        messagebox.showerror("Eroare", "CNP invalid!")

# Funcție pentru a deschide fereastra de alegeri a candidaților
def afiseaza_fereastra_candidati(cnp):
    fereastra_candidati = tk.Tk()
    fereastra_candidati.title("Alege un Candidat")

    label_bine = tk.Label(fereastra_candidati, text="Alege un candidat:")
    label_bine.pack(pady=10)

    for candidat in candidati:
        buton = tk.Button(fereastra_candidati, text=candidat, command=lambda c=candidat, f=fereastra_candidati, cnp=cnp: voteaza(c, f, cnp))
        buton.pack(pady=5)

    fereastra_candidati.mainloop()

# Funcție de vot
def voteaza(candidat, fereastra_candidati, cnp):
    global voturi, votat_deja

    if votat_deja[cnp]:
        messagebox.showinfo("Eroare", "Ai votat deja!")
        return

    index = candidati.index(candidat)
    voturi[index] += 1
    votat_deja[cnp] = True
    messagebox.showinfo("Multumim", f"Ai votat pentru {candidat}!")

    fereastra_candidati.quit()

    afiseaza_grafic()

    messagebox.showinfo("Multumesc!", "Multumim pentru vot!")
    fereastra_login.deiconify()
    plt.close()

# Funcție pentru a afișa graficul de voturi
def afiseaza_grafic():
    global voturi

    total_voturi = sum(voturi)
    procente = [vot / total_voturi * 100 if total_voturi > 0 else 0 for vot in voturi]

    fig, ax = plt.subplots()
    ax.bar(candidati, procente, color=['blue', 'green', 'red'])
    ax.set_title("Distributia voturilor")
    ax.set_xlabel("Candidati")
    ax.set_ylabel("Procentaj Voturi (%)")

    plt.tight_layout()
    plt.show()

# Funcția pentru a porni procesul de login
def start_login():
    global fereastra_login, entry_cnp, entry_judet

    fereastra_login = tk.Tk()
    fereastra_login.title("Sistem de Vot Online")

    label_cnp = tk.Label(fereastra_login, text="CNP:")
    label_cnp.pack(pady=5)
    entry_cnp = tk.Entry(fereastra_login)
    entry_cnp.pack(pady=5)

    label_judet = tk.Label(fereastra_login, text="Judet:")
    label_judet.pack(pady=5)
    entry_judet = tk.Entry(fereastra_login)
    entry_judet.pack(pady=5)

    buton_verificare = tk.Button(fereastra_login, text="Verifica si Voteaza", command=validare_votant)
    buton_verificare.pack(pady=20)

    fereastra_login.mainloop()

start_login()
