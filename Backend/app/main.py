from fastapi import FastAPI
#from app.api.master_routes import router as master_router
#from app.api.outreach_routes import router as outreach_router
#from app.api.exam_routes import router as exam_router
from app.api.dashboard_routes import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Dashboard")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.include_router(master_router)
#app.include_router(outreach_router)
#app.include_router(exam_router)
app.include_router(dashboard_router)

@app.get("/health")
def health():
    return {"status": "ok"}
