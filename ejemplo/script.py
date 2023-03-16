# -*- coding: utf-8 -*-"""Created on Tues Mar 8 2022Modified on Mon May 9 2022@author: sanarbel"""
from getpass import getpass, getuser
from os import makedirs, path 
import pandas as pd
import pyodbc
def get_date():
    """    Solicita la fecha de la conciliación por consola.   
    Returns    -------    date : String        
    Ubicación fisica del archivo seleccionado en el equipo que se ejecute.    """   
    print('><'*40)
    date = input(
        'Escriba la fecha exacta que desea conciliar en formato AAAAMMDD: ')
    return int(date)

def get_user():
    """    Solicita el usuario de NACIONAL.    
    Returns    -------    usr : String        
    Ubicación fisica del archivo seleccionado en el equipo que se ejecute.    """    
    print('><'*40)
    print('Escriba su usuario de Nacional: ')
    usr = input()
    return usr 

def guardar(data, original_name):
    """    Guarda el dataframe de datos encriptados en un archivo CSV    
    Parameters    ----------    data : DataFrame        
    Dataframe de datos encriptados    original_name : string }Nombre del archivo original  """    
    save_path = 'salidas/'    
    if not path.isdir(save_path):
        print(f'La ruta {save_path} no existe, se creará en esta carpeta...')
        makedirs(save_path)
    data.to_csv(
        save_path + original_name + '.csv',
        index=False,
    )
    print('El archivo ha sido guardado en la ruta ' + save_path + original_name + '.csv')

def inicio(opcion):
    """    inicio ejecuta el proceso asociado a la opción seleccionada en el menú  
      Parameters    ----------    opcion : int        opción seleccionada del menú   
       Raises    ------    SystemExit        
       Cuando se marca salida, cierra el programa    """    
    INICIANDO_PROCESAMIENTO = 'Iniciando procesamiento...'    
    FINALIZACION_PRIMER_QUERY = 'Primer query terminado, comenzando la generación de 1 archivo...'    
    FINALIZACION_SEGUNDO_QUERY = 'Segundo query terminado, comenzando la generación de 1 archivo...'    
    FINALIZACION_TERCER_QUERY = 'Tercer query terminado, comenzando la generación de 1 archivo...'    
    opciones = [
        '1',
        '2',
        '3',
        '4',
        # '5', '6', '7'    
        ]
    while opcion:
        # Si la opcion es 8 entonces cierra el programa        
        if opcion == '8':
            raise SystemExit        
        if opcion in opciones:
            # Se solicita la fecha por consola            
            date = get_date()
            # Se toma el usuario de sesión            
            user = 'N' + getuser()
            user = get_user()            
            # Pide la contraseña por consola            
            password = getpass(f'Escriba su contraseña de Nacional para el usuario {user.upper()}: ')
            try:
                cnx_nac = pyodbc.connect('DSN=NACIONAL;UID=' + str(user) + ';PWD=' + str(password) + '', autocommit=True )
            except pyodbc.InterfaceError:
                print('Usuario contraseña no valido...')
                opcion = menu()
                inicio(opcion)
            if opcion == '1':
                print(INICIANDO_PROCESAMIENTO)
                sql_1 = f'''SELECT TMETYIDENT, TFUNCICODE, TPROCCCODI, TAPRVEDCOD, CONCAT(AMED1_004, RIGHT(TPRIACCNUM,4)) AS TPRIACCNUM, TRANSAMOUN, TCADACEICO,
                TMESSREIND, TFECHAPROC, TLOCTRADAT, AMED1_001, AMED1_004, CONCAT(AMED1_004, RIGHT(AMED1_002,4)),AS AMED1_002, AMED1_048, AMNA1_001, AMNA1_002,
                AMNA1_017 FROM TDCLIBRAMD.TDCFFET112 INNER JOIN TDCLIBRAMD.TDCFFAMED1 ON AMED1_001 = 807 AND AMED1_002 = LPAD(TRIM(TPRIACCNUM),19, '0')
                LEFT JOIN TDCLIBRAMD.TDCFFAMNA1 ON AMED1_001 = AMNA1_001 AND AMED1_048 = AMNA1_002 WHERE TSETTLINDI = 'M' AND TRECCURCOD = '170' AND 
                TFUNCICODE <> '205' AND TFECHAPROC = '{date}' '''
                sql_2 = f'''SELECT ATPT1_001, ATPT1_002, CONCAT(ATPT1_002, RIGHT(ATPT1_026,4)) AS ATPT1_026, ATPT1_011, ATPT1_007, ATPT1_006, ATPT1_013,
                ATPT1_009, ATPT1_014, ATPT1_030, ATPT1_018, ATPT1_025 FROM TDCLIBRAMD.TDCFFATPT1 WHERE ATPT1_009 IN ('2700','2701','2706','2734','2735','2707',
                '2704','2705','2708','2709','471') AND ATPT1_013 = '{date}' AND ATPT1_025 = 0 AND ATPT1_003 = 0'''                
                sql_3 = f'''SELECT CTATJ_002 TARJETA, AMNA1_017 IDENTIFICACION, Y.* FROM TDCLIBRAMD.TDCFFCONTH Y LEFT JOIN TDCLIBRAMD.TDCFFCTATJ T ON 
                CTATJ_004 = CONROCUENT LEFT JOIN TDCLIBRAMD.TDCFFAMBS2 A ON AMBS2_002 = CTATJ_004 AND AMBS2_001 = 807 LEFT JOIN TDCLIBRAMD.TDCFFAMNA1 AM
                ON AMBS2_005=AMNA1_002 AND AMNA1_001=807 WHERE cotipo = '01' AND covlrorigi <> '0' AND comoneda = '170' AND COCODIGOTR IN ('9090','9190','9091',
                '9191','9302','9202','9305','9205','9303','9203','9204','9304') AND COFECHAPOS = '{date}' AND LEFT(cologo,1) = '6' AND coorg = '807' ORDER BY
                AMNA1_017 DESC'''
                print('Ejecutando el primer query...')
                df_1 = pd.read_sql(sql_1, cnx_nac) 
                print('Primer query terminado, comenzando la generación de 3 archivos')
                guardar(
                    df_1[[
                        'TMETYIDENT',
                        'TFUNCICODE',
                        'TPROCCCODI',
                        'TAPRVEDCOD',
                        'TPRIACCNUM',
                        'TRANSAMOUN',
                        'TCADACEICO',
                        'TMESSREIND',
                        'TFECHAPROC',
                        'TLOCTRADAT']], 'TDCFFET112' + '_' + str(date)
                )
                guardar(
                    df_1[[
                        'AMED1_001',
                        'AMED1_004',
                        'AMED1_002',
                        'AMED1_048' ]], 'TDCFFAMED1' + '_' + str(date)
                )
                guardar(
                    df_1[[
                        'AMNA1_001',
                        'AMNA1_002',
                        'AMNA1_017']], 'TDCFFAMNA1' + '_' + str(date)
                )
                print('Ejecutando el segundo query...(TDCFFATPT1)')
                df_2 = pd.read_sql(sql_2, cnx_nac)
                print(FINALIZACION_SEGUNDO_QUERY)
                guardar(df_2, 'TDCFFATPT1' + '_' + str(date))
                print('Ejecutando el tercer query...(TDCFFCONTH)')
                df_3 = pd.read_sql(sql_3, cnx_nac)
                print(FINALIZACION_TERCER_QUERY)
                guardar(df_3, 'TDCFFCONTH' + '_' + str(date))
                cnx_nac.close()
            elif opcion == '2':
                print(INICIANDO_PROCESAMIENTO)
                sql_1 = f'''WITH TARJ (TJNROTRJ, TJNRODOC) AS (SELECT DISTINCT TJNROTRJ, TJNRODOC FROM CABLIBRAMD.CABFFTARJ WHERE 
                (TJNROBCO IN ('807') OR TJNROBCO IS NULL)) SELECT TJNRODOC AS DOCIDEN, ANO||LPAD(MES,2,0)||LPAD(DIA,2,0) AS FECHA, TERCERO, OFICINA, CUENTA,
                TIPOCUENTA, TRANSAC, RIGHT(TARJETA,4) AS TARJETA, VALOR, CODAUT, FORMA0210 FROM CABLIBRANL.CABFFBEXTA LEFT JOIN TARJ ON 
                TJNROTRJ = RIGHT(TARJETA,10) WHERE TRANSAC IN(55253, 57779, 57379, 55255) AND VALOR <> 0 AND ----(TJNROBCO = '807' OR TJNROBCO IS NULL) AND 
                DIA = {str(date)[-2:]}'''
                sql_2 = f'''WITH TARJ (TJNROTRJ, TJNRODOC) AS (SELECT DISTINCT TJNROTRJ, TJNRODOC FROM CABLIBRAMD.CABFFTARJ WHERE (TJNROBCO IN ('807') OR 
                TJNROBCO IS NULL)) SELECT TJNRODOC AS DOCIDEN, CHTMTI, CHTFNC, CHTCPR, CHTIRM, CHTFPR, CHTFHT, RIGHT(CHTTAR,4) AS CHTTAR, CHTVMF/100 AS CHTVMF,
                CHTAUT, CHTDES FROM INELIBRANL.CVHTNAL LEFT JOIN TARJ ON TJNROTRJ = RIGHT(CHTTAR,10) WHERE CHTFPR = '{date}' AND CHTIDL = 'M' AND CHTFNC NOT IN 
                ('205','282') AND CHTMTI NOT IN ('1442', '1740') ----AND ---(TJNROBCO = '807' OR TJNROBCO IS NULL)'''
                print('Ejecutando primer query...(CABFFBEXTA)')
                df_1 = pd.read_sql(sql_1, cnx_nac)
                for column in ['DOCIDEN','TERCERO','OFICINA','CUENTA','TIPOCUENTA','TRANSAC','TARJETA','CODAUT','CHTTAR','CHTAUT']:
                    df_1[column]=df_1[column].astype(int)
                df_1['Usofut1'] = ''
                df_1['Usofut2'] = ''
                df_1['Usofut3'] = ''
                df_1['Usofut4'] = ''
                print(FINALIZACION_PRIMER_QUERY)
                guardar(df_1, 'CABFFBEXTA_CABLIBRANL' + '_' + str(date))
                print('Ejecutando el segundo query...(CVHTNAL)')
                df_2 = pd.read_sql(sql_2, cnx_nac)
                for column in ['DOCIDEN','CHTMTI','CHTFNC','CHTCPR','CHTIRM','CHTFPR','CHTFHT','CHTTAR','CHTAUT']:
                    df_2[column]=df_2[column].astype(int)
                df_2['Usofut1'] = ''
                df_2['Usofut2'] = ''
                df_2['Usofut3'] = ''
                df_2['Usofut4'] = ''
                print(FINALIZACION_SEGUNDO_QUERY)
                guardar(df_2, 'CVHTNAL_INELIBRANL' + '_' + str(date))
                cnx_nac.close()
            elif opcion == '3':
                print('Iniciando procesamiento...')
                sql_1 = f'''SELECT TJNRODOC AS DOCIDEN, TJCODOFC, CHTFNC, CHTMTV, CHTCPR, CHTFPR, CHTFHT, CHTCTA, RIGHT(CHTTAR,4) AS CHTTAR, CHTVME, CHTCOP,CHTTRM,
                CHTAUT, SUBSTRING(CHTICT,11,4)AS CHTICT, CHTDES FROM TMNLIBRANL.TMNFFCVHTI LEFT JOIN CABLIBRAMD.CABFFTARJ ON TJNROTRJ = RIGHT(CHTTAR,10) WHERE
                CHTCPR NOT IN ('203000', '090000', '183000') AND CHTTIP IN ('1','7') AND (TJNROBCO IN ('807') OR TJNROBCO IS NULL) AND CHTFPR ='{date}' ''' 
                sql_2 = f'''SELECT TJNRODOC AS DOCIDEN, DTPSDT, DTDATE, DTTAPC, DTBRCH, DTACCT, DTTXCD, SUBSTRING(DTDES2,13,4) AS DTDES2, 
                CAST(SUBSTRING(DTDES2,31,15) AS DECIMAL(15,2))/100 AS DTDES2, DTAMT, DTDBCR, SUBSTRING(DTDES2,17,6) AS DTDES2, DTDES1, DTDES2 FROM 
                BVDLIBT.DTRNP{str(date)[-4:]} LEFT JOIN CABLIBRAMD.CABFFTARJ ON TJNROTRJ = SUBSTRING(DTDES2,7,10) WHERE DTGLTC IN(309,536) AND DTUPST IN 
                (' ', 'C') AND (TJNROBCO IN ('807') OR TJNROBCO IS NULL)'''
                sql_3 = f'''SELECT TJNRODOC AS DOCIDEN, HDPAPLICAD, HDPFECHAUD, HDPFECTRX, HDPFECAPL, HDPTIPCTA, HDPNROCTA, HDPCODTRN, 
                RIGHT(LEFT(HDPNOMEMP,16),4) AS HDPNOMEMP, HDPVLRTRX, HDPVLRAPL, HDPDESRESP, HDPFILLER2 FROM TCBLIBRAMD.TCBFFMDEHI LEFT JOIN CABLIBRAMD.CABFFTARJ
                ON TJNROTRJ = RIGHT(LEFT(HDPNOMEMP,16),10) WHERE HDPAPLICAD IN ('X','E') AND HDPFECHAUD ='{date}' AND (TJNROBCO IN ('807') OR TJNROBCO IS NULL)'''
                print('Ejecutando primer query...(TMNFFCVHTI)')
                df_1 = pd.read_sql(sql_1, cnx_nac)
                print(FINALIZACION_PRIMER_QUERY)
                guardar(df_1, 'TMNFFCVHTI' + '_' + str(date))
                print('Ejecutando segundo query...(DTRNP0629)')
                df_2 = pd.read_sql(sql_2, cnx_nac)
                print(FINALIZACION_SEGUNDO_QUERY)
                guardar(df_2, 'DTRNP0629' + '_' + str(date))
                print('Ejecutando tercer query...(TCBFFMDEHI)')
                df_3 = pd.read_sql(sql_3, cnx_nac)
                print(FINALIZACION_TERCER_QUERY)
                guardar(df_3, 'TCBFFMDEHI' + '_' + str(date))
            elif opcion == '4':
                print(INICIANDO_PROCESAMIENTO)
                sql_1 = f'''SELECT MNITPAG, MFECTRN, AMED1_004, RIGHT(MCTAORI,4) AS MCTAORI, MVLRMVT, MNOMCON FROM RECLIBRAMD.RECFFMVTOS LEFT JOIN 
                TDCLIBRAMD.TDCFFAMED1 ON TRIM(L '0' FROM AMED1_002) = TRIM(L '0' FROM MCTAORI) WHERE AMED1_001 = 807 AND MTCTORI IN ('2', '3', '4') AND 
                MVLRMVT > 0 AND MTIPSER = '02' AND MFECTRN = '{date}' '''
                sql_2 = f''' SELECT ATPT1_001, AMNA1_017, ATPT1_006, ATPT1_013, ATPT1_002, RIGHT(ATPT1_026,4) AS ATPT1_026, ATPT1_011, ATPT1_007, ATPT1_009, 
                ATPT1_016, ATPT1_014, ATPT1_030, ATPT1_018 FROM TDCLIBRAMD.TDCFFATPT1 LEFT JOIN TDCLIBRAMD.TDCFFAMBS2 ON ATPT1_002 = AMBS2_002 AND 
                ATPT1_001 = AMBS2_001 LEFT JOIN TDCLIBRAMD.TDCFFAMNA1 ON AMBS2_005 = AMNA1_002 WHERE ATPT1_009 IN  ('8094','8320','8324','8005') AND
                ATPT1_001 = 807 AND ATPT1_025 = 0 AND ATPT1_003 = 0 AND ATPT1_013 = '{date}' ''' 
                sql_3 = f''' SELECT AMNA1_017, CONROCUENT, COFECHAPOS, COTIPO, COCTACONTB, COCTACTBCR, COVLRORIGI, COMONEDA, COORG, COLOGO, COSIORG, COLOCALCCI,
                COPLAN, CONROCUENT COCODIGOTR, CODESCRIPC, COVALORPES FROM TDCLIBRAMD.TDCFFCONTH LEFT JOIN TDCLIBRAMD.TDCFFAMBS2 ON CONROCUENT = AMBS2_002 
                AND COORG =AMBS2_001 LEFT JOIN TDCLIBRAMD.TDCFFAMNA1 ON AMBS2_005 = AMNA1_002 WHERE COCTACONTB = '1990959176' AND COFECHAPOS = '{date}' AND 
                COCODIGOTR IN ('7004','7104') '''
                print('Ejecutando primer query...(RECFFMVTOS)')
                df_1 = pd.read_sql(sql_1, cnx_nac)
                print(FINALIZACION_PRIMER_QUERY)
                guardar(df_1, 'RECFFMVTOS' + '_' + str(date))
                print('Ejecutando segundo query...(TDCFFATPT1)')
                df_2 = pd.read_sql(sql_2, cnx_nac)
                print(FINALIZACION_SEGUNDO_QUERY)
                guardar(df_2, 'TDCFFATPT1' + '_' + str(date))
                print('Ejecutando tercer query...(TDCFFCONTH)')
                df_3 = pd.read_sql(sql_3, cnx_nac)
                print(FINALIZACION_TERCER_QUERY)
                guardar(df_3, 'TDCFFCONTH' + '_' + str(date))
            elif opcion == '5':
                print(INICIANDO_PROCESAMIENTO)
            elif opcion == '6':
                print(INICIANDO_PROCESAMIENTO)
            elif opcion == '7':
                print(INICIANDO_PROCESAMIENTO)
        print('Proceso finalizado exitosamente, revisar carpeta salidas...')
        opcion = menu()
        inicio(opcion)
    else:
        print('Opcion introducida no es correcta...')
        opcion = menu()
        inicio(opcion)
def menu():
    """    menu muestra el menú del aplicativo    Returns    -------    int        número de la opción seleccionada    """    texto_menu = '''        Menu            1 : Cta 2990059102            2 : Cta 2990059067            3 : Cta 2105059117            4 : Cta 1960959176            8 : Salir        '''    print(texto_menu)
    opcion = input('Digitar la opcion a procesar: ')
    return opcionif __name__ == '__main__':
    option = menu()
    inicio(option)