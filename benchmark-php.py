#-*- coding: utf-8 -*-

import time, subprocess
from subprocess import DEVNULL

## Configuración dinámica
TITULO='Apache2 php-mod'
# Servidores que se tienen que reiniciar
SERVERS=['apache2']
##

## Configuración estática
# Se van a realizar pruebas de rendimiento con la siguiente lista de peticiones concurrentes
CONN =[1,10,25,50,75,100]
# Tiempo de la prueba
DURATION='10'
IP='www.juanpe-wordpress.org'
# Las url no tienen que tener / al principio
URLS=['','?p=1','?p=6','?m=201902','?s=prueba']
ab_check=False
apache2_check=True
root_check=True
##

##############################################################################################################
resultados=[]

## Comprobar que estan instalados los paquetes necesarios
def check_install(paquete):
    print('\nComprobar estado de '+paquete+':')
    try:
        subprocess.run(['dpkg','-s',paquete],stderr=DEVNULL,stdout=DEVNULL,check=True)
        print('\tInstalada\n')
    except subprocess.CalledProcessError:
        print('\tNo instalada\n')
        print('Instalación:\tapt -y install '+paquete+'\n')
        exit()

if ab_check:
    check_install('apach2-utils')

if apache2_check:
    check_install('apache2')

##

## Comprobar si se ejecuta como root
def check_root():
    user=subprocess.getoutput('whoami')
    if user!='root':
        exit()

if root_check:
    check_root()

##

## Programa principal
for con in CONN:

    for server in SERVERS:
        time.sleep(2)
        print('Reiniciando {}...'.format(server))
        try:
            subprocess.run(['systemctl','restart','apache2'],stderr=DEVNULL,stdout=DEVNULL,check=True)
            print(server+' reiniciado con éxito')
        except subprocess.CalledProcessError:
            print('Error al reiniciar '+server)

    lcon=[]
    print('Conexiones concurrentes: {}'.format(con))

    for url in URLS:
        print('URL: http://{}/{}'.format(IP,url))
        res=subprocess.getoutput('ab -t {} -k -c {} http://{}/{}'.format(DURATION,con,IP,url))
        # Recoger resultado "#/sec"
        try:
            reslista=' '.join(res.split()).split(' ')
            indice=reslista.index('[#/sec]')-1
            respuesta=reslista[indice]
            lcon.append(float(respuesta))
            print(respuesta+' #/seg')
        except:
            print('Error en el resultado')
            pass

    resultados.append(lcon)
    # Tiempo para que se terminen de hacer las pruebas 
    time.sleep(1)
##

## Mostrar resultados para generar gráfico
print('\n'+TITULO+'\n')
print('\nConexiones:\n')
for con in CONN:
    print(con)
print('\nResultados: #/seg\n')
for lista in resultados:
    print(int(sum(lista)/len(lista)))
##