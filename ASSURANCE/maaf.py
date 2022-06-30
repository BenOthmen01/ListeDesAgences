import pandas as pd
import requests
from bs4 import  BeautifulSoup, NavigableString

import  re
url="https://www.moneyvox.fr/pratique/agences/maaf/"
response=requests.get(url)

def get_links_CA():
    if response.ok :
        links=[]
        soup= BeautifulSoup(response.text,features="lxml")
        lis=soup.findAll('li')
        [print(str(li)+ '\n\n') for li in lis]

        for li in lis:
            a=li.find('a')
            link=a['href']
            if "https:" not in links:
                links.append("https://www.moneyvox.fr"+link)
    return links


def get_link_arr(final_arr=103):
    liste = get_links_CA()

    return liste[4:int(final_arr)]


lien_with_arr=get_link_arr()
liste=[]
for arr in lien_with_arr:
    # Il faut regarder la longueur de la liste sur paris puisque paris a les plus d'agence et de mettre sur le parametre de range
    # il faut améliorer cet axe
    for i in range(1,2):
        liste.append(arr+str(i)+"/")


listes=liste
adresse = []
Titre=[]
for row in listes:
    html_text=requests.get(str(row)).text
    soup=BeautifulSoup(html_text,"lxml")
    banques=soup.find_all('div',class_ = 'col-xs-7')
    for banque in banques:
        titles=banque.find_all('h4')
        adress=banque.find_all("p")
        for ad in adress:
            adresse.append(ad.text)
        for title in titles:
            Titre.append(title.text)


def fusionner_adresse(adresse):
    liste_ad=[]
    for ad in range(0,len(adresse),2):
        liste_ad.append(adresse[ad])
    return liste_ad

print(len(Titre))
print(len(fusionner_adresse(adresse)))


import pandas as pd
df=pd.DataFrame({"nom de l'entreprise": Titre, 'adresse':fusionner_adresse(adresse)})
df = df.loc[:,~df.columns.duplicated()].copy()
df.to_csv("maaf")
print(df)