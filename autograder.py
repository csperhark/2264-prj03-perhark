import unittest
import copy
from unittest.mock import patch

try:
    from image_processor import ImageProcessor
except ImportError:
    print("Error: Could not import 'image_processor.py'.")
    print("Please make sure this autograder script is in the same directory as your solution file.")
    import sys
    sys.exit(1)

# RGB pixel grid (Height: 2, Width: 2, Channels: 3) for testing
MOCK_PIXEL_GRID = [
    [[10, 20, 30], [40, 50, 60]],
    [[70, 80, 90], [100, 110, 120]]
]


class TestBaseImageProcessor(unittest.TestCase):
    """Base setup class for shared mock initialization."""
    def setUp(self):
        self.patcher = patch('image_processor.ReadBMP', return_value=copy.deepcopy(MOCK_PIXEL_GRID))
        self.mock_read = self.patcher.start()
        self.processor = ImageProcessor("dummy_image.bmp")
        self.initial_grid = copy.deepcopy(MOCK_PIXEL_GRID)

    def tearDown(self):
        self.patcher.stop()


class TestPart1Invert(TestBaseImageProcessor):
    """5 Test Cases for Part 1: invert() Method"""

    def test_case_1_dimensions(self):
        """Case 1: Verify image dimensions do not change."""
        self.processor.invert()
        self.assertEqual(len(self.processor.pixelgrid), len(self.initial_grid))
        self.assertEqual(len(self.processor.pixelgrid[0]), len(self.initial_grid[0]))

    def test_case_2_pixel_values(self):
        """Case 2: Verify each channel matches the formula (255 - original_value)."""
        self.processor.invert()
        for r in range(self.processor.height):
            for c in range(self.processor.width):
                for ch in range(3):
                    expected = 255 - self.initial_grid[r][c][ch]
                    self.assertEqual(self.processor.pixelgrid[r][c][ch], expected)

    def test_case_3_double_inversion(self):
        """Case 3: Applying invert() twice restores the original matrix."""
        self.processor.invert()
        self.processor.invert()
        self.assertEqual(self.processor.pixelgrid, self.initial_grid)

    def test_case_4_boundary_values(self):
        """Case 4: Correct handling of boundary values (0 and 255)."""
        self.processor.pixelgrid = [[[0, 255, 128], [255, 0, 10]]]
        self.processor.height = 1
        self.processor.width = 2
        self.processor.invert()
        self.assertEqual(self.processor.pixelgrid, [[[255, 0, 127], [0, 255, 245]]])

    def test_case_5_single_pixel(self):
        """Case 5: Inversion on a single-pixel matrix (1x1)."""
        self.processor.pixelgrid = [[[100, 150, 200]]]
        self.processor.height = 1
        self.processor.width = 1
        self.processor.invert()
        self.assertEqual(self.processor.pixelgrid, [[[155, 105, 55]]])


class TestPart2DisplayChannel(TestBaseImageProcessor):
    """5 Test Cases for Part 2: displayChannel() Method"""

    def test_case_1_red(self):
        """Case 1: 'r' channel preserves red and sets green/blue to 0."""
        self.processor.displayChannel('r')
        for r in range(self.processor.height):
            for c in range(self.processor.width):
                self.assertEqual(self.processor.pixelgrid[r][c][0], self.initial_grid[r][c][0])
                self.assertEqual(self.processor.pixelgrid[r][c][1], 0)
                self.assertEqual(self.processor.pixelgrid[r][c][2], 0)

    def test_case_2_green(self):
        """Case 2: 'g' channel preserves green and sets red/blue to 0."""
        self.processor.displayChannel('g')
        for r in range(self.processor.height):
            for c in range(self.processor.width):
                self.assertEqual(self.processor.pixelgrid[r][c][0], 0)
                self.assertEqual(self.processor.pixelgrid[r][c][1], self.initial_grid[r][c][1])
                self.assertEqual(self.processor.pixelgrid[r][c][2], 0)

    def test_case_3_blue(self):
        """Case 3: 'b' channel preserves blue and sets red/green to 0."""
        self.processor.displayChannel('b')
        for r in range(self.processor.height):
            for c in range(self.processor.width):
                self.assertEqual(self.processor.pixelgrid[r][c][0], 0)
                self.assertEqual(self.processor.pixelgrid[r][c][1], 0)
                self.assertEqual(self.processor.pixelgrid[r][c][2], self.initial_grid[r][c][2])

    def test_case_4_invalid_input(self):
        """Case 4: Invalid input (e.g., 'x') should not alter the matrix."""
        grid_before = copy.deepcopy(self.processor.pixelgrid)
        self.processor.displayChannel('x')
        self.assertEqual(self.processor.pixelgrid, grid_before)

    def test_case_5_case_sensitivity(self):
        """Case 5: Uppercase inputs (e.g., 'R') leave the matrix intact."""
        grid_before = copy.deepcopy(self.processor.pixelgrid)
        self.processor.displayChannel('R')
        self.assertEqual(self.processor.pixelgrid, grid_before)


class TestPart3Flip(TestBaseImageProcessor):
    """5 Test Cases for Part 3: flip() Method"""

    def test_case_1_vertical(self):
        """Case 1: 'v' flips rows vertically."""
        self.processor.flip('v')
        expected = copy.deepcopy(self.initial_grid)
        expected.reverse()
        self.assertEqual(self.processor.pixelgrid, expected)

    def test_case_2_horizontal(self):
        """Case 2: 'h' flips elements horizontally within each row."""
        self.processor.flip('h')
        expected = copy.deepcopy(self.initial_grid)
        for row in expected:
            row.reverse()
        self.assertEqual(self.processor.pixelgrid, expected)

    def test_case_3_double_vertical(self):
        """Case 3: Two vertical flips restore the original orientation."""
        self.processor.flip('v')
        self.processor.flip('v')
        self.assertEqual(self.processor.pixelgrid, self.initial_grid)

    def test_case_4_double_horizontal(self):
        """Case 4: Two horizontal flips restore the original orientation."""
        self.processor.flip('h')
        self.processor.flip('h')
        self.assertEqual(self.processor.pixelgrid, self.initial_grid)

    def test_case_5_invalid_axis(self):
        """Case 5: Invalid axis (e.g., 'z') does not modify the matrix."""
        grid_before = copy.deepcopy(self.processor.pixelgrid)
        self.processor.flip('z')
        self.assertEqual(self.processor.pixelgrid, grid_before)


class TestPart4Grayscale(TestBaseImageProcessor):
    """5 Test Cases for Part 4: grayscale() Method"""

    def test_case_1_average_calculation(self):
        """Case 1: Each channel is assigned the integer average sum // 3."""
        self.processor.grayscale()
        for r in range(self.processor.height):
            for c in range(self.processor.width):
                expected_avg = sum(self.initial_grid[r][c]) // 3
                self.assertEqual(self.processor.pixelgrid[r][c], [expected_avg, expected_avg, expected_avg])

    def test_case_2_uniform_color(self):
        """Case 2: Homogeneous pixels maintain their exact value."""
        self.processor.pixelgrid = [[[100, 100, 100], [200, 200, 200]]]
        self.processor.height = 1
        self.processor.width = 2
        self.processor.grayscale()
        self.assertEqual(self.processor.pixelgrid, [[[100, 100, 100], [200, 200, 200]]])

    def test_case_3_zero_and_max(self):
        """Case 3: Boundary values (pure black [0,0,0] and pure white [255,255,255])."""
        self.processor.pixelgrid = [[[0, 0, 0], [255, 255, 255]]]
        self.processor.height = 1
        self.processor.width = 2
        self.processor.grayscale()
        self.assertEqual(self.processor.pixelgrid, [[[0, 0, 0], [255, 255, 255]]])

    def test_case_4_integer_floor_division(self):
        """Case 4: Floor division (e.g., sum = 254 -> 254 // 3 = 84)."""
        self.processor.pixelgrid = [[[84, 85, 85]]]
        self.processor.height = 1
        self.processor.width = 1
        self.processor.grayscale()
        self.assertEqual(self.processor.pixelgrid, [[[84, 84, 84]]])

    def test_case_5_repeated_execution(self):
        """Case 5: Consecutive execution returns identical and idempotent results."""
        self.processor.grayscale()
        first_pass = copy.deepcopy(self.processor.pixelgrid)
        self.processor.grayscale()
        self.assertEqual(self.processor.pixelgrid, first_pass)


class TestPart5Brightness(TestBaseImageProcessor):
    """5 Test Cases for Part 5: brightness() Method"""

    def test_case_1_increase(self):
        """Case 1: '+' operator increases channels by 25 units."""
        self.processor.brightness('+')
        for r in range(self.processor.height):
            for c in range(self.processor.width):
                for ch in range(3):
                    expected = min(255, self.initial_grid[r][c][ch] + 25)
                    self.assertEqual(self.processor.pixelgrid[r][c][ch], expected)

    def test_case_2_decrease(self):
        """Case 2: '-' operator decreases channels by 25 units."""
        self.processor.brightness('-')
        for r in range(self.processor.height):
            for c in range(self.processor.width):
                for ch in range(3):
                    expected = max(0, self.initial_grid[r][c][ch] - 25)
                    self.assertEqual(self.processor.pixelgrid[r][c][ch], expected)

    def test_case_3_upper_clamping(self):
        """Case 3: Upper limit clamping to a maximum of 255."""
        self.processor.pixelgrid = [[[240, 250, 255]]]
        self.processor.height = 1
        self.processor.width = 1
        self.processor.brightness('+')
        self.assertEqual(self.processor.pixelgrid, [[[255, 255, 255]]])

    def test_case_4_lower_clamping(self):
        """Case 4: Lower limit clamping to a minimum of 0."""
        self.processor.pixelgrid = [[[10, 20, 0]]]
        self.processor.height = 1
        self.processor.width = 1
        self.processor.brightness('-')
        self.assertEqual(self.processor.pixelgrid, [[[0, 0, 0]]])

    def test_case_5_invalid_operation(self):
        """Case 5: Operations other than '+' or '-' do not modify the object."""
        grid_before = copy.deepcopy(self.processor.pixelgrid)
        self.processor.brightness('*')
        self.assertEqual(self.processor.pixelgrid, grid_before)


class TestPart6Contrast(TestBaseImageProcessor):
    """5 Test Cases for Part 6: contrast() Method"""

    def test_case_1_increase(self):
        """Case 1: '+' operator applies contrast formula with c = 45."""
        self.processor.contrast('+')
        factor = (259 * (45 + 255)) / (255 * (259 - 45))
        for r in range(self.processor.height):
            for c in range(self.processor.width):
                for ch in range(3):
                    val = self.initial_grid[r][c][ch]
                    expected = max(0, min(255, int(factor * (val - 128) + 128)))
                    self.assertEqual(self.processor.pixelgrid[r][c][ch], expected)

    def test_case_2_decrease(self):
        """Case 2: '-' operator applies contrast formula with c = -45."""
        self.processor.contrast('-')
        factor = (259 * (-45 + 255)) / (255 * (259 - (-45)))
        for r in range(self.processor.height):
            for c in range(self.processor.width):
                for ch in range(3):
                    val = self.initial_grid[r][c][ch]
                    expected = max(0, min(255, int(factor * (val - 128) + 128)))
                    self.assertEqual(self.processor.pixelgrid[r][c][ch], expected)

    def test_case_3_clamping_high(self):
        """Case 3: Upper clamping to 255 on contrast increase."""
        self.processor.pixelgrid = [[[250, 240, 230]]]
        self.processor.height = 1
        self.processor.width = 1
        self.processor.contrast('+')
        self.assertEqual(self.processor.pixelgrid, [[[255, 255, 255]]])

    def test_case_4_clamping_low(self):
        """Case 4: Lower clamping to 0 on dark values."""
        self.processor.pixelgrid = [[[5, 10, 15]]]
        self.processor.height = 1
        self.processor.width = 1
        self.processor.contrast('+')
        self.assertEqual(self.processor.pixelgrid, [[[0, 0, 0]]])

    def test_case_5_invalid_op(self):
        """Case 5: Invalid operation does not modify pixel values."""
        grid_before = copy.deepcopy(self.processor.pixelgrid)
        self.processor.contrast('/')
        self.assertEqual(self.processor.pixelgrid, grid_before)


if __name__ == '__main__':
    unittest.main(verbosity=2)
