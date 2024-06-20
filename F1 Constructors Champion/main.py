from constructors_agent import constructors_agent
from user import user

from uagents import Bureau

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    bureau.add(constructors_agent)
    bureau.add(user)
    bureau.run()
