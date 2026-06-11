import sys
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Circle
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QWidget, QPushButton,
    QHBoxLayout, QInputDialog, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QMouseEvent

class GraphEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.G = nx.DiGraph()  # Graphe orienté
        self.selected_node = None
        self.dragging_node = None
        self.pos = {}  # Positions des nœuds (pour l'affichage)
        self.init_ui()
        self.update_canvas()

    def init_ui(self):
        self.setWindowTitle("Éditeur de Graphes NetworkX")
        self.setGeometry(100, 100, 1000, 800)

        # Widget principal
        self.canvas = FigureCanvas(plt.Figure(figsize=(8, 6)))
        self.ax = self.canvas.figure.subplots()
        self.ax.set_axis_off()
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.mpl_connect("motion_notify_event", self.on_drag)
        self.canvas.mpl_connect("button_release_event", self.on_release)

        # Boutons
        self.add_node_btn = QPushButton("Ajouter un Nœud")
        self.add_node_btn.clicked.connect(self.add_node_dialog)

        self.add_edge_btn = QPushButton("Ajouter une Arête")
        self.add_edge_btn.clicked.connect(self.add_edge_dialog)

        self.save_btn = QPushButton("Sauvegarder (GraphML)")
        self.save_btn.clicked.connect(self.save_graph)

        self.load_btn = QPushButton("Charger (GraphML)")
        self.load_btn.clicked.connect(self.load_graph)

        self.clear_btn = QPushButton("Effacer Tout")
        self.clear_btn.clicked.connect(self.clear_graph)

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_node_btn)
        button_layout.addWidget(self.add_edge_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.clear_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(main_layout)
        self.setLayout(main_layout)

    def update_canvas(self):
        """Met à jour l'affichage du graphe."""
        self.ax.clear()
        self.ax.set_axis_off()

        # Dessiner les nœuds
        for node in self.G.nodes:
            x, y = self.pos.get(node, (0, 0))
            circle = Circle((x, y), 0.1, color="lightblue", ec="black", alpha=0.8)
            self.ax.add_patch(circle)
            self.ax.text(x, y, str(node), ha="center", va="center")

        # Dessiner les arêtes
        for u, v in self.G.edges:
            x1, y1 = self.pos.get(u, (0, 0))
            x2, y2 = self.pos.get(v, (0, 0))
            self.ax.arrow(x1, y1, x2 - x1, y2 - y1, head_width=0.05, color="gray", length_includes_head=True)

        self.canvas.draw()

    def on_click(self, event):
        """Gère les clics sur le canvas."""
        if event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return

        # Vérifier si on a cliqué sur un nœud
        clicked_node = None
        for node in self.pos:
            nx, ny = self.pos[node]
            if (nx - x) ** 2 + (ny - y) ** 2 <= 0.01:  # Rayon du nœud = 0.1
                clicked_node = node
                break

        if clicked_node:
            self.selected_node = clicked_node
            self.dragging_node = clicked_node
        else:
            self.selected_node = None

    def on_drag(self, event):
        """Gère le glissement de la souris pour déplacer les nœuds."""
        if self.dragging_node is None or event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return

        self.pos[self.dragging_node] = (x, y)
        self.update_canvas()

    def on_release(self, event):
        """Gère le relâchement de la souris."""
        self.dragging_node = None

    # Exemple pour ajouter une description à un nœud
    def add_node_dialog(self):
        node_name, ok = QInputDialog.getText(self, "Ajouter un Nœud", "Nom du nœud :")
        if not ok:
            return
        description, ok = QInputDialog.getText(self, "Description", "Description :")
        if ok:
            self.G.add_node(node_name, description=description)
            self.pos[node_name] = (0, 0)
            self.update_canvas()

    def add_edge_dialog(self):
        """Ouvre une boîte de dialogue pour ajouter une arête."""
        if len(self.G.nodes) < 2:
            QMessageBox.warning(self, "Erreur", "Il faut au moins 2 nœuds pour ajouter une arête.")
            return

        nodes = list(self.G.nodes)
        source, ok1 = QInputDialog.getItem(
            self, "Ajouter une Arête", "Nœud source :", nodes, 0, False
        )
        if not ok1:
            return

        target, ok2 = QInputDialog.getItem(
            self, "Ajouter une Arête", "Nœud cible :", nodes, 0, False
        )
        if not ok2:
            return

        if source == target:
            QMessageBox.warning(self, "Erreur", "Un nœud ne peut pas avoir d'arête vers lui-même.")
            return

        label, ok3 = QInputDialog.getText(
            self, "Ajouter une Arête", "Label de l'arête (optionnel) :", text=""
        )
        if ok3:
            self.G.add_edge(source, target, label=label)
            self.update_canvas()

    def save_graph(self):
        """Sauvegarde le graphe en GraphML."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder le Graphe", "", "GraphML Files (*.graphml);;All Files (*)"
        )
        if file_path:
            try:
                nx.write_graphml(self.G, file_path)
                QMessageBox.information(self, "Succès", f"Graphe sauvegardé dans {file_path}.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de la sauvegarde : {e}")

    def load_graph(self):
        """Charge un graphe depuis un fichier GraphML."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Charger le Graphe", "", "GraphML Files (*.graphml);;All Files (*)"
        )
        if file_path:
            try:
                self.G = nx.read_graphml(file_path)
                # Réinitialiser les positions (à améliorer : charger les positions aussi)
                self.pos = {node: (i * 0.2, 0) for i, node in enumerate(self.G.nodes)}
                self.update_canvas()
                QMessageBox.information(self, "Succès", f"Graphe chargé depuis {file_path}.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec du chargement : {e}")

    def clear_graph(self):
        """Efface le graphe actuel."""
        self.G.clear()
        self.pos = {}
        self.update_canvas()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphEditor()
    window.show()
    app.exec()