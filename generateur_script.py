from faker import *
from unidecode import *
from random import randint , choice, sample
import pandas as pa
import string


NB_TENRAC = 100_000

fake = Faker(locale="fr_CA")

### STOCK DE VALEURS ###
# Labels
liste_grade = (["AFFILIE", "SYMPATISANT", "ADHERANT", "CHEVALIER", "GRAND CHEVALIER", "COMMANDEUR" , "GRAND CROIX"],["AFFILIEE", "SYMPATISANTE", "ADHERANTE", "DAME", "HAUTE DAME", "COMMANDERESSE" , "GRANDE-CROIX"])
liste_rang = ["NOVICE","COMPAGNON"]
liste_titre = ["PHILANTROPHE","PROTECTEUR","HONORABLE"]
liste_dignite = ["MAITRE","GRAND CHANCELIER","GRAND MAITRE"]

# Id_Tenrac
id_tenrac = [fake.unique.random_int(min=0,max=1_000_000_000) for _ in range(NB_TENRAC)]
tenrac_org = {}
id_tenrac_grade = []

# Id_Structures
id_structure = [fake.unique.random_int(min=0,max=1_000_000_000) for _ in range(1_000)]
data_structure = pa.read_csv("./csv_sources/structure_tenrac.csv")
nom_structure = data_structure["nom"].values

# Codes_postaux
data_villes = pa.read_csv("./csv_sources/codes_villes.csv", encoding = "UTF-8")
data_villes = data_villes.reset_index(drop=True)
codes = data_villes["code_postal"]
villes = data_villes["ville"]


# Ingredients
data_ing = pa.read_csv("./csv_sources/ingredients.csv", encoding = "UTF-8")
data_ing = data_ing.drop_duplicates(subset=["Ingredient"])
data_ing = data_ing.reset_index(drop=True)
ingredients = data_ing["Ingredient"]

#Sauces

data_sauces = pa.read_csv("./csv_sources/sauces.csv", encoding = "UTF-8")
data_sauces = data_sauces.drop_duplicates(subset=["Nom"])
data_sauces = data_sauces.reset_index(drop=True)
sauces = data_sauces["Nom"]

#Plats

data_plats = pa.read_csv("./csv_sources/plats.csv", encoding = "UTF-8")
data_plats = data_plats.drop_duplicates(subset=["Nom"])
plats = data_plats["Nom"]
ids_plat = []

# Croyances
data_croyances = pa.read_csv("./csv_sources/croyances.csv", encoding="UTF-8")
data_croyances = data_croyances.drop_duplicates(subset=["doctrine"])
data_croyances = data_croyances.reset_index(drop=True)
liste_croyance = data_croyances["doctrine"]

# Doctrines qui rejettent les légumes
doctrines_rejette = ["Herbophobie Sacree", "Ordre de la Courgette Interdite", "Secte du Poireau Maudit", "Mouvement Anti-Chlorophylle", "Dogme de la Tomate Heretique", "Schisme du Radis Noir", "Alliance des Legumophobes Devots"]

# Organismes
data_org = pa.read_csv("./csv_sources/entreprises_fictives.csv",sep=";")
data_org.columns = data_org.columns.str.replace(' ', '')
org_ref = data_org["Identifiant"]
org_siret = data_org["Siret"]
org_raison = data_org["Raison_sociale"]
for i in range(len(org_ref)):
    org_siret[i] = org_siret[i].replace(" ", "")
    org_raison[i] = unidecode(org_raison[i]).upper()

# Machine
data_typeMachine = pa.read_csv("./csv_sources/typeMachine.csv") 
nomTypeM = data_typeMachine["nomTypeM"].values

# TypeEntretien
data_entretien = pa.read_csv("./csv_sources/entretiens.csv")
liste_typeEntretien = data_entretien["typeEntretien"]
liste_periodicite = data_entretien["periodicite"]

### FONCTIONS ###

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

def random_grade(sexe):
    g = randint(0, 27)

    liste = liste_grade[1] if sexe == 'F' else liste_grade[0]

    grade = (liste[6] if g == 27 else
             liste[5] if g >= 25 else
             liste[4] if g >= 22 else
             liste[3] if g >= 17 else
             liste[2] if g >= 12 else
             liste[1] if g >= 6  else
             liste[0])

    return grade

# Fichier SQL
open("./script.sql", 'w').close()
file = open("./script.sql",'a')

intension = open("./intension.sql")
str_intension = intension.read()
file.write(str_intension)

# Ouverture CSVs (Écriture)
open("./csv_finaux/codes_postaux.csv", 'w').close()
csv_codes_postaux = open("./csv_finaux/codes_postaux.csv", 'a')
open("./csv_finaux/tenrac.csv", 'w').close()
csv_tenrac = open("./csv_finaux/tenrac.csv", 'a')
open("./csv_finaux/csv_composition_plats", 'w').close()
csv_compo_plat = open("./csv_finaux/csv_compositions_plats", 'a')
open("./csv_finaux/inclusion_legume.csv", 'w').close()
csv_inclusion_legume = open("./csv_finaux/inclusion_legume.csv", 'a')
open("./csv_finaux/assaisonnement.csv", 'w').close()
csv_assaisonnement = open("./csv_finaux/assaisonnement.csv", 'a')
open("./csv_finaux/allergenes.csv", 'w').close()
csv_allergene = open("./csv_finaux/allergenes.csv", 'a')
open("./csv_finaux/contient_allergene.csv", 'w').close()
csv_contient_allergene = open("./csv_finaux/contient_allergene.csv", 'a')
open("./csv_finaux/allergiques.csv", 'w').close()
csv_allergiques = open("./csv_finaux/allergiques.csv", 'a')
open("./csv_finaux/repas.csv", 'w').close()
csv_repas = open("./csv_finaux/repas.csv", 'a')
open("./csv_finaux/lieu_partenaire.csv", 'w').close()
csv_lieu_partenaire = open("./csv_finaux/lieu_partenaire.csv", 'a')
open("./csv_finaux/reunions.csv", 'w').close()
csv_reunions = open("./csv_finaux/reunions.csv", 'a')
open("./csv_finaux/cartes.csv", 'w').close()
csv_cartes = open("./csv_finaux/cartes.csv", 'a')

open("./csv_sources/nomMachines.csv", 'w').close()
csv_nomMachines = open("nomMachines.csv", 'a')


### INSERTIONS ###

# GRADE

# Hommes
for i in range(len(liste_grade[0])-1) :
    if i == len(liste_grade[0]) -1:
        file.write(f"INSERT INTO Grade(typeGrade,superieurGrade) VALUES('{liste_grade[0][i]}',null); \n")
    else :
        file.write(f"INSERT INTO Grade(typeGrade,superieurGrade) VALUES('{liste_grade[0][i]}','{liste_grade[0][i+1]}'); \n")
# Femmes
for i in range(len(liste_grade[1])-1) :
    if i == len(liste_grade[1]) -1:
        file.write(f"INSERT INTO Grade(typeGrade,superieurGrade) VALUES('{liste_grade[1][i]}',null); \n")
    else :
        file.write(f"INSERT INTO Grade(typeGrade,superieurGrade) VALUES('{liste_grade[1][i]}','{liste_grade[1][i+1]}'); \n")

# DIGNITE
file.write(f"INSERT INTO Dignite(typeDignite,superieurDignite) VALUES('{liste_dignite[0]}','{liste_dignite[1]}'); \n")
file.write(f"INSERT INTO Dignite(typeDignite,superieurDignite) VALUES('{liste_dignite[1]}','{liste_dignite[2]}'); \n")
file.write(f"INSERT INTO Dignite(typeDignite,superieurDignite) VALUES('{liste_dignite[2]}',null); \n")

# ORGANISME
for i in range(len(org_ref)):
    file.write(f"INSERT INTO Organisme(referenceOrg,siret,raisonSociale) VALUES({org_ref[i]},'{org_siret[i]}','{org_raison[i]}'); \n")

#REPAS 

types_repas = ["Banquet", "Buffet", "Reception", "Voyage culinaire", "Rencontre", "Festoyades", "Mangeaillance", "Bon Pitance", "Francherepue", "Festin"]
adj_repas = ["Noble", "Experimentale", "Divin", "Des tenracs", "De mets precieux", "De Sir Lord Nevot", "Des Fervents defensseurs de la raclette", "des fous de fromage", "des viandards", "du plus grand chef du monde", "des femmes, les meilleures"]
ids_repas = []

for i in range(len(types_repas)-1):
    
    for j in range(len(adj_repas)-1):

        intitule = types_repas[i] + adj_repas[j]
        id_repas = i + j 
        file.write(f"INSERT INTO Repas(idRepas,intitule) VALUES({id_repas},'{intitule.upper()}'); \n") 
        csv_repas.write(f"{id_repas},{intitule} \n")
        ids_repas.append(id_repas)

#SAUCES

id_current_sauce = 0

for i in range(len(sauces)-1) : 

    file.write(f"INSERT INTO Sauce(idSauce,nomSauce) VALUES({id_current_sauce},'{sauces[i].upper()}'); \n")
    id_current_sauce += 1


# INGREDIENTS

id_current_ing = 0
id_legumes = []

for i in range(len(ingredients)-1) :

    if data_ing.iloc[[i]]["Categorie"].item() == "Legume" :
        
        file.write(f"INSERT INTO Ingredient(idIngredient,nomIngr) VALUES({id_current_ing},'{ingredients[i].upper()}'); \n") 
        file.write(f"INSERT INTO Legume(idIngredient,nomLeg) VALUES({id_current_ing},'{ingredients[i].upper()}'); \n")
        id_current_ing += 1
        id_legumes.append(id_current_ing)
    else :
        file.write(f"INSERT INTO Ingredient(idIngredient,nomIngr) VALUES({id_current_ing},'{ingredients[i].upper()}'); \n") 
        id_current_ing += 1

# GROUPE
ids_groupe = {}
for _ in range(100):
    data_groupe = {"idGroupe": fake.unique.random_int(min=1_000_000_000,max=9_999_999_999), "nbMembre": randint(2, 1000) }
    file.write(f"INSERT INTO Groupe(idGroupe, nbMembre) VALUES({data_groupe['idGroupe']},{data_groupe['nbMembre']});\n")
    ids_groupe[data_groupe["idGroupe"]] = data_groupe["nbMembre"]
        
# APPARTIENT
temp_id_tenrac = 0
for id in ids_groupe.keys():
    for _ in range(ids_groupe[id]):
        file.write(f"INSERT INTO Appartient(idTenrac,idGroupe) VALUES({id_tenrac[temp_id_tenrac]},{id}); \n")
        temp_id_tenrac += 1


# TYPEMACHINE

for i in range(len(data_typeMachine)):
    file.write(f"INSERT INTO TypeMachine(nomTypeM) VALUES('{unidecode(nomTypeM[i])}');\n")

# ADRESSE POSTALE

csv_codes_postaux.write(f"Code Postal, Ville \n")
for i in range(len(codes)):
    file.write(f"INSERT INTO AdressePostale(codePostal,ville) VALUES('{codes[i]}','{unidecode(villes[i])}'); \n")
    csv_codes_postaux.write(f"{codes[i]},{villes[i]} \n")

# TYPEENTRETIEN

for i in range(len(data_entretien)):
    file.write(f"INSERT INTO TypeEntretien(typeEnt, periodicite) VALUES('{liste_typeEntretien[i]}','{liste_periodicite[i]}');\n")

# RANG

file.write(f"INSERT INTO Rang(typeRang,superieurRang) VALUES ('{liste_rang[0]}','{liste_rang[1]}'); \n")
file.write(f"INSERT INTO Rang(typeRang,superieurRang) VALUES ('{liste_rang[1]}',null); \n")


# TITRE

file.write(f"INSERT INTO Titre(typeTitre,superieurTitre) VALUES ('{liste_titre[0]}','{liste_titre[1]}'); \n")
file.write(f"INSERT INTO Titre(typeTitre,superieurTitre) VALUES ('{liste_titre[1]}','{liste_titre[2]}'); \n")
file.write(f"INSERT INTO Titre(typeTitre,superieurTitre) VALUES ('{liste_titre[2]}',null); \n")


# CROYANCE

for i in range(len(liste_croyance)-1):
    file.write(f"INSERT INTO Croyance(doctrine) VALUES('{liste_croyance[i].upper()}'); \n")

# ALLERGENE
types_react = ["Reaction cutanee a", "Gonflement a cause de", "Traumatisme gustatif du", "Mort causee par", "Vomissements causes par"]

csv_allergene.write(f"idAller,nomAller")
csv_contient_allergene.write(f"idIngredient,idAller")
ids_allergies =[]

for i in range(len(id_legumes)-1) :

    for j in range(len(types_react)-1) :

        file.write(f"INSERT INTO Allergene(idAller,nomAller) VALUES({i+j},'{types_react[j].upper()} {ingredients[id_legumes[i]].upper()}'); \n")
        file.write(f"INSERT INTO Contient(idIngredient,idAller) VALUES({id_legumes[i]},{i+j}); \n")
        csv_allergene.write(f"{i+j},'{types_react[j].upper()} {ingredients[id_legumes[i]].upper()}' \n")
        csv_contient_allergene.write(f"{id_legumes[i]},{i+j} \n")
        ids_allergies.append(i+j)

# TENRAC
csv_tenrac.write(f"idTenrac,nomT,prenomT,courriel,tel,adresseT,sexe,doctrine,typeRang,typeTitre,codePostal,ville,referenceOrg,typeDignite,typeGrade \n")
for i in range(NB_TENRAC):
    id_ville = randint(0,randint(1,len(villes)-1))
    rtd = random_rang_titre_dignite()
    sexe = 'F' if randint(0, 3) == 0 else 'M'
    data_tenrac = {"id":id_tenrac[i], "nom":unidecode(fake.last_name()).upper(), "prenom":unidecode(fake.first_name_female() if sexe == 'F' else fake.first_name_male()).upper(), "tel":"06"+str(fake.unique.random_int(0,99_999_999)), "adresse":unidecode(fake.street_address()), "sexe":sexe, "doctrine":liste_croyance[randint(0,len(liste_croyance)-2)].upper(), "rang":rtd[0], "titre":rtd[1], "codePostal":codes[id_ville], "ville":unidecode(villes[id_ville]),"referenceOrg" : choice(org_ref), "dignite":rtd[2], "grade":random_grade(sexe)}

    file.write(f"INSERT INTO Tenrac(idTenrac,nomT,prenomT,courriel,tel,adresseT,sexe,doctrine,typeRang,typeTitre,codePostal,ville,referenceOrg,typeDignite,typeGrade) VALUES({data_tenrac["id"]},'{data_tenrac["nom"]}','{data_tenrac["prenom"]}','{email_generator(data_tenrac["nom"],data_tenrac["prenom"])}','{data_tenrac["tel"]}','{data_tenrac["adresse"]}','{data_tenrac["sexe"]}','{data_tenrac["doctrine"]}','{data_tenrac["rang"]}','{data_tenrac["titre"]}','{data_tenrac["codePostal"]}','{data_tenrac["ville"]}','{data_tenrac['referenceOrg']}','{data_tenrac["dignite"]}','{data_tenrac["grade"]}'); \n".replace("'null'","null")) # .replace(...) -> on remplace les chaines "null" par des vrais null
    csv_tenrac.write(f"{data_tenrac["id"]},{data_tenrac["nom"]},{data_tenrac["prenom"]},{email_generator(data_tenrac["nom"],data_tenrac["prenom"])},{data_tenrac["tel"]},{data_tenrac["adresse"]},{data_tenrac["sexe"]},{data_tenrac["doctrine"]},{data_tenrac["rang"]},{data_tenrac["titre"]},{data_tenrac["codePostal"]},{data_tenrac["ville"]},{data_tenrac['referenceOrg']},{data_tenrac["dignite"]},{data_tenrac["grade"]} \n")
    tenrac_org[data_tenrac["id"]] = data_tenrac["referenceOrg"]
    if data_tenrac["grade"] in ("CHEVALIER", "GRAND CHEVALIER", "COMMANDEUR" , "GRAND CROIX", "DAME", "HAUTE DAME", "COMMANDERESSE" , "GRANDE-CROIX") : id_tenrac_grade.append(data_tenrac["id"])

# STRUCTURE
for i in range(1_000):
    file.write(f"INSERT INTO Structure(idStructure,chef) VALUES({id_structure[i]},{id_tenrac[i]}); \n")

# ORDRES / CLUBS
for i in range(999):
    if i <= 100: file.write(f"INSERT INTO Ordre(idOrdre,nomO) VALUES({id_structure[i]},'{unidecode(nom_structure[i]).upper()}'); \n")
    else: file.write(f"INSERT INTO Club(idClub,nomC,idOrdre) VALUES({id_structure[i]},'{unidecode(nom_structure[i]).upper()}',{id_structure[i//10]}); \n")

# LIEU PARTENAIRE
lieux_partenaire = {}
csv_lieu_partenaire.write(f"adressePart,codePostal,ville \n")

for i in range(10000) :

    id_ville = randint(0,len(villes)-1)
    adresse = unidecode(fake.street_address())
    lieux_partenaire[i] = (codes[id_ville],villes[id_ville],adresse)
    file.write(f"INSERT INTO LieuPartenaire(adressePart,codePostal,ville) VALUES('{adresse.upper()}','{codes[id_ville]}','{villes[id_ville].upper()}'); \n")
    csv_lieu_partenaire.write(f"{adresse},{codes[id_ville]},{villes[id_ville]} \n")

# MODELE

referenceMod = [fake.unique.random_int(min=0,max=1_000_000_000) for _ in range(1000)]
    
for i in range(len(referenceMod)):
    file.write(f"INSERT INTO Modele(referenceMod) VALUES ({referenceMod[i]});\n")


#PLATS

id_current_plat = 0

for i in range(len(plats)-1) :
    id_legume = 0
    for j in range(len(id_legumes)-1) :
        if ingredients[id_legumes[j]] in plats[i] :
            id_legume = id_legumes[j]
    
    if id_legume != 0 :
        file.write(f"INSERT INTO Plat(idPlat,nomPlat,idIngredient) VALUES ({id_current_plat},'{unidecode(plats[i])}',{i}); \n")
        id_current_plat += 1
    else :
        file.write(f"INSERT INTO Plat(idPlat,nomPlat,idIngredient) VALUES ({id_current_plat},'{unidecode(plats[i])}',NULL); \n")
        id_current_plat += 1
    ids_plat.append(id_current_plat)

#REUNION

reunions = {}

csv_reunions.write(f"idRepas,codePostal,ville,AdressePart,idGroupe,dateReu,nomReu \n")

for i in range(20000) :

    repas = ids_repas[randint(0, len(ids_repas)-1)]
    lieu = lieux_partenaire[randint(0, len(lieux_partenaire)-1)]
    groupe = choice(list(ids_groupe.keys()))
    date = fake.date_time()
    nom = "Reunion du "+str(date)
    reunions[i] = (repas,lieu[0],lieu[1],lieu[2],groupe,date,nom)

    file.write(f"INSERT INTO Reunion(idRepas,codePostal,ville,AdressePart,idGroupe,dateReu,nomReu) VALUES({repas},'{lieu[0]}','{lieu[1].upper()}','{lieu[2].upper()}',{groupe},'{date}','{nom.upper()}'); \n")
    csv_reunions.write(f"{repas},{lieu[0]},{lieu[1]},{lieu[2]},{groupe},{date},{nom} \n")

# MACHINE

#Machine = (#(#nomTypeM, referenceMod), nomM VARCHAR2(50));
machines = []

nombreDeMachines = 5000
def random_ref():
    r = ""
    for _ in range(5) : r += choice(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])
    return r

set_refs = set()
csv_nomMachines.write("nomRef\n")

for _ in range(nombreDeMachines):
    ref = random_ref()    
    csv_nomMachines.write(f"MACHINE RACLETTE {ref}\n")
    machine = [unidecode(choice(nomTypeM)).upper(),choice(referenceMod),f"MACHINE RACLETTE {ref}"]
    machines.append(machine)
    file.write(f"INSERT INTO Machine(nomTypeM,referenceMod,nomM) VALUES('{machine[0]}',{machine[1]},'{machine[2]}');\n")

# REGISTRE
for i in range(100):
    file.write(f"INSERT INTO Registre(idClub,idOrdre,dateOuverture,dateFermeture) VALUES({choice(id_structure[100:])},{id_structure[i]},TO_DATE('202{randint(0,6)}-0{randint(1,9)}-0{randint(1,9)}','YYYY-MM-DD'),TO_DATE('202{randint(0,6)}-0{randint(1,9)}-0{randint(1,9)}','YYYY-MM-DD')); \n")


# CARTE
csv_cartes.write(f"idOrdre,idClub,idTenrac,referenceOrg,idCarte\n")
for id in id_tenrac:
    data_carte=[choice(id_structure[:100]),choice(id_structure[100:]),tenrac_org[id],fake.unique.random_int(min=1_000_000_000,max=9_999_999_999)]
    file.write(f"INSERT INTO Carte(idOrdre,idClub,idTenrac,referenceOrg,idCarte) VALUES({data_carte[0]},{data_carte[1]},{id},{data_carte[2]},{data_carte[3]}); \n")
    csv_cartes.write(f"{data_carte[0]},{data_carte[1]},{id},{data_carte[2]},{data_carte[3]} \n")

# ENTRETIEN
for id in id_tenrac :
    mac = choice(machines)
    file.write(f"INSERT INTO Entretien(typeEnt,idTenrac,dateEntre,idOrdre,idClub,nomTypeM,referenceMod,nomM) VALUES('{unidecode(choice(liste_typeEntretien[:]).upper())}',{id},'202{randint(0,8)}-0{randint(1,9)}-0{randint(1,9)}',{choice(id_structure[100:])},{choice(id_structure[:100])},'{mac[0]}',{mac[1]},'{mac[2]}'); \n")

# COMPOSE
def ingredient_compose(ingredient, plat_sauce) :

    return ingredient.lower() in plat_sauce.lower() 

csv_compo_plat.write(f"idPlat,idSauce,idIngredient \n")


for i in range(len(ingredients)-1) :
    insertion = ['NULL','NULL',i]
    if data_ing.iloc[[i]]["Categorie"].item() != "Legume" :
        for j in range(len(plats)-1) :
            if ingredient_compose(ingredients[i],plats[j]) :
                insertion[0] = j 
        for k in range(len(sauces)-1) :
            if ingredient_compose(ingredients[i], sauces[k]) :
                insertion[1] = k
        if insertion == ['NULL','NULL',i] :
            continue
        else :
            file.write(f"INSERT INTO Compose(idPlat,idSauce,idIngredient) VALUES({insertion[0]},{insertion[1]},{insertion[2]}); \n")
            csv_compo_plat.write(f"{insertion[0]},{insertion[1]},{insertion[2]} \n")

# PRESIDE

for i in reunions.keys():
    file.write(f"INSERT INTO Preside_EstPreside(idTenrac,idRepas,adressePart,idGroupe,idReu) VALUES({choice(id_tenrac_grade)},{reunions[i][0]},{reunions[i][3]},{reunions[i][4]},'{reunions[i][5]}'); \n")

#ASSAISONNEMENT
def assaisone(plat, sauce) :
    return sauce.lower() in plat.lower()

csv_assaisonnement.write(f"idPlat,idSauce")

for i in range(len(plats)-1) :
    for j in range(len(sauces)-1):
        if assaisone(plats[i], sauces[j]) :
            file.write(f"INSERT INTO Assaisone(idPlat,idSauce) VALUES({i},{j}); \n")
            csv_assaisonnement.write(f"{i},{j} \n")

# UTILISABLE

for reu in reunions.values():
    mac = choice(machines)
    file.write(f"INSERT INTO Utilisable(idRepas,AdressePart,idGroupe,dateReu,nomTypeM,referenceMod,nomM) VALUES({reu[0]},'{reu[3]}',{reu[4]},'{reu[5]}','{mac[0]}',{mac[1]},'{mac[2]}'); \n")


#ALLERGIE

csv_allergiques.write(f"idTenrac,idAller \n")

ids_tenrac_allergiques = sample(id_tenrac, round(NB_TENRAC*0.80))

for i in range(len(ids_tenrac_allergiques)-1) :

    allergie = choice(ids_allergies)
    tenrac = ids_tenrac_allergiques[i]
    file.write(f"INSERT INTO Allergie(idTenrac,idAller) VALUES({tenrac},{allergie}); \n")
    csv_allergiques.write(f"{tenrac},{allergie} \n")

# PARTENARIAT 

for i in range(10000):
    file.write(f"INSERT INTO Partenariat(idOrdre,codePostal,ville,adressePart) VALUES({choice(id_structure)},'{lieux_partenaire[i][0]}','{lieux_partenaire[i][1]}','{lieux_partenaire[i][2]}'); \n")

# HEURTE (Croyance <-> Legume)
for doctrine in doctrines_rejette:
    for id_leg in id_legumes:
        if randint(0,1):
            file.write(f"INSERT INTO Heurte(doctrine,idIngredient) VALUES('{doctrine}',{id_leg}); \n")

file.write("COMMIT;")

print("- - - FINI - - -")



