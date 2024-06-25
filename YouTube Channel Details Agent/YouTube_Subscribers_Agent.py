import requests
from ai_engine import UAgentResponse, UAgentResponseType
from uagents import Agent, Model, Context, Protocol
from pydantic import Field

YouTube_Subscriber_Agent = Agent()

class SubscriberRequest(Model):
    channel_id : str

subscriber_protocol = Protocol("YouTube Subscriber Protocol")

async def subsriber_counter(channel_id):
    headers = {
        "x-rapidapi-key": "",
        "x-rapidapi-host": "youtube-data8.p.rapidapi.com"
        }
    url_subscribers = "https://youtube-data8.p.rapidapi.com/channel/details"
    querystring = {"id": channel_id}
    response_subscribers = requests.get(url_subscribers, headers=headers, params=querystring)
    data_subscribers = response_subscribers.json()
    subscribers_count = data_subscribers['stats']['subscribers']
    return subscribers_count

@subscriber_protocol.on_message(model=SubscriberRequest, replies=UAgentResponse)
async def on_subscriber_request(ctx: Context, sender: str, msg: SubscriberRequest):
    ctx.logger.info(f"Received Subscriber Count Request with Channel ID: {msg.channel_id}")
    subscribers = await subsriber_counter(msg.channel_id)
    ctx.logger.info(subscribers)
    await ctx.send(sender, UAgentResponse(message=str(subscribers),type=UAgentResponseType.FINAL))

YouTube_Subscriber_Agent.include(subscriber_protocol)

YouTube_Subscriber_Agent.run()
