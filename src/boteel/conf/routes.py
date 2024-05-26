def path(
    route: str,
    view: object = None,
    name: str = None,
    method: str = ["GET", "POST"],
    kwargs: dict = None,
) -> dict:

    if not name:
        name = route.replace("/", "_")

    rt = {"path": route, "method": method, "callback": view, "name": name}
    if not kwargs:
        kwargs = dict()

    rt.update(**kwargs)
    return rt
