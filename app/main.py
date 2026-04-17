from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import Base, engine

from app.routers.portfolio import portfolio_router
from app.routers.transactions import trans_router
from app.routers.stocks import stock_router
from app.routers.user import user_router

app = FastAPI()

app.include_router(portfolio_router)
app.include_router(trans_router)
app.include_router(stock_router)
app.include_router(user_router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# creating tables in sqlite/postgres db
Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={}
    )

@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@app.get("/register", response_class=HTMLResponse, include_in_schema=False)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


