from dash import html

def kpi_card(
        title: str,
        kpi: float,
        previous:float=None, 
        unit_suffix:str='', 
        precision:int=2):

    kpi = round(kpi, precision)

    if previous:
        previous = round(previous, precision)
        diff = round(kpi - previous, precision)

        if diff > 0:
            diff_text = f"▲ +{diff} {unit_suffix}"
            diff_color = "#2ca02c"
        elif diff < 0:
            diff_text = f"▼ {diff} {unit_suffix}"
            diff_color = "#d62728"
        else:
            diff_text = "▬ 0"
            diff_color = "#ffffff"

    card_contents = [
                html.P(
                    str(title),
                    style={
                        "margin": "2px 0",
                        "fontSize": "18px",
                        "textAlign": "center",
                        "color": "#888",
                    },
                ),
                html.H2(
                    str(kpi) + f' {unit_suffix}',
                    style={
                        "margin": "0",
                        "fontSize": "42px",
                        "textAlign": "center",
                    },
                )
            ]
    if previous:
        previous_info = html.P(
                            f"Previous: {previous} {unit_suffix}",
                            style={
                                "margin": "2px 0",
                                "fontSize": "14px",
                                "textAlign": "center",
                                "color": "#888",
                            },
                        )
        diff_info = html.P(
                    diff_text,
                    style={
                        "margin": "0",
                        "fontSize": "16px",
                        "fontWeight": "bold",
                        "textAlign": "center",
                        "color": diff_color,
                    },
                )   
        card_contents.extend([previous_info, diff_info])
    
    card = html.Div(
        card_contents,
        style={
            "border": "1px solid rgba(255,255,255,0.1)",
            "borderRadius": "14px",
            "padding": "20px",
            "width": "180px",
            "boxShadow": "0 10px 30px rgba(0,0,0,0.3)",
            "backgroundColor": "rgba(255,255,255,0.05)",
            "backdropFilter": "blur(10px)",
            "color": "white",
        },
    )
    

    return html.Div(
        card,
        style={
            "display": "flex",
            "gap": "30px",
            "justifyContent": "center",
            "flexWrap": "wrap",
            "marginBottom": "120px",
        },
    )