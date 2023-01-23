from ..utils import get_modules

# Imports all routers in the current folder
routers = get_modules(__file__, "router")
