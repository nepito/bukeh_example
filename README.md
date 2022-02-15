# bukeh_example

Para correr esto debes construir la imagen:
- ` docker build -t nepito-bukeh .` 

Llamé `nepito-bukeh` para que vean que no tengo nada bajo la manga.

Ahora podemos corremos las instrucción `make run` en un nuevo contenedor. El contenedor funcionará en _background_ y expondremos el puerto 3535 del contenedor al 3535 de mi computadora:
- ` docker run -d -p 3535:3535 nepito-bukeh make run`.

- Finalmente, abrimos el http://localhost:3535/.


## Utilizando `make`

Desde tu máquina local contruye la imagen:
`make build`
y después echa a andar la aplicación:
`make up`
Ahora abre el http://localhost:3535/