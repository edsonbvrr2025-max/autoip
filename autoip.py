# -*- coding: utf-8 -*-
import time
import os
import subprocess
import sys
import requests

def install_deps():
    try:
        import requests
    except:
        os.system('pip3 install requests requests[socks] --break-system-packages')
        import requests
    print('\033[1;92m[+] Dependências OK\033[0m')

def start_tor():
    """Inicia Tor SEM abrir janelas extras"""
    os.system('pkill tor || true')
    time.sleep(1)
    # Tor em foreground no subprocess (sem daemon)
    tor_process = subprocess.Popen(['tor'], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
    time.sleep(4)
    return tor_process

def kill_tor(tor_process):
    """Para Tor limpo"""
    try:
        tor_process.terminate()
        os.system('pkill -9 tor || true')
    except:
        pass

def get_ip():
    """Pega IP com fallback"""
    services = [
        'http://checkip.amazonaws.com',
        'https://httpbin.org/ip',
        'http://icanhazip.com'
    ]
    
    for url in services:
        try:
            r = requests.get(url, 
                           proxies={'http': 'socks5://127.0.0.1:9050', 
                                   'https': 'socks5://127.0.0.1:9050'},
                           timeout=5)
            if r.status_code == 200:
                ip = r.text.strip()
                if ip.replace('.', '').replace('\n', '').isdigit():
                    return ip
        except:
            continue
    return "Falha-IP"

def force_ip_change():
    """Força troca de IP - MÉTODO SIMPLES E RÁPIDO"""
    print('\033[1;93m[*] 🔄 Trocando IP...\033[0m', end='')
    os.system('pkill tor || true')
    time.sleep(1)
    subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)  # Tempo para novo circuito
    print('\033[1;92m OK\033[0m')

def main():
    os.system('clear')
    
    # Logo
    logo = [
    "              _         _____ _____ ",
    "     /\\       | |       |_   _|  __ \\\\",
    "    /  \\  _ __| |_ ___    | | | |__) |",
    "   / /\\ \\| '__| __/ _ \\   | | |  ___/ ",
    "  / ____ \\ |  | || (_) | _| |_| |     ",
    " /_/    \\_\\_|   \\__\\___/ |_____|_|    ",
    "               A U T O   I P          ",
    "                  V 2.4 ⚡             "
    ]
    
    for line in logo:
        print(f"\033[1;93m{line}\033[0m")
    
    print("\033[1;32m✨ Sem plugins | Sem travamentos | IP real\033[0m\n")
    
    # Inicia Tor
    tor_proc = start_tor()
    print(f"\033[1;92m[+] Tor ativo | IP inicial: \033[1;93m{get_ip()}\033[0m\n")
    
    # Inputs
    while True:
        try:
            interval = int(input("\033[1;92m⏱️  Intervalo (segundos): \033[0m"))
            if interval < 3: interval = 3
            break
        except: print("\033[1;91m[!] Número válido!\033[0m")
    
    while True:
        try:
            count = int(input("\033[1;92m🔄 Nº trocas (0=infinito): \033[0m"))
            break
        except: print("\033[1;91m[!] Número válido!\033[0m")
    
    print(f"\n\033[1;92m🚀 Iniciado! Intervalo: {interval}s\033[0m\n")
    
    if count == 0:
        print("\033[1;93m[*] Modo INFINITO (Ctrl+C para parar)\033[0m\n")
        try:
            while True:
                old_ip = get_ip()
                force_ip_change()
                new_ip = get_ip()
                print(f"\033[1;92m📍 {old_ip} → \033[1;93m{new_ip}\033[0m")
                print("-" * 45)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\033[1;92m🛑 Parado pelo usuário\033[0m")
    else:
        for i in range(count):
            print(f"\033[1;94m[{i+1}/{count}]\033[0m", end=" ")
            old_ip = get_ip()
            force_ip_change()
            new_ip = get_ip()
            print(f"\033[1;92m📍 {old_ip} → \033[1;93m{new_ip}\033[0m")
            if i < count-1: time.sleep(interval)
        print("\n\033[1;92m✅ Completo!\033[0m")
    
    kill_tor(tor_proc)
    print("\033[1;92m✨ Tor finalizado limpo\033[0m")

if __name__ == "__main__":
    install_deps()
    main()
