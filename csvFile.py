import pandas as pd
import streamlit as st
import re

"""class CsvFile:
    def __init__(self,file):#,numRow,numCol):
        #self.__extract__interval_mesure(file)#,numRow,numCol)

def __extract__interval_mesure(self,data)#,numRow,numCol):
            self.interval_mesure=data.iloc[numRow,numCol]

    def concat_jour_heure(self,df,nomDate,nomHeure):
        df.loc[:,nomDate]=df[nomDate].astype(str)+' '+df[nomHeure].astype(str)
        del df[nomHeure]
        return df"""


class trendChauf():
    def __init__(self,*args):#,numRow,numCol):
        #super().__init__(file)#,numRow,numCol
        file=args
        self.__extract__nomInstallation(file)
        self.__extract__dateFichier(file)
        self.__extract__nomTrend(file)
        self.__extract__dateDebut(file)
        self.__extract__dateFin(file)
        self.__extract__interval_mesure(file)
        self.__extract__new_dataFrame(file)

    def conversion(self,*args):
        data=args[0]
        if len(args)>2:
            valeur=data.iloc[args[1],args[2]]#Reçoit 2 arguments pcq fichier xlsx
           
        else:
            valeur=data.iloc[args[1],0]
            valeur=valeur.split(";")
        return valeur
    
    def __extract__nomInstallation(self,data):
        if len(data)>1:#pour autre que csv
           valeur=self.conversion(data[0],2,0) 
        else:
            valeur=self.conversion(data[0],3)
            valeur=valeur[0]
        self.nomInstallation=valeur
    
    def __extract__dateFichier(self,data):
        if len(data)>1:
            valeur=self.conversion(data[0],2,6)
        else:
            liste=self.conversion(data[0],3)
            valeur=liste[6]
        self.datefichier=valeur
    
    def __extract__nomTrend(self,data):
        if len(data)>1:
            valeur=self.conversion(data[0], 4, 1)
        else:
            valeur=self.conversion(data[0], 5)
            valeur=valeur[1]
        self.nomTrend=valeur
    
    def __extract__dateDebut(self,data):
        if len(data)>1:
            hdebut=self.conversion(data[0], 6, 1)
            hDebut=hdebut.strftime("%H:%M:%S")
            dDebut=self.conversion(data[0], 6, 2)
        else:
            liste=self.conversion(data[0],7)
            hDebut=liste[1]
            dDebut=liste[2]
        dateDebutConcat=dDebut+' '+hDebut
        self.dateDebut=dateDebutConcat
    
    def __extract__dateFin(self,data):
        if len(data)>1:
            hfin=self.conversion(data[0], 7, 1)
            hFin=hfin.strftime("%H:%M:%S")
            dFin=self.conversion(data[0], 7, 2)
        else:
            liste=self.conversion(data[0],8)
            hFin=liste[1]
            dFin=liste[2]
        dateFinConcat=dFin+' '+hFin
        self.dateFin=dateFinConcat
    
    def __extract__interval_mesure(self,data):
        if len(data)>1:
            valeur=self.conversion(data[0],5,1)
        else:
            liste=self.conversion(data[0],6)
            valeur=liste[1]
        self.interval_mesure=valeur
    
    def concat_jour_heure(self,df,nomDate,nomHeure):
        df.loc[:,nomDate]=df[nomDate].astype(str)+' '+df[nomHeure].astype(str)
        del df[nomHeure]
        return df
    
    def extract_info(self, listeCol):#Permet de récupérer des intitulés pertinents pour les colonnes
        for elt in range(len(listeCol)):
                index=listeCol[elt].rfind(":")
                if index!=-1:
                    txt=listeCol[elt]
                    matches=re.findall(r">",txt)
                    if len(matches)>2:
                        matches = re.search(r"(\d+\.\d+\.\d+\s+[A-Za-z0-9\s]+).*?>(.*?)>", txt)
                        part1=matches.group(1)
                        part2=matches.group(2).strip()
                        nouv_elt=str(elt) + " :" + part1 + ">" + part2 + ">" + listeCol[elt][index+2:]
                    else:
                        matches=re.search(r"(\d+\.\d+\.\d+\s+[A-Za-z0-9\s]+)",txt) #\s*>\s*:\s*(.*)",txt)
                        part1=matches.group(1)
                        nouv_elt=str(elt) + " :" + part1 + ">" + listeCol[elt][index+2:]
                else:
                    nouv_elt=listeCol[elt]
                listeCol[elt]=nouv_elt
        return listeCol

    
    def __extract__new_dataFrame(self,file): #Permet de créer une nouvelle frame contenant les données et les titres des colonnes
        liste=[]
        data=file[0]
        if len(file)>1:
            liste_val=data.iloc[9,:]
            nomcolonne=[]
            for elt in liste_val:
                index=elt.rfind(":")
                if index!=-1:
                    nouv_elt=elt[index+2:]
                else:
                    nouv_elt=elt
                nomcolonne=nomcolonne+[nouv_elt]
            data.drop(data.index[1:11],inplace=True)
            data.drop(data.index[0], inplace=True)
            data.reset_index(drop=True, inplace=True)
            data.columns=nomcolonne
            df=data
        else:
            for i in range(len(data)-10):
                ligne=data.iloc[i+10,0] #Sélectionne les données
                liste.append(ligne)
            listeCol=liste[0].split(";")
            if listeCol[-1]=="": #Si la dernière ligne est un vide alors on la supprime pour ne garder que des éléments non vides
                listeCol.pop()
            new_name_col=self.extract_info(listeCol)
            name_column=new_name_col
            if name_column[1]=="Time of day":
                name_column[1]="Heure du jour"
            del liste[0]
            new_liste=[]
            for i in range (len(liste)):
                elt=liste[i].split(";")
                if elt[-1]=="":
                    elt.pop()
                new_liste=new_liste+[elt]
            df=pd.DataFrame(data=new_liste, columns=name_column)
        df=self.concat_jour_heure(df,"Date","Heure du jour")
        self.new_dataFrame=df

class trendElect ():
    def __init__(self,data):
        #super().__init__(data,numRow,numCol)
        self.__extract__frame(data)
        self._extract_interval_mesure(data)
        self._extract_debutEnregistrement(data)
        #self._extract_valMin(data)
        #self._extract_valMax(data)
        #self._extract_stat(data)
    
    def __extract__frame(self,data):
        #self.debut=data.iloc[12,2]
        self.frame=data[0].str.split(';', expand=True)
    
    def _extract_interval_mesure(self, data):
        self.interval_mesure=self.frame.iloc[12,2]
    
    def _extract_debutEnregistrement(self,data):
        self.debutEnregistrement=self.frame.iloc[13,2]

    def _extract_valMin(self,data):
        self.valMin=self.frame.min()

    def _extract_valMax(self,data):
        self.valMax=self.frame.max()

    def _extract_stat(self,data):
        self.stat=self.frame.describe()

    def concat_jour_heure(self,df,nomDate,nomHeure):
        df.loc[:,nomDate]=df[nomDate].astype(str)+' '+df[nomHeure].astype(str)
        del df[nomHeure]
        return df

    
    def iFrame(self,data,debutCol,finCol):
        nomCol=[]
        for i in range(len (self.frame.columns)):
            nomCol.append(self.frame.iloc[14,i])
        newdata=self.frame.iloc[15:]
        newdata.columns=nomCol
        timeFrame=newdata.iloc[:,0:2]
        timeFrame=self.concat_jour_heure(timeFrame,"DATE","TIME")
        dataFrame=newdata.iloc[:,debutCol:finCol]
        for i in range(len(dataFrame.columns)):
            dataFrame[dataFrame.columns[i]]=dataFrame[dataFrame.columns[i]].str.replace(",",".")
        dataFrame=dataFrame.astype(float)
        newdataFrame=pd.concat([timeFrame,dataFrame], axis=1)
        return newdataFrame

