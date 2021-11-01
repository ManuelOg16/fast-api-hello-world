#Respetar este orden importacion para tener el codigo d forma limpia
#Python importo cosas de esta libreria la cual esta por encima de Pydantic
from typing import Optional # Con optional puedo hacer tipado estatico

#Pydantic importamos cosas de esta libreria por que este orden por que Pydantic es una libreria que esta por debajo de FastAPI
from pydantic import BaseModel #Con BaseModel voy a poder crear modelos dentro de mi API


#FastAPI  importamos todo lo que necesitamos de FastAPI
from fastapi import FastAPI #la clase FastApi viene del modulo fastapi , y es la clase la que permite que todo el framework funcione
from fastapi import Body  #Body es una clase de fastAPI que a mi me permite decir explisitamente que un parametro que a mi me esta llegando es de tipo Body

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
#path operation

#Por el momento vamos a crear aqui los modelos necesarios para nuestra aplicacion
#Models
class Person(BaseModel): #Clase persona el nombre del modelo que llamaremos con la pathoperation de abajo, esta clase debe heredar de BaseModel
    first_name: str           #para definir un modelo segun pydantic vamos a colocar primero las caracteristicas los atributos de este modelo de esta entidad
    last_name: str
    age: int
    hair_color: Optional[str]= None    #esto e sun valor opcional pero debe tener un valor por defecto por si la persona no me envia nada tiene que haber algo dentro de hair_color normalmente con dbs es null en python es None esto quiere decir que puede haber algo o no
    is_married: Optional[bool] = None
#A nosotros de la persona nos interesa los primeros tres
#los ultimo dos pueden ser opcionales por eso importamos Optional de Python

#######################################
@app.get("/") #path operation decorator .. etsamos usando la operation get en el path / es decir el metodo HTTP get en el endpoint /
def home():  #el primer lugar que un usuario de nuestra API va aparecer cuando entre a la misma   #path operation function
    return {"Hello":"World"}   #cuando entremos al home vamos a retornar un json  y en python es un diccionario

#vamos a iniciar nuestra aplicacion nuestra API como se hace con uvicorn
# uvicorn main:app --reload
#http://localhost:8000/docs
#main= que es el nombre del archivo
#app=la variable que contiene el objeto que contiene nuetra aplicacion
# --reload = un modificador en el comando que es esto es cuando modificquemos algo en el codigo solo abremos el navegador y vemos el cambio 

##########################################

#Del video Request and Response Body
#vamos a crear personas con sus datos
@app.post("/person/new")      #vamos a enviar datos desde el cliente al servidor POST , si estuvieramos trayendo datos del servidor al cliente utilizariamos GET
def create_person(person: Person = Body(...)): #el constructor de esta clase Body lleva una serie de parametros el primero es el ... significa que este Request Body es obligatorio esto significa que un parametro es obligatorio o q un atributo es obligatorio
    return person  #retornamos al parametro person

#no he recibido por parte del cliente a la persona de mi modelo entonces como yo recibo esa informacion con un Request Body
#Un Request Body tambien es un parametro que si no se colcoa en la URL, se coloca en la definicion de la funcion asi (person: Person) vamos a enviar una persona que es de tipo Person 

#Analicemos desde la route path operation, tengo la path operation decorator que me dice que el cliente a traves de una peticion tipo POST es decir usando una operaciond e tipo POST accediendo a este path ("/person/new") 
#va a obtener una persona, una persona que esta sujeta al modelo de arriba, y esta persona va ser enviada al servidor por que es una peticion de tipo POST para por ejemplo guardarla en una base de datos por que estamos creando una nueva persona
#como yo se que esta persona es un Request Body por que aqui (person: Person = Body(...)) estoy colocando el nombre del parametro : el tipo por el tipado estatico a Body que es obligatorio 