from fastapi import FastAPI
from services.insights.router import router as insights_router
app=FastAPI(title='PowerX Insights')
app.include_router(insights_router,prefix='/v1/insights')
@app.get('/health')
def health(): return {'status':'ok'}