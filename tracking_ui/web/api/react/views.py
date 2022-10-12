from fastapi import APIRouter

router = APIRouter()

todos = [
    {
        "id": "1",
        "item": "Read a book.",
    },
    {
        "id": "2",
        "item": "Cycle around town.",
    },
]


@router.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return {"data": todos}


@router.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    return {
        "data": {"Todo added."},
    }


@router.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            return {
                "data": f"Todo with id {id} has been updated.",
            }

    return {
        "data": f"Todo with id {id} not found.",
    }
