# Acuse masivo de solicitudes de Radicaciones
> Aplicacion cliente que consume un servicio de la api de litigar, para cargar los acuses masivos de solicitudes de radicaciones con y sin procesos en vigilancia.
## 1 Instalación de python
[![Alt text](https://img.youtube.com/vi/Ej0b1Wio2AU/0.jpg)](https://www.youtube.com/watch?v=Ej0b1Wio2AU)
## 2 Descargar app, descomprimir y ubicar en una ruta
[![Alt text](https://img.youtube.com/vi/RQw9MFQG9Fg/0.jpg)](https://www.youtube.com/watch?v=RQw9MFQG9Fg)
## 3 Instalar entorno virtual 
[![Alt text](https://img.youtube.com/vi/-QqdtczrN9s/0.jpg)](https://www.youtube.com/watch?v=-QqdtczrN9s)
## 4 Instalar Requirements 
[![Alt text](https://img.youtube.com/vi/_b64biBNFfI/0.jpg)](https://www.youtube.com/watch?v=_b64biBNFfI)
## 5 Configuración Env
[![Alt text](https://img.youtube.com/vi/lMfY40OP-YM/0.jpg)](https://www.youtube.com/watch?v=lMfY40OP-YM)
## 6 Ejecución - Acuse con Proceso
[![Alt text](https://img.youtube.com/vi/0UhUzwolmbE/0.jpg)](https://www.youtube.com/watch?v=0UhUzwolmbE)
## 7 Ejecución - Acuse sin Proceso
[![Alt text](https://img.youtube.com/vi/xuWZQdkiReI/0.jpg)](https://www.youtube.com/watch?v=xuWZQdkiReI)
## 8 Actualizaciones
[![Alt text](https://img.youtube.com/vi/gft-8KIWesk/0.jpg)](https://www.youtube.com/watch?v=gft-8KIWesk)
# Versionamiento
- Fecha primera versión: 21/11/2022
* Python >3.6.2 +
# Instalación
## 1. Instale python desde la siguiente ruta:
Pasos a seguir, si no tiene instalado python en su pc
> https://www.python.org/downloads/
## 2. Descargue y Descomprima el proyecto
- Descargue el proyecto desde github, ya sea desde un archivo zip (descomprímirlo) o por github
> https://github.com/litigar/radicar_acuse.git
- Descomprima el archivo zip
- Copie la carpeta descomprimida en la raíz de alguna unidad, para el ejemplo se coloca en C:\radicar_acuse-main 
## 3. Instale el entorno virtual:
- Abra una terminal e ingrese a la carpeta donde descomprimió el archivo zip
> Para ubicarse en la carpeta, en la terminal debe escribir 
> - cd C:\radicar_acuse-main
- Instalar el entorno virtual
> python -m pip install virtualenv
> - Si no funciona la instrucción con la palabra python, utilice la palabra py
> - py -m pip install virtualenv
- Cree un entorno virtual
> python -m venv venv_solicitud
> - Si no funciona la instrucción con la palabra python, utilice la palabra py
> - py -m venv venv_solicitud
- Activar El Entorno Virtual
> venv_solicitud\Scripts\activate
> - Para el ejemplo del video, ejecutar:
> - C:\radicar_acuse-main\venv_solicitud\Scripts\activate
- Entorno Virtual Activo (Ejemplo del video)
> - debe aparacer entre paréntesis al lado izquierdo de la ruta el nombre del entorno.
> - (venv_solicitud) C:\radicar_acuse-main>
## 4. Instale los componentes
Con el entorno virtual activo ejecute el siguiente comando
> pip install -r requirements.txt
# Configuración inicial
- Abra el archivo .env
- Ingrese el usuario y password de litigar inmediatamente al frente de caracter igual (=)
> - user_name=
> - password=
- procesar_desde_fila
> procesar_desde_fila --> Inicia la creación de solicitudes, desde el numero de la fila indicado en este campo
- numero_ejecucion
> - numero_ejecucion --> Cuando se ejecuta el programa se genera un numero para poder consultar el resumen del cargue
> - numero_ejecucion=0 --> Si el valor es 0, se crea un nuevo numero_ejecucion carga el archivo cargue_masivo.csv, procesa cada solicitud y asocia el respectivo pdf
> - numero_ejecucion=999 --> Si el valor es diferente de 0, procesa cada solicitud y asocia el respectivo pdf al numero de ejecución indicado
- El numero de ejecución permite ver resumen del cargue desde litiradicaciones desde la siguiente ruta
> masivos -> Cargar archivos masivos -> Consultar ultimos cargues
# Funcionalidad
## 1. Ingreso de registros para cargar los acuses
- En el archivo plano cargue_masivo.csv se deben colocar los registros con los cuales se van a cargar los acuses.
- Estructura del Archivo de Cargue: Delimitador punto y coma (;) La primera fila del archivo no se va a procesar, contiene los títulos de los campos.:
- Estructura archivo para acuse de procesos EN vigilancia
> SOLICITUD_ID; FECHA_RADICACION;CANTIDAD_FOLIOS;COSTO_IMPRESION
- Estructura archivo para acuse de procesos SIN vigilancia
> SOLICITUD_ID;IDENTIFICADOR; DESPACHO_ID;FECHA_RADICACION;CANTIDAD_FOLIOS;COSTO_IMPRESION
- En cada fila del archivo se debe ingresar un numero de solicitud.
- Los datos en las campos (columnas) no debe contener el caracter punto y coma ';' pues éste es el separador de columnas.
- NOTA: Tener cuidado que en la mismo archivo cargue_masivo.csv se colocan los datos de los registros para acuse de solicitudes con procesos en vigilancia y sin vigilancia
## 2. pdfs/zip a asociar a los acuses de las solicitudes con y sin proceso
- Los archivos pdfs deben ser ubicados en la carpeta pdfs.
- El archivo debe incluir al inicio del nombre el numero de la fila (seguido de un guión bajo) al cual se le debe asociar la solicitud de radicación a crear. 
> - Ej: FILA_nombreArchivo.pdf 
> - 2_nombreArchivo.pdf 
> - 2_nombreArchivo.zip
- Solo se puede asociar un archivo (zip/pdf) por cada solicitud a la cual se le va a cargar el acuse
- NOTA: Tener cuidado que en la misma ruta se colocan los archivos para acuse con procesos en vigilancia y sin vigilancia
## 3. Logs:
- Los logs de la ejecución de la aplicación quedan ubicados en la carpeta logs.
# Ejecución de la aplicación
Estando en la terminal en la ruta principal del proyecto, ejecute los siguientes pasos:
## 1. Asegurese de tener el entorno virtual activo
- Ubicarse en la carpeta desde la terminal debe escribir 
> cd C:\radicar_acuse-main
- Activar El Entorno Virtual
> venv_solicitud\Scripts\activate
> - Para el ejemplo del video, ejecutar:
> - C:\radicar_acuse-main\venv_solicitud\Scripts\activate
- Entorno Virtual Activo
> - Debe aparacer entre paréntesis al lado izquierdo de la ruta el nombre del entorno.
> - (venv_solicitud) C:\radicar_acuse-main>
## 2. Prepare el archivo cargue_masivo.csv 
- Coloque los registros de las solicitudes a crear en el archivo cargue_masivo.csv
- No mezclar en el archivo cargue_masivo.csv registros de solicitudes de procesos en vigilancia junto con procesos sin vigilancia. Los procesos son independientes
## 3. Ubique los archivos pdf/zip en la carpeta pdfs
- Tenga en cuenta la estructura de los nombres de los archivos
- Tener cuidado que en la misma ruta se colocan los archivos para acuse con procesos en vigilancia y sin vigilancia
## 4. Verifique los valores de las variables en .env
- procesar_desde_fila
- numero_ejecucion
## 5. Ejecute la aplicación para procesos en vigilancia
En la terminal, ejecute el siguiente comando
> python acuse_con_proceso.py
- Si no funciona la instrucción con la palabra python, utilice la palabra py
> py acuse_con_proceso.py
- Si al realizar una ejecución sale un error y no se crean las solicitudes, intente de nuevo la ejecución.
- Si el error persiste, informe al administrador (grupo de página)

## 6. Ejecute la aplicación para procesos sin vigilancia
En la terminal, ejecute el siguiente comando
> python acuse_sin_proceso.py
- Si no funciona la instrucción con la palabra python, utilice la palabra py
> py acuse_sin_proceso.py
- Si al realizar una ejecución sale un error y no se crean las solicitudes, intente de nuevo la ejecución.
- Si el error persiste, informe al administrador (grupo de página)

# Modificaciones a la aplicación
- DD/MM/YYYY: 
