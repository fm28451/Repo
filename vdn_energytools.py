"""
Projet pour visualiser les données provenant des serveurs web OZW772 de chez Siemens.

Ce programme permet d'afficher les données sous forme de tableau et de graphique. L'ensemble est sauvé sur github dans le répertoire
https://github.com/FreddyM220569/Streamlit.git
Le nom d'utilisateur pour accéder à ce répertoire est Freddy_Ville


"""

import streamlit as st
import os
import pandas as pd
import plotly.express as px
#import Utils as uts



#from billManager import BillManager 

#import datetime

from csvFile import trendElect,trendChauf

#data=uts.data()

#@st.cache()
def charge_donneescsv(type_fichier):#Fonction qui permet de sélectionner un fichier d'extension csv ou xlsx
        data=st.file_uploader('Choisir le fichier de trends à analyser',type=type_fichier)
        if data is not None:
            nom_fich=data.name
            ext=nom_fich.split(".")[1]
            if ext=="csv":#crée une fonction qui renvoie les données lues
                df=pd.read_csv(data, sep="\\t", header=None, engine='python')
                return df
            elif ext=="xlsx":
                df=pd.read_excel(data)
                return df
        else:
            st.write("Charger un fichier!")

def main():

    def chgt_data(frame):
    # Itérer sur toutes les colonnes du DataFrame
        for col  in frame.columns:
        # Obtenir la première valeur de la colonne
            premiere_valeur = frame[col].iloc[0]
        # --- Condition principale : Vérifier si la première valeur est un nombre ---
        # Si c'est un nombre (int ou float), nous passons à la colonne suivante.
            if premiere_valeur in ("Marche","Arrêt"):
        # Si ce n'est PAS un nombre, nous procédons aux remplacements
        # Remplacer 'Marcher' par 120
                frame[col] = frame[col].replace('Marche', 120)
        # Remplacer 'Arrêt' par 90
                frame[col] = frame[col].replace('Arrêt', 90)
        # Convertir toute la colonne en type numérique après les remplacements
        # (important si vous souhaitez effectuer des calculs plus tard)
            #frame[i] = pd.to_numeric(frame[i], errors='coerce')
        return frame
    
    def affiche_donnees(data,origin):

        if data is not None:
            st.header("Information sur les données")
            if origin=="1":       
                st.write("Origine des données: ",data.nomInstallation, " ---- ", "Nom du trend: ", data.nomTrend)
                st.write("Interverval des mesures: ", data.interval_mesure)
                st.write("Date début des mesures: ", data.dateDebut, "----", "Date fin des mesures: ", data.dateFin )
                st.write("Données à afficher")
                st.write(data.new_dataFrame)
            elif origin=="2":
                st.write("Interverval des mesures: ", data.interval_mesure)
                st.write("Début des enregistrements: ", data.debutEnregistrement)
                #st.write("Les valeurs min sont: ", data.valMin)
                #st.write("Les valeurs max sont: ", data.valMax)
                #st.write("Les stats des données: ", data.stat)
    
    def graphique (nom_df,nomDate):
        st.header("Graphique")
        selected_columns=nom_df.columns[2:]
        fig=px.line(nom_df,x=nomDate, y=nom_df.columns[1])
        for element in selected_columns:
            fig.add_scatter(x=nom_df[nomDate],y=nom_df[element],mode='lines', name=element)
        st.plotly_chart(fig)
    
    #Lit un fichier excel.xlsx et affiche soit le tableau de données
    #soit le graphique des données.

    activites=["Choisissez","Analyse Trends chauffage","Analyse Trends électricité","HT","BT","Gaz HP","Gaz BP","Encodage des factures"]
    st.title("Ville de Namur - Energie")
    st.info("Ceci est une application qui permet d'afficher sous forme graphique ou de tableau les données récupérées de fichiers excel.\n"
            "Ces données proviennent d'enregistrement réalisées via les serveurs Web Chauffage ou des tableaux de consommation."
            " L'Energy Toolbox permet d'afficher les différents menus disponibles.")

    st.sidebar.write("""# Energy Toolbox""")
    st.sidebar.write("""## Choix de l'outil: """)
    st.sidebar.write("Choisissez un outil dans la listbox ci-dessous")
    choice=st.sidebar.selectbox("Sélectionnez la tâche à réaliser",activites)

    if choice=="Analyse Trends chauffage":
        
        st.title("Données de serveur web chauffage")
       
        #Lit un fichier excel.xlsx et affiche soit le tableau de données
        #soit le graphique des données.
        st.sidebar.info("Charge un fichier *.csv* et affiche les données sous forme de tableau et sous forme graphique")
        if st.sidebar.checkbox('Sélectionner le fichier au format *.csv*'):
            #Convertir un fichier *.csv en *.xls
            df=charge_donneescsv("csv")#Appelle une fonction qui renvoie les données lues
            if df is not None:
                data=trendChauf(df) #Objet data reprenant différents paramètre comme nom du site analysé, date début du trend, ...
                frame=data.new_dataFrame
                affiche_donnees(data,"1")
                frame=chgt_data(frame)
                graphique(frame,"Date")
        elif st.sidebar.checkbox("Sélectionner le fichier au format *.xlsx"):
            #Appelle la fonction qui modifie le fichier *.csv brut en fichier *.xlsx
            df=charge_donneescsv("xlsx")
            if df is not None:
            #crée une fonction qui renvoie les données lues
                dataf=pd.DataFrame(df)
                data=trendChauf(dataf,1)
                frame=data.new_dataFrame
                st.write(frame)
                affiche_donnees(data,"1")
                graphique(frame,"Date")       
           
    elif choice=="Analyse Trends électricité":
        if st.sidebar.checkbox('Sélectionner le fichier au format *.csv*'):
            #Convertir un fichier *.csv en *.xls
            tension=st.sidebar.checkbox('Tension (V)')
            courant=st.sidebar.checkbox('Courant (A)')
            puissance_active=st.sidebar.checkbox('Puissance active (W)')
            puissance_reactive=st.sidebar.checkbox('Puissance réactive (Var)')
            puissance_apparente=st.sidebar.checkbox('Puissance apparente (VA)')
            if tension:
                df=charge_donneescsv("csv")
                if df is not None:
                    data=trendElect(df)
                    frame=data.iFrame(df,3,6)
                    st.write(frame)
                    st.write(frame.describe())
                    affiche_donnees(data,"2")
                    graphique(frame,"DATE")
            elif courant:
                df=charge_donneescsv("csv")
                if df is not None:
                    data=trendElect(df)
                    frame=data.iFrame(df,6,10)
                    st.write(frame)
                    affiche_donnees(data,"2")
                    graphique(frame,"DATE")
            elif puissance_active:
                df=charge_donneescsv("csv")
                if df is not None:
                    data=trendElect(df) #Donne la numéro de ligne et numéro de colonne qui reprend la valeur de l'interval de mesure
                    frame=data.iFrame(df,11,15) #Donne l'index de la colonne de début et colonne de fin des valeurs souhaitées
                    st.write(frame)
                    affiche_donnees(data,"2") #Définit ce qui sera affiché
                    graphique(frame,"DATE")
            elif puissance_reactive:
                df=charge_donneescsv("csv")
                if df is not None:
                    data=trendElect(df) #Donne la numéro de ligne et numéro de colonne qui reprend la valeur de l'interval de mesure
                    frame=data.iFrame(df,15,19) #Donne l'index de la colonne de début et colonne de fin des valeurs souhaitées
                    st.write(frame)
                    affiche_donnees(data,"2") #Définit ce qui sera affiché
                    graphique(frame,"DATE")
            elif puissance_apparente:
                df=charge_donneescsv("csv")
                if df is not None:
                    data=trendElect(df) #Donne la numéro de ligne et numéro de colonne qui reprend la valeur de l'interval de mesure
                    frame=data.iFrame(df,19,23) #Donne l'index de la colonne de début et colonne de fin des valeurs souhaitées
                    st.write(frame)
                    affiche_donnees(data,"2") #Définit ce qui sera affiché
                    graphique(frame,"DATE")
    elif choice=="Encodage des factures":
        st.title("Encodage des factures")
        st.info("Cet outil va vous permettre d'encoder les différentes factures adressées par les différents fournisseurs d'énergie.\n"
            "Elles seront encodées dans différents tableaux Excel. Le tableau principal 0_MainBoard reprendra les données utiles de toutes les factures comme \n"
            "le numéro de facture, date de facture, type de facture, le montant de celle-ci et les données de consommation si elles existent \n."
            "Selon le vecteur énergétique gaz ou électricité, les factures correspodantes seront enregistrées dans 0_GAZ et 0_ELECT. Dans ces tableaux, \n"
            "il sera enregistré, entre autre, les coûts unitaires, la répartition du montant de la facture entre les fournisseurs, le GRD et le gouvernement. \n"
            "Enfin les données de consommation seront enregistrées dans leur fichier respectif et seront reprises via le code EAN du point de consommation. \n"
            "Ces fichiers sont 0_ConsoHT pour les consommation Haute Tension, 0_ConsGHP pour les consommations gaz mensuelles, 0_ConsoGBP pour les consommation gaz annuelles et \n"
            "0_ConsoBT pour les consommations Basse Tension. Ces données serviront à avoir une vision de la consommation d'énergie par point de consommation.")
        #BillManager.mainManager()
        #listeFichiers=LectureDossier(data["Main"]["path"])
        #fact=BillManager(listeFichiers)
        #fact.mainManager()
        #st.write(BillManager.nbreFactures, "ont été traitées en ", BillManager.temps, " secondes")
    elif choice=="HT":
        st.title("En développement")
    elif choice=="BT":
        st.title("En développement")
    elif choice=="Gaz HP":
        st.title("En développement")
    elif choice=="Gaz BP":
        st.title("En développement")
    



if __name__ == "__main__":

    main()
