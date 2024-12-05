import raimad as rai

class CPWLayers:
    conductor = rai.Layer('Conducting layer for signal and ground lines')
    resist = rai.Layer('Resist layer above signal line')
    insl = rai.Layer('Insulator between CPW and bridge')
    bridge = rai.Layer('Conducting part of bridge')

class CPWSegment(rai.Compo):
    class Layers(CPWLayers):
        pass

    class Options:
        length = rai.Option.Geometric(
            "length of segment",
            browser_default=10
            )
        signal_width = rai.Option.Geometric(
            "width of signal line",
            browser_default=3
            )
        gap_width = rai.Option.Geometric(
            "width of gaps between signal line and gnd lines",
            browser_default=1
            )
        gnd_width = rai.Option.Geometric(
            "width of gnd lines",
            browser_default=2
            )
        resist_margin = rai.Option.Geometric(
            "shrink width of resist on either side of segment by this much",
            browser_default=1
            )

    class Marks:
        tl_enter = rai.Mark("Start of CPW segment")
        tl_exit = rai.Mark("End of CPW segment")

    def _make(
            self,
            length: float,
            signal_width: float,
            gap_width: float,
            gnd_width: float,
            resist_margin: float,
            ):

        signal = rai.RectLW(length, signal_width).proxy().map('conductor')
        gnd1 = rai.RectLW(length, gnd_width).proxy().map('conductor')
        gnd2 = gnd1.proxy()
        resist = rai.RectLW(
            length,
            (
                + signal_width
                + gap_width * 2
                + gnd_width * 2
                - resist_margin * 2
                )
            ).proxy().map('resist')

        # gnd1 goes above signal
        gnd1.snap_above(signal)
        gnd1.move(0, gap_width)

        # gnd2 goes below signal
        gnd2.snap_below(signal)
        gnd2.move(0, -gap_width)

        # resist goes directly ontop of signal
        resist.bbox.mid.to(signal.bbox.mid)

        # Register subcompos
        self.subcompos.signal = signal
        self.subcompos.gnd1 = gnd1
        self.subcompos.gnd2 = gnd2
        self.subcompos.resist = resist

        # Resigest marks
        self.marks.tl_enter = signal.bbox.mid_left
        self.marks.tl_exit = signal.bbox.mid_right

