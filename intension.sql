DROP TABLE IF EXISTS Croyance CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Rang CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Titre CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS AdressePostale CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Ordre CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Club CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Organisme CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Dignite CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Grade CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Tenrac CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Repas CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Sauce CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Ingredient CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Groupe CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS TypeMachine CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS TypeEntretien CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Allergene CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Legume CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS LieuPartenaire CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Modele CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Registre CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Carte CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Plat CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Reunion CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Machine CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Entretien CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Menu CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Compose CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Preside_EstPreside CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Appartient CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Assaisone CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Utilisable CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Allergie CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Heurte CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Partenariat CASCADE CONSTRAINTS;
DROP TABLE IF EXISTS Contient CASCADE CONSTRAINTS;

CREATE TABLE Croyance(
doctrine VARCHAR2(60),
CONSTRAINT pk_Croyance PRIMARY KEY(doctrine)
);

CREATE TABLE Rang(
typeRang VARCHAR2(50),
superieurRang VARCHAR2(50),
CONSTRAINT pk_Rang PRIMARY KEY(typeRang),
CONSTRAINT ck_type_rang CHECK (typeRang IN ('NOVICE', 'COMPAGNON')),
CONSTRAINT fk_superieurRang FOREIGN KEY(superieurRang) REFERENCES Rang(typeRang)
);

CREATE TABLE Titre(
typeTitre VARCHAR2(50),
superieurTitre VARCHAR2(50),
CONSTRAINT pk_Titre PRIMARY KEY(typeTitre),
CONSTRAINT fk_superieurTitre FOREIGN KEY(superieurTitre) REFERENCES Titre(typeTitre)
);

CREATE TABLE AdressePostale(
codePostal CHAR(5),
ville VARCHAR2(50),
CONSTRAINT pk_Adresse_Postale PRIMARY KEY(codePostal, ville)
);

CREATE TABLE Ordre(
idOrdre NUMBER(10),
nomO VARCHAR2(50) NOT NULL,
PRIMARY KEY(idOrdre),
FOREIGN KEY(idOrdre) REFERENCES Structure(idStructure)
);



CREATE TABLE Club(
idClub NUMBER(10),
nomC VARCHAR2(50) NOT NULL,
idOrdrePere NUMBER(10) NOT NULL,
PRIMARY KEY(idClub),
FOREIGN KEY(idClub) REFERENCES Structure(idStructure),
FOREIGN KEY(idOrdrePere) REFERENCES Ordre(idOrdre)
);


CREATE TABLE Organisme(
referenceOrg NUMBER(10),
siret CHAR(14) NOT NULL,
raisonSociale VARCHAR2(50) NOT NULL,
CONSTRAINT pk_Organisme PRIMARY KEY(referenceOrg),
CONSTRAINT uk_siret UNIQUE(siret)
);

CREATE TABLE Dignite(
typeDignite VARCHAR2(50),
superieurDignite VARCHAR2(50),
CONSTRAINT pk_Dignite PRIMARY KEY(typeDignite),
CONSTRAINT ck_type_dignite CHECK (typeDignite IN ('MAITRE', 'GRAND CHANCELIER', 'GRAND MAITRE')),
CONSTRAINT fk_superieurDignite FOREIGN KEY(superieurDignite) REFERENCES Dignite(typeDignite)
);

CREATE TABLE Grade(
typeGrade VARCHAR2(50),
superieurGrade VARCHAR2(50),
CONSTRAINT pk_Grade PRIMARY KEY(typeGrade),
CONSTRAINT ck_type_grade CHECK (typeGrade IN ('AFFILIE','AFFILIEE', 'SYMPATHISANT', 'SYMPATHISANTE' ,'ADHERENT', 
'ADHERENTE', 'CHEVALIER' , 'DAME', 'GRAND CHEVALIER',
'HAUTE DAME', 'COMMANDEUR', 'COMMANDERESSE','GRAND-CROIX', 'GRANDE-CROIX')),
CONSTRAINT fk_superieurGrade FOREIGN KEY(superieurGrade) REFERENCES Grade(typeGrade)
);

CREATE TABLE Tenrac(
idTenrac NUMBER(10),
nomT VARCHAR2(50) NOT NULL,
prenomT VARCHAR2(50),
courriel VARCHAR2(50) NOT NULL,
tel CHAR(10) NOT NULL,
adresseT VARCHAR2(50) NOT NULL,
sexe VARCHAR2(1) NOT NULL,
doctrine VARCHAR2(60) NOT NULL,
typeRang VARCHAR2(50),
typeTitre VARCHAR2(50),
codePostal CHAR(5) NOT NULL,
ville VARCHAR2(50) NOT NULL,
idOrdre NUMBER(10) NOT NULL,
idClub NUMBER(10),
referenceOrg NUMBER(10) NOT NULL,
typeDignite VARCHAR2(50),
typeGrade VARCHAR2(50) NOT NULL,
CONSTRAINT pk_Tenrac PRIMARY KEY(idTenrac),
CONSTRAINT fk_doctrine FOREIGN KEY(doctrine) REFERENCES Croyance(doctrine),
CONSTRAINT fk_typeRang FOREIGN KEY(typeRang) REFERENCES Rang(typeRang),
CONSTRAINT fk_typeTitre FOREIGN KEY(typeTitre) REFERENCES Titre(typeTitre),
CONSTRAINT fk_tenrac_adressePostale FOREIGN KEY(codePostal, ville) REFERENCES AdressePostale(codePostal, ville),
CONSTRAINT fk_Tenrac_idOrdre FOREIGN KEY(idOrdre) REFERENCES Ordre(idOrdre),
CONSTRAINT fk_idClub FOREIGN KEY(idClub) REFERENCES Club(idClub),
CONSTRAINT fk_reference FOREIGN KEY(referenceOrg) REFERENCES Organisme(referenceOrg),
CONSTRAINT fk_typeDignite FOREIGN KEY(typeDignite) REFERENCES Dignite(typeDignite),
CONSTRAINT fk_typeGrade FOREIGN KEY(typeGrade) REFERENCES Grade(typeGrade),
CONSTRAINT ck_typegrade_sexe CHECK (
(sexe = 'M' AND typeGrade IN (
'AFFILIE', 'SYMPATHISANT', 'ADHERENT',
'CHEVALIER', 'GRAND CHEVALIER', 'COMMANDEUR', 'GRAND-CROIX'
))	
OR
(sexe = 'F' AND typeGrade IN (
'AFFILIEE', 'SYMPATHISANTE', 'ADHERENTE',
'DAME', 'HAUTE DAME', 'COMMANDERESSE', 'GRANDE-CROIX'
))
)
);

CREATE TABLE Structure(
   idStructure NUMBER(10),
   chef NUMBER(10) NOT NULL,
   PRIMARY KEY(idStructure),
   FOREIGN KEY(chef) REFERENCES Tenrac(idTenrac)
);

CREATE TABLE Repas(
idRepas NUMBER(10),
intitule VARCHAR2(50) NOT NULL,
CONSTRAINT pk_Repas PRIMARY KEY(idRepas)
);

CREATE TABLE Sauce(
idSauce NUMBER(10),
nomSauce VARCHAR2(50),
CONSTRAINT pk_Sauce PRIMARY KEY(idSauce)
);

CREATE TABLE Ingredient(
idIngredient NUMBER(10),
nomIngr VARCHAR2(50) NOT NULL,
CONSTRAINT pk_Ingredient PRIMARY KEY(idIngredient)
);

CREATE TABLE Groupe(
idGroupe NUMBER(10),
nbMembre NUMBER(10) NOT NULL,
CONSTRAINT pk_Groupe PRIMARY KEY(idGroupe),
CONSTRAINT ck_nbMembre CHECK (nbMembre >= 2)
);

CREATE TABLE TypeMachine(
nomTypeM VARCHAR2(50),
CONSTRAINT pk_TypeMachine PRIMARY KEY(nomTypeM)
);

CREATE TABLE TypeEntretien(
typeEnt VARCHAR2(50),
periodicite VARCHAR2(50) NOT NULL,
CONSTRAINT pk_TypeEntretien PRIMARY KEY(typeEnt)
);

CREATE TABLE Allergene(
idAller VARCHAR2(50),
nomAller VARCHAR2(50) NOT NULL,
CONSTRAINT pk_Allergen PRIMARY KEY(idAller)
);

CREATE TABLE Legume(
idIngredient NUMBER(10),
nomLeg VARCHAR2(50),
CONSTRAINT fk_idIngredient FOREIGN KEY(idIngredient) REFERENCES Ingredient(idIngredient),
CONSTRAINT pk_Legume PRIMARY KEY(idIngredient)
);

CREATE TABLE LieuPartenaire(
adressePart VARCHAR2(50),
codePostal CHAR(5) NOT NULL,
ville VARCHAR2(50) NOT NULL,
CONSTRAINT pk_LieuPartenaire PRIMARY KEY(adressePart,codePostal,ville),
CONSTRAINT fk_LieuPartenaire_adressePostale FOREIGN KEY(codePostal,ville) REFERENCES AdressePostale(codePostal, ville)
);

CREATE TABLE Modele(
nomTypeM VARCHAR2(50),
referenceMod NUMBER(10),
typeEnt VARCHAR2(50) NOT NULL,
CONSTRAINT pk_Modele PRIMARY KEY(nomTypeM, referenceMod),
CONSTRAINT fk_nomType FOREIGN KEY(nomTypeM) REFERENCES TypeMachine(nomTypeM),
CONSTRAINT fk_type FOREIGN KEY(typeEnt) REFERENCES TypeEntretien(typeEnt)
);

CREATE TABLE Registre(
idClub NUMBER(10),
idOrdre NUMBER(10),
dateOuverture DATE NOT NULL,
dateFermeture DATE,
CONSTRAINT pk_Registre PRIMARY KEY(idClub, idOrdre),
CONSTRAINT fk_Registre_idClub FOREIGN KEY(idClub) REFERENCES Club(idClub),
CONSTRAINT fk_Registre_idOrdre FOREIGN KEY(idOrdre) REFERENCES Ordre(idOrdre)
);

CREATE TABLE Carte(
idOrdre NUMBER(10),
idClub NUMBER(10),
idTenrac NUMBER(10),
referenceOrg NUMBER(10),
idCarte NUMBER(10),
CONSTRAINT pk_Carte PRIMARY KEY(idOrdre, idClub, idTenrac, referenceOrg, idCarte),
CONSTRAINT fk_Carte_Ordre FOREIGN KEY(idOrdre) REFERENCES Ordre(idOrdre),
CONSTRAINT fk_Carte_Club FOREIGN KEY(idClub) REFERENCES Club(idClub),
CONSTRAINT fk_Carte_Tenrac FOREIGN KEY(idTenrac) REFERENCES Tenrac(idTenrac),
CONSTRAINT fk_Carte_Organisme FOREIGN KEY(referenceOrg) REFERENCES Organisme(referenceOrg)
);

CREATE TABLE Plat(
idPlat NUMBER(10),
nomPlat VARCHAR2(50),
idIngredient NUMBER(10),
CONSTRAINT pk_Plat PRIMARY KEY(idPlat),
CONSTRAINT fk_Plat_Legume FOREIGN KEY(idIngredient) REFERENCES Legume(idIngredient)
);

CREATE TABLE Reunion(
   idRepas NUMBER(10),
   codePostal CHAR(5),
   ville VARCHAR2(50),
   adressePart VARCHAR2(50),
   idGroupe NUMBER(10),
   dateReu TIMESTAMP WITH TIME ZONE,
   nomReu VARCHAR2(50) NOT NULL,
   PRIMARY KEY(idRepas, codePostal, ville, adressePart, idGroupe, dateReu),
   FOREIGN KEY(idRepas) REFERENCES Repas(idRepas),
   FOREIGN KEY(codePostal, ville, adressePart) REFERENCES LieuPartenaire(codePostal, ville, adressePart),
   FOREIGN KEY(idGroupe) REFERENCES Groupe(idGroupe)
);


CREATE TABLE Machine(
nomTypeM VARCHAR2(50),
referenceMod NUMBER(10),
nomM VARCHAR2(50),
CONSTRAINT pk_Machine PRIMARY KEY(nomTypeM, referenceMod, nomM),
CONSTRAINT fk_Machine_Modele FOREIGN KEY(nomTypeM, referenceMod) REFERENCES Modele(nomTypeM, referenceMod)
);

CREATE TABLE Entretien(
typeEnt VARCHAR2(50),
idTenrac NUMBER(10),
dateEntre TIMESTAMP,
idClub NUMBER(10) NOT NULL,
idOrdre NUMBER(10) NOT NULL,
nomTypeM VARCHAR2(50) NOT NULL,
referenceMod NUMBER(10) NOT NULL,
nomM VARCHAR2(50) NOT NULL,
CONSTRAINT pk_Entretien PRIMARY KEY(typeEnt, idTenrac, dateEntre),
CONSTRAINT fk_Entretien_TypeEntretien FOREIGN KEY(typeEnt) REFERENCES TypeEntretien(typeEnt),
CONSTRAINT fk_Entretien_Tenrac FOREIGN KEY(idTenrac) REFERENCES Tenrac(idTenrac),
CONSTRAINT fk_Entretien_Registre FOREIGN KEY(idClub, idOrdre) REFERENCES Registre(idClub, idOrdre),
CONSTRAINT fk_Entretien_Machine FOREIGN KEY(nomTypeM, referenceMod, nomM) REFERENCES Machine(nomTypeM, referenceMod, nomM)
);

CREATE TABLE Menu(
idRepas NUMBER(10),
idPlat NUMBER(10),
CONSTRAINT pk_Menu PRIMARY KEY(idRepas, idPlat),
CONSTRAINT fk_Menu_Repas FOREIGN KEY(idRepas) REFERENCES Repas(idRepas),
CONSTRAINT fk_Menu_Plat FOREIGN KEY(idPlat) REFERENCES Plat(idPlat)
);

CREATE TABLE Compose(
idPlat NUMBER(10),
idSauce NUMBER(10),
idIngredient NUMBER(10),
CONSTRAINT pk_Compose PRIMARY KEY(idPlat, idSauce, idIngredient),
CONSTRAINT fk_Compose_Plat FOREIGN KEY(idPlat) REFERENCES Plat(idPlat),
CONSTRAINT fk_Compose_Sauce FOREIGN KEY(idSauce) REFERENCES Sauce(idSauce),
CONSTRAINT fk_Compose_Ingredient FOREIGN KEY(idIngredient) REFERENCES Ingredient(idIngredient)
);

CREATE TABLE Preside_EstPreside(
idTenrac NUMBER(10),
idRepas NUMBER(10),
adressePart VARCHAR2(50),
idGroupe NUMBER(10),
dateReu TIMESTAMP,
CONSTRAINT pk_PresideEstPreside PRIMARY KEY(idTenrac, idRepas, adressePart, idGroupe, dateReu),
CONSTRAINT fk_PresideEstPreside_Tenrac FOREIGN KEY(idTenrac) REFERENCES Tenrac(idTenrac),
CONSTRAINT fk_PresideEstPreside_Reunion FOREIGN KEY(idRepas, adressePart, idGroupe, dateReu) REFERENCES Reunion(idRepas, adressePart, idGroupe, dateReu)
);

CREATE OR REPLACE TRIGGER trg_check_grade_preside
BEFORE INSERT OR UPDATE ON Preside_EstPreside
FOR EACH ROW
DECLARE
v_count NUMBER;
BEGIN
SELECT COUNT(*)
INTO v_count
FROM Tenrac
WHERE idTenrac = :NEW.idTenrac
AND typeGrade IN (
SELECT typeGrade
FROM Grade
START WITH typeGrade IN ('CHEVALIER', 'DAME')
CONNECT BY typeGrade = PRIOR superieurGrade
);

IF v_count = 0 THEN
RAISE_APPLICATION_ERROR(
-20001,
'un idTenrac doit avoir un Grade d’au moins un Chevalier ou Dame'
);
END IF;
END;
/
/**
Remarque sur TRIGGER trg_check_grade_preside :
Une réunion ne peut avoir lieu sans être sous l’égide d’au moins la
présence d’un/d’une Chevalier/Dame.
*/

CREATE TABLE Appartient(
idTenrac NUMBER(10),
idGroupe NUMBER(10),
CONSTRAINT pk_Appartient PRIMARY KEY(idTenrac, idGroupe),
CONSTRAINT fk_Appartient_Tenrac FOREIGN KEY(idTenrac) REFERENCES Tenrac(idTenrac),
CONSTRAINT fk_Appartient_Groupe FOREIGN KEY(idGroupe) REFERENCES Groupe(idGroupe)
);

CREATE TABLE Assaisone(
idPlat NUMBER(10),
idSauce NUMBER(10),
CONSTRAINT pk_Assaisone PRIMARY KEY(idPlat, idSauce),
CONSTRAINT fk_Assaisone_Plat FOREIGN KEY(idPlat) REFERENCES Plat(idPlat),
CONSTRAINT fk_Assaisone_Sauce FOREIGN KEY(idSauce) REFERENCES Sauce(idSauce)
);

CREATE TABLE Utilisable(
idRepas NUMBER(10),
adressePart VARCHAR2(50),
idGroupe NUMBER(10),
dateReu TIMESTAMP,
nomTypeM VARCHAR2(50),
referenceMod NUMBER(10),
nomM VARCHAR2(50),
CONSTRAINT pk_Utilisable PRIMARY KEY(idRepas, adressePart, idGroupe, dateReu, nomTypeM, referenceMod, nomM),
CONSTRAINT fk_Utilisable_Reunion FOREIGN KEY(idRepas, adressePart, idGroupe, dateReu) REFERENCES Reunion(idRepas, adressePart, idGroupe, dateReu),
CONSTRAINT fk_Utilisable_Machine FOREIGN KEY(nomTypeM, referenceMod, nomM) REFERENCES Machine(nomTypeM, referenceMod, nomM)
);


CREATE OR REPLACE TRIGGER trg_check_machine_certifiee
BEFORE INSERT OR UPDATE ON Utilisable
FOR EACH ROW
DECLARE
v_count NUMBER;
BEGIN
SELECT COUNT(*)
INTO v_count
FROM Entretien E
JOIN Tenrac t ON t.idTenrac = E.idTenrac
WHERE E.nomTypeM    = :NEW.nomTypeM
AND E.referenceMod= :NEW.referenceMod
AND E.nomM        = :NEW.nomM
AND t.typeDignite IN (
SELECT typeDignite
FROM Dignite
START WITH typeDignite = 'MAITRE'
CONNECT BY typeDignite = PRIOR superieurDignite);

IF v_count = 0 THEN
RAISE_APPLICATION_ERROR(
-20002,
'Machine non certifiée : entretien valide requis avec Tenrac avec dignité >= Maître'
);
END IF;
END;
/
/**
Remarque sur TRIGGER trg_check_machine_certifiee :
Afin d’être accepté pour une utilisation officielle, une machine
doit présenter son certificat d’entretien effectué par un tenrac ayant obtenu la dignité idoine (au
moins Maître).
*/

CREATE TABLE Allergie(
idTenrac NUMBER(10),
idAller VARCHAR2(50),
CONSTRAINT pk_Allergie PRIMARY KEY(idTenrac, idAller),
CONSTRAINT fk_Allergie_Tenrac FOREIGN KEY(idTenrac) REFERENCES Tenrac(idTenrac),
CONSTRAINT fk_Allergie_Allergene FOREIGN KEY(idAller) REFERENCES Allergene(idAller)
);

CREATE TABLE Heurte(
idIngredient NUMBER(10),
doctrine VARCHAR2(60),
CONSTRAINT pk_Heurte PRIMARY KEY(idIngredient, doctrine),
CONSTRAINT fk_Heurte_Legume FOREIGN KEY(idIngredient) REFERENCES Legume(idIngredient),
CONSTRAINT fk_Heurte_Croyance FOREIGN KEY(doctrine) REFERENCES Croyance(doctrine)
);

CREATE TABLE Partenariat(
idOrdre NUMBER(10),
adressePart VARCHAR2(50),
CONSTRAINT pk_Partenariat PRIMARY KEY(idOrdre, adressePart),
CONSTRAINT fk_Partenariat_Ordre FOREIGN KEY(idOrdre) REFERENCES Ordre(idOrdre),
CONSTRAINT fk_Partenariat_LieuPartenaire FOREIGN KEY(adressePart) REFERENCES LieuPartenaire(adressePart)
);

CREATE TABLE Contient(
idIngredient NUMBER(10),
idAller VARCHAR2(50),
CONSTRAINT pk_Contient PRIMARY KEY(idIngredient, idAller),
CONSTRAINT fk_Partenariat_Legume FOREIGN KEY(idIngredient) REFERENCES Legume(idIngredient),
CONSTRAINT fk_Partenariat_Allergene FOREIGN KEY(idAller) REFERENCES Allergene(idAller)
);

ALTER TABLE Ordre
ADD CONSTRAINT fk_chefO FOREIGN KEY (chefO) REFERENCES Tenrac(idTenrac);
