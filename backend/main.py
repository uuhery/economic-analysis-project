from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import estimation, finance, risk, scheduling

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
app.include_router(finance.router)
app.include_router(estimation.router)
app.include_router(risk.router)
app.include_router(scheduling.router)
