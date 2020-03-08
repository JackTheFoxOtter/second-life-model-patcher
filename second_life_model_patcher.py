from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QFrame
from PyQt5.QtGui import QPalette, QColor
from styles.dark import getPalette
from PyQt5.QtCore import Qt, pyqtSlot
from xml.dom import minidom
from collada import Collada, geometry, source
import numpy as np
import sys
import os

class App(QWidget):
    lineEditPath1 = None
    lineEditPath2 = None
    valueLabels1 = []
    valueLabels2 = []
    offsetLineEdit1 = None
    offsetLineEdit2 = None
    meshLabel1 = None
    meshLabel2 = None
    mesh1 = None
    mesh2 = None

    def __init__(self):
        super().__init__()
        self.title = "Second Life Model Patcher V0.2 by JackTheFoxOtter"
        self.width = 800
        self.initUi()

    def initUi(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, 1)
        self.setFixedSize(0, 0)
        grid = QGridLayout()
        grid.setColumnMinimumWidth(1, 300)
        grid.setColumnMinimumWidth(3, 300)
        self.setLayout(grid)

        # Path input 1
        label = QLabel()
        label.setText("Primary Model")
        self.lineEditPath1 = QLineEdit()
        self.lineEditPath1.textChanged.connect(self.onTextChanged_lineEdit1)
        button = QPushButton("...", self)
        button.clicked.connect(self.onClick_chooseFile1)
        grid.addWidget(label, 0, 0, 1, 1, Qt.AlignLeft)
        grid.addWidget(self.lineEditPath1, 0, 1, 1, 3)
        grid.addWidget(button, 0, 4, 1, 1, Qt.AlignRight)
        # Path input 2
        label = QLabel()
        label.setText("Secondary Model")
        self.lineEditPath2 = QLineEdit()
        self.lineEditPath2.textChanged.connect(self.onTextChanged_lineEdit2)
        button = QPushButton("...", self)
        button.clicked.connect(self.onClick_chooseFile2)
        grid.addWidget(label, 1, 0, 1, 1, Qt.AlignLeft)
        grid.addWidget(self.lineEditPath2, 1, 1, 1, 3)
        grid.addWidget(button, 1, 4, 1, 1, Qt.AlignRight)
        # Horizontal spacer
        spacer = QFrame()
        spacer.setFrameShape(QFrame.HLine)
        spacer.setForegroundRole(QPalette.Base)
        grid.addWidget(spacer, 2, 0, 1, 5)
        # Model 1 info
        self.meshLabel1 = QLabel()
        self.meshLabel1.setText("Primary Model")
        self.meshLabel1.setForegroundRole(QPalette.Highlight)
        grid.addWidget(self.meshLabel1, 3, 0, 1, 2, Qt.AlignCenter)
        label = QLabel()
        grid.addWidget(label, 4, 0, 1, 2, Qt.AlignCenter)
        self.valueLabels1.append(label)
        label = QLabel()
        grid.addWidget(label, 5, 0, 1, 2, Qt.AlignCenter)
        self.valueLabels1.append(label)
        label = QLabel()
        grid.addWidget(label, 6, 0, 1, 2, Qt.AlignCenter)
        self.valueLabels1.append(label)
        label = QLabel()
        grid.addWidget(label, 7, 0, 1, 2, Qt.AlignCenter)
        self.valueLabels1.append(label)
        label = QLabel()
        grid.addWidget(label, 8, 0, 1, 2, Qt.AlignCenter)
        self.valueLabels1.append(label)
        label = QLabel()
        grid.addWidget(label, 9, 0, 1, 2, Qt.AlignCenter)
        self.valueLabels1.append(label)
        # Vertical spacer
        spacer = QFrame()
        spacer.setFrameShape(QFrame.VLine)
        spacer.setForegroundRole(QPalette.Base)
        grid.addWidget(spacer, 3, 2, 8, 1)
        # Model 2 info
        self.meshLabel2 = QLabel()
        self.meshLabel2.setText("Secondary Model")
        self.meshLabel2.setForegroundRole(QPalette.Highlight)
        grid.addWidget(self.meshLabel2, 3, 3, 1, 2, Qt.AlignCenter)
        label = QLabel()
        grid.addWidget(label, 4, 3, 1, 2, Qt.AlignCenter)
        self.valueLabels2.append(label)
        label = QLabel()
        grid.addWidget(label, 5, 3, 1, 2, Qt.AlignCenter)
        self.valueLabels2.append(label)
        label = QLabel()
        grid.addWidget(label, 6, 3, 1, 2, Qt.AlignCenter)
        self.valueLabels2.append(label)
        label = QLabel()
        grid.addWidget(label, 7, 3, 1, 2, Qt.AlignCenter)
        self.valueLabels2.append(label)
        label = QLabel()
        grid.addWidget(label, 8, 3, 1, 2, Qt.AlignCenter)
        self.valueLabels2.append(label)
        label = QLabel()
        grid.addWidget(label, 9, 3, 1, 2, Qt.AlignCenter)
        self.valueLabels2.append(label)
        # Offset Labels
        self.offsetLineEdit1 = QLineEdit()
        grid.addWidget(self.offsetLineEdit1, 10, 0, 1, 2)
        self.offsetLineEdit1.setReadOnly(True);
        self.offsetLineEdit1.setText("<0.0, 0.0, 0.0>")
        self.offsetLineEdit1.setAlignment(Qt.AlignCenter)
        self.offsetLineEdit2 = QLineEdit()
        grid.addWidget(self.offsetLineEdit2, 10, 3, 1, 2)
        self.offsetLineEdit2.setReadOnly(True);
        self.offsetLineEdit2.setText("<0.0, 0.0, 0.0>")
        self.offsetLineEdit2.setAlignment(Qt.AlignCenter)
        # Horizontal spacer
        spacer = QFrame()
        spacer.setFrameShape(QFrame.HLine)
        spacer.setForegroundRole(QPalette.Base)
        grid.addWidget(spacer, 11, 0, 1, 5)
        # Match Bounding Box Button
        button = QPushButton("Match Primary Bounding Box", self)
        button.clicked.connect(self.onClick_match)
        grid.addWidget(button, 12, 0, 1, 5)

        self.onTextChanged_lineEdit1()
        self.onTextChanged_lineEdit2()
        self.show()

        # DEBUG
        # self.lineEditPath1.setText('H:/#Google Sync/_Projects/_Second Life/_Objects/Modular Sci-Fi Rooms/Walls/Wall_Solid_LOD0.dae')
        # self.onClick_match()

    @pyqtSlot()
    def onClick_chooseFile1(self):
        file_path = self.openFileNameDialog("Choose Primary Model")
        if(file_path):
            self.lineEditPath1.setText(file_path)

    @pyqtSlot()
    def onClick_chooseFile2(self):
        file_path = self.openFileNameDialog("Choose Secondary Model")
        if(file_path):
            self.lineEditPath2.setText(file_path)

    @pyqtSlot()
    def onTextChanged_lineEdit1(self):
        text = self.lineEditPath1.text();
        validation_result = self.validateFilePath(text)
        if (not validation_result[0]):
            self.meshLabel1.setText(f"Primary Model (<font color=#FF4444>{validation_result[1]}</font>)")
            self.mesh1 = None
            self.clearCoordsLabels(self.valueLabels1)
            self.clearOffsetVector(self.offsetLineEdit1)
        else:
            self.meshLabel1.setText(f"Primary Model")
            self.mesh1 = Collada(text)
            coords = self.getBoundingCoordsFromCollada(self.mesh1)
            self.updateCoordsLabels(self.valueLabels1, coords)
            self.updateOffsetVector(self.offsetLineEdit1, coords)

    @pyqtSlot()
    def onTextChanged_lineEdit2(self):
        text = self.lineEditPath2.text();
        validation_result = self.validateFilePath(text)
        if (not validation_result[0]):
            self.meshLabel2.setText(f"Secondary Model (<font color=#FF4444>{validation_result[1]}</font>)")
            self.mesh2 = None
            self.clearCoordsLabels(self.valueLabels2)
            self.clearOffsetVector(self.offsetLineEdit2)
        else:
            self.meshLabel2.setText(f"Secondary Model")
            self.mesh2 = Collada(text)
            coords = self.getBoundingCoordsFromCollada(self.mesh2)
            self.updateCoordsLabels(self.valueLabels2, coords)
            self.updateOffsetVector(self.offsetLineEdit2, coords)

    @pyqtSlot()
    def onClick_match(self):
        print("Beginning matching process...")
        if (self.mesh1 == None or self.mesh2 == None):
            print("Both meshes have to be defined!")
            return
        elif (len(self.mesh2.geometries) != 1):
            print(f"Secondary mesh needs exactly 1 geometry, has {len(self.mesh2.geometries)}!")
            return
        elif (len(self.mesh2.geometries[0].primitives) < 1):
            print(f"Geometry of mesh needs to have at least one primitive, has 0!")
            return

        original_vertex_count = len(self.mesh2.geometries[0].primitives[0].vertex)
        print(f"Original number of vertices: {original_vertex_count}")
        bounds1 = self.getBoundingCoordsFromCollada(self.mesh1)
        bounds2 = self.getBoundingCoordsFromCollada(self.mesh2)

        # Check if bounding box of mesh2 is larger than that of mesh1. If it is, we can't inflate it to match mesh1's bounding box!
        if (bounds1[0] < bounds2[0] or bounds1[1] > bounds2[1] or
            bounds1[2] < bounds2[2] or bounds1[3] > bounds2[3] or
            bounds1[4] < bounds2[4] or bounds1[5] > bounds2[5]):
            print("Bounding box of secondary model exceeds bounding box of primary model on at least one axis!")
            print("Impossible to inflate bounding box of secondary model!")
            return

        # Calculate which vertices we need to inject to inflate the bounding box accordingly
        diff = [bounds1[0] != bounds2[0], bounds1[1] != bounds2[1],
                bounds1[2] != bounds2[2], bounds1[3] != bounds2[3],
                bounds1[4] != bounds2[4], bounds1[5] != bounds2[5]]
        print(f"Differences: {diff}")

        # If only one adjustment per axis (so either max or min per X,Y,Z) we only need one additional vertex to meet destination bounding box
        new_vertices = []
        if (int(diff[0]) + int(diff[1]) < 2 and int(diff[2]) + int(diff[3]) < 2 and int(diff[4]) + int(diff[5]) < 2):
            # One adjustment vertex required
            print("Requiring one adjustment vertex:")
            v = (bounds1[1] if (diff[1]) else bounds1[0], bounds1[3] if (diff[3]) else bounds1[2], bounds1[5] if (diff[5]) else bounds1[4])
            print(f"  Vertex -> {v}")
            new_vertices.append(v)

        else:
            # Two adjustment vertices required
            print("Requiring two adjustment vertices:")
            v1 = [bounds1[0], bounds1[2], bounds1[4]]
            v2 = [bounds1[1], bounds1[3], bounds1[5]]
            print(f"  Vertex 1 -> {v1}")
            print(f"  Vertex 2 -> {v2}")
            new_vertices.append(v1)
            new_vertices.append(v2)

        # Transfer and process all used sources from original mesh to new mesh
        sources = self.mesh2.geometries[0].primitives[0].sources # TODO Only from first primitive? Should this load sources from all if they aren't dublicates?
        new_sources = []
        input_list = source.InputList()
        mappings = {'VERTEX': ('X', 'Y', 'Z'),
                    'NORMAL': ('X', 'Y', 'Z'),
                    'TEXCOORD': ('S', 'T'),
                    'COLOR': ('R', 'G', 'B', 'A')} # TODO Add the mappings of the currently unsupported
        for key in sources:
            original_source = sources[key]
            if (len(original_source) > 0):
                original_source_id = original_source[0][2][1:]
                original_floats = np.array(original_source[0][4])
                if (key == 'VERTEX'):
                    # If the source type is vertex, add our adjustment vertex/vertices!
                    for new_vertex in new_vertices:
                        original_floats = np.append(original_floats, new_vertex)
                new_sources.append(source.FloatSource(original_source_id, original_floats, mappings[key]))
                input_list.addInput(len(input_list.getList()), key, f"#{original_source_id}")

        # Create modified geometry to replace original with
        geometry_id = self.mesh2.geometries[0].id
        geometry_name = self.mesh2.geometries[0].name
        geom = geometry.Geometry(self.mesh2, geometry_id, geometry_name, new_sources)

        # Primitive definition (how are the vertices connected to triangles)
        primitive_count = len(self.mesh2.geometries[0].primitives)
        for i in range(primitive_count):
            print(f"Processing primitive [{i+1}/{primitive_count}]...")
            material_id = self.mesh2.geometries[0].primitives[i].material
            indices = self.mesh2.geometries[0].primitives[i].indices
            if (i == 0):
                # Add the mapping data for our adjustment vertices
                # ('triangle' where each corner is the same adjustment vertex to have 0 face area)
                for new_vertex in new_vertices:
                    v = original_vertex_count + new_vertices.index(new_vertex)
                    data = [v] + ([0] * (len(new_sources)-1))
                    print(f"Adding new vertex {new_vertex} at index {v}")
                    indices = np.append(indices, [*data, *data, *data])
            triset = geom.createTriangleSet(indices, input_list, material_id)
            geom.primitives.append(triset)

        # Replace old geometry of mesh2 with new one
        print("Applying primitives to mesh...")
        del self.mesh2.geometries[0]
        self.mesh2.geometries.append(geom)

        # Save the modified mesh over the old file for the secondary mesh
        print(f"Done! New vertices ({len(self.mesh2.geometries[0].primitives[0].vertex)}): \n{self.mesh2.geometries[0].primitives[0].vertex}") # TODO Again, could other primitives hold more vertex data that's not dublicate? We don't take that into account!
        destination_path = f"{self.lineEditPath2.text()[:-4]}_patched.dae"
        print(f"Saving as '{destination_path}'...")
        self.mesh2.write(destination_path)

    def openFileNameDialog(self, title):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, title, "","Collada Models (*.dae);;All Files (*)", options=options)
        return fileName

    def validateFilePath(self, path):
        if (not path):
            return [False, "Not specified"]

        if os.path.isfile(path):
            split = os.path.splitext(path)
            if (len(split) == 2 and split[1] == ".dae"):
                return [True, ""]
            return [False, "Not a Collada File (*.dae)"]
        return [False, "File does not exist."]

    def getBoundingCoordsFromCollada(self, mesh):
        coords = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # MaxX, MinX, MaxY, MinY, MaxZ, MinZ
        # Set initial values from first vertex in primitive of geometry
        first_vertex = mesh.geometries[0].primitives[0].vertex[0]
        coords[0] = first_vertex[0]
        coords[1] = first_vertex[0]
        coords[2] = first_vertex[1]
        coords[3] = first_vertex[1]
        coords[4] = first_vertex[2]
        coords[5] = first_vertex[2]
        # Take all primitives of first geometry into account. (We only support having one geometry per file!)
        for primitive in mesh.geometries[0].primitives:
            vertices = primitive.vertex
            # Iterate through all other vertices and update coords values accordingly
            for i in range(len(vertices)-1):
                coords[0] = vertices[i][0] if (coords[0] < vertices[i][0]) else coords[0]
                coords[1] = vertices[i][0] if (coords[1] > vertices[i][0]) else coords[1]
                coords[2] = vertices[i][1] if (coords[2] < vertices[i][1]) else coords[2]
                coords[3] = vertices[i][1] if (coords[3] > vertices[i][1]) else coords[3]
                coords[4] = vertices[i][2] if (coords[4] < vertices[i][2]) else coords[4]
                coords[5] = vertices[i][2] if (coords[5] > vertices[i][2]) else coords[5]

        return coords

    def clearCoordsLabels(self, labels):
        for i in range(len(labels)):
            labels[i].setText("")

    def updateCoordsLabels(self, labels, coords):
        coordinateLabels = [
            "Max <font color=#EE2222><b>X</b></font>: ",
            "Min <font color=#EE2222><b>X</b></font>: ",
            "Max <font color=#22EE22><b>Y</b></font>: ",
            "Min <font color=#22EE22><b>Y</b></font>: ",
            "Max <font color=#2222EE><b>Z</b></font>: ",
            "Min <font color=#2222EE><b>Z</b></font>: "
        ]

        for i in range(len(labels)):
            labels[i].setText(coordinateLabels[i] + str(coords[i]))

    def clearOffsetVector(self, lineEdit):
        lineEdit.setText("")

    def updateOffsetVector(self, lineEdit, coords):
        offsetX = round((coords[1] + coords[0])/2, 5)
        offsetY = round((coords[3] + coords[2])/2, 5)
        offsetZ = round((coords[5] + coords[4])/2, 5)
        # offsetX = (coords[1] + coords[0])/2
        # offsetY = (coords[3] + coords[2])/2
        # offsetZ = (coords[5] + coords[4])/2
        lineEdit.setText(f"<{offsetX}, {offsetY}, {offsetZ}>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(getPalette())
    widget = App()
    sys.exit(app.exec_())
