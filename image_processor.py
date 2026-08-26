from bmp import ReadBMP, WriteBMP

class ImageProcessor:
    def __init__(self, filename):
        # Load pixel grid and store dimensions
        self.pixelgrid = ReadBMP(filename)
        self.height = len(self.pixelgrid)
        self.width = len(self.pixelgrid[0])

    def save(self, newName):
        # Save current state of the image
        WriteBMP(self.pixelgrid, newName)

    def invert(self):
        # Invert each color channel (255 - value)
        for r in range(self.height):
            for c in range(self.width):
                for ch in range(3):
                    self.pixelgrid[r][c][ch] = 255 - self.pixelgrid[r][c][ch]

    def displayChannel(self, channel):
        # Keep only the specified color channel ('r', 'g', 'b') and set others to 0
        channel_map = {'r': 0, 'g': 1, 'b': 2}
        if channel not in channel_map:
            print("Invalid channel.")
            return

        active = channel_map[channel]
        for r in range(self.height):
            for c in range(self.width):
                for ch in range(3):
                    if ch != active:
                        self.pixelgrid[r][c][ch] = 0

    def flip(self, axis):
        # Flip image horizontally ('h') or vertically ('v')
        if axis == 'v':
            self.pixelgrid.reverse()
        elif axis == 'h':
            for r in range(self.height):
                self.pixelgrid[r].reverse()
        else:
            print("Invalid axis.")

    def grayscale(self):
        # Convert to grayscale by averaging three channels
        for r in range(self.height):
            for c in range(self.width):
                avg = sum(self.pixelgrid[r][c]) // 3
                self.pixelgrid[r][c] = [avg, avg, avg]

    def brightness(self, operation):
        # Adjust brightness by adding or subtracting 25 from each channel
        delta = 25 if operation == '+' else -25 if operation == '-' else 0
        if delta == 0:
            print("Invalid operation.")
            return

        for r in range(self.height):
            for c in range(self.width):
                for ch in range(3):
                    new_val = self.pixelgrid[r][c][ch] + delta
                    # Clamp values within range [0, 255]
                    self.pixelgrid[r][c][ch] = max(0, min(255, new_val))

    def contrast(self, operation):
        # Adjust contrast using factor calculation
        con = 45 if operation == '+' else -45 if operation == '-' else None
        if con is None:
            print("Invalid operation.")
            return

        factor = (259 * (con + 255)) / (255 * (259 - con))
        for r in range(self.height):
            for c in range(self.width):
                for ch in range(3):
                    new_val = int(factor * (self.pixelgrid[r][c][ch] - 128) + 128)
                    # Clamp values within range [0, 255]
                    self.pixelgrid[r][c][ch] = max(0, min(255, new_val))


def main():
    filename = input("Enter filename containing source image (must be .bmp): ")
    try:
        img = ImageProcessor(filename)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    while True:
        print("\n==============================")
        print("Python Basic Image Processor")
        print("==============================")
        print("Select an operation:")
        print("a) Invert colors")
        print("b) Flip image")
        print("c) Display color channel")
        print("d) Convert to grayscale")
        print("e) Change brightness")
        print("f) Change contrast")
        print("------------------------------")
        print("s) SAVE picture")
        print("o) Open new image")
        print("q) Quit")
        print("==============================")

        option = input("(a/b/c/d/e/f/s/o/q): ").strip().lower()

        if option == 'a':
            img.invert()
            print("Colors inverted successfully.")

        elif option == 'b':
            axis = input("Flip (h)orizontally or (v)ertically? (h/v): ").strip().lower()
            img.flip(axis)

        elif option == 'c':
            ch = input("Display channel (r)ed, (g)reen, or (b)lue? (r/g/b): ").strip().lower()
            img.displayChannel(ch)

        elif option == 'd':
            img.grayscale()
            print("Image converted to grayscale.")

        elif option == 'e':
            while True:
                print("\n[+] increase brightness")
                print("[-] decrease brightness")
                print("[q] exit")
                sub_op = input("(+/-/q): ").strip().lower()
                if sub_op == 'q':
                    break
                elif sub_op in ['+', '-']:
                    img.brightness(sub_op)

        elif option == 'f':
            while True:
                print("\n[+] increase contrast")
                print("[-] decrease contrast")
                print("[q] exit")
                sub_op = input("(+/-/q): ").strip().lower()
                if sub_op == 'q':
                    break
                elif sub_op in ['+', '-']:
                    img.contrast(sub_op)

        elif option == 's':
            save_name = input("Enter name for edited picture (must have .bmp extension): ")
            img.save(save_name)
            print(f"Image saved as {save_name}.")

        elif option == 'o':
            filename = input("Enter filename containing source image (must be .bmp): ")
            try:
                img = ImageProcessor(filename)
                print("New image loaded.")
            except Exception as e:
                print(f"Error loading image: {e}")

        elif option == 'q':
            print("Exiting program...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()