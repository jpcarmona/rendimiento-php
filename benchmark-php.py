#-*- coding: utf-8 -*-

import os
import time
import subprocess

# Configuración
# Se van a realizar pruebas de rendimiento con la siguiente lista de peticiones concurrentes
CONN =[1,10,25,50,75,100]
TITULO='Apache2 php-mod'
# Tiempo de la prueba
DURATION='10'
IP='www.juanpe-wordpress.org'
# Las url no tienen que tener / al principio
URLS=['','?p=1','?p=6','?m=201902','?s=prueba']
# Servidores que se tienen que reiniciar
SERVERS=['apache2']

##############################################################################################################
resultados=[]

for con in CONN:

    for server in SERVERS:
        time.sleep(2)
        print('Reiniciando {}...'.format(server))
        reinicio=subprocess.run(['systemctl','restart','apache2'])
        if reinicio.returncode==0:
            print(server+' reiniciado con éxito')
        else:
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

# Mostrar resultados para generar gráfico
print('\n'+TITULO'\n')
print('\nConexiones:\n')
for con in CONN:
    print(con)
print('\nResultados: #/seg\n')
for lista in resultados:
    print(int(sum(lista)/len(lista)))


