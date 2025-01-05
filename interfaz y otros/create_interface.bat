@echo off
echo Creando la interfaz de Gabriela Fragancias...

REM Verificar si Node.js esta instalado
where /q node
if %ERRORLEVEL% neq 0 (
  echo Node.js no esta instalado. Por favor instale Node.js antes de continuar.
  pause
  exit /b
)

REM Verificar si Create React App esta instalado
where /q create-react-app
if %ERRORLEVEL% neq 0 (
  echo Create React App no esta instalado. Por favor instale Create React App antes de continuar.
  pause
  exit /b
)

REM Crear el proyecto React
create-react-app gabriela-fragancias-pwa
if %ERRORLEVEL% neq 0 (
  echo Error al crear el proyecto React.
  pause
  exit /b
)

REM Navegar al directorio del proyecto
cd gabriela-fragancias-pwa

REM Instalar dependencias adicionales
call npm install --save-dev workbox-cli
call npm install react-router-dom
call npm install register-service-worker

REM Copiar archivos personalizados
copy "..\public\index.html" "public\index.html" /Y
copy "..\public\manifest.json" "public\manifest.json" /Y
copy "..\src\App.js" "src\App.js" /Y
copy "..\src\index.js" "src\index.js" /Y
REM Agrega más líneas para otros archivos personalizados...

echo Interfaz creada con éxito.
pause