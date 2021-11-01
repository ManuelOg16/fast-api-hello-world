#Respetar este orden importacion para tener el codigo d forma limpia
#Python importo cosas de esta libreria la cual esta por encima de Pydantic
from typing import Optional # Con optional puedo hacer tipado estatico

#Pydantic importamos cosas de esta libreria por que este orden por que Pydantic es una libreria que esta por debajo de FastAPI
from pydantic import BaseModel #Con BaseModel voy a poder crear modelos dentro de mi API


#FastAPI  importamos todo lo que necesitamos de FastAPI
from fastapi import FastAPI 
from fastapi import Body  #Body es una clase de fastAPI que a mi me permite decir explisitamente que un parametro que a mi me esta llegando es de tipo Body
from fastapi import Query

app= FastAPI() 


class Person(BaseModel): #Clase persona el nombre del modelo que llamaremos con la pathoperation de abajo, esta clase debe heredar de BaseModel
    first_name: str           #para definir un modelo segun pydantic vamos a colocar primero las caracteristicas los atributos de este modelo de esta entidad
    last_name: str
    age: int
    hair_color: Optional[str]= None    #esto e sun valor opcional pero debe tener un valor por defecto por si la persona no me envia nada tiene que haber algo dentro de hair_color normalmente con dbs es null en python es None esto quiere decir que puede haber algo o no
    is_married: Optional[bool] = None


#######################################
@app.get("/") #path operation decorator .. etsamos usando la operation get en el path / es decir el metodo HTTP get en el endpoint /
def home():  #el primer lugar que un usuario de nuestra API va aparecer cuando entre a la misma   #path operation function
    return {"Hello":"World"}   #cuando entremos al home vamos a retornar un json  y en python es un diccionario

#vamos a iniciar nuestra aplicacion nuestra API como se hace con uvicorn
# uvicorn main_v:app --reload
#http://localhost:8000/docs
#main= que es el nombre del archivo
#app=la variable que contiene el objeto que contiene nuetra aplicacion
# --reload = un modificador en el comando que es esto es cuando modificquemos algo en el codigo solo abremos el navegador y vemos el cambio 

##########################################


#vamos a crear personas con sus datos
@app.post("/person/new")      #vamos a enviar datos desde el cliente al servidor POST , si estuvieramos trayendo datos del servidor al cliente utilizariamos GET
def create_person(person: Person = Body(...)): #el constructor de esta clase Body lleva una serie de parametros el primero es el ... significa que este Request Body es obligatorio esto significa que un parametro es obligatorio o q un atributo es obligatorio
    return person  #retornamos al parametro person

#Validaciones: Query Parameters
@app.get("/person/detail")
def show_person(
    name : Optional[str] = Query(None, min_length=1, max_length=50),    #los query parameters son opcionales llamamos la clase Query y el default es None por que no nos podria llegar nada pero si la persona llegase a mandar algo a escribir algo ya sabemos que el min_length=1, max_length=50
    age: str = Query(...) # pero aqui le vamos a poner que debe ser obligatorio por alguna razon , esto no e slo ideal pero podria pasar, ademas lo obligatorios deben ser un path parameter no un query parameter pero podria llegar a pasar
): # vamos a necesitar dos query parameters y los pongo en los parametros de la definicion de la funcion
    return {name: age} # retornamos un json con las dos variables
