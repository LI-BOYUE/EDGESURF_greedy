import pyautogui
import time
from PIL import ImageGrab, Image
from math import sqrt

class GameConfig:
    avoid= 80  #difference limitation
    

    class Colors:
        red = (255, 0, 0)
        black = (0, 0, 0)
        blue = (49, 195, 217)

    class Boxes: #need to locate in different environment
        box_left = (328, 578, 528, 705)
        box_right = (692, 578, 892, 705)
        box_front = (528, 828, 692, 1028) 
        box_obstacles=(548,655,672,1425)

class GameState:
    def __init__(self):  
        self.last_control = 'down'
        self.time_start = time.time()

    def image_grab(self):
        """Capture screen regions and return their color data"""
        boxes = GameConfig.Boxes
        return {
            "left": ImageGrab.grab(boxes.box_left).getdata(),
            "right": ImageGrab.grab(boxes.box_right).getdata(),
            "down": ImageGrab.grab(boxes.box_front).getdata(),
            "obstacles":ImageGrab.grab(boxes.box_obstacles).getdata(),
        }

    def count_colors(self):
        """Count relevant colors in the screen regions"""
        game_colors = GameConfig.Colors
        color_data = self.image_grab()

        def process_box(pixels):
            counts = {"red": 0, "black": 0, "blue": 0}
            for color in pixels:
                # Calculate the Euclidean distance for "blue"
                distance_to_blue = sqrt(
                    (color[0] - game_colors.blue[0])**2 +
                    (color[1] - game_colors.blue[1])**2 +
                    (color[2] - game_colors.blue[2])**2
                )
                if distance_to_blue < 50:  # Set a tolerance threshold
                    counts["blue"] += 1
            return counts
        
        #display 
        processed_data = {key: process_box(value) for key, value in color_data.items()}
        print("Processed color data:", processed_data)  # Debug output
        return processed_data

class Controls:
    def __init__(self, game_state):
        self.game_state = game_state
    """
    def execute(self, action):
        if action == "left":
            pyautogui.keyDown('left')
            pyautogui.keyUp('left')
        elif action == "right":
            pyautogui.keyDown('right')
            pyautogui.keyUp('right')
        elif action == "down":
            pyautogui.keyDown('down')
            pyautogui.keyUp('down')
        elif action == "up":
            pyautogui.keyDown('up')
            pyautogui.keyUp('up')
        self.game_state.last_control = action
    """
    def execute(self, action):
        """Perform an action in the game"""
        if action == "left":
            pyautogui.press('left')
        elif action == "right":
            pyautogui.press('right')
        elif action == "down":
            pyautogui.press('down')
        """
        elif action == "stand":
            pyautogui.press('up')
        """
        self.game_state.last_control = action
    
class GreedyController:
    def __init__(self, controls):
        self.controls = controls

    def greedy(self, state): 
        """Decide the best action based on current stat  e"""
        
        #actions = ["left", "right","down"] 
        actions = ["left", "right"] 

        # Initialize variables to track the best action
        best_action = None
        max_blue = float('-inf')  # Start with an infinitely small value

        # Evaluate each action's blue count
        for action in actions:
            if action == "left":
                blue_count = state["left"]["blue"]
            elif action == "right":
                  blue_count = state["right"]["blue"]
            elif action == "down":
                blue_count = state["down"]["blue"]
            
        
            #forcing avoid 
            #if(state["obstacles"]["blue"]<2200 or state["down"]["blue"]<13500):
            if state["obstacles"]["blue"]<87448 or state["down"]["blue"]<32762:
                state["down"]["blue"]=0
            
            elif state["obstacles"]["blue"]>=87448 and state["down"]["blue"]!=0:
                return "down"

            # Choose the action with the maximum blue_count
            if blue_count > max_blue:
                max_blue = blue_count
                best_action = action

            #correction error
            if ((state["left"]["blue"]-state["right"]["blue"]<GameConfig.avoid and state["left"]["blue"]-state["right"]["blue"]>-GameConfig.avoid) or state["left"]["blue"]-state["right"]["blue"]==0 ) and state["down"]["blue"]!=0:
                best_action= "down" 



        # Debug output for clarity
        print("Left blue:", state["left"]["blue"])
        print("Right blue:", state["right"]["blue"])
        print("Down blue:", state["down"]["blue"])
        print("Obstacles:",state["obstacles"]["blue"])
        print("Selected best action:", best_action)
        print("\n")

        return best_action

class EdgeSurfBot:
    def __init__(self):
        self.game_state = GameState()
        self.controls = Controls(self.game_state)
        self.gr_controller = GreedyController(self.controls)

    def run(self):
        """Main loop with greedy algorithm"""
        try:
            time.sleep(2)  # Wait for the game to start
            self.controls.execute("down")  # Start the game

            while True:
                #self.controls.execute("up")

                # Get current state
                color_data = self.game_state.count_colors()

                # Decide best action using greedy algorithm
                best_action = self.gr_controller.greedy(color_data)

                # Perform the action
                self.controls.execute(best_action)

                # Control loop pace
                time.sleep(0.1)
 
        except KeyboardInterrupt:
            print("\nBot stopped by user.")
        except Exception as e:
            print(f"Critical error: {e}")
        finally:
            print("Cleaning up...")

if __name__ == "__main__":
    bot = EdgeSurfBot()
    print("Starting Edge Surf Bot with Greedy...")
    print("Press Ctrl+C to stop.")
    bot.run()
