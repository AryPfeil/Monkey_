import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Connexion à la base
conn = sqlite3.connect("depenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS depenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categorie TEXT,
    montant REAL,
    date TEXT
)
""")
conn.commit()

def ajouter_depense():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter une dépense")

    tk.Label(fenetre, text="Catégorie :").grid(row=0, column=0, padx=5, pady=5)
    entree_categorie = tk.Entry(fenetre)
    entree_categorie.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(fenetre, text="Montant :").grid(row=1, column=0, padx=5, pady=5)
    entree_montant = tk.Entry(fenetre)
    entree_montant.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(fenetre, text="Date (AAAA-MM-JJ) :").grid(row=2, column=0, padx=5, pady=5)
    entree_date = tk.Entry(fenetre)
    entree_date.grid(row=2, column=1, padx=5, pady=5)

    def sauvegarder():
        try:
            categorie = entree_categorie.get()
            montant = float(entree_montant.get())
            date = entree_date.get()

            cursor.execute("INSERT INTO depenses (categorie, montant, date) VALUES (?, ?, ?)",
                           (categorie, montant, date))
            conn.commit()

            messagebox.showinfo("Succès", "✅ Dépense ajoutée avec succès !")
            fenetre.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "⚠️ Le montant doit être un nombre valide")

    tk.Button(fenetre, text="Enregistrer", command=sauvegarder).grid(row=3, column=0, columnspan=2, pady=10)

def voir_depenses():
    fenetre = tk.Toplevel(root)
    fenetre.title("Liste des dépenses")

    # Création du tableau
    colonnes = ("ID", "Catégorie", "Montant", "Date")
    table = ttk.Treeview(fenetre, columns=colonnes, show="headings")

    # Définir les en-têtes
    for col in colonnes:
        table.heading(col, text=col)
        table.column(col, width=120)

    # Récupérer les données
    cursor.execute("SELECT * FROM depenses")
    depenses = cursor.fetchall()

    for depense in depenses:
        table.insert("", tk.END, values=depense)

    table.pack(fill="both", expand=True)
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Connexion à la base
conn = sqlite3.connect("depenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS depenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categorie TEXT,
    montant REAL,
    date TEXT
)
""")
conn.commit()

def ajouter_depense():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter une dépense")

    tk.Label(fenetre, text="Catégorie :").grid(row=0, column=0, padx=5, pady=5)
    entree_categorie = tk.Entry(fenetre)
    entree_categorie.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(fenetre, text="Montant :").grid(row=1, column=0, padx=5, pady=5)
    entree_montant = tk.Entry(fenetre)
    entree_montant.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(fenetre, text="Date (AAAA-MM-JJ) :").grid(row=2, column=0, padx=5, pady=5)
    entree_date = tk.Entry(fenetre)
    entree_date.grid(row=2, column=1, padx=5, pady=5)

    def sauvegarder():
        try:
            categorie = entree_categorie.get()
            montant = float(entree_montant.get())
            date = entree_date.get()

            cursor.execute("INSERT INTO depenses (categorie, montant, date) VALUES (?, ?, ?)",
                           (categorie, montant, date))
            conn.commit()

            messagebox.showinfo("Succès", "✅ Dépense ajoutée avec succès !")
            fenetre.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "⚠️ Le montant doit être un nombre valide")

    tk.Button(fenetre, text="Enregistrer", command=sauvegarder).grid(row=3, column=0, columnspan=2, pady=10)

def voir_depenses():
    fenetre = tk.Toplevel(root)
    fenetre.title("Liste des dépenses")

    colonnes = ("ID", "Catégorie", "Montant", "Date")
    table = ttk.Treeview(fenetre, columns=colonnes, show="headings")

    for col in colonnes:
        table.heading(col, text=col)
        table.column(col, width=120)

    cursor.execute("SELECT * FROM depenses")
    depenses = cursor.fetchall()

    for depense in depenses:
        table.insert("", tk.END, values=depense)

    table.pack(fill="both", expand=True)

    def supprimer_depense():
        selection = table.selection()
        if not selection:
            messagebox.showwarning("Attention", "⚠️ Sélectionne une dépense à supprimer")
            return

        item = table.item(selection[0])
        depense_id = item["values"][0]  # L'ID est en première colonne

        # Supprimer de la base
        cursor.execute("DELETE FROM depenses WHERE id = ?", (depense_id,))
        conn.commit()

        # Supprimer du tableau
        table.delete(selection[0])

        messagebox.showinfo("Succès", f"✅ Dépense {depense_id} supprimée avec succès !")

    btn_supprimer = tk.Button(fenetre, text="🗑️ Supprimer la dépense sélectionnée", command=supprimer_depense)
    btn_supprimer.pack(pady=10)
# Fenêtre principale
root = tk.Tk()
root.title("Suivi des dépenses")

tk.Button(root, text="➕ Ajouter une dépense", command=ajouter_depense, width=25).pack(pady=10)
tk.Button(root, text="📊 Voir les dépenses", command=voir_depenses, width=25).pack(pady=10)

root.mainloop()

conn.close()