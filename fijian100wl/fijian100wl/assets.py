from pathlib import Path

from clld.web.assets import environment

import fijian100wl

environment.append_path(
    Path(fijian100wl.__file__).parent.joinpath("static").as_posix(),
    url="/fijian100wl:static/",
)
environment.load_path = list(reversed(environment.load_path))
