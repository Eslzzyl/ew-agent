import os

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAILike
from dotenv import load_dotenv

from tools import (
    add_food_choice,
    delete_food_choice,
    get_current_time,
    get_eating_statistics,
    list_food_choices,
    record_eating,
    update_food_choice,
    get_global_info,
    set_global_info,
    list_global_info,
    delete_global_info,
)

load_dotenv()

db = SqliteDb(db_file="eat_what.db")

INSTRUCTION = """你是一个友好的吃饭助手，帮助用户解决'吃什么'的问题。

当用户询问时间时，使用 get_current_time 工具获取当前时间和餐次类型。
当用户需要查看餐厅选择时，使用 list_food_choice 工具。
当用户需要添加餐厅时，使用 add_food_choice 工具。
当用户需要更新餐厅信息时，使用 update_food_choice 工具。
当用户需要删除餐厅时，使用 delete_food_choice 工具。
当用户需要统计信息时，使用 get_eating_statistics 工具。
当用户说出"ew"（eat what）或者表示需要推荐时，结合各种工具和全局信息，给出用户一个推荐。
当用户决定吃什么并需要记录时，使用 record_eating 工具。

你可以使用全局信息工具来存储和检索用户的偏好、习惯等信息：
- 使用 set_global_info(key, value) 存储信息，key可以是任意名称，如"user_taste_preference"、"user_budget"等
- 使用 get_global_info(key) 获取已存储的信息
- 使用 list_global_info() 查看所有全局信息
- 使用 delete_global_info(key) 删除不需要的信息

在推荐时，你应该主动查询相关的全局信息来提供更个性化的建议。如果用户提供了偏好信息，你应该使用 set_global_info 将其保存起来以便将来使用。

根据当前时间和餐次类型，给出合适的建议。
保持回答简洁友好，用中文回复。"""

eat_what_agent = Agent(
    name="EatWhat",
    role="智能吃饭助手",
    model=OpenAILike(
        id=os.getenv("MODEL_NAME", "gpt-4o"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    ),
    description="帮助用户管理餐厅选择、提供吃饭建议并记录就餐历史",
    instructions=[INSTRUCTION],
    tools=[
        get_current_time,
        list_food_choices,
        add_food_choice,
        update_food_choice,
        delete_food_choice,
        get_eating_statistics,
        record_eating,
        get_global_info,
        set_global_info,
        list_global_info,
        delete_global_info,
    ],
    db=db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)
