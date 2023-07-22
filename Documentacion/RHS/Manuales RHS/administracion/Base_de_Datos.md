# Documentacion RHS
***
## Base de datos

[![](https://mermaid.ink/img/pako:eNqtlF1rgzAUhv-K5KqDFrbBbnKXataG-VGS2DEQJNR0K9R2OL0Y2v--2E6qNuq6LVchJ-c9viePJwerfSQBBDKxNuI1EXGwM9RCJgrpnIWm53KKTM6M_BQoF7EM13emmJ6POOE2NpaImnNE70cPtzfn2NzzKWtkHJpFLLxAlCMHux11jOFCLUmKTY9av1Yrl4U4Dh-p5xx3dR2lPiOMYxrylwW-VFU3fKZOeiw3Fa7-SkMv6tn4vxpYGvhT-xxE7I7QAjH2rJ6nI1w2WDnR9rWGijZe8drXe1X6SZkL_SkxESeeO2TTVre4b-EL6m3PnekjOgSO5yxcIvvKH4jiJWG4yhndDUCq7Op_hqKYTIqig0F4AXaPSN7iBFaGdRC1Mk6UwuqZf5DRmA-whUFX_j7XDDFYZ2SIin6nYAximcRiE6npeQQoAOmbjGUAoNpGci2ybRqAYHdQV0WW7tnnbgVgmmRyDLL3SKTye-QCuBbbD3n4AqPldLA?type=png)](https://mermaid.live/edit#pako:eNqtlF1rgzAUhv-K5KqDFrbBbnKXataG-VGS2DEQJNR0K9R2OL0Y2v--2E6qNuq6LVchJ-c9viePJwerfSQBBDKxNuI1EXGwM9RCJgrpnIWm53KKTM6M_BQoF7EM13emmJ6POOE2NpaImnNE70cPtzfn2NzzKWtkHJpFLLxAlCMHux11jOFCLUmKTY9av1Yrl4U4Dh-p5xx3dR2lPiOMYxrylwW-VFU3fKZOeiw3Fa7-SkMv6tn4vxpYGvhT-xxE7I7QAjH2rJ6nI1w2WDnR9rWGijZe8drXe1X6SZkL_SkxESeeO2TTVre4b-EL6m3PnekjOgSO5yxcIvvKH4jiJWG4yhndDUCq7Op_hqKYTIqig0F4AXaPSN7iBFaGdRC1Mk6UwuqZf5DRmA-whUFX_j7XDDFYZ2SIin6nYAximcRiE6npeQQoAOmbjGUAoNpGci2ybRqAYHdQV0WW7tnnbgVgmmRyDLL3SKTye-QCuBbbD3n4AqPldLA)

Esta es la base de datos que usaremos para nuestra aplicacion.

#### La base de datos cumplen unas condiciones donde:
* El nombre sera siempre ***ACA_*** (angel cairon arcila) seguido de ***RHS_*** (Nombre de la app) ***Nombre_tabla***
* Los nombres en los atributos siempre seran ***TITLE***

### ACA_RHS_USERS:
    Esta sera nuestra tabla principal para usuarios, en ella almacenaremos los siguientes atributos:
        
        ID:Clave primaria
        TITLE: Nombre del usuario
        MAIL:el correo electronico del usuario
        PASSWORD:contraseña del usuario
        ID_ROLE:Clave foranea para definir el rol del usuario (Admin o trabajador)
        ID_DEPARTAMENT:Clave foranea para indicar a que departamento pertenece (RRHH,Informatica etc.)
        ID_CONTRACT: Clave foranea para relacionar al contrato con su trabajador.


### ACA_RHS_DEPARTAMENTS:

    Esta sera nuestra tabla para almacenar los departamentos que se quieran añadir.

        ID:Clave primaria
        TITLE: Nombre del departamento


### ACA_RHS_ROLES:
    
    Esta sera nuestra tabla para almacenar los roles en este caso (admin y trabajador)
    
        ID:Clave primaria
        TITLE:Nombre del rol 

### ACA_RHS_Contracts:
    
    Esta sera nuestra tabla para 
    
        ID:Clave primaria
        TITLE:Nombre del contrato
        HOURS: horas que debe de cumplir el trabajador

### ACA_RHS_WORKERS_UBICATION:
    
    Esta sera nuestra tabla para 
    
        ID:Clave primaria
        TITLE:Nombre de la ubicacion
        LATITUDE: Latitud del registro
        LONGITUDE: longitud del registro
        ID_USER: Usuario que realiza el registro
        IS_VALID: variable para permitir al usuario registrar desde esa ubicacion o no
        REVISED: variable para saber si una ubicacion introducida por el trabajador fue revisada por el administrador
        DATE_FROM: fecha en la que se realiza el registro

### ACA_RHS_RECORDS:
    
    Esta sera nuestra tabla para 
    
        ID: Clave primaria
        TITLE: Nombre del registro (Entrada,Salida,Descando,De vuelta)
        DATE_FROM: Fecha del registro
        ID_REGISTER_TYPE:Clave foranea para realizar con los tipos pre-establecidos de registros
        ID_USER:Clave foranea para saber que usuario realiza el registro

### ACA_RHS_REGISTER_TYPE:
    
    Esta sera nuestra tabla para 
    
        ID:Clave primaria
        TITLE: Tipo de registros (Entrada,Salida,Descando,De vuelta)