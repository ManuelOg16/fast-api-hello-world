#Respetar este orden importacion para tener el codigo d forma limpia
#Python importo cosas de esta libreria la cual esta por encima de Pydantic
from typing import Optional # Con optional puedo hacer tipado estatico
from enum import Enum # nos sirve para crear enumeraciones de strings nos va servir para poder definir perfectamente la validación del atributo hair
#Pydantic importamos cosas de esta libreria por que este orden por que Pydantic es una libreria que esta por debajo de FastAPI
from pydantic import BaseModel #Con BaseModel voy a poder crear modelos dentro de mi API
from pydantic import Field

#FastAPI  importamos todo lo que necesitamos de FastAPI
from fastapi import FastAPI #la clase FastApi viene del modulo fastapi , y es la clase la que permite que todo el framework funcione
from fastapi import Body  #Body es una clase de fastAPI que a mi me permite decir explisitamente que un parametro que a mi me esta llegando es de tipo Body
from fastapi import Query
from fastapi import Path

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
#al principio de los modelos aqui vamos a poner todos los modelos que vamos a crear
class  HairColor(Enum):  #Esta hereda de Enum
    white= "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"
# para poder usar esto y que el hair_color que nos envie el usuario si o si sea uno de estos y no otro 

class Person(BaseModel): #Clase persona el nombre del modelo que llamaremos con la pathoperation de abajo, esta clase debe heredar de BaseModel
    first_name: str = Field(    #para definir un modelo segun pydantic vamos a colocar primero las caracteristicas los atributos de este modelo de esta entidad
        ...,                     #Field es igual a un campo d enuestro modelo usando la clase Field
        min_length=1,
        max_length=50,
        example="Victor"
        )     # otra forma de llenar los datos automatizamente  
    last_name: str = Field( 
        ...,
        min_length=1,
        max_length=50,
        example="Ocampo") 
    age: int = Field(
       ...,
        gt=0,
        le=115,
        example=36
    )
    hair_color: Optional[HairColor]= Field(default=None) # antes estaba el str sin Field ahora ponemos la clase HairColor lo cual nos asegura que los valores deben ser lo que pusimos dentro de esta clase       #esto e sun valor opcional pero debe tener un valor por defecto por si la persona no me envia nada tiene que haber algo dentro de hair_color normalmente con dbs es null en python es None esto quiere decir que puede haber algo o no
    is_married: Optional[bool] = Field(default=None)
    #para uatomatizar los datos a la hora de probar la API una subclase dentro de la clase Person
    #esta e suna manera pero hay otra forma la de arriba con example
    # class Config:
    #     schema_extra = {   #este atributo nos sirve para definir la información por defecto para la documentación esto va ser igual a un json a un diccionario 
    #         "example": {   #se pone example por que si no no funciona
    #             "first_name": "Manuel",
    #             "last_name": "Ocampo Galvis",
    #             "age": 36, 
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }
#A nosotros de la persona nos interesa los primeros tres
#los ultimo dos pueden ser opcionales por eso importamos Optional de Python

class Location(BaseModel): #Definimos el modelo Location para pedirle al cliente en la path opetaion del put que nos envie dos Request Body
    city: str
    state: str
    country: str


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

#Validaciones: Query Parameters
@app.get("/person/detail")
def show_person(
    name : Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50, #por buenas practicas si tenemos varios querys parameters ordenamos asi con los saltos de linea
        title= "Person Name", #para definir un titulo en la documentación automatica    IMPORTANTE EN SWAGGER IA no aparece el titulo pero es por swagger en redocs si aparece
        description= "This is the person name. It's between 1 and 50 characters"  #Definimos una descripción para que quede mas claro para el usuario de nuestra API
        ),    #los query parameters son opcionales llamamos la clase Query y el default es None por que no nos podria llegar nada pero si la persona llegase a mandar algo a escribir algo ya sabemos que el min_length=1, max_length=50
    age: str = Query(
        ...,
        title= "Person Age",
        description= "This is the person age. It's required"
        ) # pero aqui le vamos a poner que debe ser obligatorio por alguna razon , esto no e slo ideal pero podria pasar, ademas lo obligatorios deben ser un path parameter no un query parameter pero podria llegar a pasar
): # vamos a necesitar dos query parameters y los pongo en los parametros de la definicion de la funcion
    return {name: age} # retornamos un json con las dos variables

#Validaciones: Path Parameters
#python lee el codigo de izquierda a derecha y de arriba hacia abajo y como fatsAPI esta funcionando sobre python vamos a tener el mismo caso
#si nosotros tenemos 2 endpoints 2 paths operations que se corresponden en el mismo path a la misma ruta la que va a valer es la ultima por que python va empezar a leer desde el principio se va encontrar con un path operation y si se llega encontrar con uno que tiene el mismo endpoint va tomar el ultimo que se encontro
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(..., gt=0)  # ser obligatorio, ademas definimos que no nos pasen un id= 0 u negativo usamos gt great >0
):
    return{person_id: "It exists!"} #respondemos un json con esta estructura

#Validaciones: Request Body 

@app.put("/person/{person_id}")     #para actualizar un determinado contenido en nuestra aplicación, cada vez que un usuario haga una peticionde tipo put a este endpoint ("/person/{person_id}") y un id en particular vamos a poder actualizar un contenido de esa persona , el cliente  le va tener que enviar a la API un Request Body
def update_person(
    person_id: int = Path(
        ...,
        title= "Person ID",
        description= "This is the person ID",
        gt=0   #le colocamos que este id debe ser mayor a cero
    ),
    person: Person = Body(...),  #ademas estamos recibiento en esta path operatoon en espeacial un Request Body y le debo poner un nombre person me va enviar la información de la persona
    # Location: Location = Body(...)  #pero que pasa si tambien le pedimos al cliente ptro parametro como location
):     
    results = person.dict()                 # para este caso cuandoq queremos combinar dos json debemos hacerlo de manera explicita con person.dict() convertimos el Request body person que viene como json convertido  en un diccionario
    results.update(Location.dict())  # aqui estamos combinando el diccionarion person con el diccionario location en una sola variable
    return results         # convertir primero person a diccionario y con el metodo update de este diccionario unir otro diccionario
    