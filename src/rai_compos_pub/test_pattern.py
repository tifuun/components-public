"""
test_pattern.py: home to TestPattern component
"""

import raimad as rai

class HalfTestPattern(rai.Compo):
    def _make(
            self,
            num_rects: int,
            rect_width: float,
            rect_length: float,
            gap_width: float,
            ):
        for x in range(num_rects):
            self.subcompos[f'rect_{x}'] = (
                rai.RectLW(rect_length, rect_width)
                .proxy()
                .move(0, (rect_width + gap_width) * x)
                )


class TestPattern(rai.Compo):
    """
    Test Pattern

    This is another example component inspired by Leon's work with
    test patterns for ebeam.
    """

    class Layers:
        left = rai.Layer('Left side of marker')
        right = rai.Layer('Right side of marker')

    class Options:
        num_rects = rai.Option.Geometric(
            "Number of rectangles on each side")
        rect_width = rai.Option.Geometric(
            "Width of each rectangle on left side")
        rect_length = rai.Option.Geometric(
            "Length of each of rectangle on left side")
        gap_width = rai.Option.Geometric(
            "Width of gap between each rectangle on left side")
        abberation = rai.Option.Geometric(
            "Scale of right side compared to left (a value of 1 = same size)")

    def _make(
            self,
            num_rects: int = 20,
            rect_width: float = 10,
            rect_length: float = 25,
            gap_width: float = 10,
            abberation: float = 1.5
            ):

        self.subcompos.left = HalfTestPattern(
            num_rects,
            rect_width,
            rect_length,
            gap_width
            ).proxy().map('left')

        self.subcompos.right = (
            self.subcompos.left
            .proxy()
            .scale(abberation)
            .snap_right(
                self.subcompos.left
                )
            .map('right')
            )

class TestPatterns(rai.Compo):
    """
    Test Patterns

    Test component consisting of multiple test patterns in differnet positions.
    """


    def _make(self):
        pattern = TestPattern()
        self.subcompos.append(pattern.proxy())
        self.subcompos.append(pattern.proxy().move(-200, 0))
        self.subcompos.append(pattern.proxy().move(200, 0))
        self.subcompos.append(
            pattern
            .proxy()
            .move(0, 400)
            .bbox.mid.rotate(rai.quartercircle)
            )

        pattern2 = (
            TestPattern(num_rects=5, rect_width=40)
            .proxy()
            .bbox.mid.rotate(rai.quartercircle)
            )
        self.subcompos.append(pattern2.proxy().move(-300, -400))
        self.subcompos.append(pattern2.proxy().move(300, -400))

if __name__ == '__main__':
    with open('a.svg', 'w') as f:
        f.write(TestPatterns()._repr_svg_())
    rai.show(TestPatterns())

