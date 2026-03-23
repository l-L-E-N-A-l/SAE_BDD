from faker import *
from unidecode import *
from random import randint
import pandas as pa

fake = Faker(locale="fr_CA")

liste_prenom = ([unidecode(fake.unique.first_name_male()).upper() for _ in range(70)],[unidecode(fake.unique.first_name_female()).upper() for _ in range(70)]) # 0 = homme , 1 = femme
liste_nom = [unidecode(fake.unique.last_name()).upper() for _ in range(250)]

liste_grade = (["AFFILIE", "SYMPATISANT", "ADHERANT", "CHEVALIER", "GRAND CHEVALIER", "COMMANDEUR" , "GRAND CROIX"],["AFFILIEE", "SYMPATISANTE", "ADHERANTE", "DAME", "HAUTE DAME", "COMMANDERESSE" , "GRANDE-CROIX"])
liste_rang = ["'NOVICE'","'COMPAGNON'"]
liste_titre = ["'PHILANTROPHE'","'PROTECTEUR'","'HONORABLE'"]
liste_dignite = ["'MAITRE'","'GRAND CHANCELIER'","'GRAND MAITRE'"]

# Codes_postaux
codes_villes = pa.read_csv("./codes_villes.csv", encoding="latin-1")
codes_villes = codes_villes.drop_duplicates(subset=["Code_postal", "Nom_de_la_commune"])
codes_villes = codes_villes.reset_index(drop=True)
codes = codes_villes["Code_postal"]
villes = codes_villes["Nom_de_la_commune"]

def email_generator(nom,prenom):
    email = ""
    n1 , n2 , n3 = randint(0,2) , randint(0,2) , randint(0,2)
    if n1 == 0:
        email += prenom.lower()
    if n1 == 1:
        email += prenom[:1].lower()
    if n1 == 2:
        email += prenom.lower()+"."
    if n2 == 0:
        email += nom
    if n2 == 1:
        email += nom.lower()
    if n2 == 2:
        email += nom.lower()+str(randint(0,9999))
    if n3 == 0:
        email += "@gmail.com"
    if n3 == 1:
        email += "@outlook.com"
    if n3 == 2:
        email += "@yahoo.com"
    return email

def random_rang_titre_dignite():
    res = []
    r , t , d = randint(0,5) , randint(0,9) , randint(0,9)
    
    if r == 5: res.append(liste_rang[1])
    elif r >= 3: res.append(liste_rang[0])
    else : res.append("null")

    if t == 9: res.append(liste_titre[2])
    elif t >= 7: res.append(liste_titre[1])
    elif t >= 4: res.append(liste_titre[0])
    else : res.append("null")

    if d == 9: res.append(liste_dignite[2])
    elif d >= 7: res.append(liste_dignite[1])
    elif d >= 4: res.append(liste_dignite[0])
    else : res.append("null")

    return res





open("./script.sql", 'w').close()
file = open("./script.sql",'a')


# ADRESSE POSTALE
for i in range(len(codes)):
    file.write(f"INSERT INTO AdressePostale(codePostal,ville) VALUES('{codes[i]}','{villes[i]}'); \n")


# TENRAC
for _ in range(100_000):
    id_ville = randint(0,len(villes)-1)
    rtd = random_rang_titre_dignite()
    data_tenrac = {"id":fake.unique.random_int(min=0,max=1_000_000_000), "nom":liste_nom[randint(0,len(liste_nom)-1)], "prenom":liste_prenom[0][randint(0,len(liste_prenom[0])-1)], "tel":"06"+str(fake.unique.random_int(0,99_999_999)), "adresse":unidecode(fake.street_address()), "sexe":'M', "rang":rtd[0], "titre":rtd[1], "codePostal":codes[id_ville], "ville":villes[id_ville], "dignite":rtd[2], "grade":liste_grade[0][randint(0,len(liste_grade[0])-1)]}
    i = randint(0,1)
    if i==1 : 
        data_tenrac["sexe"] = 'F'
        data_tenrac["prenom"] = liste_prenom[1][randint(0,len(liste_prenom[0])-1)]
        data_tenrac["grade"] = liste_grade[1][randint(0,len(liste_grade)-1)]

    file.write(f"INSERT INTO Tenrac(idTenrac,nomT,prenomT,courriel,tel,adresseT,sexe,typeRang,typeTitre,typeDignite,typeGrade) VALUES({data_tenrac["id"]},'{data_tenrac["nom"]}','{data_tenrac["prenom"]}','{email_generator(data_tenrac["nom"],data_tenrac["prenom"])}','{data_tenrac["tel"]}','{data_tenrac["adresse"]}','{data_tenrac["sexe"]}',{data_tenrac["rang"]},{data_tenrac["titre"]},{data_tenrac["dignite"]},'{data_tenrac["grade"]}'); \n")

# GRADE
for i in range(len(liste_grade[0])-1) :

    if i == len(liste_grade[0]-1) :

        file.write(f"INSERT INTO Tenrac(typeGrade) VALUES ({liste_grade[0][i]})")
    else :
        file.write(f"INSERT INTO Tenrac(typeGrade, superieurGrade) VALUES ({liste_grade[0][i]},{liste_grade[0][i+1]})")
    file.write(f"INSERT INTO Tenrac(idTenrac,nomT,prenomT,courriel,tel,adresseT,sexe,typeRang,typeTitre,codePostal,ville,typeDignite,typeGrade) VALUES({data_tenrac["id"]},'{data_tenrac["nom"]}','{data_tenrac["prenom"]}','{email_generator(data_tenrac["nom"],data_tenrac["prenom"])}','{data_tenrac["tel"]}','{data_tenrac["adresse"]}','{data_tenrac["sexe"]}',{data_tenrac["rang"]},{data_tenrac["titre"]},'{data_tenrac["codePostal"]}','{data_tenrac["ville"]}',{data_tenrac["dignite"]},'{data_tenrac["grade"]}'); \n")

print("- - - FINI - - -")