from faker import *
from unidecode import *
from random import randint
import pandas as pa

fake = Faker(locale="fr_CA")

# Prenoms / noms
liste_prenom = ([unidecode(fake.unique.first_name_male()).upper() for _ in range(70)],[unidecode(fake.unique.first_name_female()).upper() for _ in range(70)]) # 0 = homme , 1 = femme
liste_nom = [unidecode(fake.unique.last_name()).upper() for _ in range(250)]

# Labels
liste_grade = (["'AFFILIE'", "'SYMPATISANT'", "'ADHERANT'", "'CHEVALIER'", "'GRAND CHEVALIER'", "'COMMANDEUR'" , "'GRAND CROIX'"],["'AFFILIEE'", "'SYMPATISANTE'", "'ADHERANTE'", "'DAME'", "'HAUTE DAME'", "'COMMANDERESSE'" , "'GRANDE-CROIX'"])
liste_rang = ["'NOVICE'","'COMPAGNON'"] # - - - - - - - - - - - - - v
liste_titre = ["'PHILANTROPHE'","'PROTECTEUR'","'HONORABLE'"] # guillemet + apostrophe car possibilité de null (sans apostrophes)
liste_dignite = ["'MAITRE'","'GRAND CHANCELIER'","'GRAND MAITRE'"] # - - A 

# Codes_postaux
data_villes = pa.read_csv("./csv_sources/codes_villes.csv", encoding="latin-1")
data_villes = data_villes.drop_duplicates(subset=["Code_postal", "Nom_de_la_commune"])
data_villes = data_villes.reset_index(drop=True)
codes = data_villes["Code_postal"]
villes = data_villes["Nom_de_la_commune"]

# Ingredients
data_ing = pa.read_csv("./csv_sources/ingredients.csv", encoding = "UTF-8")
ingredients = data_ing["Ingredient"]
legumes = data_ing[data_ing["Categorie"]=="Légume"]["Ingredient"]

# Organismes
data_org = pa.read_csv("./csv_sources/entreprises_fictives.csv",sep=";")
data_org.columns = data_org.columns.str.replace(' ', '')
org_ref = data_org["Identifiant"]
org_siret = data_org["Siret"]
org_raison = data_org["Raison_sociale"]
for i in range(len(org_ref)):
    org_siret[i] = org_siret[i].replace(" ", "")
    org_raison[i] = unidecode(org_raison[i]).upper()

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




# Fichier SQL
open("./script.sql", 'w').close()
file = open("./script.sql",'a')

# Ouverture CSVs (Écriture)
open("./csv_finaux/codes_postaux.csv", 'w').close()
csv_codes_postaux = open("./csv_finaux/codes_postaux.csv", 'a')
open("./csv_finaux/tenrac.csv", 'w').close()
csv_tenrac = open("./csv_finaux/tenrac.csv", 'a')


# ADRESSE POSTALE
csv_codes_postaux.write(f"Code Postal, Ville \n")
for i in range(len(codes)):
    file.write(f"INSERT INTO AdressePostale(codePostal,ville) VALUES('{codes[i]}','{villes[i]}'); \n")
    csv_codes_postaux.write(f"{codes[i]},{villes[i]} \n")

# TENRAC
csv_tenrac.write(f"idTenrac,nomT,prenomT,courriel,tel,adresseT,sexe,typeRang,typeTitre,codePostal,ville,typeDignite,typeGrade \n")
for _ in range(100_000):
    id_ville = randint(0,len(villes)-1)
    rtd = random_rang_titre_dignite()
    data_tenrac = {"id":fake.unique.random_int(min=0,max=1_000_000_000), "nom":liste_nom[randint(0,len(liste_nom)-1)], "prenom":liste_prenom[0][randint(0,len(liste_prenom[0])-1)], "tel":"06"+str(fake.unique.random_int(0,99_999_999)), "adresse":unidecode(fake.street_address()), "sexe":'M', "rang":rtd[0], "titre":rtd[1], "codePostal":codes[id_ville], "ville":villes[id_ville], "dignite":rtd[2], "grade":liste_grade[0][randint(0,len(liste_grade[0])-1)]}
    i = randint(0,1)
    if i==1 : 
        data_tenrac["sexe"] = 'F'
        data_tenrac["prenom"] = liste_prenom[1][randint(0,len(liste_prenom[0])-1)]
        data_tenrac["grade"] = liste_grade[1][randint(0,len(liste_grade)-1)]

    file.write(f"INSERT INTO Tenrac(idTenrac,nomT,prenomT,courriel,tel,adresseT,sexe,typeRang,typeTitre,codePostal,ville,typeDignite,typeGrade) VALUES({data_tenrac["id"]},'{data_tenrac["nom"]}','{data_tenrac["prenom"]}','{email_generator(data_tenrac["nom"],data_tenrac["prenom"])}','{data_tenrac["tel"]}','{data_tenrac["adresse"]}','{data_tenrac["sexe"]}',{data_tenrac["rang"]},{data_tenrac["titre"]},'{data_tenrac["codePostal"]}','{data_tenrac["ville"]}',{data_tenrac["dignite"]},'{data_tenrac["grade"]}'); \n")
    csv_tenrac.write(f"{data_tenrac["id"]},{data_tenrac["nom"]},{data_tenrac["prenom"]},{email_generator(data_tenrac["nom"],data_tenrac["prenom"])},{data_tenrac["tel"]},{data_tenrac["adresse"]},{data_tenrac["sexe"]},{data_tenrac["rang"]},{data_tenrac["titre"]},{data_tenrac["codePostal"]},{data_tenrac["ville"]},{data_tenrac["dignite"]},{data_tenrac["grade"]} \n")

# GRADE
# Hommes
for i in range(len(liste_grade[0])-1) :
    if i == len(liste_grade[0]) -1:
        file.write(f"INSERT INTO Grade(typeGrade,superieurGrade) VALUES ({liste_grade[0][i]},null)")
    else :
        file.write(f"INSERT INTO Grade(typeGrade,superieurGrade) VALUES ({liste_grade[0][i]},{liste_grade[0][i+1]}); \n")
# Femmes
for i in range(len(liste_grade[1])-1) :
    if i == len(liste_grade[1]) -1:
        file.write(f"INSERT INTO Grade(typeGrade,superieurGrade) VALUES ({liste_grade[1][i]},null)")
    else :
        file.write(f"INSERT INTO Grade(typeGrade,superieurGrade) VALUES ({liste_grade[1][i]},{liste_grade[1][i+1]}); \n")


# RANG
file.write(f"INSERT INTO Rang(typeRang,superieurRang) VALUES ({liste_rang[0]},{liste_rang[1]}); \n")
file.write(f"INSERT INTO Rang(typeRang,superieurRang) VALUES ({liste_rang[1]},null); \n")


# TITRE
file.write(f"INSERT INTO Titre(typeTitre,superieurTitre) VALUES ({liste_titre[0]},{liste_titre[1]}); \n")
file.write(f"INSERT INTO Titre(typeTitre,superieurTitre) VALUES ({liste_titre[1]},{liste_titre[2]}); \n")
file.write(f"INSERT INTO Titre(typeTitre,superieurTitre) VALUES ({liste_titre[2]},null); \n")


# DIGNITE
file.write(f"INSERT INTO Dignite(typeDignite,superieurDignite) VALUES ({liste_dignite[0]},{liste_dignite[1]}); \n")
file.write(f"INSERT INTO Dignite(typeDignite,superieurDignite) VALUES ({liste_dignite[1]},{liste_dignite[2]}); \n")
file.write(f"INSERT INTO Dignite(typeDignite,superieurDignite) VALUES ({liste_dignite[2]},null); \n")

# ORGANISME
for i in range(len(org_ref)):
    file.write(f"INSERT INTO Organisme(referenceOrg,siret,raisonSociale) VALUES({org_ref[i]},'{org_siret[i]}','{org_raison[i]}'); \n")


print("- - - FINI - - -")