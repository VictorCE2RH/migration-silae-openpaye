.PHONY: migrate delete debug-migrate help class emplois update

DEBUG_PORT=5678
SCRIPT_DIR=.\scripts

help:
	@echo Commandes disponibles :
	@echo   class                 - Genere des sous-classes CRUD format Openpaye
	@echo   emplois              - Cree un fichier de regroupement des emplois CCN
	@echo   update               - Importe la version locale de traduction des emplois CCN
	@echo   migrate [args]       - Lance la migration avec les arguments specifies
	@echo   debug-migrate [args] - Lance la migration en mode debug (port %DEBUG_PORT%)
	@echo   delete [args]        - Supprime des items (avec --iscode)
	@echo.

class: 
	@echo - Openpaye CRUD subClasses format : 
	@python $(SCRIPT_DIR)\createAPIclass.py
	@echo.

scrapEmploiCCN:
	@echo - Creation fichier regroupement emplois CCN depuis Documentation Openpaye : 
	@python $(SCRIPT_DIR)\emploisCCN.py

update:
	@echo - Import version locale traduction des emplois CCN:
	@python $(SCRIPT_DIR)\importEmploiTradFile.py

idccToOpcc:
	@echo - Execution de la traduction IDCC OPCC: 
	@python $(SCRIPT_DIR)\idccToOpcc.py

test:
	@echo - Execution du fichier de test: 
	@python $(SCRIPT_DIR)\test.py

debug-migrate: debug-delete-before-migrate
	@echo - Lancement de la migration en mode debug de $(filter-out $@,$(MAKECMDGOALS)):
	python -m debugpy --listen 0.0.0.0:$(DEBUG_PORT) --wait-for-client .\typerscript.py exportsilae $(filter-out $@,$(MAKECMDGOALS))

# Version debug de delete_before_migrate si nécessaire
debug-delete-before-migrate:
	@echo - Suppression des numeros de dossiers avant la migration (mode debug): 
	python -m debugpy --listen 0.0.0.0:$(DEBUG_PORT) --wait-for-client .\typerscript.py delete $(word 1,$(filter-out debug-migrate,$(MAKECMDGOALS))) dossiers $(wordlist 2,$(words $(MAKECMDGOALS)),$(filter-out debug-migrate,$(MAKECMDGOALS))) --iscode --f

migrate: delete_before_migrate
	@echo - Lancement de la migration de $(filter-out $@,$(MAKECMDGOALS)):
	@python .\typerscript.py exportsilae $(filter-out $@,$(MAKECMDGOALS))

delete_before_migrate:
	@echo - Suppression des numeros de dossiers avant la migration : 
	@python .\typerscript.py delete $(word 1,$(filter-out migrate,$(MAKECMDGOALS))) dossiers $(wordlist 2,$(words $(MAKECMDGOALS)),$(filter-out migrate,$(MAKECMDGOALS))) --iscode

delete:
	@echo - Suppression d'item : 
	@python .\typerscript.py delete $(filter-out $@,$(MAKECMDGOALS)) --iscode

cumuls: 
	@echo - Lancement de la migration de $(filter-out $@,$(MAKECMDGOALS)):
	@python .\typerscript.py updatecumuls $(filter-out $@,$(MAKECMDGOALS))

%:
	@: