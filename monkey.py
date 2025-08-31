import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

# Connexion à la base
conn = sqlite3.connect("depenses.db")
cursor = conn.cursor()

# Table dépenses
cursor.execute("""
CREATE TABLE IF NOT EXISTS depenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categorie TEXT,
    montant REAL,
    date TEXT
)
""")

# Table catégories
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE
)
""")
conn.commit()

# Catégories par défaut
categories_defaut = ["Nourriture", "Logement", "Transport", "Loisirs", "Autre"]
for cat in categories_defaut:
    cursor.execute("INSERT OR IGNORE INTO categories (nom) VALUES (?)", (cat,))
conn.commit()

def get_categories():
    cursor.execute("SELECT nom FROM categories")
    return [row[0] for row in cursor.fetchall()]

def ajouter_categorie():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter une catégorie")

    tk.Label(fenetre, text="Nom de la catégorie :").grid(row=0, column=0, padx=5, pady=5)
    entree_nom = tk.Entry(fenetre)
    entree_nom.grid(row=0, column=1, padx=5, pady=5)

    def sauvegarder_cat():
        nom = entree_nom.get().strip()
        if nom:
            try:
                cursor.execute("INSERT INTO categories (nom) VALUES (?)", (nom,))
                conn.commit()
                messagebox.showinfo("Succès", f"✅ Catégorie '{nom}' ajoutée")
                fenetre.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erreur", "⚠️ Cette catégorie existe déjà")
        else:
            messagebox.showerror("Erreur", "⚠️ Le nom ne peut pas être vide")

    tk.Button(fenetre, text="Ajouter", command=sauvegarder_cat).grid(row=1, column=0, columnspan=2, pady=10)

def ajouter_depense():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter une dépense")

    tk.Label(fenetre, text="Catégorie :").grid(row=0, column=0, padx=5, pady=5)
    categories = get_categories()
    categorie_var = tk.StringVar(value=categories[0])
    menu_categorie = ttk.Combobox(fenetre, textvariable=categorie_var, values=categories, state="readonly")
    menu_categorie.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(fenetre, text="Montant :").grid(row=1, column=0, padx=5, pady=5)
    entree_montant = tk.Entry(fenetre)
    entree_montant.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(fenetre, text="Date (AAAA-MM-JJ) :").grid(row=2, column=0, padx=5, pady=5)
    entree_date = tk.Entry(fenetre)
    entree_date.grid(row=2, column=1, padx=5, pady=5)

    def sauvegarder():
        try:
            categorie = categorie_var.get()
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

def afficher_statistiques():
    cursor.execute("SELECT categorie, SUM(montant) FROM depenses GROUP BY categorie")
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("Statistiques", "⚠️ Aucune dépense enregistrée")
        return

    categories = [row[0] for row in data]
    montants = [row[1] for row in data]

    plt.pie(montants, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Répartition des dépenses par catégorie")
    plt.show()

# Fenêtre principale
root = tk.Tk()
root.title("Suivi des dépenses")

tk.Button(root, text="➕ Ajouter une dépense", command=ajouter_depense, width=30).pack(pady=5)
tk.Button(root, text="📊 Voir les dépenses", command=voir_depenses, width=30).pack(pady=5)
tk.Button(root, text="➕ Ajouter une catégorie", command=ajouter_categorie, width=30).pack(pady=5)
tk.Button(root, text="📈 Statistiques", command=afficher_statistiques, width=30).pack(pady=5)

root.mainloop()
conn.close()
