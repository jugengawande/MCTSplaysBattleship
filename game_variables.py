
# Grid Variables

class Settings:
    
    
    SQUARE = 50
    GRID_SIZE = 5

    #Theme Colors
    BLACK = (9, 11, 11)
    BLUE = (70,172,194)
    ORANGE = (205, 83, 52)
    YELLOW = (247, 179, 43,255)
    GREEN = (189, 191, 9)
    NAVY = (4, 36, 57, 150)

    GREY_1 = (18, 22, 22)
    GREY_2 = (67, 86, 96)
    GREY_3 = (37, 45, 45)

    PINK = (140, 33, 85)
    PURPLE = (57, 43, 88)

    NEON = (49, 203, 0)

    # Fleet 

    ship_sizes = {
    5: [2,3,4],
    7: [2,3,4],
    10: [2,3,4,5],
    12: [2,3,4,4,5],
    15: [2,3,3,4,4,5]
}

    search_colors = {
        -1 : BLACK,
        1 : YELLOW,
        0 : NAVY ,
        100: ORANGE,
    }
    

    @property
    def Fleet(self) -> list:
        return self.ship_sizes
        
    # @Fleet.setter
    # def Fleet(self, fleet_array ):
    #     self.ship_sizes = list(fleet_array)
    
    @property
    def GridSize(self):
        return Settings.GRID_SIZE
    
    @GridSize.setter
    def GridSize(self, size):
        if size > 0:
            Settings.GRID_SIZE = size
    

    @staticmethod
    def WORLD_SIZE():
        return Settings.GRID_SIZE * Settings.GRID_SIZE

    # Display Window
    @staticmethod
    def GRID_DIM():
        return (Settings.SQUARE * Settings.GRID_SIZE * 2 + 3 * Settings.SQUARE, Settings.SQUARE * Settings.GRID_SIZE * 2 + 3 * Settings.SQUARE)
    
    @staticmethod 
    def COMPETE_GRID_DIM():
        return (Settings.SQUARE * Settings.GRID_SIZE * 2 + 3 * Settings.SQUARE, Settings.SQUARE * Settings.GRID_SIZE + 2 * Settings.SQUARE)