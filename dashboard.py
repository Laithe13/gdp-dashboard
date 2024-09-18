import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Configuration du titre de l'application
st.title("Tableau de bord interactif")


# Entrées utilisateur interactives
# st.sidebar.header("Paramètres d'entrée")

# Données d'entrée utilisateur

st.sidebar.header("Paramètres d'investissement")
nombre_investisseurs = st.sidebar.number_input('Nombre d’investisseurs', value=10)
investissement_moyen_par_personne = st.sidebar.number_input('Investissement moyen par personne', value=6100)
duree_blocage_investissement = st.sidebar.number_input('Durée minimale du blocage de l’investissement de chaque investisseur (mois)', value=6)

st.sidebar.header("Paramètres associés au tractopelle")
prix_unitaire_pelle = st.sidebar.number_input('Prix unitaire du tractopelle + marteau piqueur', value=50000)
nombre_pelle = st.sidebar.number_input('Nombre de tractopelle acheté', value = 1)
prix_douane_pelle = st.sidebar.number_input('Prix douane du tractopelle + marteau piqueur', value=5000)
prix_envoi_pelle = st.sidebar.number_input('Prix d’envoi du tractopelle + marteau piqueur', value=5000)
essence_mois_pelle = st.sidebar.number_input('Essence par mois du tractopelle', value=700)
entretien_annuel_machine = st.sidebar.number_input('Entretien annuel par tractopelle', value=5000)
rentabilite_jour_pelle = st.sidebar.number_input('Rentabilité journalière par pelle', value=1000)
jours_travail_pelle_semaine = st.sidebar.number_input('Nombre de jours de travail moyen par semaine du tractopelle', value=5)

st.sidebar.header("Paramètres associés au camion benne")
prix_unitaire_camion = st.sidebar.number_input('Prix unitaire du camion benne', value=30000)
nombre_camion = st.sidebar.number_input('Nombre de camion benne acheté', value=0)
prix_douane_camion = st.sidebar.number_input('Prix douane du camion benne', value=5000)
prix_envoi_camion = st.sidebar.number_input('Prix d’envoi du camion benne', value=5000)
essence_mois_camion = st.sidebar.number_input('Essence par mois du camion benne', value=400)
rentabilite_jour_camion = st.sidebar.number_input('Rentabilité journalière par camion benne', value=400)
jours_travail_camion_semaine = st.sidebar.number_input('Nombre de jours de travail moyen par semaine du camion benne', value=6)

st.sidebar.header("Paramètres associés aux salaires")
salaire_chauffeur = st.sidebar.number_input("Salaire mensuel d'un chauffeur", value=1000)
salaire_responsable = st.sidebar.number_input('Salaire mensuel du responsable', value=2000)



# Calculs basés sur les formules fournies
capital_depart = nombre_investisseurs * investissement_moyen_par_personne
fond_depart_necessaire = (nombre_pelle * (prix_unitaire_pelle + prix_douane_pelle + prix_envoi_pelle) +
                          nombre_camion * (prix_unitaire_camion + prix_douane_camion + prix_envoi_camion))
caisse_depart = capital_depart - fond_depart_necessaire

charge_fixe_mois = salaire_chauffeur*(nombre_pelle+nombre_camion) + salaire_responsable  # Valeur fixe de charge fixe par mois
charge_variable_mois = (essence_mois_pelle * nombre_pelle + essence_mois_camion * nombre_camion)
chiffre_affaire_mois = (rentabilite_jour_pelle * jours_travail_pelle_semaine * 4 * nombre_pelle +
                        rentabilite_jour_camion * jours_travail_camion_semaine * 4 * nombre_camion)
benefice_par_mois = chiffre_affaire_mois - (charge_fixe_mois + charge_variable_mois)

benefice_6_mois = benefice_par_mois * duree_blocage_investissement
benefice_6_mois_investisseur = benefice_6_mois / nombre_investisseurs
benefice_1_an = benefice_par_mois * 12
dividende = benefice_1_an / 2  # Dividende est 50% du bénéfice annuel
dividende_moyen_par_investisseur = dividende / nombre_investisseurs

duree_rentabilisation = round(capital_depart / benefice_par_mois,0)

# Création du DataFrame pour le tableau jaune
data_tableau_jaune = {
    'Paramètre': [
        'Capital de départ',
        'Fond de départ nécessaire pour acheter et rapatrier le matériel',
        'Caisse de départ',
        'Charge fixe par mois',
        'Charge variable par mois',
        "Chiffre d'affaire par mois",
        'Bénéfice par mois',
        'Bénéfice - investissement + caisse en 6 mois',
        'Bénéfice - investissement + caisse en 6 mois par investisseur',
        'Bénéfice - investissement + caisse en 1 an',
        "Dividende de l'année",
        "Dividende moyenne de l'année par investisseur"
    ],
    'Valeur (€)': [
        round(capital_depart, 2),
        round(fond_depart_necessaire, 2),
        round(caisse_depart, 2),
        round(charge_fixe_mois, 2),
        round(charge_variable_mois, 2),
        round(chiffre_affaire_mois, 2),
        round(benefice_par_mois, 2),
        round(benefice_6_mois, 2),
        round(benefice_6_mois_investisseur, 2),
        round(benefice_1_an, 2),
        round(dividende, 2),
        round(dividende_moyen_par_investisseur, 2)
    ]
}

# Affichage du tableau jaune avec les calculs dynamiques
df_tableau_jaune = pd.DataFrame(data_tableau_jaune)
df_tableau_jaune['Valeur (€)'] = df_tableau_jaune['Valeur (€)'].apply(lambda x: f"{x:.0f}")
st.subheader("Tableau de bord prévisionnel du projet tractopelle")
st.dataframe(df_tableau_jaune)

# Données pour le graphique
temps = ['Départ', 'Achats', 'Mois 1', 'Mois 2', 'Mois 3', 'Mois 4', 'Mois 5', 'Mois 6', 'Mois 7', 'Mois 8', 'Mois 9', 'Mois 10', 'Mois 11', 'Mois 12']
caisse = [round(capital_depart, 2), round(caisse_depart, 2)]  # Instants initiaux

# Calcul de l'évolution de la caisse
nouvelle_valeur = round(caisse_depart, 2)
for i in range(1, 13):  # Ajout des données pour chaque mois
    if round(caisse_depart, 2) >= 0:
        nouvelle_valeur = nouvelle_valeur + benefice_par_mois
        caisse.append(nouvelle_valeur)
    else:
        caisse.append(round(caisse_depart, 2))

# Calcul du ROI moyen par investisseur
roi_moyen_par_mois = round(benefice_par_mois/ nombre_investisseurs, 2) 

# Création du graphique en barres avec Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=temps, y=caisse, color='skyblue', ax=ax)

# Définir le titre et les labels
ax.set_title(f"Évolution de l'argent de la société\nROI par mois = $\mathbf{{{int(roi_moyen_par_mois)}}}$ € / Durée de rentabilité $\mathbf{{{int(duree_rentabilisation)}}}$ mois", fontsize=14)
ax.set_xlabel("Temps", fontsize=12)
ax.set_ylabel("Montant en caisse (€)", fontsize=12)

# Ajuster la taille et la rotation des étiquettes de l'axe des abscisses
ax.tick_params(axis='x', labelsize=8)  # Taille de police des labels de l'axe des abscisses
plt.xticks(rotation=45)

# Afficher le graphique dans Streamlit ou dans un notebook
st.pyplot(fig)  # Si vous êtes dans Streamlit

