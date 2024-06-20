from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from model import Response, Code
import os

constructors_agent = ""

user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://localhost:8000/submit"],
)

fund_agent_if_low(user.wallet.address())

@user.on_event('startup')
async def agent_address(ctx: Context):
    ctx.logger.info(user.address)

@user.on_interval(period=30, messages=Code)
async def interval(ctx: Context):
    constructors_year = str(input('Please enter the year you want the F1 constructors champion for: '))
    await ctx.send(constructors_agent, Code(code = constructors_year))

@user.on_message(Response)
async def handle_query_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(msg.response)
