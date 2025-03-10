from settings import *
from meshes.chunk_mesh import ChunkMesh
import random
from terrain_gen import *

class Chunk:
    def __init__(self, world, position):
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True

        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum = self.app.player.frustum.is_on_frustum

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model
    
    def set_uniform(self):
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        voxels = np.zeros(CHUNK_VOL, dtype='uint8')

        # fill chunk
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
        
        # Compute player's chunk (outside @njit)
        player_x, _, player_z = PLAYER_POS  # Extract player's x and z
        player_chunk_x = int(player_x) // CHUNK_SIZE
        player_chunk_z = int(player_z) // CHUNK_SIZE

        self.generate_terrain(voxels, cx, cy, cz, player_chunk_x, player_chunk_z)
        
        if np.any(voxels):
            self.is_empty = False

        return voxels
    
    @staticmethod
    @njit
    def generate_terrain(voxels, cx, cy, cz, player_chunk_x, player_chunk_z):
        chunk_x = cx // CHUNK_SIZE
        chunk_z = cz // CHUNK_SIZE

        for x in range(CHUNK_SIZE):
            wx = x + cx
            for z in range(CHUNK_SIZE):
                wz = z + cz
                world_height = get_height(wx, wz)
                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)

                    # If this is the player's chunk, add a STONE border
                if chunk_x == player_chunk_x and chunk_z == player_chunk_z:
                        if ROAD_HEIGHT >= cy and (x < ROAD_WIDTH or x > CHUNK_SIZE - 1 - ROAD_WIDTH or z < ROAD_WIDTH or z > CHUNK_SIZE - 1 - ROAD_WIDTH):
                            road_y = ROAD_HEIGHT - cy
                            if 0 <= road_y < CHUNK_SIZE - 1:
                                voxels[get_index(x, road_y, z)] = STONE

