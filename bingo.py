from dash import Dash, html, Output, Input, callback, State, ctx
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import random

# Set grid size here - change this to 3, 5, 6, etc. for different grid sizes
GRID_SIZE = 5

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@900&display=swap');
            
            .meme-text {
                color: white !important;
                font-family: 'Roboto', sans-serif !important;
                font-weight: 900 !important;
                font-size: 20px !important;
                letter-spacing: 1px !important;
                -webkit-text-stroke: 2px black !important;
                text-stroke: 2px black !important;
                paint-order: stroke fill !important;
            }
            
            .bingo-button {
                background-color: rgba(0, 0, 0, 0.4) !important;
                backdrop-filter: blur(5px) !important;
                transition: all 0.3s ease !important;
            }
            
            .bingo-button:hover {
                background-color: rgba(128, 0, 128, 0.6) !important;
                transform: scale(1.05);
            }
            
            .refresh-button {
                background: none;
                border: none;
                font-size: 24px;
                opacity: 0.6;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .refresh-button:hover {
                opacity: 1;
                transform: rotate(180deg);
            }
            
            /* Added to ensure the page takes full height */
            html, body {
                height: 100%;
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

button_texts = [
    "Beat the level without taking damage",
    "Kill exactly 3 koopas",
    "Finish the level with a fireflower",
    "Level is only one screen wide",
    "Level contains exactly 5 blue pipes",
    "Level must be created by a German player",
    "Complete level using only duck-jumping",
    "Defeat Bowser without using power-ups",
    "Collect all 5 red coins",
    "Level can only use underground theme",
    "Beat level in under 30 seconds",
    "No jumping allowed",
    "Use shell bounces to progress",
    "Level must have exactly 7 enemies",
    "Start and end on a moving platform",
    "Complete level without touching the ground",
    "Use exactly 3 P-switches to progress",
    "Level must include a hidden vine path",
    "Beat level while carrying a koopa shell",
    "Survive a level with constant lava/saw blade threats",
    "Complete level using only Yoshi",
    "Defeat all enemies using only fireball throws",
    "Navigate entire level using only trampolines",
    "Beat level without collecting a single coin",
    "Finish level with less than 50 seconds on the timer",
    "Use cape flight to complete entire course",
    "Complete level by only moving right",
    "Survive level with constant falling platforms",
    "Beat Bowser Jr. without touching the ground",
    "Navigate a level filled with one-block gaps",
    "Complete level by using only koopa shells for movement",
    "Survive a level with continuous enemy spawns",
    "Beat level using exclusively spin jumps",
    "Navigate a level with zero ground contact",
    "Complete course while maintaining star power"
]


total_cells = GRID_SIZE * GRID_SIZE
if len(button_texts) < total_cells:
    button_texts = button_texts * (total_cells // len(button_texts) + 1)

def create_board():
    return random.sample(button_texts, total_cells)

initial_texts = create_board()

win_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Perfectly Balanced!", className="outlined-text")),
        dbc.ModalBody(html.Div([
            "Congratulations! You did it! You're the greatest gamer!",
            html.Div(id="win-type", className="mt-2 outlined-text")
        ])),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-modal", className="ml-auto")
        ),
    ],
    id="win-modal",
    is_open=False,
)

def create_grid(texts):
    grid = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            button_num = i * GRID_SIZE + j
            button = html.Div([
                html.Button(
                    texts[button_num],
                    id=f'btn-{button_num + 1}',
                    className='meme-text bingo-button',
                    style={
                        'width': '150px',
                        'height': '150px',
                        'margin': '5px',
                        'position': 'relative',
                        'border': '2px solid rgba(255, 255, 255, 0.5)',
                        'borderRadius': '10px',
                        'padding': '1px',
                        'wordWrap': 'break-word',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'textAlign': 'center',
                        'cursor': 'pointer',
                        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
                        'fontSize': '30px',
                    }
                ),
                html.Div(
                    '❌',
                    id=f'x-{button_num + 1}',
                    style={
                        'position': 'absolute',
                        'top': '50%',
                        'left': '50%',
                        'transform': 'translate(-50%, -50%)',
                        'fontSize': '30px',
                        'display': 'none',
                        'pointerEvents': 'none',
                        'textShadow': '0 0 10px gold'
                    }
                )
            ], style={'position': 'relative'})
            row.append(button)
        grid.append(html.Div(row, style={'display': 'flex', 'justifyContent': 'center'}))
    return grid

# Replace this URL with your actual image URL
background_image = "https://upload.wikimedia.org/wikipedia/commons/5/50/Doug_Thanos_%28cropped%29.jpg"

app.layout = html.Div([
    win_modal,
    html.Div(
        id='grid-container',
        children=create_grid(initial_texts),
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',  # Added to center vertically
            'padding': '20px',
            'borderRadius': '15px',
            'backgroundImage': f'url({background_image})',
            'backgroundSize': 'cover',
            'backgroundPosition': 'center',
            'backgroundRepeat': 'no-repeat',
            'minHeight': '100vh',
            'width': '100%',
            'backgroundColor': 'rgba(0, 0, 0, 0.3)',
            'backgroundBlendMode': 'overlay',
            'position': 'relative'
        }
    ),
    html.Button(
        "🔄",
        id="recreate-btn",
        className="refresh-button",
        style={
            'position': 'fixed',
            'bottom': '20px',
            'left': '20px',
            'zIndex': '1000'
        }
    ),
    html.Div(id='board-state', style={'display': 'none'}, children='0' * total_cells),
    html.Div(id='win-message', style={'display': 'none'})
], style={
    'height': '100vh',  # Make the container full height
    'display': 'flex',  # Use flexbox
    'flexDirection': 'column',  # Stack children vertically
    'justifyContent': 'center'  # Center children vertically
})


@callback(
    Output('grid-container', 'children'),
    Output('board-state', 'children'),
    Input('recreate-btn', 'n_clicks'),
    prevent_initial_call=False
)
def recreate_board(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return create_grid(create_board()), '0' * total_cells

@callback(
    [Output('board-state', 'children', allow_duplicate=True),
     Output('win-modal', 'is_open'),
     Output('win-type', 'children')],
    [Input(f'btn-{i}', 'n_clicks') for i in range(1, total_cells + 1)],
    State('board-state', 'children'),
    prevent_initial_call=True
)
def check_win(*args):
    n_clicks_list = args[:total_cells]
    current_state = list(args[total_cells])
    
    if ctx.triggered_id:
        button_idx = int(ctx.triggered_id.split('-')[1]) - 1
        current_state[button_idx] = '1' if n_clicks_list[button_idx] and n_clicks_list[button_idx] % 2 == 1 else '0'
    
    grid_state = [current_state[i:i+GRID_SIZE] for i in range(0, total_cells, GRID_SIZE)]
    win_message = "Congratulations, Doug! You did it! You're the greatest gamer!"
    # Check win conditions
    for row_idx, row in enumerate(grid_state):
        if all(cell == '1' for cell in row):
            return ''.join(current_state), True, f"You absolutely destroyed row {row_idx + 1}!"
    
    for col_idx in range(GRID_SIZE):
        if all(grid_state[row][col_idx] == '1' for row in range(GRID_SIZE)):
            return ''.join(current_state), True, f"You absolutely destroyed row column {col_idx + 1}!"
    
    if all(grid_state[i][i] == '1' for i in range(GRID_SIZE)):
        return ''.join(current_state), True, "You absolutely destroyed the diagonal ↘!"
    
    if all(grid_state[i][GRID_SIZE-1-i] == '1' for i in range(GRID_SIZE)):
        return ''.join(current_state), True, "You absolutely destroyed the diagonal ↙!"
    
    return ''.join(current_state), False, ""

@callback(
    Output('win-modal', 'is_open', allow_duplicate=True),
    Input('close-modal', 'n_clicks'),
    prevent_initial_call=True
)
def close_modal(n_clicks):
    return False

for i in range(1, total_cells + 1):
    @callback(
        Output(f'x-{i}', 'style'),
        Input(f'btn-{i}', 'n_clicks'),
        prevent_initial_call=True
    )
    def toggle_x(n_clicks, i=i):
        if n_clicks is None:
            return {'display': 'none'}
        
        style = {
            'position': 'absolute',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'fontSize': '50px',
            'pointerEvents': 'none',
            'textShadow': '0 0 10px gold',
            'animation': 'sparkle 1.5s infinite'
        }
        
        style['display'] = 'block' if n_clicks % 2 == 1 else 'none'
        return style

if __name__ == '__main__':
    app.run_server(debug=True, port="10000", host="0.0.0.0")
