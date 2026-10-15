from dashboard.plots import kpi_card
from dashboard.utils import connect_to_database, fetch_query_results

from dash import Dash, html, dcc, Input, Output, callback

from dotenv import load_dotenv
import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / "infrastructure" / ".env"
load_dotenv(ENV_FILE)

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")



cursor = connect_to_database(POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD).cursor()


current_weight = fetch_query_results(cursor, "select * from gold.daily_user_measurements").ffill().iloc[-1]['avg_weight']
avg_weight_last_7d = fetch_query_results(
    cursor,
    """
    select
        avg(avg_weight)
    from gold.daily_user_measurements
    where local_date > CURRENT_DATE - 7
    """)['avg'].iloc[0]

avg_bf_last_7d = fetch_query_results(
    cursor,
    """
    select
        avg(avg_body_fat)
    from gold.daily_user_measurements
    where local_date > CURRENT_DATE - 7
    """)['avg'].iloc[0]


current_bf = fetch_query_results(cursor, "select * from gold.daily_user_measurements").ffill().iloc[-1]['avg_body_fat']


def overview_tab():
    current_weight_kpi = kpi_card(title="Current weight",
                                  kpi=current_weight,
                                  unit_suffix='kg')

    current_bf_kpi = kpi_card(title='Current BF%',
                              kpi = current_bf,
                              unit_suffix='%')

    avg_weight_last_7d_kpi = kpi_card(title="Avg weight (7d)",
                                      kpi = avg_weight_last_7d,
                                      unit_suffix='kg')

    avg_bf_last_7d_kpi = kpi_card(title='Avg BF% (7d)',
                              kpi = avg_bf_last_7d,
                              unit_suffix='%')
    
    output = html.Div(
        [
            current_weight_kpi, 
            current_bf_kpi,
            avg_weight_last_7d_kpi,
            avg_bf_last_7d_kpi
        ],
        style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px",
        }
    )
    
    return output

def nutrition_tab():
    pass

def activity_tab():
    pass

def sleep_tab():
    pass



def main():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        html.H1('Beautiful report!'),
        html.Div(),
        dcc.Tabs(id="tabs", value='overview', children=[
            dcc.Tab(label='Overview', value='overview'),
            dcc.Tab(label='Nutrition', value='nutrition'),
            dcc.Tab(label='Activity', value='activity'),
            dcc.Tab(label='Sleep', value='sleep'),
        ]),
        html.Div(id='tabs-content')
    ])

    @callback(Output('tabs-content', 'children'),
                Input('tabs', 'value'))
    def render_tabs(tab):
        TAB_DICT = {
            'overview' : overview_tab(),
            'nutrition' : nutrition_tab(),
            'activity' : activity_tab(),
            'sleep' : sleep_tab()
        }
        return TAB_DICT[tab]

    
    app.run(debug=False, host="0.0.0.0", port=7259)
    



if __name__ == '__main__':
    main()