# Documentacion RHS
***
## Base de datos 2

La base de datos dipone de varias herraientas que vamos a detallar:

1. Todas las tablas que contienen un ID se generan automaticamente con una secuencia de Num.anterior + 1 
   2. Para la tabla de RECORDS se tienen 2 triggers para evitar hacer registros en un orden no correcto.

           create or replace TRIGGER ACA_RHS_RECORDS_T2
           BEFORE INSERT ON ACA_RHS_RECORDS
           FOR EACH ROW
           DECLARE
             V_LAST_RECORD_TYPE NUMBER;
           BEGIN
               -- buscamos el ultimo registro de ese usuario para ese dia ,
               SELECT NVL(ID_REGISTER_TYPE, 99)
               INTO V_LAST_RECORD_TYPE
               FROM ACA_RHS_RECORDS
               WHERE ID_USER = :NEW.ID_USER
               AND TRUNC(DATE_FROM) = TRUNC(:NEW.DATE_FROM)
               ORDER BY DATE_FROM DESC, ID DESC
               FETCH FIRST 1 ROW ONLY;
               IF :NEW.ID_REGISTER_TYPE = 1 AND V_LAST_RECORD_TYPE = 1 THEN
                   RAISE_APPLICATION_ERROR(-20001, 'REGISTRO NO REALIZADO -> " No puedes crear un registro entrada sin salir primero " ');
               END IF;
               IF :NEW.ID_REGISTER_TYPE = 2 AND V_LAST_RECORD_TYPE = 2 THEN
                   RAISE_APPLICATION_ERROR(-20002, 'REGISTRO NO REALIZADO -> " No puedes crear un registro salida sin entrar primero " ');
               END IF;
           EXCEPTION
               WHEN NO_DATA_FOUND THEN
                  V_LAST_RECORD_TYPE := 99;
           END;
           /

Este trigger evitara que podamos realizar registros de entrada o salida de forma incorrecta.

                create or replace TRIGGER "ACA_RHS_RECORDS_T4"  
    BEFORE INSERT ON ACA_RHS_RECORDS 
    FOR EACH ROW 
    DECLARE 
        V_LAST_RECORD_TYPE NUMBER; 
    BEGIN 
        SELECT NVL(ID_REGISTER_TYPE, 0) 
        INTO V_LAST_RECORD_TYPE 
        FROM ACA_RHS_RECORDS 
        WHERE ID_USER = :NEW.ID_USER 
        AND TRUNC(DATE_FROM) = TRUNC(:NEW.DATE_FROM) 
        ORDER BY DATE_FROM DESC, ID DESC 
        FETCH FIRST 1 ROW ONLY; 
     
        IF :NEW.ID_REGISTER_TYPE = 4 AND V_LAST_RECORD_TYPE = 4 THEN 
            RAISE_APPLICATION_ERROR(-20001, 'No puedes crear un registro de salida sin iniciar uno nuevo primero'); 
        END IF; 
     
        IF :NEW.ID_REGISTER_TYPE = 3 AND V_LAST_RECORD_TYPE = 3 THEN 
            RAISE_APPLICATION_ERROR(-20001, 'No puedes crear un registro de entrada sin finalizar el ultimo primero'); 
        END IF; 
     
    EXCEPTION 
        WHEN NO_DATA_FOUND THEN 
            IF :NEW.ID_REGISTER_TYPE = 4 THEN 
                V_LAST_RECORD_TYPE := 0; 
                RAISE_APPLICATION_ERROR(-20001, 'Debes primero iniciar la pausa antes de pararla'); 
            END IF; 
     
            V_LAST_RECORD_TYPE := 1; 
            -- manejar otras condiciones aquí si es necesario 
    END; 
    /

Este trigger tambien evitara que realicemos registros de pausa y vuelta de forma incorrecta.