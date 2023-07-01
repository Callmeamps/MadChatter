import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import (
    create_async_playwright_browser,
    # create_sync_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.
)
from langchain.agents import initialize_agent
import chainlit as cl
# from chainlit import user_session


load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

CHATGPT = ChatOpenAI(temperature=0.5)
async_browser = create_async_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
tools = toolkit.get_tools()
memory = ConversationBufferMemory(memory_key="chat_history")
# tools_by_name = {tool.name: tool for tool in tools}
# navigate_tool = tools_by_name["navigate_browser"]
# get_elements_tool = tools_by_name["get_elements"]

# template = """Question: {question}

# Answer: Let's think step by step."""

@cl.langchain_rename
def rename(orig_author: str):
    for tool in tools:
        dict_item = {
            tool.name: f"Mad Chatter's {tool.name.replace('_', ' ').capitalize()}"
        }
        return dict_item.get(orig_author, orig_author)

saved_messages = []

@cl.action_callback("action_button")
async def save_message(action):
    await cl.Message(content=f"Executed {action}").send()
    # Optionally remove the action button from the chatbot user interface
    await action.remove()
    

@cl.langchain_factory(use_async=True)
def factory():
    # prompt = PromptTemplate(template=template, input_variables=["question"])
    agent_chain = initialize_agent(
        tools,
        CHATGPT,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )
    return agent_chain


@cl.langchain_run
async def run(agent, input_str):
    actions = [
        cl.Action(name="action_button", value="example_value", description="Click me!")
    ]
    res = await agent.arun(input_str, callbacks=[cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content=res["text"], actions=actions).send()
