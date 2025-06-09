# 🎯 Hands-On Tutorial: Adding Task Completion Feature

**Learn by building! Let's add the ability to mark tasks as complete.**

This tutorial will walk you through adding a new feature to your Pyramid task manager. You'll learn how web applications are built by actually building one!

## 🎯 What We're Building

By the end of this tutorial, you'll be able to:
- Mark tasks as completed with a checkbox
- See which tasks are done vs. pending
- Toggle task status back and forth

## 📚 What You'll Learn

- How to modify database models
- How to update HTML templates
- How to handle form submissions
- How to update views/controllers
- How different parts of a web app work together

## 🚀 Before You Start

Make sure your basic task manager is working:
1. Run `python task.py`
2. Visit http://localhost:6543
3. Add a few test tasks

## Step 1: Understanding the Current Model

First, let's look at our current `Task` model in `tasks/models.py`:

```python
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)  # ← This already exists!
```

**Good news!** The `completed` field already exists, but we're not using it yet. Let's activate it!

## Step 2: Update the Task List Template

Open `tasks/templates/task_list.jinja2` and modify it to show task status:

**Find this section (it might look different):**
```html
{% for task in tasks %}
    <div class="task">
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>
    </div>
{% endfor %}
```

**Replace it with:**
```html
{% for task in tasks %}
    <div class="task {% if task.completed %}completed{% endif %}">
        <form method="POST" action="{{ request.route_url('task_toggle', id=task.id) }}" style="display: inline;">
            <input type="hidden" name="_csrf" value="{{ csrf_token }}">
            <input type="checkbox" 
                   onchange="this.form.submit()" 
                   {% if task.completed %}checked{% endif %}>
        </form>
        
        <div class="task-content">
            <h3 class="{% if task.completed %}strikethrough{% endif %}">
                <a href="{{ request.route_url('task', id=task.id) }}">{{ task.title }}</a>
            </h3>
            <p>{{ task.description }}</p>
            <small>Status: {% if task.completed %}✅ Completed{% else %}⏳ Pending{% endif %}</small>
        </div>
    </div>
{% endfor %}
```

**What this does:**
- Shows a checkbox for each task
- Automatically submits form when checkbox is clicked
- Shows different styling for completed tasks
- Displays task status with emojis

## Step 3: Add CSS Styling

Create or update `tasks/static/style.css`:

```css
/* Basic task styling */
.task {
    border: 1px solid #ddd;
    margin: 10px 0;
    padding: 15px;
    border-radius: 5px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}

.task.completed {
    background-color: #f0f8f0;
    border-color: #90EE90;
}

.task-content {
    flex-grow: 1;
}

.strikethrough {
    text-decoration: line-through;
    color: #666;
}

/* Checkbox styling */
input[type="checkbox"] {
    transform: scale(1.2);
    margin-right: 10px;
}

/* Status styling */
small {
    color: #666;
    font-style: italic;
}
```

## Step 4: Add a New Route

Open `tasks/__init__.py` and find the `setup_routes` function. Add a new route:

```python
def setup_routes(config):
    """Configure application routes."""
    config.add_static_view(name="static", path="tasks:static")
    config.add_route("tasks", "/")
    config.add_route("task_add", "/tasks/add")
    config.add_route("task", "/tasks/{id}")
    config.add_route("task_toggle", "/tasks/{id}/toggle")  # ← Add this line
```

## Step 5: Create the Toggle View

Open `tasks/views.py` and add this new function:

```python
@view_config(route_name="task_toggle", request_method="POST")
def toggle_task(request):
    """
    Toggle the completion status of a task.
    
    Args:
        request: Pyramid request object with task ID in matchdict.
        
    Returns:
        Redirects back to the task list.
    """
    # Validate CSRF token
    token = request.POST.get("_csrf")
    if not token or token != request.session.get_csrf_token():
        # For security, just redirect on invalid token
        return HTTPFound(location=request.route_url("tasks"))
    
    # Get the task
    task_id = request.matchdict["id"]
    task = DBSession.query(Task).filter(Task.id == task_id).first()
    
    if task:
        # Toggle the completion status
        task.completed = not task.completed
        DBSession.flush()  # Save the change
    
    # Redirect back to the task list
    return HTTPFound(location=request.route_url("tasks"))
```

**What this function does:**
1. Checks security (CSRF token)
2. Finds the task by ID
3. Flips the `completed` status (True → False, False → True)
4. Saves the change to database
5. Redirects back to task list

## Step 6: Test Your New Feature

1. **Stop your server** (Ctrl+C in terminal)
2. **Restart it**: `python task.py`
3. **Open your browser**: http://localhost:6543
4. **Try it out**:
   - Click checkboxes next to tasks
   - Watch them change appearance
   - See the status updates

## Step 7: Add Task Filtering (Bonus!)

Let's add the ability to show only completed or pending tasks.

**Update `tasks/views.py` task_list function:**

```python
@view_config(route_name="tasks", renderer="task_list.jinja2")
def task_list(request):
    """
    Display a list of all tasks with optional filtering.
    """
    # Get filter parameter
    filter_type = request.GET.get('filter', 'all')
    
    # Build query based on filter
    query = DBSession.query(Task)
    
    if filter_type == 'completed':
        query = query.filter(Task.completed == True)
    elif filter_type == 'pending':
        query = query.filter(Task.completed == False)
    # 'all' shows everything (no additional filter)
    
    tasks = query.all()
    
    return {
        "tasks": tasks, 
        "csrf_token": get_csrf_token(request),
        "current_filter": filter_type
    }
```

**Update `tasks/templates/task_list.jinja2` to add filter buttons:**

Add this after the `<h2>Tasks</h2>` line:

```html
<div class="filter-buttons">
    <a href="{{ request.route_url('tasks') }}" 
       class="filter-btn {% if current_filter == 'all' %}active{% endif %}">
       All Tasks
    </a>
    <a href="{{ request.route_url('tasks') }}?filter=pending" 
       class="filter-btn {% if current_filter == 'pending' %}active{% endif %}">
       ⏳ Pending
    </a>
    <a href="{{ request.route_url('tasks') }}?filter=completed" 
       class="filter-btn {% if current_filter == 'completed' %}active{% endif %}">
       ✅ Completed
    </a>
</div>
```

**Add CSS for filter buttons:**

```css
.filter-buttons {
    margin: 20px 0;
    text-align: center;
}

.filter-btn {
    display: inline-block;
    padding: 8px 16px;
    margin: 0 5px;
    background-color: #f0f0f0;
    color: #333;
    text-decoration: none;
    border-radius: 4px;
    border: 1px solid #ddd;
}

.filter-btn:hover {
    background-color: #e0e0e0;
}

.filter-btn.active {
    background-color: #007bff;
    color: white;
    border-color: #007bff;
}
```

## 🎉 Congratulations!

You've just built a complete feature from scratch! You now have:
- ✅ Task completion toggle
- ✅ Visual feedback for completed tasks
- ✅ Status indicators
- ✅ Task filtering (bonus)

## 🔍 What You Learned

1. **Database Integration**: How to use existing database fields
2. **HTML Forms**: Creating interactive elements
3. **URL Routing**: Adding new endpoints
4. **View Functions**: Processing requests and responses
5. **Template Updates**: Modifying the user interface
6. **CSS Styling**: Making things look good
7. **Security**: CSRF token validation

## 🚀 Try These Challenges

Now that you understand the pattern, try adding:

1. **Task Deletion**: Add a "Delete" button for each task
2. **Task Editing**: Allow modifying task title and description
3. **Due Dates**: Add date fields to tasks
4. **Task Categories**: Add tags or categories
5. **Task Priority**: High, Medium, Low priority levels

## 🔧 Troubleshooting

### Checkbox doesn't work
- Check that the route is added in `__init__.py`
- Verify the view function is in `views.py`
- Make sure you restarted the server

### Styling looks wrong
- Check that `style.css` is in the `static` folder
- Verify the CSS is linked in `base.jinja2`
- Clear your browser cache (Ctrl+F5)

### Database errors
- Stop the server
- Delete `tasks.db` and `tasks.db-journal`
- Restart the server (database recreates automatically)

## 📚 Understanding the Code Flow

When you click a checkbox, here's what happens:

1. **Browser**: Submits form to `/tasks/{id}/toggle`
2. **Pyramid**: Routes request to `toggle_task` function
3. **View**: Validates security, finds task, toggles status
4. **Database**: Saves the change
5. **Response**: Redirects back to task list
6. **Browser**: Reloads page with updated data
7. **Template**: Shows updated task with new status

This is the fundamental pattern of web development!

## 🎯 Next Steps

- Try the challenges above
- Read about SQLAlchemy relationships
- Learn about user authentication
- Explore Pyramid's advanced features
- Build your own web application!

---

**Great job! You're now thinking like a web developer! 🎉**

Remember: Every complex application is built by combining simple features like this one. Keep practicing and building!