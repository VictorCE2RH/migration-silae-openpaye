from dataclasses import dataclass


@dataclass
class Contact:
    identifiant: str
    nom: str
    prenom: str
    fonction: str
    telBureau: str
    eMail: str


@dataclass
class Contacts:
    Liste: list[Contact]
