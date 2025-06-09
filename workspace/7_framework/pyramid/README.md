# Pyramid Task Manager - A Beginner's Guide

Welcome to your first Pyramid web application! This is a simple task management system built with the Pyramid web framework. This project is perfect for learning web development with Python.

## 📚 What is Pyramid?

Pyramid is a Python web framework that helps you build web applications. It's known for being:
- **Flexible**: You can build small or large applications
- **Well-documented**: Great learning resources
- **Minimalist**: Doesn't force you into a specific way of doing things
- **Fast**: Good performance for web applications

## 🎯 What This Project Does

This task manager allows you to:
- View a list of all your tasks
- Add new tasks with titles and descriptions
- View detailed information about individual tasks
- Store tasks in a database (SQLite)

## 🏗️ Project Structure

Here's how the project is organized:

```
pyramid/
├── task.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── tasks.db               # SQLite database (created automatically)
├── test_application.py    # Test script to verify everything works
└── tasks/                 # Main application package
    ├── __init__.py        # App configuration and setup
    ├── models.py          # Database models (Task model)
    ├── views.py           # Request handlers (controllers)
    ├── static/            # CSS, JS, images
    └── templates/         # HTML templates
        ├── base.jinja2    # Base template
        ├── task_list.jinja2
        ├── task_detail.jinja2
        └── add_task.jinja2
```

## 🔧 Technologies Used

- **Pyramid**: Web framework
- **SQLAlchemy**: Database toolkit (ORM - Object Relational Mapping)
- **Jinja2**: Template engine for HTML
- **SQLite**: Lightweight database
- **WSGI**: Web Server Gateway Interface

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.7+ installed on your system.

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd python-beginner/workspace/7_framework/pyramid
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python task.py
   ```

4. **Open your browser and visit:**
   ```
   http://localhost:6543
   ```

That's it! Your task manager should be running.

### Running Tests

To make sure everything is working correctly:

```bash
python test_application.py
```

This will run automated tests to verify all features work properly.

## 📖 Understanding the Code

### 1. Application Entry Point (`task.py`)

This is where your application starts:

```python
def main():
    """Initialize and run the Pyramid task management application."""
    global_config = {}
    settings = {
        'sqlalchemy.url': 'sqlite:///tasks.db'
    }
    
    app = create_app(global_config, **settings)
    server = make_server("0.0.0.0", 6543, app)
    print("Serving on http://localhost:6543...")
    server.serve_forever()
```

**What it does:**
- Sets up database connection to SQLite
- Creates the web application
- Starts a web server on port 6543

### 2. Application Configuration (`tasks/__init__.py`)

This file configures your entire application:

- **Database setup**: Connects to SQLite database
- **Session management**: Handles user sessions and security
- **Routes**: Maps URLs to functions
- **Templates**: Sets up HTML templating

### 3. Database Model (`tasks/models.py`)

Defines what a "Task" looks like in the database:

```python
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
```

**What each field means:**
- `id`: Unique number for each task
- `title`: Short name for the task (required)
- `description`: Longer explanation (optional)
- `completed`: Whether the task is done (not used yet, but ready for future features)

### 4. Views/Controllers (`tasks/views.py`)

These functions handle web requests:

- **`task_list`**: Shows all tasks on the home page
- **`task_detail`**: Shows one specific task
- **`add_task_view`**: Shows the form to add a new task
- **`add_task_submit`**: Processes the form when submitted

### 5. Templates (`tasks/templates/`)

HTML files that define how pages look:

- **`base.jinja2`**: Common layout for all pages
- **`task_list.jinja2`**: Homepage showing all tasks
- **`task_detail.jinja2`**: Individual task page
- **`add_task.jinja2`**: Form to create new tasks

## 🌐 URL Routes

Your application responds to these URLs:

| URL | What it does |
|-----|-------------|
| `/` | Shows list of all tasks |
| `/tasks/add` | Form to add a new task (GET) or process form (POST) |
| `/tasks/{id}` | Shows details of a specific task |
| `/static/*` | Serves CSS, images, and other static files |

## 🔒 Security Features

This application includes important security measures:

### CSRF Protection
- **What it is**: Cross-Site Request Forgery protection
- **Why it matters**: Prevents malicious websites from submitting forms on your behalf
- **How it works**: Each form includes a secret token that must match

### Session Management
- Uses signed cookies to track user sessions
- Secure session configuration

## 🎓 Learning Concepts

This project demonstrates several important web development concepts:

### 1. **MVC Pattern** (Model-View-Controller)
- **Model**: `models.py` - Database structure
- **View**: Templates - What users see
- **Controller**: `views.py` - Business logic

### 2. **ORM** (Object-Relational Mapping)
- Instead of writing SQL, you work with Python objects
- SQLAlchemy handles database operations

### 3. **Template Inheritance**
- `base.jinja2` provides common layout
- Other templates extend it to avoid repetition

### 4. **Web Security**
- CSRF tokens protect forms
- Input validation prevents bad data

### 5. **Database Relationships**
- Ready to add features like user accounts
- Structured data storage

## 🔧 Common Customizations

### Adding New Fields to Tasks

1. **Update the model** (`models.py`):
   ```python
   due_date = Column(DateTime, nullable=True)
   ```

2. **Update the form** (`add_task.jinja2`):
   ```html
   <input type="date" name="due_date">
   ```

3. **Update the view** (`views.py`):
   ```python
   due_date = request.POST.get("due_date")
   ```

### Changing the Port

In `task.py`, change `6543` to your preferred port:
```python
server = make_server("0.0.0.0", 8080, app)  # Now runs on port 8080
```

### Adding CSS Styles

Edit `tasks/static/style.css` to customize the appearance.

## 🐛 Troubleshooting

### "Module not found" errors
Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### Port already in use
Either:
- Stop other applications using port 6543
- Change the port number in `task.py`

### Database errors
Delete `tasks.db` and `tasks.db-journal`, then restart the application.

### Template not found
Make sure your templates are in the `tasks/templates/` directory.

## 🎯 Next Steps

Once you're comfortable with this project, try:

1. **Add task completion**: Allow marking tasks as done
2. **Add user authentication**: Multiple users with their own tasks
3. **Add task editing**: Modify existing tasks
4. **Add task deletion**: Remove tasks
5. **Add categories**: Organize tasks by type
6. **Add due dates**: Set deadlines for tasks
7. **Add search**: Find specific tasks

## 📚 Further Reading

- [Pyramid Documentation](https://docs.pylonsproject.org/projects/pyramid/en/latest/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [Web Security Basics](https://developer.mozilla.org/en-US/docs/Web/Security)

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new features
- Fix bugs
- Improve documentation
- Share with other learners

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed for learning.

---

**Happy coding! 🎉**

Remember: The best way to learn is by doing. Try modifying the code, break things, fix them, and experiment with new features!