from bottle import BaseTemplate

from boteel.core.utils.module_loading import import_string


def context_processor(dotted_path: str) -> None:

    module = import_string(dotted_path)

    if not callable(module):
        raise ValueError(
            "'%s' should be callable, recieved '%s' instead" % (
                dotted_path, type(module)
            )
        )

    context: dict = module()
    
    if not isinstance(context, dict):
        raise ValueError(
            "Context function '%s' should return a dict object, recieved '%s' instead" % (
                dotted_path, type(context)
            )
        )
    
    BaseTemplate.defaults.update(context)