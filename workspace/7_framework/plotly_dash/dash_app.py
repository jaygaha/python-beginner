import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


def create_sample_data():
    """Create a sample DataFrame for the Dash app."""
    return pd.DataFrame(
        {
            "Category": ["A", "B", "C", "A", "B", "C"],
            "Values": [10, 15, 7, 12, 9, 8],
            "Type": ["X", "X", "X", "Y", "Y", "Y"],
        }
    )


def create_app_layout():
    """Define the layout for the Dash app."""
    return html.Div(
        [
            html.H1("My First Dash App", style={"textAlign": "center"}),
            html.Label("Select a Category Type:"),
            dcc.Dropdown(
                id="type-dropdown",
                options=[
                    {"label": "Type X", "value": "X"},
                    {"label": "Type Y", "value": "Y"},
                ],
                value="X",
                style={"width": "50%", "margin": "auto"},
            ),
            dcc.Graph(id="bar-graph"),
        ]
    )


def register_callbacks(app, df):
    """Register callbacks to update the graph based on dropdown selection."""

    @app.callback(Output("bar-graph", "figure"), [Input("type-dropdown", "value")])
    def update_graph(selected_type):
        """Update the bar graph based on the selected type."""
        filtered_df = df[df["Type"] == selected_type]
        fig = px.bar(
            filtered_df,
            x="Category",
            y="Values",
            title=f"Values for Type {selected_type}",
        )
        return fig


def main():
    """Initialize and run the Dash app."""
    app = Dash(__name__)
    df = create_sample_data()
    app.layout = create_app_layout()
    register_callbacks(app, df)
    app.run(debug=True)


if __name__ == "__main__":
    main()
