src/: The highest level of an app, contains common models, configs, and constants, etc.
src/main.py: Root of the project, which inits the FastAPI app
Each package has its own router, schemas, models, etc.

router.py: is the core of each module with all the endpoints
schemas.py: for pydantic models
models.py: for database models
service.py: module-specific business logic
dependencies.py: router dependencies
constants.py: module-specific constants and error codes
config.py: e.g. env vars
utils.py: non-business logic functions, e.g. response normalization, data enrichment, etc.
exceptions.py: module-specific exceptions, e.g. PostNotFound, InvalidUserData



## Tips
Dependencies can be reused multiple times, and they won't be recalculated - FastAPI caches dependency's result within a request's scope by default, i.e. if valid_post_id gets called multiple times in one route, it will be called only once.