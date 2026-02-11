from fastapi import HTTPException
from src.lib.env_config import Config
from src.lib.helper.fetch_mcp_tools import fetch_mcp_tools
from src.models.message import Role
from src.lib.helper.save_message import save_message
from src.lib.helper.get_message_history import get_or_create_conversation
from src.models.user import User
from sqlmodel import Session
from agents import Agent, Runner, RunConfig,  function_tool, RunContextWrapper,ModelSettings
from src.lib.agent_instructions import instructions_with_user_id

from agents.mcp import MCPServerStreamableHttp,MCPServerStreamableHttpParams
async def create_chat_for_user(token:str, agent_config,session: Session, query: str, user_id: str) :
    try:
        # Fetch conversation history from database
        history,conv_id = get_or_create_conversation(session,user_id=user_id)
        print(history,conv_id)

        # Build message array for agent (history + new message)
        message_array_for_agent = history + [{"role": "user", "content": query}]
        # print("message_array_for_agent)",message_array_for_agent)

        # Store user message in database
        save_message(
            session=session,user_id=user_id,conversation_id=conv_id,
            role=Role.USER,content=query
        )

        # 5. Fetch MCP tools
        # mcp_tools = await fetch_mcp_tools(token=token)
        # print(mcp_tools)

        mcp_params = MCPServerStreamableHttpParams(
            url=Config.MCP_SERVER_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # print("mcp_params",mcp_params)
         # 2. Server instance banayein
        mcp_server = MCPServerStreamableHttp(params=mcp_params)

        async with mcp_server:


        # Create run configuration
            runConfig = RunConfig(
                model=agent_config.model(),
                model_provider=agent_config.client(),
                model_settings= ModelSettings(
                    tool_choice="required",
                    
                )
            )
            # return "abc"
            starting_agent = Agent(
                name="Task Agent",
                instructions= instructions_with_user_id,
                # tools=tools ,
                mcp_servers=[mcp_server]
                # tool_use_behavior="stop_on_first_tool"
            )

            # # Run the agent with the user's query and context
            result = await Runner.run(
                starting_agent=starting_agent,
                input=message_array_for_agent,
                run_config=runConfig,
                context={"user_id": user_id}
            )
            print("Final Output:", result.final_output)
            save_message(
                session=session,user_id=user_id,conversation_id=conv_id,
                role=Role.ASSISTANT,content=result.final_output
            )
            return {"status": "success", "query": query, "result": result.final_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
