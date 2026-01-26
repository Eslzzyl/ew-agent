from agent import eat_what_agent
from models import init_db
from prompt_toolkit import prompt


def main():
    print("=" * 50)
    print("🍽️  Eat What - 智能吃饭助手")
    print("=" * 50)
    print("输入 'quit' 或 'exit' 退出程序\n")

    init_db()

    session_id = "default_session"
    user_id = "default_user"

    while True:
        try:
            user_input = prompt("🤔 你想吃什么？> ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 再见！祝你用餐愉快！")
                break

            print("\n💬 EatWhat 正在思考...\n")
            eat_what_agent.print_response(
                user_input, session_id=session_id, user_id=user_id, stream=True
            )
            print()

        except KeyboardInterrupt:
            print("\n\n👋 再见！祝你用餐愉快！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}\n")


if __name__ == "__main__":
    main()
