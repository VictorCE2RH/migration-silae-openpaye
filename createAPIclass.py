
themes = [
    "Absences", "BulletinsPaies", "Contrats", "ContratSortant", "Dossiers",
    "Editions", "Etablissements", "HeuresSupplementaires", "Options", 
    "Primes", "Salaries", "SoldeToutComptes", "Variables", "VariablesBulletins"
]

print("")
for theme in themes:
    class_name = f"{theme}EP"
    print(f'__{theme.upper()}__ = "{theme.lower()}"')
print("")
print("api_map = {")
for theme in themes:
    class_name = f"{theme}EP"
    print(f'    __{theme.upper()}__: {class_name},')
print("}")

for theme in themes:
    class_name = f"{theme}EP"
    print(f"""class {class_name}(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__(__{theme.upper()}__, auth_key)""")