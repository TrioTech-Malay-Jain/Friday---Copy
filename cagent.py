import os
from dotenv import load_dotenv
import logging
import asyncio

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RoomOutputOptions, JobContext
from livekit.plugins import google, cartesia, deepgram, noise_cancellation, silero

from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web, triotech_info, create_lead, detect_lead_intent
import config

load_dotenv()
logging.basicConfig(level=logging.INFO)


class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.LLM(model="gemini-1.5-flash", temperature=0.8),
            tools=[get_weather, search_web, triotech_info, create_lead, detect_lead_intent],
        )


async def entrypoint(ctx: JobContext):
    # Setup conversation logging
    config.setup_conversation_log()
    
    agent = Assistant()

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=google.LLM(model="gemini-1.5-flash", temperature=0.8),
        tts=cartesia.TTS(
            model="sonic-2",
            language="hi",
            voice="f91ab3e6-5071-4e15-b016-cde6f2bcd222",
        ),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(noise_cancellation=noise_cancellation.BVC()),
        room_output_options=RoomOutputOptions(audio_enabled=True),
    )

    await session.generate_reply(instructions=SESSION_INSTRUCTION)
    await asyncio.Future()  # Run until externally stopped


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
