"""
chart.py - Performance Plotting Module
Course: Design & Analysis of Algorithms (ETCCDA302)
Student: Saksham Singh | Roll No: 2501730270

Generates a line plot comparing runtime growth across input sizes
for Merge Sort, 0/1 Knapsack, Dijkstra, and Route Planning.
Saves the visualization to screenshots/runtime_chart.png.
"""

import os
from benchmark import run_all_benchmarks


def generate_chart():
    records = run_all_benchmarks()
    sizes = [r["n"] for r in records]
    t_sort = [r["t_sort"] for r in records]
    t_knap = [r["t_knapsack"] for r in records]
    t_dijk = [r["t_dijkstra"] for r in records]
    t_tour = [r["t_route"] for r in records]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    chart_file = os.path.join(base_dir, "..", "screenshots", "runtime_chart.png")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
        fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=150)

        ax.plot(sizes, t_sort, marker="o", linewidth=2, color="#1f77b4", label="Merge Sort: O(n log n)")
        ax.plot(sizes, t_knap, marker="s", linewidth=2, color="#ff7f0e", label="0/1 Knapsack (DP): O(n * W)")
        ax.plot(sizes, t_dijk, marker="^", linewidth=2, color="#2ca02c", label="Dijkstra Single-Run: O((V+E) log V)")
        ax.plot(sizes, t_tour, marker="D", linewidth=2, color="#d62728", label="Route Tour (Dijkstra + TSP): O(k^2 + k*Graph)")

        ax.set_title("Mini-Courier Planner: Algorithmic Runtime vs Input Size (N)", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Number of Input Parcels (N)", fontsize=11, labelpad=8)
        ax.set_ylabel("Average Execution Time (Milliseconds)", fontsize=11, labelpad=8)
        ax.set_xticks(sizes)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(frameon=True, facecolor="white", edgecolor="#cccccc", fontsize=10)

        fig.tight_layout()
        fig.savefig(chart_file, dpi=180)
        print(f"Chart saved with matplotlib: {chart_file}")

    except ImportError:
        # High-fidelity fallback renderer using Pillow
        from PIL import Image, ImageDraw, ImageFont

        w, h = 1200, 750
        img = Image.new("RGB", (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        try:
            f_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
            f_label = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 17)
            f_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 16)
            f_tick = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 15)
        except Exception:
            f_title = f_label = f_bold = f_tick = ImageFont.load_default()

        # Margins
        mx_left, mx_right, my_top, my_bottom = 110, 50, 80, 90
        plot_w = w - mx_left - mx_right
        plot_h = h - my_top - my_bottom

        # Background grid and axis
        draw.rectangle([mx_left, my_top, mx_left + plot_w, my_top + plot_h], fill=(250, 250, 252), outline=(200, 200, 205), width=1)

        # Title
        title_str = "Mini-Courier Planner: Algorithmic Runtime vs Input Size (N)"
        tw = draw.textlength(title_str, font=f_title)
        draw.text(((w - tw) // 2, 30), title_str, fill=(20, 20, 20), font=f_title)

        # Y scale: 0 to 2.5 ms
        y_max = 2.5
        for y_val in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]:
            py = my_top + plot_h - int((y_val / y_max) * plot_h)
            draw.line([mx_left, py, mx_left + plot_w, py], fill=(225, 225, 230), width=1)
            yt_str = f"{y_val:.1f}"
            ytw = draw.textlength(yt_str, font=f_tick)
            draw.text((mx_left - ytw - 14, py - 9), yt_str, fill=(80, 80, 80), font=f_tick)

        # X scale: sizes 25, 50, 100, 200
        x_min, x_max = 0, 220
        def get_x(val):
            return mx_left + int(((val - x_min) / (x_max - x_min)) * plot_w)

        def get_y(val):
            return my_top + plot_h - int((val / y_max) * plot_h)

        for s in sizes:
            px = get_x(s)
            draw.line([px, my_top, px, my_top + plot_h], fill=(225, 225, 230), width=1)
            st_str = str(s)
            stw = draw.textlength(st_str, font=f_tick)
            draw.text((px - stw // 2, my_top + plot_h + 10), st_str, fill=(80, 80, 80), font=f_tick)

        # Axis Titles
        x_label = "Number of Input Parcels (N)"
        xtw = draw.textlength(x_label, font=f_label)
        draw.text(((w - xtw) // 2, my_top + plot_h + 45), x_label, fill=(30, 30, 30), font=f_label)

        # Y label
        draw.text((15, my_top - 35), "Average Runtime (ms)", fill=(30, 30, 30), font=f_label)

        series = [
            ("Merge Sort: O(n log n)", t_sort, (31, 119, 180), "circle"),
            ("0/1 Knapsack (DP): O(n * W)", t_knap, (255, 127, 14), "square"),
            ("Dijkstra Single-Run: O((V+E) log V)", t_dijk, (44, 160, 44), "triangle"),
            ("Route Tour (Dijkstra + TSP)", t_tour, (214, 39, 40), "diamond")
        ]

        # Draw lines & markers
        for name, vals, col, shape in series:
            pts = [(get_x(s), get_y(v)) for s, v in zip(sizes, vals)]
            for p1, p2 in zip(pts, pts[1:]):
                draw.line([p1, p2], fill=col, width=3)
            for px, py in pts:
                if shape == "circle":
                    draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=col, outline=(255, 255, 255), width=2)
                elif shape == "square":
                    draw.rectangle([px - 5, py - 5, px + 5, py + 5], fill=col, outline=(255, 255, 255), width=2)
                elif shape == "triangle":
                    draw.polygon([(px, py - 6), (px - 5, py + 5), (px + 5, py + 5)], fill=col, outline=(255, 255, 255))
                elif shape == "diamond":
                    draw.polygon([(px, py - 6), (px - 5, py), (px, py + 6), (px + 5, py)], fill=col, outline=(255, 255, 255))

        # Legend Box
        leg_x, leg_y, leg_w, leg_h = mx_left + 25, my_top + 25, 330, 140
        draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=6, fill=(255, 255, 255, 230), outline=(210, 210, 215), width=1)
        for idx, (name, _, col, shape) in enumerate(series):
            iy = leg_y + 18 + idx * 28
            draw.line([leg_x + 16, iy, leg_x + 46, iy], fill=col, width=3)
            if shape == "circle":
                draw.ellipse([leg_x + 31 - 4, iy - 4, leg_x + 31 + 4, iy + 4], fill=col)
            elif shape == "square":
                draw.rectangle([leg_x + 31 - 4, iy - 4, leg_x + 31 + 4, iy + 4], fill=col)
            elif shape == "triangle":
                draw.polygon([(leg_x + 31, iy - 5), (leg_x + 31 - 4, iy + 4), (leg_x + 31 + 4, iy + 4)], fill=col)
            elif shape == "diamond":
                draw.polygon([(leg_x + 31, iy - 5), (leg_x + 31 - 4, iy), (leg_x + 31, iy + 5), (leg_x + 31 + 4, iy)], fill=col)

            draw.text((leg_x + 58, iy - 8), name, fill=(40, 40, 40), font=f_bold)

        img.save(chart_file, quality=95)
        print(f"Chart saved with PIL fallback: {chart_file}")


if __name__ == "__main__":
    generate_chart()
