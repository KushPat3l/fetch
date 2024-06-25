import requests
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Model, Context, Protocol
from pydantic import Field

YouTube_ChannelRequest_Agent = Agent()

class YouTubeRequest(Model):
    channel_id : str
    response: str
    details: str

YouTube_protocol = Protocol('YouTube details protocol')

@YouTube_protocol.on_message(model=YouTubeRequest, replies=UAgentResponse)
async def on_youtube_request(ctx: Context, sender: str, msg: YouTubeRequest):
    ctx.logger.info(f"Received YouTube Request from {sender} with Channel ID: {msg.channel_id} and details: {msg.details}")
    ctx.logger.info(msg.response)
    message = msg.response
    await ctx.send(sender, UAgentResponse(message=str(message), type=UAgentResponseType.FINAL))

YouTube_ChannelRequest_Agent.include(YouTube_protocol)

YouTube_ChannelRequest_Agent.run()
