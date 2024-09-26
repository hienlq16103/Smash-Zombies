import pygame
pygame.font.init()
# Điểm số
class GameStat:
    def __init__(self):
        self.hit_count = 0
        self.miss_count = 0
        self.score = 0
        # Font settings for displaying stats
        self.font = pygame.font.Font(None, 36)

    @property
    def hit_miss_ratio(self):
        if self.miss_count == 0:
            return self.hit_count
        return self.hit_count / self.miss_count

    def update_score(self, hit):
        if hit:
            self.hit_count += 1
            self.score += 10  # Increase score for each hit
        else:
            self.miss_count += 1

    def display_stat(self, screen):
        # Render stats on the screen
        hit_text = self.font.render(f"Hits: {self.hit_count}", True, (89, 255, 255))
        miss_text = self.font.render(f"Misses: {self.miss_count}", True, (89, 255, 255))
        ratio_text = self.font.render(f"Hit/Miss Ratio: {self.hit_miss_ratio:.2f}", True, (89, 255, 255))
        score_text = self.font.render(f"Score: {self.score}", True, (89, 255, 255))

        # Draw the stats onto the screen
        screen.blit(hit_text, (10, 10))
        screen.blit(miss_text, (10, 50))
        screen.blit(ratio_text, (10, 90))
        screen.blit(score_text, (10, 130))

