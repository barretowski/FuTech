from fastapi import FastAPI, HTTPException, Query
import httpx
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

app = FastAPI(title="API Futebol")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    "x-apisports-key": API_KEY
}
BASE_URL = "https://v3.football.api-sports.io"

@app.get("/ligas")
async def listar_ligas():
    ligas = [
        {"id": 71, "nome": "Brasileirão Série A"},
        {"id": 2, "nome": "Premier League"},
        {"id": 3, "nome": "La Liga"},
    ]
    return ligas

@app.get("/jogador")
async def buscar_estatisticas(
    jogador: str = Query(..., description="Nome do jogador para busca"),
    temporada: int = Query(2023, description="Temporada"),
    liga: int = Query(71, description="ID da liga")
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/players",
            params={"search": jogador, "season": temporada, "league": liga},
            headers=HEADERS
        )
        data = response.json()

    if not data["response"]:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")

    info = data["response"][0]
    estatisticas = info["statistics"][0]
    partidas = estatisticas["games"]["appearences"] or 1  # evitar divisão por zero

    return {
        "jogador": info["player"]["name"],
        "time": estatisticas["team"]["name"],
        "campeonato": estatisticas["league"]["name"],
        "temporada": estatisticas["league"]["season"],
        "media_faltas": estatisticas["fouls"]["committed"] / partidas,
        "media_desarmes": estatisticas["tackles"]["total"] / partidas,
        "media_chutes": estatisticas["shots"]["total"] / partidas,
    }
