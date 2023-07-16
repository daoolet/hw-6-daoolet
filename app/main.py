from fastapi import Cookie, FastAPI, Form, Request, Response, templating
from fastapi.responses import RedirectResponse

from jose import jwt

from flowers_repository import Flower, FlowersRepository
from purchases_repository import Purchase, PurchasesRepository
from users_repository import User, UsersRepository

app = FastAPI()
templates = templating.Jinja2Templates("../templates")


flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ваше решение сюда

# --------------- SIGN UP

@app.get("/signup")
def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def post_sigup(
    request: Request,
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
):
    users_repository.save(
        User(email, full_name, password)
    )

    return RedirectResponse("/login", status_code = 303)


# --------------- LOGIN

def create_jwt(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "kek", "HS256")
    return token

def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "kek", "HS256")
    return data["user_id"]

@app.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def post_login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...)
):
    user = users_repository.get_by_email(email)
    if not user:
        return Response("Loggin Failed: Wrong email or password")
    
    if user.password == password:
        token = create_jwt(user.id)
        response.set_cookie("token", token)
        return RedirectResponse("/profile", status_code = 303)
 
    return Response("Loggin Failed: Wrong email or password")


# --------------- PROFILE

@app.get("/profile")
def get_profile(
    request: Request,
    token: str = Cookie()
):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(int(user_id))

    context = {
        "request": request,
        "user": user
    }

    return templates.TemplateResponse("profile.html", context)


# --------------- FLOWERS

@app.get("/flowers")
def get_flowers(request: Request):

    flowers = flowers_repository.get_all()

    context = {
        "request": request,
        "flowers": flowers
    }

    return templates.TemplateResponse("flowers.html",context)

@app.post("/flowers")
def post_flowers(
    request: Request,
    name: str = Form(...),
    count: int = Form(...),
    cost: int = Form(...),
):
    
    flowers_repository.save(
        Flower(name=name, count=count, cost=cost)
    )

    print(flowers_repository.get_all())

    return RedirectResponse("/flowers", status_code = 303)


# --------------- CART

@app.get("/cart/items")
def get_cart(request: Request):
     
    cart_flowers = flowers_repository.get_cart_flowers()
    total_cost = sum(i.cost for i in cart_flowers)

    context = {
        "request": request,
        "cart_flowers": cart_flowers,
        "total_cost": total_cost
        }
    
    return templates.TemplateResponse("cart.html", context)

@app.post("/cart/items")
def post_cart(
    request: Request,
    response: Response,
    flower_id: int = Form(...)
):
    
    current_flower = flowers_repository.get_by_id(flower_id)
    flowers_repository.add_cart_flowers(current_flower)

    response = RedirectResponse("/flowers", status_code = 303)
    response.set_cookie("flower_id", flower_id)

    return response


# конец решения
