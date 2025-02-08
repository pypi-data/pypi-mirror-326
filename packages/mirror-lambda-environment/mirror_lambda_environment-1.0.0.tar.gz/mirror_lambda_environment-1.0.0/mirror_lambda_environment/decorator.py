from typing import Optional

from mirror_lambda_environment import MirrorLambdaEnvironment


def mirror_lambda_environment(
    function_name: Optional[str] = None,
    prompt: Optional[bool] = False
):
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            with MirrorLambdaEnvironment(function_name, prompt):
                res = func(*args, **kwargs)
            return res
        return wrapper_func
    return decorator_func
