from litestar import Router
from src.api.endpoints.users import UsersController


router = Router(
    path="/api",
    route_handlers=[UsersController]
)