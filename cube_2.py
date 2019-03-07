import numpy as np

class RubiksCube():
    def __init__(self):
        # Initialize state with proper shape of 2x2x2 Rubik's Cube
        self.cube = np.zeros((6, 2, 2), dtype=np.float32)

        # Dictionary for performing actions
        self.actions_map = {0: self.horizontal_cw,
                            1: self.horizontal_ccw,
                            2: self.vertical_cw,
                            3: self.vertical_ccw,
                            4: self.planar_cw,
                            5: self.planar_ccw}

        # Human readable dictionary for mapping actions to index of action
        self.actions = {'horizontal_cw': 0,
                        'horizontal_ccw': 1,
                        'vertical_cw': 2,
                        'vertical_ccw': 3,
                        'planar_cw': 4,
                        'planar_ccw': 5}

        # 3D interpretation of which 2x2 face corresponds to the faces on a 2x2x2 Rubik's Cube
        self.faces = {'Front': 0,
                      'Top': 1,
                      'Back': 2,
                      'Bottom': 3,
                      'Right': 4,
                      'Left': 5}

        self.num_actions = len(self.actions_map)

    def reset(self):
        cube_index_short = np.arange(0, self.cube.shape[0]*self.cube.shape[1]*self.cube.shape[2]-3, 1, dtype=np.int32)
        cube_index_short[10:] += 1
        cube_index_short[14:] += 1
        cube_index_short[17:] += 1
        np.random.shuffle(cube_index_short)
        cube_index = np.zeros(self.cube.shape[0]*self.cube.shape[1]*self.cube.shape[2], dtype=np.int32)
        j = 0
        for i in range(cube_index.shape[0]):
            if i != 10 and i != 15 and i != 19:
                cube_index[i] = cube_index_short[j]
                j += 1

        cube_index[10] = 10
        cube_index[15] = 15
        cube_index[19] = 19
        cube = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5])
        count = 0
        for i in range(self.cube.shape[0]):
            for j in range(self.cube.shape[1]):
                for k in range(self.cube.shape[2]):
                    self.cube[i, j, k] = cube[cube_index[count]]
                    count += 1

        # Solved initial condition for debugging purposes
        #self.cube = np.array([[[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]]])

        # Decimal labels are for debugging purposes to have uniqueness for each square
        #self.cube = np.array([[[0.0, 0.1], [0.2, 0.3]], [[1.0, 1.1], [1.2, 1.3]], [[2.0, 2.1], [2.2, 2.3]], [[3.0, 3.1], [3.2, 3.3]], [[4.0, 4.1], [4.2, 4.3]], [[5.0, 5.1], [5.2, 5.3]]])

        self.done = False

        # Number of steps variable
        self.t = 0

        return self.cube

    def step(self, action):
        # Perform action using action dictionary
        self.actions_map[action]()

        # Increase steps taken by one
        self.t += 1

        # Check to see if Rubik's Cube is solved (All squares on a face match for all faces)
        check = np.zeros(6, dtype=np.int32)
        for i in range(6):
            face = self.cube[i]
            if face[0, 0] == face[0, 1] and face[0, 0] == face[1, 0] and face[0, 0] == face[1, 1]:
                check[i] = 1

        if np.sum(check) == 6:
            reward = 0
            self.done = True

        # Check to see if maximum number of steps has been reached
        elif self.t == 100:
            reward = -1
            self.done = True

        elif not self.done:
            reward = -1

        else:
            print('Game has already ended due to number of steps or solve conditions. Please reset the environment to play again.')
            reward = -1

        return self.cube, reward, self.done, {}

    # Rotate top half in the clockwise direction
    def horizontal_cw(self):
        new_cube = np.zeros(self.cube.shape, dtype=np.float32)
        for i in range(self.cube.shape[0]):
            for j in range(self.cube.shape[1]):
                for k in range(self.cube.shape[2]):
                    new_cube[i, j, k] = self.cube[i, j, k]

        new_cube[0, 0] = self.cube[4, 0]

        new_cube[1, 0, 0] = self.cube[1, 1, 0]
        new_cube[1, 0, 1] = self.cube[1, 0, 0]
        new_cube[1, 1, 0] = self.cube[1, 1, 1]
        new_cube[1, 1, 1] = self.cube[1, 0, 1]

        new_cube[2, 0] = self.cube[5, 0]

        new_cube[4, 0] = self.cube[2, 0]

        new_cube[5, 0] = self.cube[0, 0]

        self.cube = new_cube

    # Rotate top half in the counter-clockwise direction
    def horizontal_ccw(self):
        new_cube = np.zeros(self.cube.shape, dtype=np.float32)
        for i in range(self.cube.shape[0]):
            for j in range(self.cube.shape[1]):
                for k in range(self.cube.shape[2]):
                    new_cube[i, j, k] = self.cube[i, j, k]

        new_cube[0, 0] = self.cube[5, 0]

        new_cube[1, 0, 0] = self.cube[1, 0, 1]
        new_cube[1, 0, 1] = self.cube[1, 1, 1]
        new_cube[1, 1, 0] = self.cube[1, 0, 0]
        new_cube[1, 1, 1] = self.cube[1, 1, 0]

        new_cube[2, 0] = self.cube[4, 0]

        new_cube[4, 0] = self.cube[0, 0]

        new_cube[5, 0] = self.cube[2, 0]

        self.cube = new_cube

    # Rotate left half in the clockwise direction
    def vertical_cw(self):
        new_cube = np.zeros(self.cube.shape, dtype=np.float32)
        for i in range(self.cube.shape[0]):
            for j in range(self.cube.shape[1]):
                for k in range(self.cube.shape[2]):
                    new_cube[i, j, k] = self.cube[i, j, k]

        new_cube[0, 0, 0] = self.cube[1, 0, 0]
        new_cube[0, 1, 0] = self.cube[1, 1, 0]

        new_cube[1, 0, 0] = self.cube[2, 0, 0]
        new_cube[1, 1, 0] = self.cube[2, 1, 0]

        new_cube[2, 0, 0] = self.cube[3, 0, 0]
        new_cube[2, 1, 0] = self.cube[3, 1, 0]

        new_cube[3, 0, 0] = self.cube[0, 0, 0]
        new_cube[3, 1, 0] = self.cube[0, 1, 0]

        new_cube[5, 0, 0] = self.cube[5, 1, 0]
        new_cube[5, 0, 1] = self.cube[5, 0, 0]
        new_cube[5, 1, 0] = self.cube[5, 1, 1]
        new_cube[5, 1, 1] = self.cube[5, 0, 1]

        self.cube = new_cube

    # Rotate left half in the counter-clockwise direction
    def vertical_ccw(self):
        new_cube = np.zeros(self.cube.shape, dtype=np.float32)
        for i in range(self.cube.shape[0]):
            for j in range(self.cube.shape[1]):
                for k in range(self.cube.shape[2]):
                    new_cube[i, j, k] = self.cube[i, j, k]

        new_cube[0, 0, 0] = self.cube[3, 0, 0]
        new_cube[0, 1, 0] = self.cube[3, 1, 0]

        new_cube[1, 0, 0] = self.cube[0, 0, 0]
        new_cube[1, 1, 0] = self.cube[0, 1, 0]

        new_cube[2, 0, 0] = self.cube[1, 0, 0]
        new_cube[2, 1, 0] = self.cube[1, 1, 0]

        new_cube[3, 0, 0] = self.cube[2, 0, 0]
        new_cube[3, 1, 0] = self.cube[2, 1, 0]

        new_cube[5, 0, 0] = self.cube[5, 0, 1]
        new_cube[5, 0, 1] = self.cube[5, 1, 1]
        new_cube[5, 1, 0] = self.cube[5, 0, 0]
        new_cube[5, 1, 1] = self.cube[5, 1, 0]

        self.cube = new_cube

    # Rotate front half in the clockwise direction
    def planar_cw(self):
        new_cube = np.zeros(self.cube.shape, dtype=np.float32)
        for i in range(self.cube.shape[0]):
            for j in range(self.cube.shape[1]):
                for k in range(self.cube.shape[2]):
                    new_cube[i, j, k] = self.cube[i, j, k]

        new_cube[0, 0, 0] = self.cube[0, 1, 0]
        new_cube[0, 0, 1] = self.cube[0, 0, 0]
        new_cube[0, 1, 0] = self.cube[0, 1, 1]
        new_cube[0, 1, 1] = self.cube[0, 0, 1]

        new_cube[1, 1, 0] = self.cube[5, 1, 1]
        new_cube[1, 1, 1] = self.cube[5, 0, 1]

        new_cube[3, 0, 0] = self.cube[4, 1, 0]
        new_cube[3, 0, 1] = self.cube[4, 0, 0]

        new_cube[4, 0, 0] = self.cube[1, 1, 0]
        new_cube[4, 1, 0] = self.cube[1, 1, 1]

        new_cube[5, 0, 1] = self.cube[3, 0, 0]
        new_cube[5, 1, 1] = self.cube[3, 0, 1]

        self.cube = new_cube

    # Rotate front half in the counter-clockwise direction
    def planar_ccw(self):
        new_cube = np.zeros(self.cube.shape, dtype=np.float32)
        for i in range(self.cube.shape[0]):
            for j in range(self.cube.shape[1]):
                for k in range(self.cube.shape[2]):
                    new_cube[i, j, k] = self.cube[i, j, k]

        new_cube[0, 0, 0] = self.cube[0, 0, 1]
        new_cube[0, 0, 1] = self.cube[0, 1, 1]
        new_cube[0, 1, 0] = self.cube[0, 0, 0]
        new_cube[0, 1, 1] = self.cube[0, 1, 0]

        new_cube[1, 1, 0] = self.cube[4, 0, 0]
        new_cube[1, 1, 1] = self.cube[4, 1, 0]

        new_cube[3, 0, 0] = self.cube[5, 0, 1]
        new_cube[3, 0, 1] = self.cube[5, 1, 1]

        new_cube[4, 0, 0] = self.cube[3, 0, 1]
        new_cube[4, 1, 0] = self.cube[3, 0, 0]

        new_cube[5, 0, 1] = self.cube[1, 1, 1]
        new_cube[5, 1, 1] = self.cube[1, 1, 0]

        self.cube = new_cube
