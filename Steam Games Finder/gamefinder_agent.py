import requests
from uagents import Agent, Model, Context, Protocol
from uagents.setup import fund_agent_if_low
from model import Response, Code
import os

gamefinder_agent = Agent(
    name='gamefinder_data_agent',
    port=1123,
    seed="Constructors Data Agent Secret Seed Phrase",
    endpoint="http://localhost:1123/submit",
)

fund_agent_if_low(gamefinder_agent.wallet.address())

@gamefinder_agent.on_event('startup')
async def address(ctx: Context):
    ctx.logger.info(gamefinder_agent.address)

MAX_RESULTS = 5

async def get_games_by_name(name):
    search_url = "https://steam-api7.p.rapidapi.com/search"
    search_querystring = {"query": name, "limit": MAX_RESULTS}
    headers = {
        "x-rapidapi-key" : "",
        "x-rapidapi-host" : "steam-api7.p.rapidapi.com"
    }

    search_response = requests.get(search_url, headers=headers, params=search_querystring)
    if search_response.status_code == 200 and search_response.json():
        games = search_response.json()
        games5 = [result['name'] for result in games['results']]
        games5_string = ', '.join(games5)
        return games5_string
    else:
        return f"Failed to retrieve games named similar to {name}"
    
@gamefinder_agent.on_message(model=Code, replies=Response)
async def game_names(ctx: Context, sender:str, msg: Code):
    name = msg.code
    gamesearch = await get_games_by_name(name)
    await ctx.send(sender, Response(response=gamesearch))
