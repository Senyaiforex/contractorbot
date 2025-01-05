from functools import wraps

from database import get_async_session


def base_session(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        async for session_instance in get_async_session():
            result = await function(*args, **kwargs, session=session_instance)
            return result

    return wrapper