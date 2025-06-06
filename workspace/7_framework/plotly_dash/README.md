# Plotly Dash Tutorial App

This is a beginner-friendly Plotly Dash application that demonstrates how to create an interactive web-based dashboard using Python. The app features a dropdown menu to filter data by type and displays a dynamic bar chart using Plotly Express. The code is formatted with Black and linted with Flake8 to ensure readability, consistency, and error-free development.

## Features
- Interactive dropdown to select between two data types ("X" or "Y").
- Dynamic bar chart that updates based on the selected type.
- Modular Python code following PEP 8 guidelines.
- Code formatting with Black for consistent style.
- Linting with Flake8 to catch errors and enforce coding standards.
- Simple sample dataset for demonstration.

## Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

## Installation
1. **Clone or Download the Repository**:
   - If using Git, clone the repository:
     ```bash
     git clone <repository-url>
     cd <repository-directory>
     ```
   - Alternatively, download the code and extract it to a directory.

2. **Install Dependencies**:
   Run the following command to install the required Python packages:
   ```bash
   pip install dash plotly pandas black flake8
   ```

## Code Formatting and Linting
To ensure code readability, consistency, and error reduction, this project uses:
- **Black**: An opinionated code formatter that enforces a consistent style.
- **Flake8**: A linter that checks for PEP 8 compliance and potential errors (e.g., unused variables).

### Setup and Usage
1. **Format Code with Black**:
   Run Black to automatically format `dash_tutorial.py`:
   ```bash
   black dash_tutorial.py
   ```
   Black will reformat the code to follow its style guidelines (e.g., consistent indentation, line lengths).

2. **Check Code with Flake8**:
   Run Flake8 to verify code quality and catch errors:
   ```bash
   flake8 dash_tutorial.py
   ```
   Flake8 will report any style violations or potential issues. Fix any reported errors manually if needed.

3. **Automate Formatting and Linting**:
   To streamline{keyword}format and lint before committing code to a repository, create a `.pre-commit` file:
   ```bash
   # .pre-commit
   - black dash_tutorial.py
   - flake8 dash_tutorial.py
   ```

## Usage
1. **Save the Code**:
   Ensure the main script (`dash_tutorial.py`) is in your working directory.

2. **Run the Application**:
   Execute the script to start the Dash server:
   ```bash
   python dash_tutorial.py
   ```

3. **View the App**:
   Open a web browser and navigate to `http://127.0.0.1:8050/`. You’ll see a dashboard with:
   - A title: "My First Dash App"
   - A dropdown menu to select "Type X" or "Type Y"
   - A bar chart that updates based on your selection

4. **Interact**:
   Use the dropdown to switch between data types and observe the bar chart update in real-time.

## Project Structure
- `dash_tutorial.py`: The main Python script containing the Dash app code, organized into modular functions.
- `README.md`: This file, providing documentation and instructions.

## Code Overview
The app is built using:
- **Dash**: For creating the web application framework.
- **Plotly Express**: For generating interactive bar charts.
- **Pandas**: For handling the sample dataset.
- **Modular Design**: The code is structured into functions (`create_sample_data`, `create_app_layout`, `register_callbacks`, `main`) for clarity and maintainability.
- **Black**: Ensures consistent code formatting (e.g., line lengths, indentation).
- **Flake8**: Enforces PEP 8 compliance and catches potential errors.

## Example
After running the app, select "Type X" from the dropdown to see a bar chart of values for categories A, B, and C. Switch to "Type Y" to update the chart with different data.

## Next Steps
- **Extend the App**: Add more interactive components like sliders or tables using Dash’s `dcc` module.
- **Use Real Data**: Replace the sample DataFrame in `create_sample_data` with your own dataset (e.g., from a CSV file).
- **Deploy**: Host the app on platforms like Heroku or Render for public access.

## Troubleshooting
- **Port Conflict**: If `http://127.0.0.1:8050/` is unavailable, another process may be using port 8050. Stop the conflicting process or change the port in `app.run_server(port=8051)`.
- **Dependencies**: Ensure all packages are installed correctly. Use `pip list` to verify.
- **Flake8 Errors**: If Flake8 reports issues, review the output and adjust the code (e.g., remove unused imports or fix line lengths).

## License
This project is licensed under the MIT License.

## Contact
For questions or feedback, feel free to reach out via [your-preferred-contact-method].