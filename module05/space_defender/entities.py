"""
Game entity classes - Player, Bullet, Asteroid, and Enemy.

This module contains all drawable game entities including the player spaceship,
bullets, asteroids, and enemy ships. Each class handles its own rendering,
movement, and collision detection.
"""

import pygame
import random
import math
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, BULLET_SPEED,
    ASTEROID_BASE_SPEED, ENEMY_BASE_SPEED, MAX_HEALTH, INVINCIBLE_DURATION,
    Colors
)


class Player(pygame.sprite.Sprite):
    """
    Player spaceship class.
    
    The player controls a spaceship at the bottom of the screen.
    Can move left/right and fire bullets upward.
    
    Attributes:
        x, y: Position coordinates
        width, height: Sprite dimensions
        velocity_x: Horizontal movement speed
        health: Current health points
        invincible_counter: Frames of invincibility remaining
    """

    def __init__(self, x: float, y: float):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.velocity_x = 0
        
        # Create player sprite (triangle pointing up)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_player()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Game mechanics
        self.health = MAX_HEALTH
        self.invincible_counter = 0
        self.invincible_duration = INVINCIBLE_DURATION
        self.rapid_fire_counter = 0
        self.rapid_fire_duration = 0  # 0 means not active

    def _draw_player(self):
        """Draw the player spaceship as a triangle."""
        # Clear surface
        self.image.fill((0, 0, 0, 0))
        
        # Draw triangle (spaceship)
        points = [
            (self.width // 2, 0),           # Top point
            (0, self.height),                # Bottom left
            (self.width, self.height)        # Bottom right
        ]
        pygame.draw.polygon(self.image, Colors.GREEN, points)
        
        # Draw cockpit
        pygame.draw.circle(self.image, Colors.CYAN, (self.width // 2, 15), 3)

    def update(self, keys: dict):
        """
        Update player position based on input.
        
        Args:
            keys: Dictionary of pressed keys
        """
        # Handle input
        if keys.get('left'):
            self.velocity_x = -PLAYER_SPEED
        elif keys.get('right'):
            self.velocity_x = PLAYER_SPEED
        else:
            self.velocity_x = 0

        # Update position
        self.x += self.velocity_x
        
        # Boundary collision
        if self.x < self.width // 2:
            self.x = self.width // 2
        elif self.x > SCREEN_WIDTH - self.width // 2:
            self.x = SCREEN_WIDTH - self.width // 2

        # Update rect
        self.rect.centerx = self.x
        self.rect.centery = self.y

        # Update invincibility
        if self.invincible_counter > 0:
            self.invincible_counter -= 1

        # Flash effect when invincible
        if self.invincible_counter > 0 and self.invincible_counter % 10 < 5:
            temp_image = self.image.copy()
            temp_image.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = temp_image
        else:
            self._draw_player()

    def fire_bullet(self) -> 'Bullet':
        """
        Create and return a bullet fired by the player.
        
        Returns:
            Bullet: A new bullet object
        """
        return Bullet(self.x, self.y - self.height // 2, 0, -BULLET_SPEED)
    
    def activate_rapid_fire(self, duration: int = 300):
        """Activate rapid fire mode (5 seconds = 300 frames at 60 FPS)."""
        self.rapid_fire_counter = 0
        self.rapid_fire_duration = duration
    
    def activate_invincibility(self, duration: int = 300):
        """Activate extended invincibility from powerup (5 seconds = 300 frames at 60 FPS)."""
        self.invincible_counter = duration
    
    def is_rapid_fire_active(self) -> bool:
        """Check if rapid fire is currently active."""
        return self.rapid_fire_duration > 0
    
    def update_rapid_fire(self):
        """Update rapid fire state."""
        if self.rapid_fire_duration > 0:
            self.rapid_fire_counter += 1
            self.rapid_fire_duration -= 1

    def take_damage(self):
        """Reduce health and apply invincibility frames."""
        if self.invincible_counter <= 0:
            self.health -= 1
            self.invincible_counter = self.invincible_duration

    def draw(self, surface: pygame.Surface):
        """Draw the player sprite."""
        surface.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    """
    Bullet class for projectiles fired by the player.
    
    Can move in any direction based on velocity components.
    
    Attributes:
        x, y: Position coordinates
        vel_x, vel_y: Velocity components
        radius: Collision radius
    """

    def __init__(self, x: float, y: float, vel_x: float, vel_y: float, color: tuple = Colors.YELLOW):
        super().__init__()
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = 3
        self.color = color
        
        # Create bullet sprite
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        """Update bullet position."""
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (self.x, self.y)

    def is_offscreen(self) -> bool:
        """Check if bullet has left the screen."""
        return (self.x < -self.radius or self.x > SCREEN_WIDTH + self.radius or
                self.y < -self.radius or self.y > SCREEN_HEIGHT + self.radius)

    def draw(self, surface: pygame.Surface):
        """Draw the bullet sprite."""
        surface.blit(self.image, self.rect)


class Asteroid(pygame.sprite.Sprite):
    """
    Asteroid enemy class.
    
    Asteroids move downward and must be destroyed by bullets.
    Destroying asteroids awards points.
    
    Attributes:
        x, y: Position coordinates
        size: Asteroid size (1=large, 2=medium, 3=small)
        radius: Collision radius
        vel_x, vel_y: Velocity components
        rotation: Current rotation angle
        rotation_speed: Rate of rotation
    """

    def __init__(self, x: float, y: float, size: int = 1, velocity: float = None):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size  # 1 = large, 2 = medium, 3 = small
        self.radius = 20 - (size - 1) * 7
        self.vel_y = velocity if velocity is not None else ASTEROID_BASE_SPEED
        self.vel_x = random.uniform(-1, 1)
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)
        
        # Create asteroid sprite
        self._create_image()

    def _create_image(self):
        """Create an irregular asteroid shape."""
        size = self.radius * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Create irregular polygon for asteroid
        points = []
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            distance = self.radius * random.uniform(0.7, 1.0)
            x = self.radius + distance * math.cos(angle)
            y = self.radius + distance * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(self.image, Colors.GRAY, points)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        """Update asteroid position and rotation."""
        self.x += self.vel_x
        self.y += self.vel_y
        self.rotation += self.rotation_speed
        
        # Wrap around screen horizontally
        if self.x < -self.radius:
            self.x = SCREEN_WIDTH + self.radius
        elif self.x > SCREEN_WIDTH + self.radius:
            self.x = -self.radius
        
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def is_offscreen(self) -> bool:
        """Check if asteroid has fallen below the screen."""
        return self.y > SCREEN_HEIGHT + self.radius

    def draw(self, surface: pygame.Surface):
        """Draw the asteroid sprite."""
        surface.blit(self.image, self.rect)


class EnemyShip(pygame.sprite.Sprite):
    """
    Enemy spaceship class.
    
    Enemy ships move downward and toward the player.
    They have more health than asteroids and award more points.
    
    Attributes:
        x, y: Position coordinates
        width, height: Sprite dimensions
        health: Current health points
        player_x: Tracked player x position
        vel_x, vel_y: Velocity components
    """

    def __init__(self, x: float, y: float, player_x: float = SCREEN_WIDTH // 2, wave: int = 1):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 35
        self.height = 40
        self.health = 2
        self.player_x = player_x
        self.wave = wave
        
        # Create enemy sprite (triangle pointing down)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_enemy()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Movement
        self.vel_y = ENEMY_BASE_SPEED
        self.vel_x = 0
        self.move_timer = 0
        self.move_change_interval = random.randint(20, 50)
        
        # Shooting (only in waves 3+)
        self.shoot_timer = 0
        self.shoot_interval = random.randint(60, 120) if wave >= 3 else float('inf')

    def _draw_enemy(self):
        """Draw the enemy spaceship."""
        self.image.fill((0, 0, 0, 0))
        
        # Draw inverted triangle (enemy)
        points = [
            (0, 0),                      # Top left
            (self.width, 0),             # Top right
            (self.width // 2, self.height)  # Bottom point
        ]
        pygame.draw.polygon(self.image, Colors.RED, points)
        
        # Draw cockpit
        pygame.draw.circle(self.image, Colors.YELLOW, (self.width // 2, 20), 2)

    def update(self, player_x: float = None):
        """
        Update enemy position.
        
        Args:
            player_x: Current player x position for tracking
        """
        if player_x is not None:
            self.player_x = player_x
        
        # Update movement with randomness
        self.move_timer += 1
        if self.move_timer >= self.move_change_interval:
            self.move_timer = 0
            self.move_change_interval = random.randint(20, 50)
            # Random chance to move left, right, or stay still
            random_move = random.choice([-1, 0, 1])
            distance = self.player_x - self.x
            if abs(distance) > 10:
                # If far from player, move toward them
                self.vel_x = 2 if distance > 0 else -2
            else:
                # Otherwise move randomly
                self.vel_x = random_move * 1.5

        self.x += self.vel_x
        self.y += self.vel_y
        
        # Boundary collision
        if self.x < self.width // 2:
            self.x = self.width // 2
        elif self.x > SCREEN_WIDTH - self.width // 2:
            self.x = SCREEN_WIDTH - self.width // 2

        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        # Update shoot timer
        self.shoot_timer += 1

    def fire_bullet(self) -> 'Bullet':
        """
        Create and return a bullet fired from the enemy.
        Only returns a bullet if enough time has passed.
        
        Returns:
            Bullet or None: A new bullet object or None if not ready to shoot
        """
        if self.wave >= 3 and self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            self.shoot_interval = random.randint(60, 120)
            return Bullet(self.x, self.y + self.height // 2, 0, 4, Colors.RED)
        return None

    def can_shoot(self) -> bool:
        """Check if this enemy can shoot (based on wave)."""
        return self.wave >= 3

    def is_offscreen(self) -> bool:
        """Check if enemy has fallen below the screen."""
        return self.y > SCREEN_HEIGHT + self.height // 2

    def take_damage(self) -> bool:
        """
        Reduce health.
        
        Returns:
            bool: True if enemy is destroyed
        """
        self.health -= 1
        return self.health <= 0

    def draw(self, surface: pygame.Surface):
        """Draw the enemy sprite."""
        surface.blit(self.image, self.rect)


class Powerup(pygame.sprite.Sprite):
    """
    Powerup class for temporary enhancements.
    
    Two types of powerups:
    - RAPID_FIRE: Enables stream of bullets when holding space
    - INVINCIBILITY: Grants 5 seconds of invincibility
    
    Attributes:
        x, y: Position coordinates
        powerup_type: Type of powerup ('RAPID_FIRE' or 'INVINCIBILITY')
        radius: Collision radius
    """

    TYPE_RAPID_FIRE = 'RAPID_FIRE'
    TYPE_INVINCIBILITY = 'INVINCIBILITY'

    def __init__(self, x: float, y: float, powerup_type: str):
        super().__init__()
        self.x = x
        self.y = y
        self.powerup_type = powerup_type
        self.radius = 12
        self.rotation = 0
        self.rotation_speed = 3
        
        # Create powerup sprite
        self._create_image()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def _create_image(self):
        """Create powerup sprite based on type."""
        size = self.radius * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if self.powerup_type == self.TYPE_RAPID_FIRE:
            # Draw rapid fire powerup as a star (yellow)
            color = Colors.YELLOW
            self._draw_star(color)
        else:  # INVINCIBILITY
            # Draw invincibility powerup as a shield (cyan)
            color = Colors.CYAN
            pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius - 1)
            pygame.draw.circle(self.image, Colors.WHITE, (self.radius, self.radius), self.radius - 3, 2)

    def _draw_star(self, color):
        """Draw a star shape for rapid fire powerup."""
        points = []
        for i in range(10):
            angle = (i / 10) * 2 * math.pi - math.pi / 2
            if i % 2 == 0:
                distance = self.radius
            else:
                distance = self.radius * 0.6
            x = self.radius + distance * math.cos(angle)
            y = self.radius + distance * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(self.image, color, points)

    def update(self):
        """Update powerup position and rotation."""
        self.y += 2  # Fall downward
        self.rotation += self.rotation_speed
        self.rect.centery = self.y

    def is_offscreen(self) -> bool:
        """Check if powerup has fallen below the screen."""
        return self.y > SCREEN_HEIGHT + self.radius

    def draw(self, surface: pygame.Surface):
        """Draw the powerup sprite."""
        surface.blit(self.image, self.rect)
