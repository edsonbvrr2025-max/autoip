import os
choice = input('[+] para instalar pressione (Y) para desinstalar pressione (N)')
run = os.system
if str(choice) =='Y' or str(choice)=='y':

    run('chmod 777 autoip.py')
    run('mkdir /usr/share/aut')
    run('cp autoip.py /usr/share/aut/autoip.py')

    cmnd=(' #! /bin/sh \n exec python3 /usr/share/aut/autoip.py "$@"')
    with open('/usr/bin/aut','w')as file:
        file.write(cmnd)
    run('chmod +x /usr/bin/aut & chmod +x /usr/share/aut/autoip.py')
    print('''\n\nParabéns, o Auto IP foi instalado com sucesso. \na partir de agora basta digitar \x1b[6;30;42maut\x1b[python3 autoip.py no terminal ''')
if str(choice)=='N' or str(choice)=='n':
    run('rm -r /usr/share/aut ')
    run('rm /usr/bin/aut ')
    print('[!] O Auto Tor Ip changer foi removido com sucesso.')
