from faker import *
from unidecode import *
from random import randint

fake = Faker(locale="fr_CA")

liste_prenom = ([unidecode(fake.unique.first_name_male()).upper() for _ in range(70)],[unidecode(fake.unique.first_name_female()).upper() for _ in range(70)]) # 0 = homme , 1 = femme
liste_nom = [unidecode(fake.unique.last_name()).upper() for _ in range(250)]
liste_dignite = ["MAITRE","GRAND CHANCELIER","GRAND MAITRE"]
liste_grade = (["AFFILIE", "SYMPATISANT", "ADHERANT", "CHEVALIER", "GRAND CHEVALIER", "COMMANDEUR" , "GRAND CROIX"],["AFFILIE", "SYMPATISANT", "ADHERANT", "DAME", "HAUTE DAME", "COMMANDEUR" , "GRAND CROIX"])

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

open("./script.sql", 'w').close()
file = open("./script.sql",'a')


for _ in range(100_000):
    i = randint(0,1)
    if i == 0 :
        data_tenrac = (liste_nom[randint(0,len(liste_nom)-1)],liste_prenom[0][randint(0,len(liste_prenom[0])-1)],'M',liste_grade[0][randint(0,len(liste_grade[0])-1)])
    else : data_tenrac = (liste_nom[randint(0,len(liste_nom)-1)],liste_prenom[1][randint(0,len(liste_prenom[1])-1)],'F',liste_grade[1][randint(0,len(liste_grade[1])-1)])

    file.write(f"INSERT INTO Tenrac(idTenrac,nomT,prenomT,courriel,tel,adresseT,sexe,typeGrade) VALUES({fake.unique.random_int(min=0,max=1_000_000_000)},'{data_tenrac[0]}','{data_tenrac[1]}','{email_generator(data_tenrac[0],data_tenrac[1])}','06{fake.unique.random_int(0,99_999_999)}','{unidecode(fake.street_address())}','{data_tenrac[2]}','{data_tenrac[3]}'); \n")
    