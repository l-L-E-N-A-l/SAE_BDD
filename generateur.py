from faker import *
from unidecode import *
from random import randint

fake = Faker(locale="fr_CA")

liste_prenom_m = [unidecode(fake.unique.first_name_male()).upper() for _ in range(70)]
liste_prenom_f = [unidecode(fake.unique.first_name_female()).upper() for _ in range(70)]
liste_nom = [unidecode(fake.unique.last_name()).upper() for _ in range(250)]

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
        nom_prenom_sexe = (liste_nom[randint(0,len(liste_nom)-1)],liste_prenom_m[randint(0,len(liste_prenom_m)-1)],'M')
    else : nom_prenom_sexe = (liste_nom[randint(0,len(liste_nom)-1)],liste_prenom_f[randint(0,len(liste_prenom_f)-1)],'F')
    file.write(f"INSERT INTO Tenrac(idTenrac,nom,prenom,email,telephone,adresse,sexe) VALUES({fake.unique.random_int(min=0,max=1_000_000_000)},'{nom_prenom_sexe[0]}','{nom_prenom_sexe[1]}','{email_generator(nom_prenom_sexe[0],nom_prenom_sexe[1])}','06{fake.unique.random_int(0,99_999_999)}','{unidecode(fake.street_address())}','{nom_prenom_sexe[2]}'); \n")
    