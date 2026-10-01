@echo off
title Prueba Netcat UDP - UNSAAC Lab 02 Ejercicio 5.1
echo Enviando mensaje con Netcat al Servidor UDP (puerto 12000)...
echo hola servidor unsaac desde netcat | nc -u -w 2 127.0.0.1 12000
echo.
pause
