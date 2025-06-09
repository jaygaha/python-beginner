# 🛠️ Troubleshooting Guide - Pyramid Task Manager

**Having issues? Don't worry! This guide covers the most common problems and their solutions.**

## 🚨 Common Startup Issues

### 1. "python: command not found"

**Problem**: Your system doesn't recognize the `python` command.

**Solutions**:
```bash
# Try python3 instead
python3 task.py

# Or check if Python is installed
python --version
python3 --version
```

**If Python isn't installed**:
- Visit https://python.org/downloads/
- Download and install Python 3.7+
- Make sure to check "Add Python to PATH" during installation

### 2. "No module named 'pyramid'"

**Problem**: Dependencies aren't installed.

**Solution**:
```bash
# Install required packages
pip install -r requirements.txt

# If using python3, try:
pip3 install -r requirements.txt
```

### 3. "Address already in use" or "Port 6543 is busy"

**Problem**: Another application is using port 6543.

**Solutions**:

**Option 1**: Change the port in `task.py`:
```python
# Change this line:
server = make_server("0.0.0.0", 6543, app)
# To this (using port 8080):
server = make_server("0.0.0.0", 8080, app)
```
Then visit http://localhost:8080

**Option 2**: Find and stop the other application:
```bash
# On Mac/Linux:
lsof -i :6543
kill -9 <PID>

# On Windows:
netstat -ano | findstr :6543
taskkill /PID <PID> /F
```

### 4. "Permission denied"

**Problem**: You don't have permission to run on the port.

**Solutions**:
- Use a port number above 1024 (like 8080)
- Run with sudo (not recommended for development)
- Check if another user is running the application

## 🌐 Browser Issues

### 1. "This site can't be reached"

**Checklist**:
- Is the server running? (Look for "Serving on http://localhost:6543...")
- Are you using the correct URL? (http://localhost:6543)
- Did you change the port? Use the new port number
- Try 127.0.0.1 instead of localhost: http://127.0.0.1:6543

### 2. "404 Not Found"

**Problem**: The URL doesn't match any routes.

**Common causes**:
- Typing error in URL
- Route not added in `__init__.py`
- View function not properly decorated

**Check**:
```python
# In tasks/__init__.py, make sure routes are added:
config.add_route("tasks", "/")
config.add_route("task_add", "/tasks/add")
config.add_route("task", "/tasks/{id}")
```

### 3. Page loads but looks broken (no CSS)

**Problem**: Static files aren't loading.

**Solutions**:
- Check if `tasks/static/style.css` exists
- Verify static route in `__init__.py`:
  ```python
  config.add_static_view(name="static", path="tasks:static")
  ```
- Clear browser cache (Ctrl+F5 or Cmd+Shift+R)

## 💾 Database Issues

### 1. "Database is locked"

**Problem**: SQLite database is being used by another process.

**Solutions**:
```bash
# Stop the server (Ctrl+C)
# Delete database files
rm tasks.db
rm tasks.db-journal

# Restart the server
python task.py
```

### 2. "No such table: tasks"

**Problem**: Database tables weren't created.

**Solution**:
The app should create tables automatically. If not:
```bash
# Delete the database and restart
rm tasks.db
python task.py
```

### 3. Tasks disappear after restart

**This is normal!** Each time you delete `tasks.db`, all data is lost.

**To keep data**:
- Don't delete `tasks.db` unless troubleshooting
- The database file contains all your tasks

## 🔧 Code Issues

### 1. "ImportError" or "ModuleNotFoundError"

**Problem**: Python can't find your modules.

**Solutions**:
- Make sure you're in the right directory:
  ```bash
  cd python-beginner/workspace/7_framework/pyramid
  ```
- Check that `__init__.py` files exist in the `tasks` folder
- Verify file structure matches the documentation

### 2. "NameError: name 'something' is not defined"

**Problem**: Using a variable or function that doesn't exist.

**Common causes**:
- Typo in variable name
- Missing import statement
- Function not defined

**Check**:
- Spelling of variable names
- Import statements at top of files
- Function definitions

### 3. "IndentationError"

**Problem**: Python is very strict about indentation.

**Solutions**:
- Use consistent indentation (4 spaces recommended)
- Don't mix tabs and spaces
- Check that all code blocks are properly indented

## 🔒 Security Issues

### 1. "Invalid security token" when submitting forms

**Problem**: CSRF token mismatch.

**Solutions**:
- Make sure forms include the CSRF token:
  ```html
  <input type="hidden" name="_csrf" value="{{ csrf_token }}">
  ```
- Check that the token is passed to templates
- Clear browser cookies if the issue persists

### 2. Forms don't submit

**Checklist**:
- Form has `method="POST"`
- Form action points to correct URL
- CSRF token is included
- Submit button is inside the form

## 🎨 Template Issues

### 1. "TemplateNotFound"

**Problem**: Jinja2 can't find your template file.

**Solutions**:
- Check file exists in `tasks/templates/`
- Verify filename spelling exactly matches
- Check template path configuration in `__init__.py`:
  ```python
  config.add_jinja2_search_path("tasks:templates")
  ```

### 2. Variables not showing in templates

**Problem**: Template variables aren't being passed from views.

**Check**:
- View function returns dictionary with variable names
- Template uses correct variable names: `{{ variable_name }}`
- No typos in variable names

### 3. Template inheritance not working

**Problem**: Child templates don't extend base template.

**Check**:
- First line of child template: `{% extends "base.jinja2" %}`
- Blocks are properly defined: `{% block content %}...{% endblock %}`
- Base template has matching block names

## 🧪 Testing Issues

### 1. Test script fails

**Problem**: `test_application.py` doesn't pass.

**Solutions**:
- Make sure main application works first
- Check that all dependencies are installed
- Run tests with: `python test_application.py`
- Look at specific error messages

### 2. "Connection refused" during tests

**Problem**: Test server can't start.

**Solutions**:
- Make sure port 6544 is available (tests use different port)
- Stop any running instances of the main application
- Check firewall settings

## 📱 Development Tips

### 1. Enable Debug Mode

Add this to your `task.py` for better error messages:
```python
settings = {
    'sqlalchemy.url': 'sqlite:///tasks.db',
    'pyramid.debug_all': True,  # Add this line
}
```

### 2. Check Server Logs

Always look at the terminal where you ran `python task.py`. Error messages appear there.

### 3. Use Print Statements

Add debug prints to your code:
```python
def some_function():
    print("Function called!")  # Debug line
    # Your code here
```

### 4. Browser Developer Tools

- Press F12 in your browser
- Check "Console" tab for JavaScript errors
- Check "Network" tab for failed requests

## 🆘 Getting Help

### When to Ask for Help

- You've tried the solutions above
- Error messages don't make sense
- Code works but behavior is unexpected

### What to Include

1. **Exact error message** (copy and paste)
2. **What you were trying to do**
3. **What you expected to happen**
4. **Your operating system** (Windows, Mac, Linux)
5. **Python version** (`python --version`)
6. **Relevant code** (the part that's not working)

### Where to Get Help

- Stack Overflow (tag with "python" and "pyramid")
- Pyramid community forums
- Python Discord servers
- Local Python meetups

## 🔄 Starting Fresh

If everything is broken and you want to start over:

```bash
# Stop the server (Ctrl+C)

# Delete database
rm tasks.db
rm tasks.db-journal

# Reinstall dependencies
pip install -r requirements.txt

# Restart server
python task.py
```

This gives you a clean slate!

## 📝 Prevention Tips

1. **Make small changes** - test after each change
2. **Keep backups** - copy working code before experimenting
3. **Read error messages** - they usually tell you what's wrong
4. **Test in browser** - always check if your changes work
5. **Use version control** - learn Git for better code management

---

**Remember: Every developer faces these issues! Don't get discouraged - debugging is part of learning! 🚀**

The key is to read error messages carefully, make small changes, and test frequently. You've got this! 💪