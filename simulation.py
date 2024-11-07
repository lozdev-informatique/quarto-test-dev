from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import pandas as pd
import osmnx as ox
from matplotlib import pyplot as plt

def simulation(bikes_routes, start_date) :
    """
    Fonction pour créer une simulation des trajets dans Montpellier sur une journée.
    
    Paramètres :
    - bikes_routes : Liste des trajets de vélos sur une journée

    Retourne :
    - anim (FuncAnimation) : Animation simulant le traffic de vélo
    """

    # Création de la figure et des axes
    G = ox.graph_from_place('Montpellier, France', network_type='bike')
    fig, ax = ox.plot_graph(G, node_size=0, show=False, close=False)
    plt.subplots_adjust(bottom=0.25)  # Ajuster pour le slider

    # Configuration des axes
    x_values = []
    y_values = []
    for bike in bikes_routes:
        for point in bike['route']:
            x_values.append(point[0])
            y_values.append(point[1])

    ax.set_xlim(min(x_values) - 0.01, max(x_values) + 0.01)
    ax.set_ylim(min(y_values) - 0.01, max(y_values) + 0.01)

    # Créer les objets de vélo
    bike_objects = {bike['id']: ax.plot([], [], 'bo')[0] for bike in bikes_routes}

    def init():
        for bike in bike_objects.values():
            bike.set_data([], [])
        return bike_objects.values()

    def update(frame):
        # Met à jour la position des vélos en fonction du temps
        current_time = pd.Timestamp(f'{start_date} 00:00:00') + pd.Timedelta(minutes=15*frame)
        for bike in bikes_routes:
            departure = bike['departure_time']
            return_time = bike['return_time']
            route = bike['route']
            
            # Assurez-vous que les comparaisons se font entre Timestamp
            if departure <= current_time <= return_time and len(route) > 0:
                route_length = len(route)
                progress = (current_time - departure) / (return_time - departure)
                position_index = min(int(progress * (route_length - 1)), route_length - 1)
                current_position = route[position_index]
                x, y = current_position
                bike_objects[bike['id']].set_data([x], [y])
            else:
                bike_objects[bike['id']].set_data([], [])
        return bike_objects.values()

    # Lancement de l'animation et sauvegarde
    anim = FuncAnimation(fig, update, frames=96, init_func=init, blit=True, interval=100)
    plt.close()
    return anim