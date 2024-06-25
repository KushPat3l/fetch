import requests
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Model, Context, Protocol
from pydantic import Field

YouTube_NumVideos_Agent = Agent()

class NumVideoRequest(Model):
    channel_id : str

numvideo_protocol = Protocol("YouTube NumVideo Protocol")

async def numvid_finder(channel_id):
    headers = {
        "x-rapidapi-key": "",
        "x-rapidapi-host": "youtube-data8.p.rapidapi.com"
        }
    url_subscribers = "https://youtube-data8.p.rapidapi.com/channel/details"
    querystring = {"id": channel_id}
    response_numvideo = requests.get(url_subscribers, headers=headers, params=querystring)
    data_numvideo = response_numvideo.json()
    numvid_name = data_numvideo['stats']['videos']
    return numvid_name

@numvideo_protocol.on_message(model=NumVideoRequest, replies=UAgentResponse)
async def on_subscriber_request(ctx: Context, sender: str, msg: NumVideoRequest):
    ctx.logger.info(f"Received Latest NumVideo Request with Channel ID: {msg.channel_id}")
    latestvid = await numvid_finder(msg.channel_id)
    ctx.logger.info(latestvid)
    await ctx.send(sender, UAgentResponse(message=str(latestvid),type=UAgentResponseType.FINAL))

YouTube_NumVideos_Agent.include(numvideo_protocol)

YouTube_NumVideos_Agent.run()
