from fastapi import FastAPI

app = FastAPI(
    title="Circuito API",
    description="API para gerenciar equipes, pilotos, corridas e resultados de F1.",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health_check():
    # so confirma que a api ta no ar
    return {"status": "ok"}