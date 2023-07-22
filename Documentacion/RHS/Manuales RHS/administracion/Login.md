# Documentacion RHS
***
## Login

![Imagen del login](../../Images/Login.png "Title")


Para empezar la aplicacion dispone de un **login** para autenticar a los usuarios ya que es una aplicacion
interna de una empresa,cada trabajador dispondre de una cuenta creada previamente creada por el administrador
del departamento o de la app.

#### Codigo:

    FUNCTION ACA_AUTHENTICATE( p_username IN VARCHAR2, p_password IN VARCHAR2) RETURN BOOLEAN IS
        l_valid_user NUMBER;
    BEGIN
        SELECT NVL(COUNT(*),0) INTO l_valid_user FROM ACA_RHS_USERS WHERE mail = LOWER(p_username) AND password = p_password;
        
        IF l_valid_user = 0 THEN
            RETURN FALSE;
        ELSE
            RETURN TRUE;
        END IF;
    END;

Disponemos de la funcion ***ACA_AUTENTICATE*** donde disponemos de 2 parametros ***p_username*** y ***p_password*** estos son los campos de texto que podemos
visualizar en la imagen, donde el usuario introduce su correo y contraseña.

    SELECT NVL(COUNT(*),0) INTO l_valid_user FROM ACA_RHS_USERS WHERE mail = LOWER(p_username) AND password = p_password;

Despues mediante la siguiente consultar comprobaremos que los datos introducidos son validos, comprobando tanto MAIL como password

    IF l_valid_user = 0 THEN
            RETURN FALSE;
        ELSE
            RETURN TRUE;
        END IF;

Comprobamos que si el valor de ***l_valid_user*** es igual a 0 NO existe ningun usuario con esos datos

en caso de que nos se cumpla el usuario es valido y retornaremos ***TRUE*** y el usuario podra acceder
