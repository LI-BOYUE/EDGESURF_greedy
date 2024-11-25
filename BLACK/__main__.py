import pyautogui
import time
from PIL import ImageGrab, Image

class GameConfig:
    avoid = 100  #difference limitation

    class Colors:
        red = (255, 0, 0)
        black = (0, 0, 0)

    class Boxes:#need to locate in different environment
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
            "obstacles": ImageGrab.grab(boxes.box_obstacles).getdata(),
            #"behind": ImageGrab.grab(boxes.box_behind).getdata(), 
        }

    def count_colors(self):
        """Count relevant colors in the screen regions"""
        game_colors = GameConfig.Colors
        color_data = self.image_grab()

        def process_box(pixels):
            counts = {"red": 0, "black": 0}
            for color in pixels:
                if color[:3] == game_colors.red:  # Ignore alpha channel
                    counts["red"] += 1
                elif color[:3] == game_colors.black:
                    counts["black"] += 1
            return counts

        return {key: process_box(value) for key, value in color_data.items()}
        

class Controls:
    def __init__(self, game_state):
        self.game_state = game_state

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
        """Decide the best action based on current state"""
        
        #actions = ["left", "right","down"] 
        actions = ["left", "right"] 

        # Initialize variables to track the best action
        best_action = None
        min_black = float('inf')  # Start with an infinitely large value

        # Evaluate each action's black count
        for action in actions:
            if action == "down":
                black_count = state["down"]["black"]
            elif action == "left":
                black_count = state["left"]["black"]
            elif action == "right":
                black_count = state["right"]["black"]
            
            """
            elif action == "stand":
                black_count = state["stand"]["black"]  # no "stand" 
            """

            #forcing avoid 
            #if(state["obstacles"]["blue"]<2200 or state["down"]["blue"]<13500):
            if state["obstacles"]["black"] >0 or state["down"]["black"] >0 :
                state["down"]["black"]=1000000
            elif  state["obstacles"]["black"] ==0 and state["down"]["black"]!=1000000:
                return "down"

            # Always choose the action with the minimum black_count
            if black_count < min_black:
                min_black = black_count
                best_action = action
            
            #correction error
            if ((state["left"]["black"]-state["right"]["black"]<GameConfig.avoid and state["left"]["black"]-state["right"]["black"]>-GameConfig.avoid) or state["left"]["black"]-state["right"]["black"]==0 ) and state["down"]["black"]!=1000000:
                best_action= "down" 

        # Debug output for clarity
        print("Left black:", state["left"]["black"])
        print("Right black:", state["right"]["black"])
        print("Front black:", state["down"]["black"])
        print("obstacles black:", state["obstacles"]["black"])
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
                # Get current state
                color_data = self.game_state.count_colors()

                # Decide best action using greedy algorithm
                best_action = self.gr_controller.greedy(color_data)
                
                """
                # 显示抓取的区域图片
                img = ImageGrab.grab(GameConfig.Boxes.box_left)
                img.show()  # 用于调试，查看抓取的图像是否符合预期
                """
                

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
