from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware



class Credentials(BaseModel):
    username: str
    password: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


LOGIN_URL = "https://login.iiit.ac.in/cas/login?service=https%3A%2F%2Fmess.iiit.ac.in%2Fmess%2Fweb%2Findex.php"


@app.post("/")
async def root(credentials: Credentials):
    login_soup = BeautifulSoup(requests.get(LOGIN_URL).content, "lxml")
    execution = login_soup.select_one('input[name="execution"]')["value"]
    payload = {"username": credentials.username, "password": credentials.password, "execution": execution,
               "_eventId": "submit", "geolocation": ""}

    session = requests.Session()
    result = session.post(LOGIN_URL, data=payload)
    result_soup = BeautifulSoup(result.content, "lxml")
    title = result_soup.select_one("title").contents
    print(title)
    if title and title[0] == 'Authentication Succeeded with Warnings - CAS – Central Authentication Service':
        execution = result_soup.select_one('input[name="execution"]')["value"]
        payload["execution"] = execution
        payload["_eventId"] = "proceed"
        result = session.post(LOGIN_URL, data=payload)
        result_soup = BeautifulSoup(result.content, "lxml")
        title = result_soup.select_one("title").contents
        print(title)
        print(session.cookies)

    return {"PHPSESSID": session.cookies.get("PHPSESSID"), "TGC": session.cookies.get("TGC")}
