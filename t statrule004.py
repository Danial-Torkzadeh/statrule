import numpy as np
from scipy.stats import t as student_t
from svgwrite import Drawing, rgb
import math

def generate_t_distribution_slide_rule(output_file="t_distribution_slide_rule_enhanced.svg"):
    # === CONFIGURABLE LINES: Define your 4 degrees of freedom here ===
    df1 = 7    # ✅ CHANGE THIS VALUE AS NEEDED
    df2 = 14   # ✅ CHANGE THIS VALUE AS NEEDED
    df3 = 28   # ✅ CHANGE THIS VALUE AS NEEDED
    df4 = 35  # ✅ CHANGE THIS VALUE AS NEEDED
    
    # Create list from these 4 variables
    dfs = [df1, df2, df3, df4]
    
    # Configuration
    width, height = 1800, 800
    margin = 80
    rule_width = width - 2 * margin

    # Adjusted probability display range
    P_DISPLAY_MIN, P_DISPLAY_MAX = 0.001, 0.999
    P_LOGIT_MIN, P_LOGIT_MAX = 0.0005, 0.9995

    # Create SVG drawing
    dwg = Drawing(output_file, size=(width, height), profile='full')
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=rgb(248, 248, 240)))

    # Logit-based position mapping
    def p_to_position_logit(p):
        p_clamped = max(P_LOGIT_MIN, min(P_LOGIT_MAX, p))
        logit_p = math.log(p_clamped / (1 - p_clamped))
        
        logit_display_min = math.log(P_DISPLAY_MIN / (1 - P_DISPLAY_MIN))
        logit_display_max = math.log(P_DISPLAY_MAX / (1 - P_DISPLAY_MAX))
        
        normalized = (logit_p - logit_display_min) / (logit_display_max - logit_display_min)
        normalized = max(0.0, min(1.0, normalized))
        return margin + rule_width * normalized

    p_to_position = p_to_position_logit

    # Fixed vertical positions for 4 df lines
    prob_y = 150
    t_y_positions = [250, 350, 450, 550]  # Fixed for df1, df2, df3, df4
    
    # Fixed colors for 4 df lines
    t_colors = [rgb(255, 0, 0), rgb(0, 128, 0), rgb(0, 0, 255), rgb(128, 0, 128)]  # Red, Green, Blue, Purple

    # Draw probability baseline
    dwg.add(dwg.line(start=(margin, prob_y), end=(width - margin, prob_y),
                     stroke=rgb(0, 0, 0), stroke_width=2))
    dwg.add(dwg.text("Probability (P)", insert=(width/2, prob_y - 30), text_anchor="middle",
                     font_size=12, font_family="Arial", fill=rgb(0, 0, 0)))

    # Draw t-distribution baselines - using df1, df2, df3, df4 explicitly
    dwg.add(dwg.line(start=(margin, t_y_positions[0]), end=(width - margin, t_y_positions[0]),
                     stroke=t_colors[0], stroke_width=2))
    dwg.add(dwg.text(f"t-distribution (df={df1})", insert=(width/2, t_y_positions[0] - 30), 
                     text_anchor="middle", font_size=12, font_family="Arial", fill=t_colors[0]))

    dwg.add(dwg.line(start=(margin, t_y_positions[1]), end=(width - margin, t_y_positions[1]),
                     stroke=t_colors[1], stroke_width=2))
    dwg.add(dwg.text(f"t-distribution (df={df2})", insert=(width/2, t_y_positions[1] - 30), 
                     text_anchor="middle", font_size=12, font_family="Arial", fill=t_colors[1]))

    dwg.add(dwg.line(start=(margin, t_y_positions[2]), end=(width - margin, t_y_positions[2]),
                     stroke=t_colors[2], stroke_width=2))
    dwg.add(dwg.text(f"t-distribution (df={df3})", insert=(width/2, t_y_positions[2] - 30), 
                     text_anchor="middle", font_size=12, font_family="Arial", fill=t_colors[2]))

    dwg.add(dwg.line(start=(margin, t_y_positions[3]), end=(width - margin, t_y_positions[3]),
                     stroke=t_colors[3], stroke_width=2))
    dwg.add(dwg.text(f"t-distribution (df={df4})", insert=(width/2, t_y_positions[3] - 30), 
                     text_anchor="middle", font_size=12, font_family="Arial", fill=t_colors[3]))

    # Probability ticks
    def add_probability_ticks():
        main_probs = [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 0.995, 0.999]
        for p in main_probs:
            if p < P_DISPLAY_MIN or p > P_DISPLAY_MAX:
                continue
            x_pos = p_to_position(p)
            if p in [0.001, 0.005, 0.01, 0.025, 0.05, 0.95, 0.975, 0.99, 0.995, 0.999]:
                tick_size, stroke_width, font_size = 15, 2.0, 10
            elif p in [0.1, 0.9]:
                tick_size, stroke_width, font_size = 12, 1.5, 9
            else:
                tick_size, stroke_width, font_size = 8, 1.0, 8
            dwg.add(dwg.line(start=(x_pos, prob_y), end=(x_pos, prob_y - tick_size),
                             stroke=rgb(0, 0, 0), stroke_width=stroke_width))
            if p >= 0.1 and p <= 0.9 or p in [0.001, 0.005, 0.01, 0.025, 0.05, 0.95, 0.975, 0.99, 0.995, 0.999]:
                label = f"{p:.3f}" if (p < 0.1 or p > 0.9) else f"{p:.2f}"
                dwg.add(dwg.text(label, insert=(x_pos, prob_y - tick_size - 10), 
                                 text_anchor="middle", font_size=font_size, 
                                 font_family="Arial", fill=rgb(0, 0, 0)))

    def add_probability_minor_ticks():
        main_probs = [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 0.995, 0.999]
        for i in range(len(main_probs) - 1):
            p1, p2 = main_probs[i], main_probs[i+1]
            if p1 < P_DISPLAY_MIN or p2 > P_DISPLAY_MAX:
                continue
            if p1 < 0.1 or p2 > 0.9:
                step = (p2 - p1) / 5
                for j in range(1, 5):
                    p_minor = p1 + j * step
                    if P_DISPLAY_MIN <= p_minor <= P_DISPLAY_MAX:
                        x_pos = p_to_position(p_minor)
                        dwg.add(dwg.line(start=(x_pos, prob_y), end=(x_pos, prob_y - 6),
                                         stroke=rgb(0, 0, 0), stroke_width=0.7))
            else:
                step = (p2 - p1) / 4
                for j in range(1, 4):
                    p_minor = p1 + j * step
                    if P_DISPLAY_MIN <= p_minor <= P_DISPLAY_MAX:
                        x_pos = p_to_position(p_minor)
                        dwg.add(dwg.line(start=(x_pos, prob_y), end=(x_pos, prob_y - 4),
                                         stroke=rgb(0, 0, 0), stroke_width=0.5))

    # === IMPROVED T-TICKS FUNCTION - using df1, df2, df3, df4 explicitly ===
    def add_t_ticks(df, y_pos, color):
        t_candidates = np.arange(-5.0, 5.01, 0.1)
        
        def is_round_t(t_val):
            t_abs = abs(t_val)
            if t_abs < 0.1:
                return True
            if t_abs <= 3.0:
                return abs(t_val * 10 - round(t_val * 10)) < 1e-5
            else:
                return abs(t_val * 2 - round(t_val * 2)) < 1e-5
        
        labeled_t_vals = [t for t in t_candidates if is_round_t(t)]
        
        labeled_points = []
        for t_val in labeled_t_vals:
            p = student_t.cdf(t_val, df)
            if p < P_DISPLAY_MIN or p > P_DISPLAY_MAX:
                continue
            x_pos = p_to_position(p)
            labeled_points.append((t_val, p, x_pos))
        
        # Draw labeled ticks
        for t_val, p, x_pos in labeled_points:
            tick_size = 12
            stroke_width = 1.8
            font_size = 9
            
            dwg.add(dwg.line(start=(x_pos, y_pos), end=(x_pos, y_pos + tick_size),
                             stroke=color, stroke_width=stroke_width))
            
            # Format label
            if abs(t_val) < 10:
                if abs(t_val - round(t_val, 1)) < 1e-5:
                    t_label = f"{t_val:.1f}"
                else:
                    t_label = f"{t_val:.2f}"
            else:
                t_label = f"{t_val:.1f}"
            dwg.add(dwg.text(t_label, insert=(x_pos, y_pos + tick_size + 12), 
                             text_anchor="middle", font_size=font_size, 
                             font_family="Arial", fill=color))

        # Add minor unmarked ticks
        for i in range(len(labeled_points) - 1):
            t1, p1, x1 = labeled_points[i]
            t2, p2, x2 = labeled_points[i+1]
            
            in_tail = (abs(t1) > 2.5) or (abs(t2) > 2.5)
            num_minors = 4 if in_tail else 1
            
            for j in range(1, num_minors + 1):
                frac = j / (num_minors + 1)
                t_minor = t1 + frac * (t2 - t1)
                p_minor = student_t.cdf(t_minor, df)
                if p_minor < P_DISPLAY_MIN or p_minor > P_DISPLAY_MAX:
                    continue
                x_minor = p_to_position(p_minor)
                dwg.add(dwg.line(start=(x_minor, y_pos), end=(x_minor, y_pos + 8),
                                 stroke=color, stroke_width=0.7))

    # Add all ticks - using df1, df2, df3, df4 explicitly
    add_t_ticks(df1, t_y_positions[0], t_colors[0])
    add_t_ticks(df2, t_y_positions[1], t_colors[1])
    add_t_ticks(df3, t_y_positions[2], t_colors[2])
    add_t_ticks(df4, t_y_positions[3], t_colors[3])

    # Add probability ticks
    add_probability_ticks()
    add_probability_minor_ticks()

    # Title and info
    dwg.add(dwg.text("Enhanced T-Distribution Slide Rule", insert=(width/2, 60), text_anchor="middle",
                     font_size=18, font_family="Arial", font_weight="bold", fill=rgb(0, 0, 0)))
    dwg.add(dwg.text("Expanded Probability Scale with Warped T-Distribution Scales", 
                     insert=(width/2, 90), text_anchor="middle",
                     font_size=12, font_family="Arial", fill=rgb(100, 100, 100)))

    explanation_y = t_y_positions[3] + 80  # Using df4's y position
    dwg.add(dwg.text("How to use: Align probability on top scale with corresponding t-value on any t-distribution scale", 
                     insert=(width/2, explanation_y), text_anchor="middle",
                     font_size=10, font_family="Arial", fill=rgb(80, 80, 80)))
    dwg.add(dwg.text("Expanded extremes for higher precision in tail probabilities", 
                     insert=(width/2, explanation_y + 20), text_anchor="middle",
                     font_size=10, font_family="Arial", fill=rgb(80, 80, 80)))

    # Legend - using df1, df2, df3, df4 explicitly
    legend_x = margin
    legend_y = t_y_positions[3] + 120  # Using df4's y position
    dwg.add(dwg.circle(center=(legend_x, legend_y), r=5, fill=t_colors[0]))
    dwg.add(dwg.text(f"df = {df1}", insert=(legend_x + 15, legend_y + 5), 
                     font_size=10, font_family="Arial", fill=t_colors[0]))
    
    legend_x += 120
    dwg.add(dwg.circle(center=(legend_x, legend_y), r=5, fill=t_colors[1]))
    dwg.add(dwg.text(f"df = {df2}", insert=(legend_x + 15, legend_y + 5), 
                     font_size=10, font_family="Arial", fill=t_colors[1]))
    
    legend_x += 120
    dwg.add(dwg.circle(center=(legend_x, legend_y), r=5, fill=t_colors[2]))
    dwg.add(dwg.text(f"df = {df3}", insert=(legend_x + 15, legend_y + 5), 
                     font_size=10, font_family="Arial", fill=t_colors[2]))
    
    legend_x += 120
    dwg.add(dwg.circle(center=(legend_x, legend_y), r=5, fill=t_colors[3]))
    dwg.add(dwg.text(f"df = {df4}", insert=(legend_x + 15, legend_y + 5), 
                     font_size=10, font_family="Arial", fill=t_colors[3]))

    # Bounding box
    rule_box = dwg.rect(insert=(margin-10, prob_y-40), size=(rule_width+20, t_y_positions[3] - prob_y + 180),
                        fill="none", stroke=rgb(200, 200, 200), stroke_width=1.5, rx=6, ry=6)
    dwg.add(rule_box)

    dwg.save()
    print(f"Enhanced T-distribution slide rule saved as {output_file}")
    print(f"Created with degrees of freedom: df1={df1}, df2={df2}, df3={df3}, df4={df4}")
    print("Probability scale uses tuned logit expansion for balanced extreme/center spacing")
    print("T-scales now feature round-number labels and increased minor tick density")


def generate_custom_t_slide_rule(df1=5, df2=12, df3=30, df4=100, output_file="custom_t_slide_rule_enhanced.svg"):
    # Wrapper function to allow passing df values as parameters
    original_func = generate_t_distribution_slide_rule
    # We'll need to modify the function to accept parameters, so let's create a temporary version
    import types
    def temp_func(output_file=output_file):
        # Use the same configurable lines approach
        globals()['df1'], globals()['df2'], globals()['df3'], globals()['df4'] = df1, df2, df3, df4
        generate_t_distribution_slide_rule(output_file)
    
    temp_func(output_file)


if __name__ == "__main__":
    # This is the ONLY place you need to change df values
    generate_t_distribution_slide_rule()
