"""
Main game class and game logic.

This module contains the SpaceDefenderGame class which manages the overall
game state, entity updates, collision detection, and rendering.
"""

import pygame
import random
import math
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FONT_LARGE, FONT_MEDIUM, FONT_SMALL,
    WAVE_SIZE, TOTAL_WAVES, ASTEROID_BASE_SPEED, ENEMY_BASE_SPEED,
    ENEMY_SPAWN_RATE, POINTS_ASTEROID, POINTS_ENEMY, POINTS_WAVE_BONUS,
    Colors
)
from game_state import GameState
from entities import Player, Bullet, Asteroid, EnemyShip, Powerup


class SpaceDefenderGame:
    """
    Main game class for Space Defender.
    
    Manages game state, entity spawning, collision detection,
    and overall game logic.
    
    Attributes:
        screen: Pygame display surface
        clock: Pygame clock for FPS management
        game_state: Current game state (enum)
        player: Player spaceship instance
        bullets, asteroids, enemies: Lists of game entities
        score: Current game score
        current_wave: Current wave number
    """

    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Defender")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.MENU
        
        # Game entities
        self.player = None
        self.bullets = []
        self.enemy_bullets = []
        self.asteroids = []
        self.enemies = []
        self.powerups = []
        
        # Game state variables
        self.score = 0
        self.current_wave = 1
        self.enemies_spawned = 0
        self.enemies_killed_this_wave = 0
        self.spawn_timer = 0
        self.wave_start_display_timer = 0  # Timer to display wave start message
        
        # Fonts
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)

    def initialize_game(self):
        """Reset and initialize the game."""
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        self.bullets = []
        self.enemy_bullets = []
        self.asteroids = []
        self.enemies = []
        self.powerups = []
        self.score = 0
        self.current_wave = 1
        self.enemies_spawned = 0
        self.enemies_killed_this_wave = 0
        self.wave_start_display_timer = 120  # Show wave start message for 2 seconds
        self.game_state = GameState.PLAYING

    def handle_events(self):
        """Handle user input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.initialize_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                
                elif self.game_state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        # Only allow normal shooting (rapid fire handled separately)
                        if not self.player.is_rapid_fire_active():
                            bullet = self.player.fire_bullet()
                            self.bullets.append(bullet)
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.PAUSED
                
                elif self.game_state == GameState.PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.PLAYING
                    elif event.key == pygame.K_m:
                        self.game_state = GameState.MENU
                
                elif self.game_state in [GameState.GAME_OVER, GameState.GAME_WON]:
                    if event.key == pygame.K_SPACE:
                        self.game_state = GameState.MENU

    def get_pressed_keys(self) -> dict:
        """
        Get currently pressed keys relevant to gameplay.
        
        Returns:
            dict: Dictionary of key states
        """
        keys = pygame.key.get_pressed()
        return {
            'left': keys[pygame.K_LEFT] or keys[pygame.K_a],
            'right': keys[pygame.K_RIGHT] or keys[pygame.K_d],
            'shoot': keys[pygame.K_SPACE],
        }

    def spawn_enemies(self):
        """Spawn enemies based on wave number and spawn rate."""
        if self.game_state != GameState.PLAYING:
            return

        # Calculate spawn rate (increases with wave)
        spawn_rate = ENEMY_SPAWN_RATE + (self.current_wave - 1) * 0.5
        
        self.spawn_timer += 1
        if self.spawn_timer >= 60 / spawn_rate:
            self.spawn_timer = 0
            
            if self.enemies_spawned < WAVE_SIZE * self.current_wave:
                # 70% asteroids, 30% enemy ships
                if random.random() < 0.7:
                    x = random.randint(50, SCREEN_WIDTH - 50)
                    speed = ASTEROID_BASE_SPEED + (self.current_wave - 1) * 0.3
                    asteroid = Asteroid(x, -20, velocity=speed)
                    self.asteroids.append(asteroid)
                else:
                    x = random.randint(50, SCREEN_WIDTH - 50)
                    enemy = EnemyShip(x, -30, self.player.x, self.current_wave)
                    self.enemies.append(enemy)
                
                self.enemies_spawned += 1

    def update(self):
        """Update game state."""
        if self.game_state != GameState.PLAYING:
            return

        # Get input
        keys = self.get_pressed_keys()
        
        # Update player
        self.player.update(keys)
        self.player.update_rapid_fire()
        
        # Update wave start display timer
        if self.wave_start_display_timer > 0:
            self.wave_start_display_timer -= 1
        
        # Handle rapid fire shooting
        if keys.get('shoot') and self.player.is_rapid_fire_active():
            # Rapid fire: shoot every 5 frames while holding space
            if self.player.rapid_fire_counter % 5 == 0:
                bullet = self.player.fire_bullet()
                self.bullets.append(bullet)
        
        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.is_offscreen():
                self.powerups.remove(powerup)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_offscreen():
                self.bullets.remove(bullet)
        
        # Update asteroids
        for asteroid in self.asteroids[:]:
            asteroid.update()
            if asteroid.is_offscreen():
                self.asteroids.remove(asteroid)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player.x)
            # Enemy shooting in waves 3+
            if enemy.can_shoot():
                bullet = enemy.fire_bullet()
                if bullet:
                    self.enemy_bullets.append(bullet)
            if enemy.is_offscreen():
                self.enemies.remove(enemy)
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_offscreen():
                self.enemy_bullets.remove(bullet)

        # Check collisions: bullets with asteroids
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if self._check_collision(bullet, asteroid):
                    self.bullets.remove(bullet)
                    # Small chance of powerup drop (5%)
                    if random.random() < 0.05:
                        powerup_type = random.choice([Powerup.TYPE_RAPID_FIRE, Powerup.TYPE_INVINCIBILITY])
                        powerup = Powerup(asteroid.x, asteroid.y, powerup_type)
                        self.powerups.append(powerup)
                    self.asteroids.remove(asteroid)
                    self.score += POINTS_ASTEROID
                    break

        # Check collisions: bullets with enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if self._check_collision(bullet, enemy):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy.take_damage():
                        # Higher chance of powerup drop for enemies (15%)
                        if random.random() < 0.15:
                            powerup_type = random.choice([Powerup.TYPE_RAPID_FIRE, Powerup.TYPE_INVINCIBILITY])
                            powerup = Powerup(enemy.x, enemy.y, powerup_type)
                            self.powerups.append(powerup)
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        self.score += POINTS_ENEMY
                        self.enemies_killed_this_wave += 1
                    break

        # Check collisions: player with asteroids
        for asteroid in self.asteroids[:]:
            if self._check_collision(self.player, asteroid):
                self.player.take_damage()
                self.asteroids.remove(asteroid)
                if self.player.health <= 0:
                    self.game_state = GameState.GAME_OVER

        # Check collisions: player with enemies
        for enemy in self.enemies[:]:
            if self._check_collision(self.player, enemy):
                self.player.take_damage()
                if self.player.health <= 0:
                    self.game_state = GameState.GAME_OVER
        
        # Check collisions: player with enemy bullets
        for bullet in self.enemy_bullets[:]:
            if self._check_collision(self.player, bullet):
                self.player.take_damage()
                self.enemy_bullets.remove(bullet)
                if self.player.health <= 0:
                    self.game_state = GameState.GAME_OVER

        # Check collisions: player with powerups
        for powerup in self.powerups[:]:
            if self._check_collision(self.player, powerup):
                if powerup.powerup_type == Powerup.TYPE_RAPID_FIRE:
                    self.player.activate_rapid_fire(300)  # 5 seconds
                    self.score += 50
                elif powerup.powerup_type == Powerup.TYPE_INVINCIBILITY:
                    self.player.activate_invincibility(300)  # 5 seconds
                    self.score += 50
                self.powerups.remove(powerup)

        # Check wave completion
        if (self.enemies_spawned >= WAVE_SIZE * self.current_wave and
                len(self.enemies) == 0 and len(self.asteroids) == 0):
            
            if self.current_wave >= TOTAL_WAVES:
                self.game_state = GameState.GAME_WON
            else:
                self.current_wave += 1
                self.enemies_spawned = 0
                self.enemies_killed_this_wave = 0  # Reset for new wave
                self.wave_start_display_timer = 120  # Show wave start message
                self.score += POINTS_WAVE_BONUS
        
        # Spawn enemies
        self.spawn_enemies()

    def _check_collision(self, obj1, obj2) -> bool:
        """
        Check collision between two objects using bounding circles.
        
        Args:
            obj1: First object with rect attribute
            obj2: Second object with rect attribute
            
        Returns:
            bool: True if objects collide
        """
        dx = obj1.rect.centerx - obj2.rect.centerx
        dy = obj1.rect.centery - obj2.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Get radii
        r1 = getattr(obj1, 'radius', max(obj1.rect.width, obj1.rect.height) // 2)
        r2 = getattr(obj2, 'radius', max(obj2.rect.width, obj2.rect.height) // 2)
        
        return distance < r1 + r2

    def draw(self):
        """Render the game screen."""
        self.screen.fill(Colors.BLACK)

        if self.game_state == GameState.MENU:
            self._draw_menu()
        elif self.game_state == GameState.PLAYING:
            self._draw_game()
        elif self.game_state == GameState.PAUSED:
            self._draw_pause()
        elif self.game_state == GameState.GAME_OVER:
            self._draw_game_over()
        elif self.game_state == GameState.GAME_WON:
            self._draw_game_won()

        pygame.display.flip()

    def _draw_menu(self):
        """Draw the main menu screen."""
        title = self.font_large.render("SPACE DEFENDER", True, Colors.CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Instructions
        instructions = [
            "INSTRUCTIONS:",
            "LEFT/RIGHT ARROW or A D: Move",
            "SPACE: Fire bullets",
            "ESC: Pause game",
            "",
            "OBJECTIVES:",
            "- Destroy asteroids and enemy ships",
            "- Survive all 5 waves to win!",
            "",
            "SCORING:",
            "+10 pts asteroid | +25 pts enemy",
            "+50 pts wave bonus",
        ]

        y = 130
        for line in instructions:
            if line == "INSTRUCTIONS:" or line == "OBJECTIVES:" or line == "SCORING:":
                text = self.font_small.render(line, True, Colors.YELLOW)
            else:
                text = self.font_small.render(line, True, Colors.WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 24

        # Start prompt
        start_text = self.font_medium.render("Press SPACE to start", True, Colors.GREEN)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(start_text, start_rect)
        
        # Quit prompt
        quit_text = self.font_small.render("Press ESC to quit", True, Colors.GRAY)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.screen.blit(quit_text, quit_rect)

    def _draw_game(self):
        """Draw the game in progress."""
        # Draw entities
        self.player.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # Draw HUD
        self._draw_hud()

    def _draw_hud(self):
        """Draw heads-up display (score, health, wave)."""
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, Colors.WHITE)
        self.screen.blit(score_text, (10, 10))

        # Health
        health_text = self.font_medium.render(f"Health: {self.player.health}", True, Colors.RED)
        self.screen.blit(health_text, (SCREEN_WIDTH - 230, 10))

        # Wave
        wave_text = self.font_medium.render(f"Wave: {self.current_wave}/{TOTAL_WAVES}",
                                            True, Colors.CYAN)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, 10))
        self.screen.blit(wave_text, wave_rect)

        # Wave start message
        if self.wave_start_display_timer > 0:
            wave_start_text = self.font_large.render(f"Wave {self.current_wave} is starting...", True, Colors.CYAN)
            wave_start_rect = wave_start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(wave_start_text, wave_start_rect)

    def _draw_pause(self):
        """Draw the pause menu overlay."""
        # Draw the game in the background
        self._draw_game()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font_large.render("PAUSED", True, Colors.YELLOW)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(pause_text, pause_rect)

        # Instructions
        instructions = [
            "ESC: Resume game",
            "M: Return to menu",
        ]

        y = SCREEN_HEIGHT // 2 + 20
        for line in instructions:
            text = self.font_medium.render(line, True, Colors.WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 50

    def _draw_game_over(self):
        """Draw game over screen."""
        self._draw_game()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, Colors.RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)

        # Final score
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, Colors.WHITE)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, score_rect)

        # Wave reached
        wave_text = self.font_medium.render(f"Wave Reached: {self.current_wave}", True, Colors.CYAN)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(wave_text, wave_rect)

        # Restart prompt
        restart_text = self.font_small.render("Press SPACE to return to menu", True, Colors.GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(restart_text, restart_rect)

    def _draw_game_won(self):
        """Draw game won screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(Colors.BLACK)
        self.screen.blit(overlay, (0, 0))

        # Victory text
        victory_text = self.font_large.render("VICTORY!", True, Colors.GREEN)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(victory_text, victory_rect)

        # Final score
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, Colors.WHITE)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(final_score_text, score_rect)

        # Waves completed
        waves_text = self.font_medium.render("All waves defeated!", True, Colors.CYAN)
        waves_rect = waves_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(waves_text, waves_rect)

        # Restart prompt
        restart_text = self.font_small.render("Press SPACE to return to menu", True, Colors.GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(restart_text, restart_rect)

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
