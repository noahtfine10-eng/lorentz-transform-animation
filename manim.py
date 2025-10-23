from manim import *
import numpy as np

class LTF(Scene):
    def construct(self):
        
        grid = NumberPlane(
            x_range = (-40, 40),
            y_range=(-20, 20),
            x_length=40,
            y_length=20,
        ).add_coordinates().set_opacity(0.5).scale(1)

        grid_labels = grid.get_axis_labels(x_label='x', y_label='ct')

        redgrid = grid.copy().set_color(RED).remove(*grid.get_axis_labels())

        redgrid_y_label_dot = Dot(grid.c2p(0.5, 7, 0)).set_opacity(0)
        redgrid_y_label = always_redraw(lambda: MathTex("ct'", color=RED).move_to([redgrid_y_label_dot.get_x(), redgrid_y_label_dot.get_y(), 0]).set_opacity(0.5))
        redgrid_x_label_dot = Dot(grid.c2p(6.7*2, 0.5, 0)).set_opacity(0)
        redgrid_x_label = always_redraw(lambda: MathTex("x'", color=RED).move_to([redgrid_x_label_dot.get_x(), redgrid_x_label_dot.get_y(), 0]).set_opacity(0.5))


        # labels for current v
        v_tracker = ValueTracker(0)
        v_label = always_redraw(
            lambda: MathTex("v_{S'} = ", round(v_tracker.get_value(), 2)).to_corner(UR, buff=1)
        )
        
        def getLTF(v): 
            if v == 1:
                def light(p):
                    return p
                
                return light

            gamma = 1/np.sqrt(1 - v**2)

            def LorentzTransform(p):
                M = [[gamma, -gamma * v],
                    [-gamma * v, gamma]]
                x, t, z = p[0], p[1], p[2]
                x_prime, t_prime = np.dot(M, [x, t])
                return (x_prime, t_prime, z)
            
            return LorentzTransform
        
        
        LTFgrid = redgrid.copy().apply_function(getLTF(0.5))


        #model some worldlines
        stepsize = 0.05

        def para_func(x0, y0, v=0, Flat:bool = False):
            x, y, z= grid.c2p(x0, y0)

            if Flat:
                def output_func_L(t):
                    t = t * grid.y_axis.unit_size
                    return [x + t, y, 0]
                return output_func_L

            def output_func(t):
                return [x+v*t, t+y, 0]
            
            return output_func
        
                
        
        starA = ParametricFunction(para_func(-2.5, -25, 0),  t_range=(0, 50),  color = ORANGE)
        starA = DashedVMobject(starA, num_dashes= 50, dashed_ratio=0.8)


        starB = ParametricFunction(para_func(2.5, -25, 0), t_range=(0, 50, stepsize), color=PURPLE)
        starB = DashedVMobject(starB, num_dashes= 50, dashed_ratio=0.8)
        
        rocketspeed = 0.5
        rocketlaunch_fake = Dot(grid.c2p(-2.5, -((1/rocketspeed)*2.5), rocketspeed)).set_opacity(0)
        rocketlaunch = always_redraw(lambda: Dot().move_to((rocketlaunch_fake.get_x(),rocketlaunch_fake.get_y(), 0)))
        rocketlaunch_label = always_redraw(
            lambda: Tex('Launch from Star A').move_to((rocketlaunch.get_x(), rocketlaunch.get_y()-0.5, 1)).scale(0.7)
        )
        rocketship = ParametricFunction(para_func(-2.5, -((1/rocketspeed)*2.5), rocketspeed), t_range=(0, 5, stepsize), color=GREY)
        rocketland_fake = Dot(grid.c2p(2.5, ((1/rocketspeed)*2.5), rocketspeed)).set_opacity(0)
        rocketland = always_redraw(lambda: Dot().move_to((rocketland_fake.get_x(),rocketland_fake.get_y(), 0)))
        rocketland_label = always_redraw(lambda: Tex('Landing at Star B').move_to((rocketland_fake.get_x(),rocketland_fake.get_y()+0.5, 1)).scale(0.7))

        # ANIMATIONS!! 

        # introduce scenario

        self.play(Create(VGroup(grid, grid_labels)))
        self.wait()
        self.play(Create(starA), Create(starB), rate_func = linear, run_time = 2)
        self.wait()

        #launch rocket
        self.play(Create(rocketlaunch))
        self.play(Write(rocketlaunch_label))
        self.wait()
        self.play(Create(rocketship), run_time = 2)
        self.play(Create(rocketland))
        self.play(Write(rocketland_label))
        self.wait()

        # Δt (in S)
        normalizeS_top = DashedVMobject(ParametricFunction(para_func(2.5, 5, 0, Flat=True), t_range=(0, 2, 0.1)), dashed_ratio=0.3)
        normalizeS_bottom = DashedVMobject(ParametricFunction(para_func(-2.5, -5, 0, Flat=True), t_range=(0, 7, 0.1)), dashed_ratio=0.3)
        dtS = Arrow(grid.c2p(4.5, -5, 0), grid.c2p(4.5, 5, 0), tip_length=0.15)
        dtS_label = MathTex('\\Delta ct = 10.00 \\ \\text{ly}').scale(0.7).next_to(dtS, RIGHT, 0.5).set_z(1)

        self.play(Create(normalizeS_top), Create(normalizeS_bottom))
        self.play(Create(dtS), Write(dtS_label))
        self.wait(2)
        self.play(FadeOut(VGroup(normalizeS_top, normalizeS_bottom, dtS, dtS_label)))



        # introduce velocity, apply transform

        dispmatrix = Tex(r"""
                        \begin{align*}
                            x' = \gamma(x - \beta ct) \\
                            ct' = \gamma(ct - \beta x)
                        \end{align*}
                        """).scale(0.6).move_to(grid.c2p(-11, -2.5, 1))
        
        dispmatrix_back = Rectangle(color=WHITE, height=3*grid.y_axis.unit_size, width=5*grid.x_axis.unit_size, fill_color = BLACK, fill_opacity = 1).move_to(grid.c2p(-11, -2.5, 0.1))

        self.play(Write(v_label))
        self.play(Create(redgrid), Create(redgrid_x_label_dot), Create(redgrid_y_label_dot), Write(redgrid_y_label), Write(redgrid_x_label))
        self.wait()
        self.play(FadeIn(dispmatrix_back), Write(dispmatrix))
        self.play(Transform(redgrid, LTFgrid),
                    Transform(starA, starA.copy().apply_function(getLTF(rocketspeed))),
                    Transform(starB, starB.copy().apply_function(getLTF(rocketspeed))),
                    Transform(rocketship, rocketship.copy().apply_function(getLTF(rocketspeed))),
                    Transform(rocketlaunch_fake, rocketlaunch_fake.copy().apply_function(getLTF(rocketspeed))),
                    Transform(redgrid_x_label_dot, redgrid_x_label_dot.copy().apply_function(getLTF(rocketspeed))),
                    Transform(redgrid_y_label_dot, redgrid_y_label_dot.copy().apply_function(getLTF(rocketspeed))),
                    Transform(rocketland_fake, rocketland_fake.copy().apply_function(getLTF(rocketspeed))),
                      v_tracker.animate.set_value(rocketspeed), rate_func=linear, run_time = 3)
        self.wait()
        self.play(FadeOut(redgrid), FadeOut(redgrid_x_label), FadeOut(redgrid_y_label))
        self.play(FadeOut(dispmatrix_back), FadeOut(dispmatrix))

        # find Δt' (|t'| = 4.33013)
        normalizeS_top = DashedVMobject(ParametricFunction(para_func(0, 4.33, 0, Flat=True), t_range=(0, 2, 0.1)), dashed_ratio=0.3)
        normalizeS_bottom = DashedVMobject(ParametricFunction(para_func(0, -4.33, 0, Flat=True), t_range=(0, 2, 0.1)), dashed_ratio=0.3)
        dtS = Arrow(grid.c2p(2, -4.33, 0), grid.c2p(2, 4.33, 0), tip_length=0.15)
        dtS_label = MathTex("\\Delta ct' = 8.66 \\ \\text{ly}").scale(0.7).next_to(dtS, RIGHT, 0.5)

        self.play(Create(normalizeS_top), Create(normalizeS_bottom))
        self.play(Create(dtS), Write(dtS_label))
        self.wait(2)
        self.play(FadeOut(VGroup(normalizeS_top, normalizeS_bottom, dtS, dtS_label)))

        self.wait()
