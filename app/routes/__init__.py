# Import tất cả các router ở đây
from .auth import router as auth_router
from .home import router as home_router

# Nếu có nhiều router, import thêm ở đây

# Tạo danh sách routers để dễ include vào main
all_routers = [auth_router,home_router]
