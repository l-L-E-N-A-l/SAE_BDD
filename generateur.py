from faker import *
from unidecode import *
from random import randint

fake = Faker(locale="fr_CA")

liste_prenom = [unidecode(fake.unique.first_name()).upper() for _ in range(185)]
liste_nom = [unidecode(fake.unique.last_name()).upper() for _ in range(250)]

open("./script.sql", 'w').close()
file = open("./script.sql",'a')

#tables = open("./ldd.txt",'r')
#file.write(tables.read())

for _ in range(1_000_000):
    file.write(f"INSERT INTO Tenrac(idTenrac,nom,prenom) VALUES({fake.unique.random_int(min=0,max=1_000_000_000)},'{liste_nom[randint(0,len(liste_nom)-1)]}','{liste_prenom[randint(0,len(liste_prenom)-1)]}'); \n")
    