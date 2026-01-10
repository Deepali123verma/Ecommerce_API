from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from routers import users, products, orders, order_items

# ------------------- Initialize FastAPI App -------------------
app = FastAPI(
    title="E-Commerce Backend API",
    version="1.0.0",
    description="A FastAPI-based E-Commerce backend with CRUD operations and JWT Authentication."
)

# ------------------- Include Routers -------------------
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(order_items.router)

# ------------------- Root Endpoint -------------------
@app.get("/")
@app.head("/")
def root():
    return {"message": "Welcome to the E-Commerce API!"}

# ------------------- Swagger Authorize Button -------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"]:
        if path not in ["/auth/token", "/users/register"]:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [
                    {"BearerAuth": []}
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

