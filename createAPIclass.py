
themes = [
    "Absences", "BulletinsPaies", "Contrats", "ContratSortant", "Dossiers",
    "Editions", "Etablissements", "HeuresSupplementaires", "Options", 
    "Primes", "Salaries", "SoldeToutComptes", "Variables", "VariablesBulletins"
]

for theme in themes:
    class_name = f"{theme}EP"
    print(f"""class {class_name}(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("{theme}", auth_key)""")

print("{")
for theme in themes:
    class_name = f"{theme}EP"
    print(f'    "{theme.lower()}": opapi.{class_name},')
print("}")