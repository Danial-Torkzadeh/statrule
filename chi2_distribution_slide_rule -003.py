import numpy as np
from scipy.stats import chi2
from svgwrite import Drawing, rgb
import math

def generate_chi2_distribution_slide_rule(output_file="chi2_distribution_slide_rule_enhanced005.svg"):
    # === CONFIGURABLE LINES: Define your 4 degrees of freedom here ===
    df1 = 7    # ✅ CHANGE THIS VALUE AS NEEDED
    df2 = 14   # ✅ CHANGE THIS VALUE AS NEEDED
    df3 = 28   # ✅ CHANGE THIS VALUE AS NEEDED
    df4 = 35   # ✅ CHANGE THIS VALUE AS NEEDED
    
    # Create list from these 4 variables
    dfs = [df1, df2, df3, df4]
    
    # Configuration
    width, height = 1800, 800
    margin = 80
    rule_width = width - 2 * margin

    # Adjusted probability display range for chi-square (right-tailed)
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
    chi2_y_positions = [250, 350, 450, 550]  # Fixed for df1, df2, df3, df4
    
    # Fixed colors for 4 df lines
    chi2_colors = [rgb(255, 0, 0), rgb(0, 128, 0), rgb(0, 0, 255), rgb(128, 0, 128)]  # Red, Green, Blue, Purple

    # Draw probability baseline
    dwg.add(dwg.line(start=(margin, prob_y), end=(width - margin, prob_y),
                     stroke=rgb(0, 0, 0), stroke_width=2))
    dwg.add(dwg.text("Probability (P) - Right Tail", insert=(width/2, prob_y - 30), text_anchor="middle",
                     font_size=12, font_family="Arial", fill=rgb(0, 0, 0)))

    # Draw chi-square distribution baselines - using df1, df2, df3, df4 explicitly
    dwg.add(dwg.line(start=(margin, chi2_y_positions[0]), end=(width - margin, chi2_y_positions[0]),
                     stroke=chi2_colors[0], stroke_width=2))
    dwg.add(dwg.text(f"Chi-square distribution (df={df1})", insert=(width/2, chi2_y_positions[0] - 30), 
                     text_anchor="middle", font_size=12, font_family="Arial", fill=chi2_colors[0]))

    dwg.add(dwg.line(start=(margin, chi2_y_positions[1]), end=(width - margin, chi2_y_positions[1]),
                     stroke=chi2_colors[1], stroke_width=2))
    dwg.add(dwg.text(f"Chi-square distribution (df={df2})", insert=(width/2, chi2_y_positions[1] - 30), 
                     text_anchor="middle", font_size=12, font_family="Arial", fill=chi2_colors[1]))

    dwg.add(dwg.line(start=(margin, chi2_y_positions[2]), end=(width - margin, chi2_y_positions[2]),
                     stroke=chi2_colors[2], stroke_width=2))
    dwg.add(dwg.text(f"Chi-square distribution (df={df3})", insert=(width/2, chi2_y_positions[2] - 30), 
                     text_anchor="middle", font_size=12, font_family="Arial", fill=chi2_colors[2]))

    dwg.add(dwg.line(start=(margin, chi2_y_positions[3]), end=(width - margin, chi2_y_positions[3]),
                     stroke=chi2_colors[3], stroke_width=2))
    dwg.add(dwg.text(f"Chi-square distribution (df={df4})", insert=(width/2, chi2_y_positions[3] - 30), 
                     text_anchor="middle", font_size=12, font_family="Arial", fill=chi2_colors[3]))

    # Probability ticks (using right-tail probabilities for chi-square)
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

    # === COMPREHENSIVE CHI-SQUARE TICKS FUNCTION WITH ALL DECIMAL MARKS ===
    def add_chi2_ticks(degrees_of_freedom, y_pos, color):
        # Determine chi-square range that maps to visible probability range
        try:
            min_chi2 = chi2.ppf(1 - P_DISPLAY_MAX, degrees_of_freedom)
            max_chi2 = chi2.ppf(1 - P_DISPLAY_MIN, degrees_of_freedom)
            
            # Handle edge cases for very small or large df
            if min_chi2 < 0 or math.isnan(min_chi2):
                min_chi2 = 0.1
            if max_chi2 > 1000 or math.isnan(max_chi2):
                max_chi2 = degrees_of_freedom * 5
        except:
            # Fallback if ppf fails
            min_chi2 = 0.1
            max_chi2 = degrees_of_freedom * 5
        
        # Ensure we have at least some reasonable range
        if max_chi2 - min_chi2 < 1:
            max_chi2 = min_chi2 + 5
            
        # Generate major tick values (at integer chi-square values)
        major_ticks = []
        # Start from the first integer >= min_chi2
        start_int = max(1, math.ceil(min_chi2))
        
        # Add major ticks at integer values within range
        for chi2_val in range(start_int, int(max_chi2) + 1):
            p_right_tail = 1 - chi2.cdf(chi2_val, degrees_of_freedom)
            if P_DISPLAY_MIN <= p_right_tail <= P_DISPLAY_MAX:
                x_pos = p_to_position(p_right_tail)
                major_ticks.append((chi2_val, p_right_tail, x_pos))
        
        # Add major ticks with labels
        for chi2_val, p, x_pos in major_ticks:
            tick_size = 15
            stroke_width = 2.0
            font_size = 10
            
            # Format label as integer
            chi2_label = f"{chi2_val:.0f}"
            
            dwg.add(dwg.line(start=(x_pos, y_pos), end=(x_pos, y_pos + tick_size),
                             stroke=color, stroke_width=stroke_width))
            dwg.add(dwg.text(chi2_label, insert=(x_pos, y_pos + tick_size + 14), 
                             text_anchor="middle", font_size=font_size, 
                             font_family="Arial", fill=color))
        
        # === ADD DECIMAL TICKS EVERY 0.1 UNITS FOR FULL COVERAGE ===
        # Generate all possible decimal ticks in the range
        current = start_int
        while current <= max_chi2:
            # For each 0.1 increment
            for dec in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
                chi2_val = current + dec
                if chi2_val > max_chi2:
                    break
                    
                p_right_tail = 1 - chi2.cdf(chi2_val, degrees_of_freedom)
                if P_DISPLAY_MIN <= p_right_tail <= P_DISPLAY_MAX:
                    x_pos = p_to_position(p_right_tail)
                    
                    # Add a small tick for the decimal
                    tick_height = 5
                    dwg.add(dwg.line(start=(x_pos, y_pos), end=(x_pos, y_pos + tick_height),
                                     stroke=color, stroke_width=0.6))
            
            current += 1
        
        # === ADD FINE TAIL MARKS (0.01 INCREMENTS) IN EXTREME RIGHT TAIL ===
        # This is the high-precision region for hypothesis testing
        tail_start_p = 0.990
        tail_end_p = 0.999
        tail_start_x = p_to_position(tail_start_p)
        tail_end_x = p_to_position(tail_end_p)
        
        if tail_end_x - tail_start_x > 10:  # Only if there's enough space
            # Get the chi-square range for the tail region
            start_chi2 = chi2.ppf(1 - tail_start_p, degrees_of_freedom)
            end_chi2 = chi2.ppf(1 - tail_end_p, degrees_of_freedom)
            
            # Generate 0.01 marks in this range for maximum precision
            current = start_chi2
            
            while current <= end_chi2:
                p_val = 1 - chi2.cdf(current, degrees_of_freedom)
                if tail_start_p <= p_val <= tail_end_p:
                    x_pos = p_to_position(p_val)
                    
                    # Add very fine 0.01 mark
                    dwg.add(dwg.line(start=(x_pos, y_pos), end=(x_pos, y_pos + 3),
                                     stroke=color, stroke_width=0.3))
                current += 0.01  # 0.01 increments for extreme precision

    # Add all ticks - using df1, df2, df3, df4 explicitly
    add_chi2_ticks(df1, chi2_y_positions[0], chi2_colors[0])
    add_chi2_ticks(df2, chi2_y_positions[1], chi2_colors[1])
    add_chi2_ticks(df3, chi2_y_positions[2], chi2_colors[2])
    add_chi2_ticks(df4, chi2_y_positions[3], chi2_colors[3])

    # Add probability ticks
    add_probability_ticks()
    add_probability_minor_ticks()

    # Title and info
    dwg.add(dwg.text("Enhanced Chi-Square Distribution Slide Rule", insert=(width/2, 60), text_anchor="middle",
                     font_size=18, font_family="Arial", font_weight="bold", fill=rgb(0, 0, 0)))
    dwg.add(dwg.text("Right-Tail Probabilities with Warped Chi-Square Scales", 
                     insert=(width/2, 90), text_anchor="middle",
                     font_size=12, font_family="Arial", fill=rgb(100, 100, 100)))

    explanation_y = chi2_y_positions[3] + 80  # Using df4's y position
    dwg.add(dwg.text("How to use: Align right-tail probability on top scale with corresponding chi-square value on any chi-square scale", 
                     insert=(width/2, explanation_y), text_anchor="middle",
                     font_size=10, font_family="Arial", fill=rgb(80, 80, 80)))
    dwg.add(dwg.text("Expanded extremes for higher precision in tail probabilities (important for hypothesis testing)", 
                     insert=(width/2, explanation_y + 20), text_anchor="middle",
                     font_size=10, font_family="Arial", fill=rgb(80, 80, 80)))

    # Legend - using df1, df2, df3, df4 explicitly
    legend_x = margin
    legend_y = chi2_y_positions[3] + 120  # Using df4's y position
    dwg.add(dwg.circle(center=(legend_x, legend_y), r=5, fill=chi2_colors[0]))
    dwg.add(dwg.text(f"df = {df1}", insert=(legend_x + 15, legend_y + 5), 
                     font_size=10, font_family="Arial", fill=chi2_colors[0]))
    
    legend_x += 120
    dwg.add(dwg.circle(center=(legend_x, legend_y), r=5, fill=chi2_colors[1]))
    dwg.add(dwg.text(f"df = {df2}", insert=(legend_x + 15, legend_y + 5), 
                     font_size=10, font_family="Arial", fill=chi2_colors[1]))
    
    legend_x += 120
    dwg.add(dwg.circle(center=(legend_x, legend_y), r=5, fill=chi2_colors[2]))
    dwg.add(dwg.text(f"df = {df3}", insert=(legend_x + 15, legend_y + 5), 
                     font_size=10, font_family="Arial", fill=chi2_colors[2]))
    
    legend_x += 120
    dwg.add(dwg.circle(center=(legend_x, legend_y), r=5, fill=chi2_colors[3]))
    dwg.add(dwg.text(f"df = {df4}", insert=(legend_x + 15, legend_y + 5), 
                     font_size=10, font_family="Arial", fill=chi2_colors[3]))

    # Bounding box
    rule_box = dwg.rect(insert=(margin-10, prob_y-40), size=(rule_width+20, chi2_y_positions[3] - prob_y + 180),
                        fill="none", stroke=rgb(200, 200, 200), stroke_width=1.5, rx=6, ry=6)
    dwg.add(rule_box)

    # Fix right-hand side emptiness by adding a vertical line and extending the probability scale
    dwg.add(dwg.line(start=(width - margin, prob_y), end=(width - margin, chi2_y_positions[3] + 100),
                     stroke=rgb(0, 0, 0), stroke_width=1.5))
    
    # Add a small label at the far right to indicate the end of the scale
    dwg.add(dwg.text("End", insert=(width - margin - 15, chi2_y_positions[3] + 120),
                     font_size=10, font_family="Arial", fill=rgb(0, 0, 0), text_anchor="end"))
    
    # Also extend the probability scale slightly to make it more visually balanced
    dwg.add(dwg.line(start=(margin, prob_y), end=(width - margin - 10, prob_y),
                     stroke=rgb(0, 0, 0), stroke_width=2))

    dwg.save()
    print(f"Enhanced Chi-square distribution slide rule saved as {output_file}")
    print(f"Created with degrees of freedom: df1={df1}, df2={df2}, df3={df3}, df4={df4}")
    print("Probability scale uses right-tail probabilities (1 - CDF)")
    print("Chi-square scales now feature comprehensive decimal marking")

def generate_custom_chi2_slide_rule(df1=5, df2=12, df3=30, df4=100, output_file="custom_chi2_slide_rule_enhanced.svg"):
    # Wrapper function to allow passing df values as parameters
    import types
    def temp_func(output_file=output_file):
        # Use the same configurable lines approach
        globals()['df1'], globals()['df2'], globals()['df3'], globals()['df4'] = df1, df2, df3, df4
        generate_chi2_distribution_slide_rule(output_file)
    
    temp_func(output_file)


if __name__ == "__main__":
    # This is the ONLY place you need to change df values
    generate_chi2_distribution_slide_rule()
