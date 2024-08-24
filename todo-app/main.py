# main.py

from fasthtml.common import (
    fast_app,
    Style,
    Input,
    patch,
    AX,
    Li,
    Form,
    Group,
    Button,
    Card,
    Ul,
    Main,
    H1,
    Title,
    Div,
    clear,
    Hidden,
    CheckboxX,
    fill_form,
    serve,
)

# Initialize the application
# The line `app, rt, todos, Todo = fast_app(...)` is initializing the application and setting up the
# necessary components for handling tasks related to a to-do list. Here is a breakdown of what each
# variable represents:
app, rt, todos, Todo = fast_app(
    "data/todos.db",
    hdrs=[Style(":root { --pico-font-size: 100%; }")],
    id=int,
    title=str,
    done=bool,
    pk="id",
)

id_currunt = "current-todo"


def todo_id(id):
    """
    The `todo_id` function takes an `id` parameter and returns a string formatted as "todo-{id}".

    :param id: The `id` parameter is used as input to the `todo_id` function, which generates a
    formatted string containing the prefix "todo-" followed by the provided `id` value
    :return: The function `todo_id` takes an `id` as input and returns a string in the format
    "todo-{id}".
    """
    return f"todo-{id}"


# Define how each task is displayed
@patch
def __ft__(self: Todo):
    """
    The function generates a list item with a title, completion status, and edit link for a todo item.

    :param self: The `self` parameter refers to the current instance of the `Todo` class. It is a
    reference to the object on which the method `__ft__` is being called
    :type self: Todo
    :return: The code snippet is defining a special method `__ft__` for a class `Todo`. Inside this
    method, it creates a list item (`Li`) containing the title of the todo item with a link to its
    details page, a checkbox indicating completion status, a separator (" | "), and a link to edit the
    todo item. The list item is then returned.
    """
    show = AX(self.title, f"/todos/{self.id}", id_currunt)
    edit = AX("edit", f"/edit/{self.id}", id_currunt)
    completed = " ✅" if self.done else ""
    return Li(show, completed, " | ", edit, id=todo_id(self.id))


# Helper functions
def create_input_field(**kw):
    """
    The function `create_input_field` creates an input field for a new Todo with specified attributes.
    :return: An Input field with the specified attributes and any additional keyword arguments provided.
    """
    return Input(
        id="new-title",
        name="title",
        placeholder="Enter a new Todo",
        required=True,
        **kw,
    )


# Route to display the task list and add new tasks
@rt("/")
async def get():
    """
    This Python function creates a web page for a to-do list with a title, task list, and add button.
    :return: Title element with the title "My To-Do List", Main element containing an H1 element with
    the same title, a task list with a Card element containing a list of to-dos, an input field to add
    new tasks, and a button to add tasks.
    """
    add = Form(
        Group(create_input_field(), Button("Add")),
        hx_post="/",
        target_id="todo-list",
        hx_swap="beforeend",
    )
    task_list = (
        Card(Ul(*todos(), id="todo-list"), header=add, footer=Div(id=id_currunt)),
    )
    title = "My To-Do List"
    return Title(title), Main(H1(title), task_list, cls="container")


# Route to delete a task


@rt("/todos/{id}")
async def delete(id: int):
    """
    This Python function deletes a task with a specific ID from a list of todos and then clears the
    current ID.

    :param id: The `id` parameter in the route represents the unique identifier of the task that needs
    to be deleted. This identifier is used to locate and remove the specific task from the list of todos
    :type id: int
    :return: The code is returning a function or method named `clear` with the parameter `id_currunt`.
    However, there seems to be a typo in the code as `id_currunt` should likely be `id_current` or some
    other variable name.
    """

    todos.delete(id)
    return clear(id_currunt)


# Route to add a new task


@rt("/")
async def post(todo: Todo):
    """
    This Python function defines a route to add a new task using a POST request and returns the inserted
    task along with an input field.

    :param todo: The `todo` parameter is the data representing a new task that the user wants to add. It
    is of type `Todo`, which likely contains information such as the task name, description, due date,
    priority, etc. The `post` route is designed to receive this `todo` data and
    :type todo: Todo
    :return: The code is returning the result of inserting the new task `todo` into the `todos`
    collection. Additionally, it is also returning an input field created using the `create_input_field`
    function with the `hx_swap_oob` attribute set to "true".
    """
    return todos.insert(todo), create_input_field(hx_swap_oob="true")


# Route to display the edit form for a task


@rt("/edit/{id}")
async def get(id: int):
    """
    The function defines a route in Python to display an edit form for a task identified by its ID.

    :param id: The `id` parameter in the route `/edit/{id}` is used to identify the specific task that
    needs to be edited. It is passed as an integer to the route handler function `get(id: int)` to
    retrieve the task with that particular ID for editing
    :type id: int
    :return: The code is returning a form with fields for editing a task, including a title input, a
    save button, a hidden field for the task ID, and a checkbox for marking the task as done. The form
    is configured to make a PUT request to the root URL ("/") when submitted, and the target ID for the
    form is set to the specific task ID. The form is filled with data from
    """
    res = Form(
        Group(Input(id="title"), Button("Save")),
        Hidden(id="id"),
        CheckboxX(id="done", label="Done"),
        hx_put="/",
        target_id=todo_id(id),
        id="edit",
    )
    return fill_form(res, todos.get(id))


# Route to update a task
@rt("/")
async def put(todo: Todo):
    """
    This Python function uses FastAPI to handle PUT requests for updating a todo item in a collection,
    and then clears the current ID.

    :param todo: The `todo` parameter is an object of type `Todo`, which likely represents a task or
    item to be added or updated in a list of todos. The function `put` is designed to upsert (update or
    insert) this `todo` object into the list of todos and then clear the
    :type todo: Todo
    :return: the result of calling the `upsert` method on the `todos` object with the `todo` object as
    an argument. Additionally, it is also calling the `clear` function with the `id_currunt` parameter.
    The return value of the `put` function is not explicitly specified in the code snippet provided.
    """
    return todos.upsert(todo), clear(id_currunt)


@rt("/todos/{id}")
async def get(id: int):
    """
    This Python function retrieves a todo item by its ID and creates a button to delete it.

    :param id: The `id` parameter in the code snippet represents the unique identifier of a todo item.
    It is used to retrieve a specific todo item from the `todos` collection based on this identifier
    :type id: int
    :return: The code snippet is returning a Div element containing the title of a todo item and a
    Button element with the label "delete". The Button element is configured with attributes for
    handling a delete action, such as the endpoint for the delete request, the target ID for the element
    to be replaced after deletion, and the swap behavior for the response.
    """
    todo = todos.get(id)
    btn = Button(
        "delete",
        hx_delete=f"/todos/{todo.id}",
        target_id=todo_id(todo.id),
        hx_swap="outerHTML",
    )
    return Div(Div(todo.title), btn)


# Start the application server
serve()
