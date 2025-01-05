@echo off
REM Crear directorios
mkdir Gabriela_Fragancias_Project
mkdir Gabriela_Fragancias_Project\backend
mkdir Gabriela_Fragancias_Project\backend\gabriela_fragancias
mkdir Gabriela_Fragancias_Project\backend\migrations
mkdir Gabriela_Fragancias_Project\frontend
mkdir Gabriela_Fragancias_Project\frontend\src
mkdir Gabriela_Fragancias_Project\frontend\src\components
mkdir Gabriela_Fragancias_Project\frontend\public
mkdir Gabriela_Fragancias_Project\migrations
mkdir Gabriela_Fragancias_Project\docs

REM Crear archivos
type nul > Gabriela_Fragancias_Project\backend\manage.py
type nul > Gabriela_Fragancias_Project\backend\requirements.txt
type nul > Gabriela_Fragancias_Project\backend\gabriela_fragancias\__init__.py
type nul > Gabriela_Fragancias_Project\backend\gabriela_fragancias\settings.py
type nul > Gabriela_Fragancias_Project\backend\gabriela_fragancias\urls.py
type nul > Gabriela_Fragancias_Project\backend\gabriela_fragancias\wsgi.py
type nul > Gabriela_Fragancias_Project\backend\gabriela_fragancias\models.py
type nul > Gabriela_Fragancias_Project\backend\migrations\__init__.py
type nul > Gabriela_Fragancias_Project\frontend\package.json
type nul > Gabriela_Fragancias_Project\frontend\src\App.js
type nul > Gabriela_Fragancias_Project\frontend\src\index.js
type nul > Gabriela_Fragancias_Project\frontend\src\components\PerfumeList.js
type nul > Gabriela_Fragancias_Project\frontend\src\components\ClienteList.js
type nul > Gabriela_Fragancias_Project\frontend\public\index.html
type nul > Gabriela_Fragancias_Project\migrations\migrate_db.py
type nul > Gabriela_Fragancias_Project\docs\proposal.pdf
type nul > Gabriela_Fragancias_Project\README.md

echo Estructura de archivos y carpetas creada exitosamente.
pause