CREATE TABLE Grade(
   typeGrade VARCHAR2(50),
   superieurGrade VARCHAR2(50),
   CONSTRAINT pk_Grade PRIMARY KEY(typeGrade),
   CONSTRAINT ck_type_grade CHECK (typeGrade IN (('Affilié','Affiliée', 'Sympathisant', 'Sympathisante' ,'Adhérent', 
                                                 'Adhérente' ,
                                                 'Chevalier' , 'Dame', 'Grand Chevalier',
                                                 'Haute Dame', 'Commandeur', 'Commanderesse','Grand’Croix', 'Grande’Croix'))),
   CONSTRAINT fk_superieurGrade FOREIGN KEY(superieurGrade) REFERENCES Grade(typeGrade)
);

CREATE TABLE Dignite(
   typeDignite VARCHAR2(50),
   superieurDignite VARCHAR2(50),
   CONSTRAINT pk_Dignite PRIMARY KEY(typeDignite),
   CONSTRAINT ck_type_dignite CHECK (typeDignite IN (('Maître', 'Grand Chancelier', 'Grand Maître'))),
   CONSTRAINT fk_superieurDignite FOREIGN KEY(superieurDignite) REFERENCES Dignite(typeDignite)
);

CREATE TABLE Organisme(
   reference NUMBER(10),
   siret CHAR(14) NOT NULL,
   raisonSociale VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_Organisme PRIMARY KEY(reference),
   CONSTRAINT uk_siret UNIQUE(siret)
);

CREATE TABLE Ordre(
   numOrdre NUMBER(10),
   nom VARCHAR2(50) NOT NULL,
   chefO NUMBER(10) NOT NULL,
   CONSTRAINT fk_chefO FOREIGN KEY(chefO) REFERENCES Tenrac(idTenrac),
   CONSTRAINT pk_Ordre PRIMARY KEY(numOrdre)
);

CREATE TABLE Repas(
   idRepas NUMBER(10),
   intitule VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_Repas PRIMARY KEY(idRepas)
);

CREATE TABLE Sauce(
   idSauce NUMBER(10),
   nom VARCHAR2(50),
   CONSTRAINT pk_Sauce PRIMARY KEY(idSauce)
);

CREATE TABLE Ingredient(
   idIngredient NUMBER(10),
   nom VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_Ingredient PRIMARY KEY(idIngredient)
);

CREATE TABLE Groupe(
   idGroupe NUMBER(10),
   nbMembre NUMBER(10) NOT NULL,
   CONSTRAINT pk_Groupe PRIMARY KEY(idGroupe),
   CONSTRAINT ck_nbMembre CHECK (nbMembre >= 2)
);

CREATE TABLE TypeMachine(
   nomType VARCHAR2(50),
   CONSTRAINT pk_TypeMachine PRIMARY KEY(nomType)
);

CREATE TABLE AdressePostale(
   codePostal CHAR(5),
   ville VARCHAR2(50),
   CONSTRAINT pk_Adresse_Postale PRIMARY KEY(codePostal, ville)
);

CREATE TABLE TypeEntretien(
   type VARCHAR2(50),
   periodicite VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_TypeEntretien PRIMARY KEY(type)
);

CREATE TABLE Rang(
   typeRang VARCHAR2(50),
   superieurRang VARCHAR2(50),
   CONSTRAINT pk_Rang PRIMARY KEY(typeRang),
   CONSTRAINT ck_type_rang CHECK (typeRang IN (('Novice', 'Compagnon'))),
   CONSTRAINT fk_superieurRang FOREIGN KEY(superieurRang) REFERENCES Rang(typeRang)
);

CREATE TABLE Titre(
   typeTitre VARCHAR2(50),
   superieurTitre VARCHAR2(50),
   CONSTRAINT pk_Titre PRIMARY KEY(typeTitre),
   CONSTRAINT fk_superieurTitre FOREIGN KEY(superieurTitre) REFERENCES Titre(typeTitre)
);

CREATE TABLE Croyance(
   doctrine VARCHAR2(60),
   CONSTRAINT pk_Croyance PRIMARY KEY(doctrine)
);

CREATE TABLE Allergene(
   idAller VARCHAR2(50),
   nomAller VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_Allergen PRIMARY KEY(idAller)
);

CREATE TABLE Club(
   numClub NUMBER(10),
   nom VARCHAR2(50) NOT NULL,
   chefC VARCHAR2(50) NOT NULL,
   numOrdre NUMBER(10) NOT NULL,
   CONSTRAINT pk_Club PRIMARY KEY(numClub),
   CONSTRAINT fk_numOrdre FOREIGN KEY(numOrdre) REFERENCES Ordre(numOrdre)
);

CREATE TABLE Legume(
   idIngredient NUMBER(10),
   nom VARCHAR2(50),
   CONSTRAINT fk_idIngredient FOREIGN KEY(idIngredient) REFERENCES Ingredient(idIngredient),
   CONSTRAINT pk_Legume PRIMARY KEY(idIngredient)
);

CREATE TABLE LieuPartenaire(
   adresse VARCHAR2(50),
   codePostale CHAR(5) NOT NULL,
   ville VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_LieuPartenaire PRIMARY KEY(adresse),
   CONSTRAINT fk_adresse_postale FOREIGN KEY(codePostale,ville) REFERENCES AdressePostale(codePostale, ville)
);

CREATE TABLE Modele(
   nomType VARCHAR2(50),
   reference NUMBER(10),
   type VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_Modele PRIMARY KEY(nomType, reference),
   CONSTRAINT fk_nomType FOREIGN KEY(nomType) REFERENCES TypeMachine(nomType),
   CONSTRAINT fk_type FOREIGN KEY(type) REFERENCES TypeEntretien(type)
);

CREATE TABLE Registre(
   numClub NUMBER(10),
   numOrdre NUMBER(10),
   dateOuverture DATE NOT NULL,
   dateFermeture DATE,
   CONSTRAINT pk_Registre PRIMARY KEY(numClub, numOrdre),
   CONSTRAINT fk_numClub FOREIGN KEY(numClub) REFERENCES Club(numClub),
   CONSTRAINT fk_numOrdre FOREIGN KEY(numOrdre) REFERENCES Ordre(numOrdre)
);

CREATE TABLE Tenrac(
   idTenrac NUMBER(10),
   nom VARCHAR2(50) NOT NULL,
   prenom VARCHAR2(50),
   courriel VARCHAR2(50) NOT NULL,
   tel CHAR(10) NOT NULL,
   adresse VARCHAR2(50) NOT NULL,
   sexe VARCHAR2(1) NOT NULL,
   doctrine VARCHAR2(60) NOT NULL,
   typeRang VARCHAR2(50),
   typeTitre VARCHAR2(50),
   codePostal CHAR(5) NOT NULL,
   ville VARCHAR2(50) NOT NULL,
   numOrdre NUMBER(10) NOT NULL,
   numClub NUMBER(10),
   reference NUMBER(10) NOT NULL,
   typeDignite VARCHAR2(50),
   typeGrade VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_Tenrac PRIMARY KEY(idTenrac),
   CONSTRAINT fk_doctrine FOREIGN KEY(doctrine) REFERENCES Croyance(doctrine),
   CONSTRAINT fk_typeRang FOREIGN KEY(typeRang) REFERENCES Rang(typeRang),
   CONSTRAINT fk_typeTitre FOREIGN KEY(typeTitre) REFERENCES Titre(typeTitre),
   CONSTRAINT fk_adresse_postale FOREIGN KEY(codePostal, ville) REFERENCES AdressePostale(codePostal, ville),
   CONSTRAINT fk_numOrdre FOREIGN KEY(numOrdre) REFERENCES Ordre(numOrdre),
   CONSTRAINT fk_numClub FOREIGN KEY(numClub) REFERENCES Club(numClub),
   CONSTRAINT fk_reference FOREIGN KEY(reference) REFERENCES Organisme(reference),
   CONSTRAINT fk_typeDignite FOREIGN KEY(typeDignite) REFERENCES Dignite(typeDignite),
   CONSTRAINT fk_typeGrade FOREIGN KEY(typeGrade) REFERENCES Grade(typeGrade),
   CONSTRAINT ck_typegrade_sexe CHECK (
    (sexe = 'M' AND typeGrade IN (
        'Affilié', 'Sympathisant', 'Adhérent',
        'Chevalier', 'Grand Chevalier', 'Commandeur', 'Grand’Croix'
    ))
    OR
    (sexe = 'F' AND typeGrade IN (
        'Affiliée', 'Sympathisante', 'Adhérente',
        'Dame', 'Haute Dame', 'Commanderesse', 'Grande’Croix'
    ))
   )
);

/**
CONSTRAINT pk_Notation PRIMARY KEY (numEt, code),
	CONSTRAINT fk_Notation_Module FOREIGN KEY (code) REFERENCES Module(code),
	CONSTRAINT fk_Notation_Etudiant FOREIGN KEY (numEt) REFERENCES Etudiant (numEt)

    CONSTRAINT uk_Prof_01 UNIQUE (nomProf, prenomProf)

    CONSTRAINT ck_anneeEt CHECK (anneeEt BETWEEN 1 AND 3),
*/

CREATE TABLE Carte(
   numOrdre NUMBER(10),
   numClub NUMBER(10),
   idTenrac NUMBER(10),
   reference NUMBER(10),
   idCarte NUMBER(10),
   CONSTRAINT pk_Carte PRIMARY KEY(numOrdre, numClub, idTenrac, reference, idCarte),
   CONSTRAINT fk_Carte_Ordre FOREIGN KEY(numOrdre) REFERENCES Ordre(numOrdre),
   CONSTRAINT fk_Carte_Club FOREIGN KEY(numClub) REFERENCES Club(numClub),
   CONSTRAINT fk_Carte_Tenrac FOREIGN KEY(idTenrac) REFERENCES Tenrac(idTenrac),
   CONSTRAINT fk_Carte_Organisme FOREIGN KEY(reference) REFERENCES Organisme(reference)
);

CREATE TABLE Plat(
   idPlat NUMBER(10),
   nom VARCHAR2(50),
   idIngredient NUMBER(10),
   CONSTRAINT pk_Plat PRIMARY KEY(idPlat),
   CONSTRAINT fk_Plat_Legume FOREIGN KEY(idIngredient) REFERENCES Legume(idIngredient)
);

CREATE TABLE Reunion(
   idRepas NUMBER(10),
   adresse VARCHAR2(50),
   idGroupe NUMBER(10),
   date_heure TIMESTAMP WITH TIME ZONE,
   nom VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_Reunion PRIMARY KEY(idRepas, adresse, idGroupe, date_heure),
   CONSTRAINT fk_Reunion_Repas FOREIGN KEY(idRepas) REFERENCES Repas(idRepas),
   CONSTRAINT fk_Reunion_LieuPartenaire FOREIGN KEY(adresse) REFERENCES LieuPartenaire(adresse),
   CONSTRAINT fk_Reunion_Groupe FOREIGN KEY(idGroupe) REFERENCES Groupe(idGroupe)
);


CREATE TABLE Machine(
   nomType VARCHAR2(50),
   reference NUMBER(10),
   nom VARCHAR2(50),
   CONSTRAINT pk_Machine PRIMARY KEY(nomType, reference, nom),
   CONSTRAINT fk_Machine_Modele FOREIGN KEY(nomType, reference) REFERENCES Modele(nomType, reference)
);

CREATE TABLE Entretien(
   type VARCHAR2(50),
   idTenrac NUMBER(10),
   date_ TIMESTAMP,
   numClub NUMBER(10) NOT NULL,
   numOrdre NUMBER(10) NOT NULL,
   nomType VARCHAR2(50) NOT NULL,
   reference NUMBER(10) NOT NULL,
   nom VARCHAR2(50) NOT NULL,
   CONSTRAINT pk_Entretien PRIMARY KEY(type, idTenrac, date_),
   CONSTRAINT fk_Entretien_TypeEntretien FOREIGN KEY(type) REFERENCES TypeEntretien(type),
   CONSTRAINT fk_Entretien_Tenrac FOREIGN KEY(idTenrac) REFERENCES Tenrac(idTenrac),
   CONSTRAINT fk_Entretien_Registre FOREIGN KEY(numClub, numOrdre) REFERENCES Registre(numClub, numOrdre),
   CONSTRAINT fk_Entretien_Machine FOREIGN KEY(nomType, reference, nom) REFERENCES Machine(nomType, reference, nom)
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
   adresse VARCHAR2(50),
   idGroupe NUMBER(10),
   date_heure TIMESTAMP WITH TIME ZONE,
   CONSTRAINT pk_PresideEstPreside PRIMARY KEY(idTenrac, idRepas, adresse, idGroupe, date_heure),
   CONSTRAINT fk_PresideEstPreside_Tenrac FOREIGN KEY(idTenrac) REFERENCES Tenrac(idTenrac),
   CONSTRAINT fk_PresideEstPreside_Reunion FOREIGN KEY(idRepas, adresse, idGroupe, date_heure) REFERENCES Reunion(idRepas, adresse, idGroupe, date_heure)
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
        'Chevalier', 'Dame', 'Grand Chevalier',
        'Haute Dame', 'Commandeur', 'Grand’Croix'
        );

    IF v_count = 0 THEN
        RAISE_APPLICATION_ERROR(
        -20001,
        'un idTenrac doit avoir un Grade d’au moins la Chevalier/Dame'
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
   adresse VARCHAR2(50),
   idGroupe NUMBER(10),
   date_heure TIMESTAMP WITH TIME ZONE,
   nomType VARCHAR2(50),
   reference NUMBER(10),
   nom VARCHAR2(50),
   CONSTRAINT pk_Utilisable PRIMARY KEY(idRepas, adresse, idGroupe, date_heure, nomType, reference, nom),
   CONSTRAINT fk_Utilisable_Reunion FOREIGN KEY(idRepas, adresse, idGroupe, date_heure) REFERENCES Reunion(idRepas, adresse, idGroupe, date_heure),
   CONSTRAINT fk_Utilisable_Machine FOREIGN KEY(nomType, reference, nom) REFERENCES Machine(nomType, reference, nom),
   CONSTRAINT fk_Utilisable_Entretien FOREIGN KEY(nomType, reference, nom) REFERENCES Entretien(nomType, reference, nom) --verifier...
   --CONSTRAINT ck_Utilisable CHECK ((nomType, reference, nom) IN (SELECT (nomType, reference, nom) FROM Entretien))
);
/**
Remarque sur CONSTRAINT ck_Utilisable_Entretien :
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
   numOrdre NUMBER(10),
   adresse VARCHAR2(50),
   CONSTRAINT pk_Partenariat PRIMARY KEY(numOrdre, adresse),
   CONSTRAINT fk_Partenariat_Ordre FOREIGN KEY(numOrdre) REFERENCES Ordre(numOrdre),
   CONSTRAINT fk_Partenariat_LieuPartenaire FOREIGN KEY(adresse) REFERENCES LieuPartenaire(adresse)
);

CREATE TABLE Contient(
   idIngredient NUMBER(10),
   idAller VARCHAR2(50),
   CONSTRAINT pk_Contient PRIMARY KEY(idIngredient, idAller),
   CONSTRAINT fk_Partenariat_Legume FOREIGN KEY(idIngredient) REFERENCES Legume(idIngredient),
   CONSTRAINT fk_Partenariat_Allergene FOREIGN KEY(idAller) REFERENCES Allergene(idAller)
);


