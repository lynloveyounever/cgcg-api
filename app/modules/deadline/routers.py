from fastapi import APIRouter
# 1. 導入子 Router - 直接從模組導入，無需 __init__.py
from .rest.cruds import rest_router
from .tools.ai_tools import tools_router

# 2. 創建這個模組對外暴露的單一 Router 實例
# 我們可以使用一個通用的名稱，例如 module_router
module_router = APIRouter(prefix='/deadline')

# 3. 將內部的子 Router 掛載到這個單一實例上
# 📌 注意：可以在這裡為子 Router 添加子前綴或特定的 tags
module_router.include_router(
    rest_router,
    prefix="/rest",      # 讓所有人類 API 路徑都以 /rest 開頭
    tags=["Deadline REST API"]
)

module_router.include_router(
    tools_router,
    prefix="/tools",     # 讓所有 AI 工具路徑都以 /tools 開頭
    tags=["Deadline AI Tools"]
)

# 最終，這個文件只導出 module_router
__all__ = ["module_router"]