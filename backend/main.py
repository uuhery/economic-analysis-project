from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.finance import router as finance_router
from api.estimation import router as estimation_router

app = FastAPI(title="Economic Analysis API")

# 允许跨域（前端请求用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(finance_router, prefix="/api/finance")
app.include_router(estimation_router, prefix="/api/estimate")
