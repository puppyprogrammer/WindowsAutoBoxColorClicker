import pyautogui
import time
import threading

class ColorClicker:
    def __init__(self, targets, tolerance=10, delay=0.1):
        """
        targets: list of dicts {'region': (x,y,w,h), 'color': (r,g,b)}
        tolerance: int, allowable difference in color values
        delay: float, seconds to wait between checks
        """
        self.targets = targets
        self.tolerance = tolerance
        self.delay = delay
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

import mss
from PIL import Image

    def _run_loop(self):
        print(f"Bot started. Watching {len(self.targets)} targets.")
        with mss.mss() as sct:
            while self.running:
                try:
                    for target in self.targets:
                        if not self.running: break
                        
                        region = target['region']
                        target_color = target['color']
                        
                        if target_color is None:
                            continue
                        
                        # MSS expects {'top': y, 'left': x, 'width': w, 'height': h}
                        # Our region is (x, y, w, h)
                        monitor = {
                            "left": int(region[0]),
                            "top": int(region[1]),
                            "width": int(region[2]),
                            "height": int(region[3])
                        }
                        
                        # Take a screenshot of the region using MSS
                        try:
                            sct_img = sct.grab(monitor)
                            # Convert to PIL Image
                            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                        except Exception as e:
                            with open("bot_debug.log", "a") as f:
                                f.write(f"Screenshot failed for region {region}: {e}\n")
                            continue
                        
                        # Check if the color exists in the image
                        found_point = self._find_color(img, target_color)
                        
                        if found_point:
                            # Convert local image coordinates to screen coordinates
                            screen_x = region[0] + found_point[0]
                            screen_y = region[1] + found_point[1]
                            
                            log_msg = f"Target {target_color} found at local({found_point}) -> screen({screen_x}, {screen_y})\n"
                            print(log_msg)
                            with open("bot_debug.log", "a") as f:
                                f.write(log_msg)
                                
                            # Save debug image
                            from PIL import ImageDraw
                            debug_img = img.copy()
                            draw = ImageDraw.Draw(debug_img)
                            draw.rectangle([found_point[0]-5, found_point[1]-5, found_point[0]+5, found_point[1]+5], outline="red", width=2)
                            debug_img.save("debug_found.png")
                            
                            pyautogui.click(x=screen_x, y=screen_y)
                            
                            # Wait a bit to avoid rapid-fire clicking on the same frame
                            time.sleep(0.5)
                    
                    # Small sleep to prevent CPU hogging and respect user delay
                    time.sleep(self.delay)
                    
                except Exception as e:
                    err_msg = f"Error in bot loop: {e}\n"
                    print(err_msg)
                    with open("bot_debug.log", "a") as f:
                        f.write(err_msg)
                    time.sleep(1)

    def _find_color(self, img, target_color):
        """
        Scans the image for the target color.
        Returns (x, y) of the first match, or None.
        """
        width, height = img.size
        pixels = img.load()
        
        tr, tg, tb = target_color
        
        # Simple pixel scan
        for x in range(0, width, 2): # Skip every other pixel for speed
            for y in range(0, height, 2):
                r, g, b = pixels[x, y]
                
                if (abs(r - tr) <= self.tolerance and
                    abs(g - tg) <= self.tolerance and
                    abs(b - tb) <= self.tolerance):
                    return (x, y)
        return None
