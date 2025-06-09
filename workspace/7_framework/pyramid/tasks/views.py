from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.view import view_config
from pyramid.csrf import get_csrf_token
from pyramid.session import check_csrf_token

from .models import Task, DBSession


@view_config(route_name="tasks", renderer="task_list.jinja2")
def task_list(request):
    """
    Display a list of all tasks.

    Args:
        request: Pyramid request object.

    Returns:
        Dictionary with tasks and CSRF token for the template.
    """
    tasks = DBSession.query(Task).all()
    return {"tasks": tasks, "csrf_token": get_csrf_token(request)}


@view_config(route_name="task", renderer="task_detail.jinja2")
def task_detail(request):
    """
    Display details of a single task.

    Args:
        request: Pyramid request object with task ID in matchdict.

    Returns:
        Dictionary with task data or raises HTTPNotFound if task not found.
    """
    task_id = request.matchdict["id"]
    task = DBSession.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPNotFound()

    return {"task": task, "csrf_token": get_csrf_token(request)}


@view_config(route_name="task_add", renderer="add_task.jinja2", request_method="GET")
def add_task_view(request):
    """
    Display the form to add a new task.

    Args:
        request: Pyramid request object.

    Returns:
        Dictionary with CSRF token for the form.
    """
    return {"csrf_token": get_csrf_token(request)}


@view_config(route_name="task_add", renderer="add_task.jinja2", request_method="POST")
def add_task_submit(request):
    """
    Handle form submission to add a new task.

    Args:
        request: Pyramid request object with form data.

    Returns:
        Dictionary with form data and errors,
        or redirects to task list on success.
    """
    errors = []
    title = request.POST.get("title", "").strip()
    description = request.POST.get("description", "").strip()

    # Validate CSRF token
    token = request.POST.get("_csrf")
    if not token or token != request.session.get_csrf_token():
        errors.append("Invalid security token. Please try again.")

    if not title:
        errors.append("Title is required.")

    if errors:
        return {
            "errors": errors,
            "title": title,
            "description": description,
            "csrf_token": get_csrf_token(request),
        }

    task = Task(title=title, description=description)
    DBSession.add(task)
    DBSession.flush()

    return HTTPFound(location=request.route_url("tasks"))