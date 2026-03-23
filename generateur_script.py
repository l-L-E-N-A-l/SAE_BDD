from faker import *
from unidecode import *
from random import randint
import pandas as pa

fake = Faker(locale="fr_CA")

liste_prenom = ([unidecode(fake.unique.first_name_male()).upper() for _ in range(70)],[unidecode(fake.unique.first_name_female()).upper() for _ in range(70)]) # 0 = homme , 1 = femme
liste_nom = [unidecode(fake.unique.last_name()).upper() for _ in range(250)]

liste_grade = (["AFFILIE", "SYMPATISANT", "ADHERANT", "CHEVALIER", "GRAND CHEVALIER", "COMMANDEUR" , "GRAND CROIX"],["AFFILIE", "SYMPATISANT", "ADHERANT", "DAME", "HAUTE DAME", "COMMANDEUR" , "GRAND-CROIX"])
liste_rang = ["'NOVICE'","'COMPAGNON'"]
liste_titre = ["'PHILANTROPHE'","'PROTECTEUR'","'HONORABLE'"]
liste_dignite = ["'MAITRE'","'GRAND CHANCELIER'","'GRAND MAITRE'"]

codes_villes = pa.read_csv("./codes_villes")
codes_villes = codes_villes[["Nom_de_la_commune","Code_postal"]]

def email_generator(nom, prenom):
    match randint(0, 2):
        case 0: prefixe = prenom.lower()
        case 1: prefixe = prenom[:1].lower()
        case 2: prefixe = prenom.lower() + "."

    match randint(0, 2):
        case 0: milieu = nom
        case 1: milieu = nom.lower()
        case 2: milieu = nom.lower() + str(randint(0, 9999))

    match randint(0, 2):
        case 0: domaine = "@gmail.com"
        case 1: domaine = "@outlook.com"
        case 2: domaine = "@yahoo.com"

    return prefixe + milieu + domaine


def random_rang_titre_dignite():
    r, t, d = randint(0, 5), randint(0, 9), randint(0, 9)

    rang = liste_rang[1] if r == 5 else liste_rang[0] if r >= 3 else "null"
    
    titre = (liste_titre[2] if t == 9 else
             liste_titre[1] if t >= 7 else
             liste_titre[0] if t >= 4 else "null")
    
    dignite = (liste_dignite[2] if d == 9 else
               liste_dignite[1] if d >= 7 else
               liste_dignite[0] if d >= 4 else "null")

    return [rang, titre, dignite]


open("./script.sql", 'w').close()
file = open("./script.sql",'a')



# TENRAC
for _ in range(100_000):
    rtd = random_rang_titre_dignite()
    data_tenrac = {"id":fake.unique.random_int(min=0,max=1_000_000_000), "nom":liste_nom[randint(0,len(liste_nom)-1)], "prenom":liste_prenom[0][randint(0,len(liste_prenom[0])-1)], "tel":"06"+str(fake.unique.random_int(0,99_999_999)), "adresse":unidecode(fake.street_address()), "sexe":'M', "rang":rtd[0], "titre":rtd[1], "dignite":rtd[2], "grade":liste_grade[0][randint(0,len(liste_grade[0])-1)]}
    i = randint(0,1)
    if i==1 : 
        data_tenrac["sexe"] = 'F'
        data_tenrac["prenom"] = liste_prenom[1][randint(0,len(liste_prenom[0])-1)]

    file.write(f"INSERT INTO Tenrac(idTenrac,nomT,prenomT,courriel,tel,adresseT,sexe,typeRang,typeTitre,typeDignite,typeGrade) VALUES({data_tenrac["id"]},'{data_tenrac["nom"]}','{data_tenrac["prenom"]}','{email_generator(data_tenrac["nom"],data_tenrac["prenom"])}','{data_tenrac["tel"]}','{data_tenrac["adresse"]}','{data_tenrac["sexe"]}',{data_tenrac["rang"]},{data_tenrac["titre"]},{data_tenrac["dignite"]},'{data_tenrac["grade"]}'); \n")
    
