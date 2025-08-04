# Import tất cả các router ở đây
from .auth_route import router as auth_router
from .home_route import router as home_router
from .category_route import router as category_router
from .search_route import router as search_router

# Nếu có nhiều router, import thêm ở đây

# Tạo danh sách routers để dễ include vào main
all_routers = [auth_router,home_router,category_router,search_router]
