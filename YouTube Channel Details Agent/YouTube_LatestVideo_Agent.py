import requests
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Model, Context, Protocol
from pydantic import Field

YouTube_LatestVideo_Agent = Agent()

class LatestVideoRequest(Model):
    channel_id : str

latestvideo_protocol = Protocol("YouTube LatestVideo Protocol")

async def latestvid_finder(channel_id):
    headers = {
        "x-rapidapi-key": "4ff9a910bcmsh8b61448da38e5dep14f78fjsn3acc6acb49aa",
        "x-rapidapi-host": "youtube-data8.p.rapidapi.com"
        }
    url_subscribers = "https://youtube-data8.p.rapidapi.com/channel/videos"
    querystring = {"id": channel_id}
    response_latestvideo = requests.get(url_subscribers, headers=headers, params=querystring)
    data_latestvideo = response_latestvideo.json()
    latestvideo_name = data_latestvideo['contents'][0]['video']['title']
    return latestvideo_name

@latestvideo_protocol.on_message(model=LatestVideoRequest, replies=UAgentResponse)
async def on_subscriber_request(ctx: Context, sender: str, msg: LatestVideoRequest):
    ctx.logger.info(f"Received Latest Video Request with Channel ID: {msg.channel_id}")
    latestvid = await latestvid_finder(msg.channel_id)
    ctx.logger.info(latestvid)
    await ctx.send(sender, UAgentResponse(message=str(latestvid),type=UAgentResponseType.FINAL))

YouTube_LatestVideo_Agent.include(latestvideo_protocol)

YouTube_LatestVideo_Agent.run()
