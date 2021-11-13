#Respetar este orden importacion para tener el codigo d forma limpia
#Python importo cosas de esta libreria la cual esta por encima de Pydantic
from typing import Optional # Con optional puedo hacer tipado estatico
from enum import Enum   # nos sirve para crear enumeraciones de strings nos va servir para poder definir perfectamente la validación del atributo hair

#Pydantic importamos cosas de esta libreria por que este orden por que Pydantic es una libreria que esta por debajo de FastAPI
from pydantic import BaseModel #Con BaseModel voy a poder crear modelos dentro de mi API
from pydantic import Field
from pydantic import EmailStr

#FastAPI  importamos todo lo que necesitamos de FastAPI
from fastapi import FastAPI #la clase FastApi viene del modulo fastapi , y es la clase la que permite que todo el framework funcione
from fastapi import Body  #Body es una clase de fastAPI que a mi me permite decir explisitamente que un parametro que a mi me esta llegando es de tipo Body
from fastapi import Query
from fastapi import Path
from fastapi import status #este nos permite acceder a diferentes status code de HTTP
from fastapi import Form
from fastapi import Header, Cookie




app= FastAPI() 

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
class PersonBase(BaseModel):
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

class Person(PersonBase): #Clase persona el nombre del modelo que llamaremos con la pathoperation de abajo, esta clase debe heredar de BaseModel
    password: str = Field(
    ...,
    min_length=8
    )

class PersonOut(PersonBase):
    pass
     
class Location(BaseModel): #Definimos el modelo Location para pedirle al cliente en la path opetaion del put que nos envie dos Request Body
    city: str
    state: str
    country: str

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguel2021")
    message: str = Field(default="Login Succesfully!")

#######################################
@app.get(
    path="/",  #puedo poner path, que es tambien el endpoint la ruta
    status_code=status.HTTP_200_OK
    ) #path operation decorator .. etsamos usando la operation get en el path / es decir el metodo HTTP get en el endpoint /
def home():  #el primer lugar que un usuario de nuestra API va aparecer cuando entre a la misma   #path operation function
    return {"Hello":"World"}   #cuando entremos al home vamos a retornar un json  y en python es un diccionario


##########################################

#Del video Request and Response Body
#vamos a crear personas con sus datos
@app.post(
    path="/person/new",         #este enpoint es para crear una persona por eso 201
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED  
    ) #con el response_model=PersonOut vamos a devolder todo menos la contraseña xq la borramos en la clase  PersonOut    #vamos a enviar datos desde el cliente al servidor POST , si estuvieramos trayendo datos del servidor al cliente utilizariamos GET
def create_person(person: Person = Body(...)): #el constructor de esta clase Body lleva una serie de parametros el primero es el ... significa que este Request Body es obligatorio esto significa que un parametro es obligatorio o q un atributo es obligatorio
    return person  #retornamos al parametro person


#Validaciones: Query Parameters
@app.get(
    path="/person/detail",    #estamos obteniendo un resultado y si todo sale bien necesitamos un 200
    status_code=status.HTTP_200_OK
    )
def show_person(
    name : Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50, #por buenas practicas si tenemos varios querys parameters ordenamos asi con los saltos de linea
        title= "Person Name", #para definir un titulo en la documentación automatica    IMPORTANTE EN SWAGGER IA no aparece el titulo pero es por swagger en redocs si aparece
        description= "This is the person name. It's between 1 and 50 characters",  #Definimos una descripción para que quede mas claro para el usuario de nuestra API
        example="Rocío" #path y query parametrs automaticos
        ),    #los query parameters son opcionales llamamos la clase Query y el default es None por que no nos podria llegar nada pero si la persona llegase a mandar algo a escribir algo ya sabemos que el min_length=1, max_length=50
    age: str = Query(
        ...,
        title= "Person Age",
        description= "This is the person age. It's required",
        example=25  #path y query parametrs automaticos documentacion
        ) # pero aqui le vamos a poner que debe ser obligatorio por alguna razon , esto no e slo ideal pero podria pasar, ademas lo obligatorios deben ser un path parameter no un query parameter pero podria llegar a pasar
): # vamos a necesitar dos query parameters y los pongo en los parametros de la definicion de la funcion
    return {name: age} # retornamos un json con las dos variables


@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
    ..., 
    gt=0,
    example=21 #path y query parametrs automaticos documentacion
    ) 
):
    return{person_id: "It exists!"} #respondemos un json con esta estructura

#Validaciones: Request Body 

@app.put(
    path="/person/{person_id}",
    response_model=PersonOut,
    status_code=status.HTTP_200_OK)     #para actualizar un determinado contenido en nuestra aplicación, cada vez que un usuario haga una peticionde tipo put a este endpoint ("/person/{person_id}") y un id en particular vamos a poder actualizar un contenido de esa persona , el cliente  le va tener que enviar a la API un Request Body
def update_person(
    person_id: int = Path(
        ...,
        title= "Person ID",
        description= "This is the person ID",
        gt=0,   #le colocamos que este id debe ser mayor a cero
        example=21   #path y query parametrs automaticos documentacion
    ), 
    person: Person = Body(...),  #ademas estamos recibiento en esta path operatoon en espeacial un Request Body y le debo poner un nombre person me va enviar la información de la persona
    # Location: Location = Body(...)  #pero que pasa si tambien le pedimos al cliente ptro parametro como location
):     
    results = person.dict()                 # para este caso cuandoq queremos combinar dos json debemos hacerlo de manera explicita con person.dict() convertimos el Request body person que viene como json convertido  en un diccionario
    # results.update(Location.dict())  # aqui estamos combinando el diccionarion person con el diccionario location en una sola variable
    return results         # convertir primero person a diccionario y con el metodo update de este diccionario unir otro diccionario

#Forms
@app.post(
    path="/login",           #creamos el endpoint
    response_model=LoginOut,  #esta va ser la respuesta que le vamos a dar al usuario
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)): #vamos a recibir dos parametros que van a venir desde un formulario que esta en el fronted, FORM nos sirve para indicar que un parametro dentro de una path operation function viene de un formulario 
    return LoginOut(username=username)

#Cookies and Headers Parameters
@app.post(
    path="/contact",  #un formulario de contacto en el endpoint
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
    ...,
    max_length=20,
    min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),  #el head que nos dice quien esta intentado usar esta API
    ads: Optional[str] = Cookie(default=None)       #va controlar las cookies que nos envia este servidor que tenemos que esta trabajando con la API
):
    return user_agent  #vamos a ver quien nos esta enviando este mensaje despues de haberlo enviado