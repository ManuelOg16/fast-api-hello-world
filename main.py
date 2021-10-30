from fastapi import FastAPI #la clase FastApi viene del modulo fastapi , y es la clase la que permite que todo el framework funcione

#lo primero es definir una variable app que va contener toda mi aplicacion
#para inicializarla bien vamos a colocarle una instancia de la clase FastAPI
#como sabemos que esto es una instancia FastAPI por que ponemos los parentesis esto significa
#que lo que va a pasar en el fondo es que la clase FastAPI se va ejecutar y con el constructor
#se va crear un objeto de tipo FastAPI y se va guardar dentro de app
app= FastAPI() 

#para que este proyecto funcione hay que crear las paths operations decorator
#esto es un decorador por la @, va decorar una funcion creada posteriormente
#este decorador esta usando el metodo get que viene del objeto app que a su vez es una instancia  de FastAPI
#el metodo get es esa funcion que hace como decorador que va decorar la funcion que vamos a crear abajo que va controlar esta primera path operation que estamos creando
#entonces decimos que en (/) osea en el home de nuestra aplicacion se va ejecutar una funcion def home()
@app.get("/")
def home():  #el rpimer lugar que un usuario de nuestra API va aparecer cuando entre a la misma
    return {"Hello":"World"}   #cuando entremos al home vamos a retornar un json  y en python es un diccionario

#vamos a iniciar nuestra aplicacion nuestra API como se hace con uvicorn
# uvicorn main:app --reload
#main= que es el nombre del archivo
#app=la variable que contiene el objeto que contiene nuetra aplicacion
# --reload = un modificador en el comando que es esto es cuando modificquemos algo en el codigo solo abremos el navegador y vemos el cambio 