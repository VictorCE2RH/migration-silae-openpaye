from silae import Dossier
import role
from etablissement import Etablissment


# TODO: request default manager from API
emptyContact = {
    "identifiant": "",
    "codeCollaborateur": "",
    "nomNaissance": "",
    "nomUsuel": "",
    "prenom": "",
    "email": "",
    "telephoneBureau": "",
    "telephonePortable": "",
    "storedSince": "",
}


def parseDossiers(
    dossierMap: dict[str, Dossier],
    contactMap: dict[str, dict[str, str]],
    max: int,
    defaultContact: dict[str, str] = emptyContact,
) -> list[dict[str, str]]:
    openpaye_dossiers: list[dict[str, str]] = []
    i = 1  # compte le nombre de dossiers créés
    for numero, dossier in dossierMap.items():
        contact = contactMap[numero]
        print(f"Parsing Dossier : {dossier.numero}")
        numero = dossier.numero
        raisonSociale = dossier.raisonSociale
        email = contact.get("E-mail")
        tel = contact.get("Téléphone")
        nom_contact = (
            contact.get("Employeur").removeprefix("Mr").removeprefix("Mme").strip()
        )
        qualite = role.associer_role(contact.get("Qualité")).value
        openpaye_dossier: dict[str, str] = {
            "code": numero,
            "nom_dossier": raisonSociale,
            "adresse_email": email,
            "telephone": tel,
            "nom_contact": nom_contact,
            "qualite": qualite,
            "annee": "2024",
        }
        openpaye_dossiers.append(openpaye_dossier)
        print(f"[{i}] Dossier {dossier.numero} ajouté à la liste de création")
        if max > 0 and i == max:
            print("Limite max de dossiers créés atteint, arret de la boucle")
            break
        else:
            i += 1

    return openpaye_dossiers


def parseEtablissements(etabMap: dict[str, any]) -> list[Etablissment]:
    print(f"Parsing Etablissements Silae -> Openpaye")
    id = 0
    for siret, data in etabMap.items():
        print(f"Parsing {siret} ")
            contact = contactMap[numero]
            NumToEtablissements[numero] = Etablissment(None, etabJson.get("nomInterne"),contact.get("Raison sociale"),etabJson.get("etablissementPrincipal"),etabJson.get("siret"),Adresse(etabJson.get("adresse_postale"),"","",contact.get("Code postal"),contact.get("Ville"),"","","FR"),"","","",contact.get("Code NAF"),"",)
        id += 1
