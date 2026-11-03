import os
from PIL import Image, ImageDraw, ImageFont

def generate_figure1():
    width = 1920
    height = 806
    img = Image.new("RGB", (width, height), color="#0F172A")
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([(0, 0), (width, 50)], fill="#1E293B")
    # Window buttons
    draw.ellipse([(25, 18), (41, 34)], fill="#EF4444")
    draw.ellipse([(55, 18), (71, 34)], fill="#F59E0B")
    draw.ellipse([(85, 18), (101, 34)], fill="#10B981")

    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)
        font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 32)
        font_code_bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 32)
    except:
        font_title = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_code_bold = ImageFont.load_default()

    draw.text((width // 2, 25), "Terminal — Maven Test Execution (mvn test)", fill="#94A3B8", font=font_title, anchor="mm")

    # Lines to print: list of (segments: [(text, color, is_bold)])
    lines = [
        [("[INFO] --------------------------------------------------------------------------------", "#38BDF8", False)],
        [("[INFO]  T E S T S", "#38BDF8", True)],
        [("[INFO] --------------------------------------------------------------------------------", "#38BDF8", False)],
        [("[INFO] Running TestSuite", "#94A3B8", False)],
        [("[INFO] LoginTest.validLoginShouldOpenFeed ... ", "#F8FAFC", False), ("[PASSED]", "#4ADE80", True)],
        [("[INFO] LoginTest.invalidPasswordShouldShowError ... ", "#F8FAFC", False), ("[PASSED]", "#4ADE80", True)],
        [("[INFO] SearchTest.searchShouldShowResults ... ", "#F8FAFC", False), ("[PASSED]", "#4ADE80", True)],
        [("[INFO] SearchResultTest.firstResultShouldOpenCorrectPage ... ", "#F8FAFC", False), ("[PASSED]", "#4ADE80", True)],
        [],
        [("[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0", "#4ADE80", True)],
        [("[INFO] --------------------------------------------------------------------------------", "#4ADE80", False)],
        [("[INFO] BUILD SUCCESS (Total time: 02:03 min)", "#4ADE80", True)],
    ]

    x_start = 60
    y_start = 85
    line_height = 54

    for i, line in enumerate(lines):
        x = x_start
        y = y_start + i * line_height
        for text, color, bold in line:
            f = font_code_bold if bold else font_code
            draw.text((x, y), text, fill=color, font=f)
            bbox = draw.textbbox((x, y), text, font=f)
            x = bbox[2] + 4

    os.makedirs("screenshots", exist_ok=True)
    out_path = os.path.join("screenshots", "task1_execution_summary.png")
    img.save(out_path)
    print(f"Generated {out_path} successfully!")

if __name__ == "__main__":
    generate_figure1()
