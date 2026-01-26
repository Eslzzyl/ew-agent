from datetime import datetime, timedelta
from typing import Optional

from agno.tools import tool
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from models import EatingHistory, FoodChoice, GlobalInfo, SessionLocal


@tool
def get_current_time() -> str:
    """获取当前系统时间并判断餐次类型

    Returns:
        当前时间和餐次类型（早饭、午饭、晚饭、其他）
    """
    now = datetime.now()
    hour = now.hour

    if 6 <= hour < 11:
        meal_type = "早饭"
    elif 11 <= hour < 15:
        meal_type = "午饭"
    elif 17 <= hour < 22:
        meal_type = "晚饭"
    else:
        meal_type = "其他"

    return f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}, 餐次: {meal_type}"


@tool
def list_food_choices() -> str:
    """列出所有已记录的餐厅和餐品选择

    Returns:
        所有餐厅选择的列表，包含ID、名称、餐品类型和描述
    """
    db: Session = SessionLocal()
    try:
        choices = db.query(FoodChoice).order_by(FoodChoice.created_at.desc()).all()

        if not choices:
            return "目前还没有记录任何餐厅选择。"

        result = "已记录的餐厅选择：\n"
        for choice in choices:
            description = choice.description if choice.description else "无"
            result += f"ID: {choice.id} | 餐厅: {choice.name} | 餐品: {choice.food_type} | 描述: {description}\n"

        return result
    finally:
        db.close()


@tool
def add_food_choice(
    name: str, food_type: str, description: Optional[str] = None
) -> str:
    """添加一个新的餐厅和餐品选择

    Args:
        name: 餐厅名称
        food_type: 餐食品种
        description: 描述（可选），根据用户评价得出

    Returns:
        添加结果信息
    """
    db: Session = SessionLocal()
    try:
        new_choice = FoodChoice(name=name, food_type=food_type, description=description)
        db.add(new_choice)
        db.commit()
        db.refresh(new_choice)
        return f"成功添加餐厅选择！ID: {new_choice.id}, 餐厅: {name}, 餐品: {food_type}"
    except Exception as e:
        db.rollback()
        return f"添加失败: {str(e)}"
    finally:
        db.close()


@tool
def update_food_choice(
    choice_id: int,
    name: Optional[str] = None,
    food_type: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """更新已存在的餐厅选择

    Args:
        choice_id: 餐厅选择的ID
        name: 新的餐厅名称（可选）
        food_type: 新的餐食品种（可选）
        description: 新的描述（可选），根据用户评价得出

    Returns:
        更新结果信息
    """
    db: Session = SessionLocal()
    try:
        choice = db.query(FoodChoice).filter(FoodChoice.id == choice_id).first()

        if not choice:
            return f"未找到ID为 {choice_id} 的餐厅选择。"

        if name:
            choice.name = name
        if food_type:
            choice.food_type = food_type
        if description is not None:
            choice.description = description

        db.commit()
        return f"成功更新餐厅选择！ID: {choice_id}"
    except Exception as e:
        db.rollback()
        return f"更新失败: {str(e)}"
    finally:
        db.close()


@tool
def delete_food_choice(choice_id: int) -> str:
    """删除一个餐厅选择

    Args:
        choice_id: 餐厅选择的ID

    Returns:
        删除结果信息
    """
    db: Session = SessionLocal()
    try:
        choice = db.query(FoodChoice).filter(FoodChoice.id == choice_id).first()

        if not choice:
            return f"未找到ID为 {choice_id} 的餐厅选择。"

        db.delete(choice)
        db.commit()
        return f"成功删除餐厅选择！ID: {choice_id}, 餐厅: {choice.name}"
    except Exception as e:
        db.rollback()
        return f"删除失败: {str(e)}"
    finally:
        db.close()


@tool
def get_eating_statistics(days: int = 7) -> str:
    """获取最近一段时间用户吃饭情况的统计信息

    Args:
        days: 统计最近多少天的数据，默认7天

    Returns:
        统计信息，包括就餐次数、热门餐厅、餐次分布等
    """
    db: Session = SessionLocal()
    try:
        start_date = datetime.now() - timedelta(days=days)

        histories = (
            db.query(EatingHistory).filter(EatingHistory.eaten_at >= start_date).all()
        )

        if not histories:
            return f"最近 {days} 天没有吃饭记录。"

        total_count = len(histories)

        meal_type_stats = (
            db.query(EatingHistory.meal_type, func.count(EatingHistory.id))
            .filter(EatingHistory.eaten_at >= start_date)
            .group_by(EatingHistory.meal_type)
            .all()
        )

        popular_choices = (
            db.query(FoodChoice.name, func.count(EatingHistory.id))
            .join(EatingHistory)
            .filter(EatingHistory.eaten_at >= start_date)
            .group_by(FoodChoice.id, FoodChoice.name)
            .order_by(desc(func.count(EatingHistory.id)))
            .limit(5)
            .all()
        )

        result = f"最近 {days} 天吃饭统计：\n"
        result += f"总就餐次数: {total_count}\n\n"

        result += "餐次分布：\n"
        for meal_type, count in meal_type_stats:
            result += f"  {meal_type}: {count} 次\n"

        result += "\n热门餐厅（TOP 5）：\n"
        for idx, (name, count) in enumerate(popular_choices, 1):
            result += f"  {idx}. {name}: {count} 次\n"

        return result
    except Exception as e:
        return f"获取统计信息失败: {str(e)}"
    finally:
        db.close()


@tool
def record_eating(
    food_choice_id: int, meal_type: str, user_id: Optional[str] = None
) -> str:
    """记录一次吃饭行为

    Args:
        food_choice_id: 餐厅选择的ID
        meal_type: 餐次类型（早饭、午饭、晚饭）
        user_id: 用户ID（可选）

    Returns:
        记录结果信息
    """
    db: Session = SessionLocal()
    try:
        choice = db.query(FoodChoice).filter(FoodChoice.id == food_choice_id).first()

        if not choice:
            return f"未找到ID为 {food_choice_id} 的餐厅选择。"

        history = EatingHistory(
            food_choice_id=food_choice_id, meal_type=meal_type, user_id=user_id
        )
        db.add(history)
        db.commit()

        return f"成功记录！{meal_type}吃了 {choice.name} 的 {choice.food_type}"
    except Exception as e:
        db.rollback()
        return f"记录失败: {str(e)}"
    finally:
        db.close()


@tool
def get_global_info(key: str) -> str:
    """获取全局信息

    Args:
        key: 信息键名

    Returns:
        信息值，如果不存在则返回提示信息
    """
    db: Session = SessionLocal()
    try:
        info = db.query(GlobalInfo).filter(GlobalInfo.key == key).first()

        if not info:
            return f"未找到键名为 '{key}' 的全局信息。"

        return f"键名: {key}\n值: {info.value}\n更新时间: {info.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception as e:
        return f"获取全局信息失败: {str(e)}"
    finally:
        db.close()


@tool
def set_global_info(key: str, value: str) -> str:
    """设置或更新全局信息

    Args:
        key: 信息键名
        value: 信息值

    Returns:
        设置结果信息
    """
    db: Session = SessionLocal()
    try:
        info = db.query(GlobalInfo).filter(GlobalInfo.key == key).first()

        if info:
            info.value = value
            info.updated_at = datetime.now()
            db.commit()
            return f"成功更新全局信息！键名: {key}"
        else:
            new_info = GlobalInfo(key=key, value=value)
            db.add(new_info)
            db.commit()
            return f"成功创建全局信息！键名: {key}"
    except Exception as e:
        db.rollback()
        return f"设置全局信息失败: {str(e)}"
    finally:
        db.close()


@tool
def list_global_info() -> str:
    """列出所有全局信息

    Returns:
        所有全局信息的列表
    """
    db: Session = SessionLocal()
    try:
        infos = db.query(GlobalInfo).order_by(GlobalInfo.updated_at.desc()).all()

        if not infos:
            return "目前还没有任何全局信息。"

        result = "全局信息列表：\n"
        result += "-" * 50 + "\n"
        for info in infos:
            value_preview = (
                info.value[:50] + "..." if len(info.value) > 50 else info.value
            )
            result += f"键名: {info.key}\n"
            result += f"值: {value_preview}\n"
            result += f"更新时间: {info.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += "-" * 50 + "\n"

        result += f"共 {len(infos)} 条记录"
        return result
    except Exception as e:
        return f"列出全局信息失败: {str(e)}"
    finally:
        db.close()


@tool
def delete_global_info(key: str) -> str:
    """删除全局信息

    Args:
        key: 信息键名

    Returns:
        删除结果信息
    """
    db: Session = SessionLocal()
    try:
        info = db.query(GlobalInfo).filter(GlobalInfo.key == key).first()

        if not info:
            return f"未找到键名为 '{key}' 的全局信息。"

        db.delete(info)
        db.commit()
        return f"成功删除全局信息！键名: {key}"
    except Exception as e:
        db.rollback()
        return f"删除全局信息失败: {str(e)}"
    finally:
        db.close()


@tool
def suggest_food(
    meal_type: Optional[str] = None, description: Optional[str] = None
) -> str:
    """根据用户需求推荐吃饭的选择

    Args:
        meal_type: 餐次类型（可选），如"早饭"、"午饭"、"晚饭"
        description: 用户描述的偏好（可选），如"清淡"、"辣"、"快餐"等

    Returns:
        推荐的餐厅选择
    """
    db: Session = SessionLocal()
    try:
        query = db.query(FoodChoice)

        if description:
            query = query.filter(FoodChoice.description.like(f"%{description}%"))

        choices = query.all()

        if not choices:
            return "没有找到符合要求的餐厅选择，请先添加一些选择。"

        result = f"为您推荐的{meal_type if meal_type else ''}选择：\n"

        for idx, choice in enumerate(choices, 1):
            desc = choice.description if choice.description else "无"
            result += f"{idx}. {choice.name} - {choice.food_type} (描述: {desc})\n"

        result += f"\n您可以根据ID使用 record_eating 工具记录您的选择。"

        return result
    except Exception as e:
        return f"推荐失败: {str(e)}"
    finally:
        db.close()
