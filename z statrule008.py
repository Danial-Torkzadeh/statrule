import numpy as np
from scipy.stats import norm
from svgwrite import Drawing, rgb
import math

def generate_enhanced_stat_slide_rule(output_file="enhanced_slide_rule_fixed.svg"):
    # Configuration
    width, height = 1800, 600
    margin = 80
    rule_width = width - 2 * margin

    # Focus on positive half only
    z_min, z_max = 0, 3.5
    p_min = norm.cdf(z_min)  # 0.5
    p_max = norm.cdf(z_max)  # ~0.9998

    # Create SVG drawing
    dwg = Drawing(output_file, size=(width, height), profile='full')

    # Draw background
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=rgb(248, 248, 240)))

    # Core transformation function (fixed remaining_width calculation)
    def z_to_position(z):
        if z <= 2.0:
            return margin + rule_width * (z - z_min) / (z_max - z_min)
        else:
            base_pos = margin + rule_width * (2.0 - z_min) / (z_max - z_min)
            right_end = margin + rule_width  # = width - margin
            remaining_width = right_end - base_pos
            # Log compress beyond z=2.0
            log_factor = math.log(1 + (z - 2.0)) / math.log(1 + (z_max - 2.0))
            return base_pos + remaining_width * log_factor

    # Draw the rules with optimized vertical distance
    rule_y1, rule_y2 = 200, 280
    rule_color = rgb(40, 40, 40)

    # Draw the rule baselines
    dwg.add(dwg.line(start=(margin, rule_y1), end=(width - margin, rule_y1),
                     stroke=rule_color, stroke_width=2))
    dwg.add(dwg.line(start=(margin, rule_y2), end=(width - margin, rule_y2),
                     stroke=rule_color, stroke_width=2))

    # Add scale labels with smaller font (8px)
    dwg.add(dwg.text("Z-Score", insert=(width/2, rule_y1 - 30), text_anchor="middle",
                     font_size=8, font_family="Arial", fill=rgb(0, 0, 0)))
    dwg.add(dwg.text("Probability", insert=(width/2, rule_y2 + 35), text_anchor="middle",
                     font_size=8, font_family="Arial", fill=rgb(0, 0, 0)))

    # --------- Helper: robust tick/label generation ----------
    def generate_ticks(scale_type, values, tick_sizes, stroke_widths, is_z_scale=True, label_values=None):
        # label rounding resolution depends on scale_type
        label_round = 2 if scale_type == "z" else 4
        if label_values is not None:
            label_set = set(round(v, label_round) for v in label_values)
        else:
            label_set = None

        last_label_pos = -1e9

        for i, value in enumerate(values):
            # map value to x-position
            if scale_type == "z":
                x_pos = z_to_position(value)
                y_base = rule_y1 if is_z_scale else rule_y2
                direction = -1 if is_z_scale else 1
            else:  # p-scale
                # p -> z, then position
                z_val = norm.ppf(value)
                x_pos = z_to_position(z_val)
                y_base = rule_y1 if is_z_scale else rule_y2
                direction = -1 if is_z_scale else 1

            # draw tick mark
            tick_size = tick_sizes[i]
            stroke_width = stroke_widths[i]
            dwg.add(dwg.line(start=(x_pos, y_base),
                             end=(x_pos, y_base + direction * tick_size),
                             stroke=rule_color, stroke_width=stroke_width))

            # Add label only for requested rounded values and avoid overlap
            if label_set and round(value, label_round) in label_set:
                min_spacing = 30 if scale_type == "z" else 15
                if abs(x_pos - last_label_pos) > min_spacing:
                    if scale_type == "z":
                        # Robust formatting by rounding
                        v_rounded = round(value, 2)
                        # integer?
                        if abs(v_rounded - round(v_rounded)) < 1e-9:
                            label = f"{int(round(v_rounded))}"
                            font_size = 14
                            y_text = y_base + direction * (tick_size + 25)
                        # one-decimal?
                        elif abs(v_rounded * 10 - round(v_rounded * 10)) < 1e-9:
                            label = f"{v_rounded:.1f}"
                            font_size = 12
                            y_text = y_base + direction * (tick_size + 20)
                        else:
                            # fallback (two decimals)
                            label = f"{v_rounded:.2f}"
                            font_size = 10
                            y_text = y_base + direction * (tick_size + 18)

                        dwg.add(dwg.text(label, insert=(x_pos, y_text), text_anchor="middle",
                                         font_size=font_size, font_family="Arial", fill=rgb(0, 0, 0)))
                        last_label_pos = x_pos

                    else:
                        # p-scale formatting (vertical labels)
                        v_rounded = round(value, 4)
                        if value < 0.9:
                            label = f"{value:.2f}"[1:]  # .52 etc
                        elif value < 0.99:
                            label = f"{value:.3f}"[1:]
                        else:
                            label = f"{value:.4f}"[1:]
                        font_size = 10
                        y_text = y_base + direction * (tick_size + 30)
                        text = dwg.text(label, insert=(x_pos, y_text), text_anchor="middle",
                                        font_size=font_size, font_family="Arial", fill=rgb(0, 0, 0))
                        # rotate around insertion point (x_pos, y_text)
                        text.rotate(90, (x_pos, y_text))
                        dwg.add(text)
                        last_label_pos = x_pos

    # ---------------- Z scale ticks ----------------
    # Build a rounded set of z-values to avoid float equality issues
    set_z = set()
    # Major ticks
    major_z = [0.0, 1.0, 2.0, 3.0, 3.5]
    for z in major_z:
        set_z.add(round(z, 2))
    # decimal ticks .1 increments
    for integer in range(0, 4):
        for d in range(1, 10):
            z = round(integer + d/10.0, 2)
            if z <= 3.5:
                set_z.add(z)
    # 0.05 ticks
    steps_005 = int(3.5 / 0.05) + 1
    for i in range(steps_005 + 1):
        z = round(i * 0.05, 2)
        if z <= 3.5:
            set_z.add(z)
    # 0.01 ticks
    steps_001 = int(3.5 / 0.01) + 1
    for i in range(steps_001 + 1):
        z = round(i * 0.01, 2)
        if z <= 3.5:
            set_z.add(z)

    z_values = sorted(set_z)

    # Now determine tick sizes & stroke widths reliably by inspecting the integer*100 representation
    z_tick_sizes = []
    z_stroke_widths = []
    for z in z_values:
        val100 = int(round(z * 100))
        if val100 % 100 == 0:
            z_tick_sizes.append(15)
            z_stroke_widths.append(2.0)
        elif val100 % 10 == 0:
            # 0.1 increments
            z_tick_sizes.append(10)
            z_stroke_widths.append(1.2)
        elif val100 % 5 == 0:
            # 0.05 increments
            z_tick_sizes.append(6)
            z_stroke_widths.append(0.8)
        else:
            # 0.01 increments (micro ticks)
            z_tick_sizes.append(4)
            z_stroke_widths.append(0.5)

    # Labels we want on z-scale (rounded)
    z_label_values = [
        0, 1.0, 2.0, 3.0, 3.5,
        0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
        1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
        2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9,
        3.1, 3.2, 3.3, 3.4
    ]
    z_label_values = sorted(set(round(v, 2) for v in z_label_values))

    generate_ticks("z", z_values, z_tick_sizes, z_stroke_widths, is_z_scale=True, label_values=z_label_values)

    # ---------------- P scale ticks ----------------
    p_values_set = set()
    major_p = [
        0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7,
        0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9,
        0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99,
        0.991, 0.992, 0.993, 0.994, 0.995, 0.996, 0.997, 0.998, 0.999
    ]
    for p in major_p:
        p_values_set.add(round(p, 4))

    # minor p intervals via rounded numpy ranges
    minor_p_intervals = [
        (0.5, 0.6, 0.01),
        (0.6, 0.7, 0.01),
        (0.7, 0.8, 0.01),
        (0.8, 0.9, 0.01),
        (0.9, 0.95, 0.005),
        (0.95, 0.99, 0.002),
        (0.99, 0.999, 0.001)
    ]
    for start, end, step in minor_p_intervals:
        # use integer stepping to avoid float drift
        n_steps = int(round((end - start) / step))
        for k in range(1, n_steps):
            p = round(start + k * step, 6)
            if p < end:
                p_values_set.add(round(p, 6))

    p_values = sorted(p_values_set)

    # Build p tick sizes (major vs minor)
    p_tick_sizes = []
    p_stroke_widths = []
    major_set = set(round(x, 6) for x in major_p)
    for p in p_values:
        if round(p, 6) in major_set:
            p_tick_sizes.append(12)
            p_stroke_widths.append(1.5)
        else:
            p_tick_sizes.append(8)
            p_stroke_widths.append(1.0)

    # Generate p-scale ticks, labels at major_p positions (use same generate_ticks function)
    generate_ticks("p", p_values, p_tick_sizes, p_stroke_widths, is_z_scale=False, label_values=major_p)

    # Add subtle grid lines at major intervals
    for z in [1.0, 2.0, 3.0]:
        x_pos = z_to_position(z)
        dwg.add(dwg.line(start=(x_pos, rule_y1 - 15), end=(x_pos, rule_y2 + 15),
                         stroke=rgb(230, 230, 230), stroke_width=1, stroke_dasharray="3,3"))

    # Add region indicators
    dwg.add(dwg.text(".", insert=(margin + rule_width*0.25, rule_y2 + 55),
                     text_anchor="middle", font_size=11,
                     font_family="Arial", fill=rgb(120, 120, 120)))

    dwg.add(dwg.text(".", insert=(margin + rule_width*0.75, rule_y2 + 55),
                     text_anchor="middle", font_size=11,
                     font_family="Arial", fill=rgb(120, 120, 120)))

    # Add decorative bounding box
    rule_box = dwg.rect(insert=(margin-10, rule_y1-25), size=(rule_width+20, rule_y2-rule_y1+50),
                        fill="none", stroke=rgb(200, 200, 200), stroke_width=1.5, rx=6, ry=6)
    dwg.add(rule_box)

    # Add clean title and information
    dwg.add(dwg.text("High-Detail Statistical Slide Rule",
                     insert=(width/2, 60), text_anchor="middle",
                     font_size=18, font_family="Arial", font_weight="bold", fill=rgb(0, 0, 0)))

    dwg.add(dwg.text("Z-Score to Probability Conversion (Normal Distribution)",
                     insert=(width/2, 90), text_anchor="middle",
                     font_size=12, font_family="Arial", fill=rgb(100, 100, 100)))

    # Add measurement guide marks at the ends
    for x in [margin, width - margin]:
        dwg.add(dwg.line(start=(x, rule_y1 - 8), end=(x, rule_y2 + 8),
                         stroke=rgb(120, 120, 120), stroke_width=1.5))

    # Save the SVG
    dwg.save()
    print(f"High-detail slide rule saved as {output_file}")
    print("Fixes applied:")
    print("- Robust float-handling for labels (rounded membership checks)")
    print("- Corrected compressed-region position math in z_to_position()")
    print("- Deterministic tick-size assignment (100*x logic) to avoid accidental skipping")
    print("- Labels for decimals and p-values now appear where expected")

if __name__ == "__main__":
    generate_enhanced_stat_slide_rule()
