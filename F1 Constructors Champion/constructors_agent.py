import requests
from uagents import Agent, Model, Context, Protocol
from uagents.setup import fund_agent_if_low
from model import Response, Code
import os

constructors_agent = Agent(
    name='constructors_data_agent',
    port=1123,
    seed="Constructors Data Agent Secret Seed Phrase",
    endpoint="http://localhost:1123/submit",
)

fund_agent_if_low(constructors_agent.wallet.address())

@constructors_agent.on_event('startup')
async def address(ctx: Context):
    ctx.logger.info(constructors_agent.address)

async def get_constructors_table_by_year(year):
    search_url = "https://f1-motorsport-data.p.rapidapi.com/standings-controllers"
    search_querystring = {"year": year}
    headers = {
        "x-rapidapi-key" : "",
        "x-rapidapi-host" : "f1-motorsport-data.p.rapidapi.com"
    }

    search_response = requests.get(search_url, headers=headers, params=search_querystring)
    if search_response.status_code == 200 and search_response.json():
        leader = search_response.json()['standings']['entries'][0]['team']['displayName']
        return leader
    else:
        return f"Failed to retrieve constructors leader for {year}"
    
@constructors_agent.on_message(model=Code, replies=Response)
async def constructors_details(ctx: Context, sender:str, msg: Code):
    year = msg.code
    construction = await get_constructors_table_by_year(year)
    await ctx.send(sender, Response(response=construction))

