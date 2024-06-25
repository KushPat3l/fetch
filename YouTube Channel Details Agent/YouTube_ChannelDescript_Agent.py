import requests
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Model, Context, Protocol
from pydantic import Field

YouTube_ChannelDescription_Agent = Agent()

class ChannelDescriptionRequest(Model):
    channel_id : str

channeldesc_protocol = Protocol("YouTube ChannelDescription Protocol")

async def chandesc_finder(channel_id):
    headers = {
        "x-rapidapi-key": "",
        "x-rapidapi-host": "youtube-data8.p.rapidapi.com"
        }
    url_subscribers = "https://youtube-data8.p.rapidapi.com/channel/details"
    querystring = {"id": channel_id}
    response_chandesc = requests.get(url_subscribers, headers=headers, params=querystring)
    data_chandesc = response_chandesc.json()
    chandesc_name = data_chandesc['description']
    return chandesc_name

@channeldesc_protocol.on_message(model=ChannelDescriptionRequest, replies=UAgentResponse)
async def on_subscriber_request(ctx: Context, sender: str, msg: ChannelDescriptionRequest):
    ctx.logger.info(f"Received Latest NumVideo Request with Channel ID: {msg.channel_id}")
    chandesc = await chandesc_finder(msg.channel_id)
    ctx.logger.info(chandesc)
    await ctx.send(sender, UAgentResponse(message=str(chandesc),type=UAgentResponseType.FINAL))

YouTube_ChannelDescription_Agent.include(channeldesc_protocol)

YouTube_ChannelDescription_Agent.run()

