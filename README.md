# Dashboard para analizar el riesgo de crédito

Este proyecto es un Dashboard para analizar las características que tienen ciertos atributos que influyen en la decisión de si una persona obtiene un crédito o no; es decir, en cuan riesgosos son.

## Integrantes

* Daniel Ganoza Chavez (20196030)
* Javier Tocto Sanchez (20161672)
* Daniel Arturo Castillo Rios (20171658) 
* Fidel Moisés Apari Sánchez (20212126)

[Link al dataset](https://www.kaggle.com/datasets/laotse/credit-risk-dataset)

> [!NOTE] El dataset se encuentra en el repostiorio

# Índice

* **Instalación**: Este proyecto tendrá dos formas de instalación conforme usted se sienta más cómodo, preferiblemente se usará venv
    * Instalación sin venv
    * Instalación con venv
* **Estructura del proyecto**: Se explica cuál será la distribución de archivos
* **Cómo contribuir (cómo usar Git y Github)**: Si usted es un usuario nuevo en el uso de git y github, trataré de explicar aquí una forma sencilla de cómo 
    * **Sobre Git y Github**: Expliación resumido de ambas tecnologías, porque muchas personas consideran que son lo mismo
    * **Diccionario de términos**: Algunos términos populares en el uso de git
    * **Proceso para contribuir**: Pasos de cómo contribuir de forma básica
    * **Tutoriales**
        * Cómo instalar git: Links
        * Cómo configurar git (Iniciar sesión y ello): Links
        * Pasos iniciales: Explicación
        * Primer commit: Explicación
        * Cómo publicar cambios realizados: Explicación
        * Tutoriales extra para usar github: Links
* **Cómo añadir páginas**: Explicación de como añadir páginas al sitio

# Instalación

Para usar este proyecto es preferible tener python 3.12.4, preferiblemente mediante Anaconda para poder realizar ambientes virtuales

## Instalación sin venv

Esta es la forma de instalación, por así decirlo, más sencilla. Usa este método si te sientes cómodo

1. Instalar las dependencias necesarias para este proyecto que están en el archivo requirements.txt
    ```
    pip install -r requirements.txt
    ```

2. Ejecutar la página principal
    ```
    streamlit run app.py
    ```
> [!IMPORTANT]
> Si usas esta forma de instalación y quieres añadir dependencias, por favor, comúnicate con el propietario del proyecto:
> ```bash
> pip freeze > requirements.txt
> ```

## Instalación con venv

Los venv, también llamados ambientes virtuales permiten aislar la versión de python y sus dependencias a un solo proyecto; es decir, puedes tener varios proyectos con diferentes dependencias aisladas gracias a esta herramienta

1. Crear el ambiente virtual desde anaconda, la versión de python será 3.12.4:
    ```
    conda create -n <nombre del ambiente> python=3.12.4
    ```

2. Activar el ambiente virtual
    ```
    conda activate <nombre del ambiente que puso>
    ```
    Opcionalmente, si quiere desactivarlo para usar la forma base de anaconda, etc. Usa este comando:
    ```
    conda deactivate
    ```

3. Instalar las dependencias necesarias para este proyecto que están en el archivo requirements.txt
    ```
    pip install -r requirements.txt
    ```

4. Ejecutar la página principal
    ```
    streamlit run app.py
    ```

> [!IMPORTANT]
> Si quiere añadir nuevas dependencias y está usando un venv, entonces usa:
> ```bash
> pip freeze > requirements.txt
> ```

# Estructura del proyecto

* data: Almacena los datos que se usarán en el proyecto
* pages: Directorio con páginas en extesnión .py. Ahí se encuentran las páginas de streamlit
    * datos.py: Para dar un vistazo a los datos actuales
    * visual.py: Aun no tiene propósito claro, pero se relacionará con el modelo final
    * formulario.py: Archivo para predecir el resultado de un registro, permitirá imprimir el resultado
* utils: Tiene métodos para usar dentro de pages
    * crear_reporte: Permite crear el resporte necesario para formulario.py
* app.py: Es el archivo principal que ejecuta la navegación de las páginas
* .gitignore: Ignora ciertos archivos innecesarios como archivos de cache
* requirements.txt: Contiene las librerías necesarias para el proyecto
* README.md: Lo estás leyendo capo

# Cómo contribuir

## Sobre Git y Github

Primero es necesario mencionar algunas qué son Git y Github:
* **Git**: Es una herramienta en local para versionar código, esto quiere decir que te permite realizar diferentes versiones de tu código
* **Github**: Es la aplicación web que permite almacenar y compartir repositorios de github en la nube

## Diccionario de términos

* **Repositorio**: Es la carpeta donde git versiona el proyecto de tu interes, en este caso el repositorio es toda esta carpeta
* **Stage area**: Es como una memoria RAM para los cambios aun no registrados del todo. Es un paso intermedio y obligatorio para registrar commits
* **Commit**: Es un cambio registrado en el historial, tiene su identificador y su propia descripción
* **Commitear**: Es la acción de realizar cambios en el historial del repositorio git
* **Pushear**: Subir el historial de cambios de Git a GitHub
* **Branch o ramas**: Permite realizar bifuracaciones dentro de un repositorio git, cada rama tiene su historial, aunque comparten el historial con la rama de donde partieron. Más adelante se verá como usarlos
* **Mergear**: Cada rama tiene su historial, mergear es una tarea que trata de juntar dos ramas. Principalemente se usará para mergear hacia la rama principal

## Proceso para contribuir

Este proceso es un resumen de los pasos básicos para hacer cambios en el repositorio de Github, es un listado de lo que se expicará a continuación

* Clonas el repositorio de Github: Básicamente realizas una copia en tu escritorio para realizar cambios locales
* Creas tu propia rama: Esto con el fin de evitar errores al tener cambios diferentes de diferentes equipos
* Por cada cambio que quieras hacer: Realizas un git add y luego git commit
* Luego que hallas realizado todos tus cambios, subes los cambios en github
* En Github publicas tu rama para mergearlo, en este proceso debes dar detalles de lo que hiciste para saber cómo mergearlo

## Tutoriales

### Cómo instalar git

[Video 1](https://www.youtube.com/watch?v=jdXKwLNUfmg)

[Tutorial de la documetnación oficial](https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Instalaci%C3%B3n-de-Git)

### Cómo configurar git (Iniciar sesión y ello)

[Video de como configurar correo y username](https://www.youtube.com/watch?v=E_l1L6Ayiiw)

[Video 2](https://www.youtube.com/watch?v=LzVfVs5n3Gw)

Este siguiente link es para conectare y que puedan usar el repositorio remoto, es necesario tener cuenta en github:

[Video para conectarse con tokens](https://www.youtube.com/watch?v=2nzOI-ynXF4)

### Pasos iniciales

> [!IMPORTANT]
> Usar **Git Bash**

Dependiendo de cómo te autenticaste en github, requerirás usar uno de los siguientes comandos:

```
git clone https://github.com/Fidnix/ProyectoFinalAnalisisDatos.git
git clone git@github.com:Fidnix/ProyectoFinalAnalisisDatos.git
gh repo clone Fidnix/ProyectoFinalAnalisisDatos
```

Por favor, no descargues el zip, tuve problemas con un compañero que uso esa manera para registrar sus cambios y tuvimos que rehacer varias cosas

### Primer commit

En primer lugar, sí o sí es necesario que crees una nueva rama, si no se entiende bien qué es la rama, es un espacio del historial a parte de otras ramas como la rama principal, que sirve para realizar cmabios propios, son útiles para evitar errores al programar en diferentes equipos y en diferentes tiempos:

```
git branch Nombre_de_la_rama_no_se_pon_tu_nombre
```

Una vez lo crees, no has cambiado de rama, en el git bash dirá que estás en la rama principal (main), para cambiar de rama usas:

```
git switch nombre_de_tu_rama
```

Una vez estés dentro de la carpeta, puedes realizar cualquier cambio en los archivos (Si usas Visual Stduio Code, se verá que cambios realizas)

Para registrar cambios en el staging area

```
git add filename1 filenam2....
```
O para registrar el cambio de toda la carpeta:

```
git add .
```

Luego, requerirás realizar el commit con su descripción para ver los cambios:

```
git commit -m "Descripción....Pon cualquier wea"
```

Para ver el historial del repositorio, recuerda presionar la tecla "q" para salir de esa vista:

```
git log
```

Y listo, ya realizaste tu primer commit

### Cómo publicar cambios realizados

Solo usa:

```
git push -u origin Nombre_de_la_rama
```

Esto debería mandar los cambios al repositorio en Github, si por aube da errores, busca tutos o comúnicate conmigo

Luego tendrás que ir a Github (en tu navegador) y explicar los cambios de tu rama: (Próximamente explicaré más esto)

### Tutoriales extra para usar github

El siguiente video explica más características de Git, así que solo enfocate en lo que necesites:

[Video](https://www.youtube.com/watch?v=niPExbK8lSw)

[Video 2](https://www.youtube.com/watch?v=vlCXdvcgiE0)

[Video 3](https://www.youtube.com/watch?v=VdGzPZ31ts8)

# Cómo añadir páginas

Para añadir páginas, usa la carpeta pages y añade el archivo que quieres definir como página.
Luego añade en app.py las líneas de configuración de la página:

```python
pages = [
    ...,
    st.Page(ruta_pagina, title=nombre_pagina),
]
```