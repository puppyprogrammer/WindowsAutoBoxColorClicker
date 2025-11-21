import pyautogui
import time
import threading

class ColorClicker:
    def __init__(self, region, target_color, tolerance=10, delay=0.1):
        """
        region: tuple (x, y, width, height)
        target_color: tuple (r, g, b)
        tolerance: int, allowable difference in color values
        delay: float, seconds to wait between checks
        """
        self.region = region
        self.target_color = target_color
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

    def _run_loop(self):
        print(f"Bot started. Watching region {self.region} for color {self.target_color}")
        while self.running:
            try:
                # Take a screenshot of the region
                # region is (left, top, width, height)
                img = pyautogui.screenshot(region=self.region)
                
                # Check if the color exists in the image
                found_point = self._find_color(img)
                
                if found_point:
                    # Convert local image coordinates to screen coordinates
                    screen_x = self.region[0] + found_point[0]
                    screen_y = self.region[1] + found_point[1]
                    
                    print(f"Color found at ({screen_x}, {screen_y})! Clicking...")
                    pyautogui.click(x=screen_x, y=screen_y)
                    
                    # Wait a bit to avoid rapid-fire clicking on the same frame
                    time.sleep(0.5)
                
                # Small sleep to prevent CPU hogging and respect user delay
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"Error in bot loop: {e}")
                time.sleep(1)

    def _find_color(self, img):
        """
        Scans the image for the target color.
        Returns (x, y) of the first match, or None.
        """
        width, height = img.size
        pixels = img.load()
        
        tr, tg, tb = self.target_color
        
        # Simple pixel scan
        # Optimization: Could use numpy for faster array processing if needed, 
        # but for a small region, python loop is usually fine.
        for x in range(0, width, 2): # Skip every other pixel for speed
            for y in range(0, height, 2):
                r, g, b = pixels[x, y]
                
                if (abs(r - tr) <= self.tolerance and
                    abs(g - tg) <= self.tolerance and
                    abs(b - tb) <= self.tolerance):
                    return (x, y)
        return None
