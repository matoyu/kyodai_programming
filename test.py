import pygame
import time

def main():
    pygame.init()
    pygame.mixer.init()

    # Load sound effects
    explosion_sound = pygame.mixer.Sound("explosion.wav")
    laser_sound = pygame.mixer.Sound("laser.wav")

    try:
        # Play the explosion sound effect
        print("Playing explosion sound effect...")
        explosion_sound.play()
        time.sleep(2)  # Wait for 2 seconds

        # Play the laser sound effect
        print("Playing laser sound effect...")
        laser_sound.play()
        time.sleep(2)  # Wait for 2 seconds

    finally:
        pygame.mixer.quit()
        pygame.quit()

if __name__ == "__main__":
    main()