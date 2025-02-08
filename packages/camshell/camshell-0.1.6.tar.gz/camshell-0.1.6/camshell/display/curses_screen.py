import curses
from typing import Callable

from camshell.interfaces import Display, Image, Size


class CursesScreen(Display):
    """Curses-based screen renderer for 256-color terminals."""

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~ Overload these to create custom color maps ~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CHARMAP = " .:-=+*#%@"

    def init_colors(self) -> None:
        curses.start_color()
        if not curses.has_colors():
            raise RuntimeError("Terminal does not support colors")
        self.max_colors = curses.COLORS
        curses.use_default_colors()
        for i in range(1, min(curses.COLORS, 256)):
            curses.init_pair(i, i, self.background_color)

    def get_color_index(self, r: int, g: int, b: int) -> int:
        return 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)

    def get_character(self, r: int, g: int, b: int, intensity: int) -> str:
        index = intensity // (256 // (len(self.CHARMAP) - 1))
        char = self.CHARMAP[index]
        return char

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, mono_color: bool = False) -> None:
        self.mono_color = mono_color
        self.screen = None
        self.max_colors = 0
        self.background_color = -1
        self.__screen_size: Size | None = None

    def initialize(self) -> None:
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.curs_set(0)
        if not self.mono_color:
            self.init_colors()
        self.__screen_size = Size(
            width=self.screen.getmaxyx()[1] - 1, height=self.screen.getmaxyx()[0] - 1
        )

    def finalize(self) -> None:
        if self.screen is None:
            return
        curses.curs_set(1)
        self.screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        self.screen = None

    def get_size(self) -> Size:
        assert self.__screen_size is not None, "Screen size is not set"
        return self.__screen_size

    def resolve_pixel(self, image: Image, x: int, y: int) -> tuple[str, int]:
        b, g, r = image.get_rgb(x, y)
        intensity = int(image.get_intensity(x, y))
        char = self.get_character(r, g, b, intensity)
        if self.mono_color:
            return char, 127
        return char, self.get_color_index(r, g, b)

    def render(self, image: Image) -> None:
        assert self.screen is not None, "Screen is not initialized"
        assert self.__screen_size is not None, "Screen size is not set"

        for y in range(min(image.size.height, self.__screen_size.height)):
            for x in range(min(image.size.width, self.__screen_size.width)):
                char, color = self.resolve_pixel(image, x, y)
                self.add_char(x, y, char, color)
        self.refresh()

    def add_char(self, x: int, y: int, char: str, color: int) -> None:
        self.screen.addch(y, x, char, curses.color_pair(color))

    def refresh(self) -> None:
        self.screen.refresh()


class CursesScreenImproved(CursesScreen):
    CHARMAP = " .:-=+*#%@"

    def __init__(
        self,
        mono_color=False,
        gamma: tuple[float, float, float, float] = (1.1, 1.0, 1.0, 10.0),
    ):
        super().__init__(mono_color)
        self.color_gamma = gamma[:3]
        self.intensity_gamma = gamma[3]

    def get_color_index(self, r: int, g: int, b: int) -> int:
        r = int((r / 255.0) ** (1.0 / self.color_gamma[0]) * 255.0)
        g = int((g / 255.0) ** (1.0 / self.color_gamma[1]) * 255.0)
        b = int((b / 255.0) ** (1.0 / self.color_gamma[2]) * 255.0)
        return super().get_color_index(r, g, b)

    def get_character(self, r: int, g: int, b: int, intensity: int) -> str:
        normalized_intensity = intensity / 255.0
        corrected_intensity = normalized_intensity ** (1.0 / self.intensity_gamma)

        index = int(corrected_intensity * (len(self.CHARMAP) - 1))
        char = self.CHARMAP[index]
        return char


class MoreResolutionScreen(CursesScreenImproved):
    class BrailleKalmanFilter:
        Q = 0.5  # Process noise: how much we allow changes in balance
        R = 0.1  # Measurement noise: how much we trust the new measurement

        def __init__(self, target: float, x_func: Callable[[], float]) -> None:
            self.target = target
            self.__x_func = x_func
            self.estimate = None

        def update(self) -> float:
            if (value := self.__x_func()) is None:
                return self.estimate

            if self.estimate is None:
                self.estimate = value
                return self.estimate

            self.Q = max(0.01, self.Q * 0.5)
            K = self.Q / (self.Q + self.R)
            measurement = self.target - value
            self.estimate += K * (measurement)

            self.estimate = max(0, min(self.estimate, 1))
            return self.estimate

    def __init__(self, mono_color=False, gamma=(1.1, 1, 1, 10)):
        super().__init__(mono_color, gamma)
        self.braille_balance = 0.5
        self.__braille_balance_controller = 0
        self.__num_of_pixels = 0
        self.__kalman = self.BrailleKalmanFilter(
            target=0.5,
            x_func=lambda: self.__braille_balance_controller / self.__num_of_pixels,
        )

    def get_size(self):
        return super().get_size() * Size(2, 2)

    def convert_braille_char(self, intensities: list[int]) -> str:
        BRAILLE_OFFSET = 0x2800
        self.__num_of_pixels += 6
        threshold = 255 * (1 - self.braille_balance)
        for i, x in enumerate(intensities):
            if x > threshold:
                self.__braille_balance_controller += 1
                BRAILLE_OFFSET += 1 << i
        return chr(BRAILLE_OFFSET)

    @staticmethod
    def braille_intensity(r: int, g: int, b: int) -> int:
        ALPHA = 0.8
        brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
        colorfulness = (max(r, g, b) - min(r, g, b)) / 255.0
        return ((1 - ALPHA) * brightness + ALPHA * colorfulness) * 255

    def resolve_pixel(self, image: Image, x: int, y: int) -> tuple[str, int]:
        bgr = [0, 0, 0]
        intensities = []
        for j in range(3):
            y_ = y * 2 + j
            if not (0 <= y_ < image.size.height):
                continue
            yw = y_ * image.size.width
            for i in range(2):
                # Instead of using this
                # bgr_ = image.get_rgb(x_, y_)
                # this is used for performance:
                x_ = x * 2 + i
                ywx = (yw + x_) * 3
                b, g, r = image.data[ywx], image.data[ywx + 1], image.data[ywx + 2]
                intensities.append(self.braille_intensity(r, g, b))
                if j < 2:
                    bgr[0] += b
                    bgr[1] += g
                    bgr[2] += r
        b, g, r = [int(x / 4) for x in bgr]

        char = self.convert_braille_char(intensities)
        if self.mono_color:
            return char, 127
        return char, self.get_color_index(r, g, b)

    def render(self, image: Image) -> None:
        super().render(image.resize(self.get_size()))
        self.braille_balance = self.__kalman.update()
        self.__num_of_pixels = 0
        self.__braille_balance_controller = 0


class EfficientScreen(MoreResolutionScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__cache_size: Size = Size(0, 0)
        self.__cache_chars = ""
        self.__cache_colors = []

    def render(self, image: Image) -> None:
        if (
            self.__cache_size is None
            or self.__cache_size.width != image.size.width
            or self.__cache_size.height != image.size.height
        ):
            self.__cache_size = image.size
            self.__cache_chars = (
                [" "] * self.__cache_size.width * self.__cache_size.height
            )
            self.__cache_colors = (
                [127] * self.__cache_size.width * self.__cache_size.height
            )
        super().render(image)

    def add_char(self, x, y, char, color) -> None:
        index = y * self.__cache_size.width + x
        if self.__cache_chars[index] != char or self.__cache_colors[index] != color:
            self.__cache_chars[index] = char
            self.__cache_colors[index] = color
            super().add_char(x, y, char, color)
