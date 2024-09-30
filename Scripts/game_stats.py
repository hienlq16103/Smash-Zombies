import pygame
pygame.font.init()
# Cập nhật điểm số cho người chơi

class GameStat:
    """
    The GameStat class is responsible for tracking and displaying game statistics such as 
    hit count, miss count, hit-miss ratio, and score. 
    
    This class also provides methods to update the player's score and render the statistics 
    to the screen.
    """
    
    def __init__(self):
        """
        Initialize the GameStat class with default values for hit count, miss count, and score.

        Attributes:
        -----------
        __hit_count : int
            Number of successful hits made by the player.
        
        __miss_count : int
            Number of missed attempts made by the player.

        __score : int
            The current score based on the number of hits.
            
        __font : pygame.font.Font
            Font object used to render text on the screen. Initialized with default font 
            and size 36.
        """
        self.__hit_count = 0
        self.__miss_count = 0
        self.__score = 0
        # Font settings for displaying stats
        self.__font = pygame.font.Font(None, 36)

    @property
    def hit_miss_ratio(self):
        """
        Calculate and return the ratio of hits to misses.
        
        Returns:
        --------
        float:
            The ratio of hits to misses. If no misses are present, the ratio is equal to the number of hits.
        """
        if self.__miss_count == 0:
            return self.__hit_count
        return self.__hit_count / self.__miss_count

    def update_score(self, hit):
        """
        Update the score based on whether the player made a hit or a miss.

        Parameters:
        ------------
        hit : bool
            True if the player made a hit, False if the player missed.

        Behavior:
        ---------
        - If the player hits, the hit count is increased by 1, and the score is increased by 10 points.
        - If the player misses, the miss count is increased by 1.
        """
        if hit:
            self.__hit_count += 1
            self.__score += 10  # Increase score for each hit
        else:
            self.__miss_count += 1

    def display_stat(self, screen):
        """
        Render and display the current game statistics (hits, misses, hit-miss ratio, score) on the screen.

        Parameters:
        ------------
        screen : pygame.Surface
            The Pygame surface where the stats will be drawn.

        Behavior:
        ---------
        - Draws four text blocks on the screen: 
            1. Total hits
            2. Total misses
            3. Hit/Miss ratio
            4. Total score
        - The stats are drawn starting at coordinates (10, 10) with a vertical spacing of 40 pixels for each block.
        """
        # Render stats on the screen
        hit_text = self.__font.render(f"Hits: {self.__hit_count}", True, (89, 255, 255))
        miss_text = self.__font.render(f"Misses: {self.__miss_count}", True, (89, 255, 255))
        ratio_text = self.__font.render(f"Hit/Miss Ratio: {self.hit_miss_ratio:.2f}", True, (89, 255, 255))
        score_text = self.__font.render(f"Score: {self.__score}", True, (89, 255, 255))

        # Draw the stats onto the screen
        screen.blit(hit_text, (10, 10))
        screen.blit(miss_text, (10, 50))
        screen.blit(ratio_text, (10, 90))
        screen.blit(score_text, (10, 130))