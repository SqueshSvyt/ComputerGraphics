import numpy as np


class Vertex:
    def __init__(self, position):
        self.position = np.array(position, dtype=np.float32)  # Vertex coordinates [x, y, z]
        self.half_edge = None  # Reference to an outgoing half-edge


class HalfEdge:
    def __init__(self, vertex):
        self.vertex = vertex  # Vertex at the end of this half-edge
        self.next = None  # Next half-edge in the face (counter-clockwise)
        self.opposite = None  # Opposite half-edge (if exists)
        self.face = None  # Face this half-edge belongs to


class Face:
    def __init__(self):
        self.half_edge = None  # Reference to one half-edge of this face


class HalfEdgeMesh:
    def __init__(self, vertices, faces):
        """
        Initialize a Half-Edge mesh from vertices and triangular faces.
        :param vertices: List of [x, y, z] coordinates (np.float32)
        :param faces: List of [v0, v1, v2] indices defining triangles (np.uint32)
        """
        self.vertices = []
        self.half_edges = []
        self.faces = []

        # Create vertices
        for pos in vertices:
            v = Vertex(pos)
            self.vertices.append(v)

        # Create faces and half-edges
        edge_map = {}  # Map (v0, v1) to half-edge for finding opposites
        for face_idx, (v0, v1, v2) in enumerate(faces):
            f = Face()
            self.faces.append(f)

            # Create three half-edges for the triangle
            he0 = HalfEdge(self.vertices[v0])
            he1 = HalfEdge(self.vertices[v1])
            he2 = HalfEdge(self.vertices[v2])

            # Link half-edges in a loop (counter-clockwise)
            he0.next = he1
            he1.next = he2
            he2.next = he0

            # Assign face to half-edges
            he0.face = f
            he1.face = f
            he2.face = f
            f.half_edge = he0

            # Assign outgoing half-edge to vertices (arbitrarily choose one)
            self.vertices[v0].half_edge = he0
            self.vertices[v1].half_edge = he1
            self.vertices[v2].half_edge = he2

            self.half_edges.extend([he0, he1, he2])

            # Map edges for finding opposites
            edge_map[(v0, v1)] = he0
            edge_map[(v1, v2)] = he1
            edge_map[(v2, v0)] = he2

        # Link opposite half-edges
        for (v0, v1), he in edge_map.items():
            if (v1, v0) in edge_map:
                he.opposite = edge_map[(v1, v0)]
                edge_map[(v1, v0)].opposite = he

    def get_vertices_faces(self):
        """Return vertices and faces for rendering."""
        vertices = np.array([v.position for v in self.vertices], dtype=np.float32)
        faces = []
        for f in self.faces:
            if f.half_edge:  # Only include faces that haven't been deleted
                he = f.half_edge
                v0 = self.vertices.index(he.vertex)
                v1 = self.vertices.index(he.next.vertex)
                v2 = self.vertices.index(he.next.next.vertex)
                faces.append([v0, v1, v2])
        return vertices, np.array(faces, dtype=np.uint32) if faces else np.array([], dtype=np.uint32)

    def delete_face(self, face_idx):
        """Delete a face and its half-edges."""
        if face_idx >= len(self.faces):
            return

        face = self.faces[face_idx]
        if not face.half_edge:
            return  # Already deleted

        # Mark half-edges as deleted
        he = face.half_edge
        for _ in range(3):
            if he.opposite:
                he.opposite.opposite = None  # Unlink opposite
            he = he.next

        # Remove the face
        he = face.half_edge
        for _ in range(3):
            next_he = he.next
            he.next = None
            he.face = None
            he = next_he
        face.half_edge = None
        self.faces[face_idx] = None  # Mark as deleted

    def transform_triangle(self, face_idx, translation=None, rotation=None, scale=None):
        """Transform a triangle by applying translation, rotation, and/or scaling."""
        if face_idx >= len(self.faces) or not self.faces[face_idx] or not self.faces[face_idx].half_edge:
            return

        # Get the vertices of the triangle
        face = self.faces[face_idx]
        he = face.half_edge
        vertices = [he.vertex, he.next.vertex, he.next.next.vertex]

        # Compute centroid for rotation/scaling
        centroid = np.mean([v.position for v in vertices], axis=0)

        # Apply transformations
        for vertex in vertices:
            pos = vertex.position

            # Translation
            if translation is not None:
                pos += np.array(translation, dtype=np.float32)

            # Rotation (around centroid)
            if rotation is not None:
                pos -= centroid  # Translate to origin (relative to centroid)
                rx, ry, rz = [np.radians(angle) for angle in rotation]
                # Rotate X
                x, y, z = pos
                pos = np.array([x, y * np.cos(rx) - z * np.sin(rx), y * np.sin(rx) + z * np.cos(rx)])
                # Rotate Y
                x, y, z = pos
                pos = np.array([x * np.cos(ry) + z * np.sin(ry), y, -x * np.sin(ry) + z * np.cos(ry)])
                # Rotate Z
                x, y, z = pos
                pos = np.array([x * np.cos(rz) - y * np.sin(rz), x * np.sin(rz) + y * np.cos(rz), z])
                pos += centroid  # Translate back

            # Scaling (relative to centroid)
            if scale is not None:
                pos = centroid + (pos - centroid) * np.array(scale, dtype=np.float32)

            vertex.position = pos