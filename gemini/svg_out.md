```python
#! /usr/bin/env python3

import sys
import xml.dom.minidom
import re

def modify_svg(input_file, output_file):
    """Modifies an SVG file to change stroke-width and circle radius.

    Args:
        input_file: Path to the input SVG file.
        output_file: Path to the output SVG file.
    
    Raises:
        FileNotFoundError: If the input SVG file does not exist.
        Exception: If any error occurs during XML processing.  Provides informative error messages.

    """
    try:
        with open(input_file, 'r') as f:
            svg_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Input file '{input_file}' not found.")

    try:
        dom = xml.dom.minidom.parseString(svg_content)
    except Exception as e:
        raise Exception(f"Error parsing XML: {e}.  Please ensure the input file is a valid SVG file.")


    pattern1 = r"stroke-width:\s*\d+(\.\d+)?\s*"  # Matches "stroke-width: [number]"
    pattern2 = r"stroke-width: 3"  # Replacement string


    for element in dom.getElementsByTagName("polyline"):
        style = element.getAttribute("style")
        if style:
            new_style = re.sub(pattern1, pattern2, style)
            if new_style != style:
                element.setAttribute("style", new_style)
            else:
                element.setAttribute("style", style + ";stroke-width:3")
        else:
            element.setAttribute("style", "stroke-width:3")


    for element in dom.getElementsByTagName("circle"):
        style = element.getAttribute("style")
        r = element.getAttribute("r")

        new_style = re.sub(pattern1, pattern2, style)
        if new_style != style:
            element.setAttribute("style", new_style)
        else:
            element.setAttribute("style", style + ";stroke-width:3")

        try:
            element.setAttribute("r", "5")
        except Exception as e:
            raise Exception(f"Error setting circle radius: {e}")


    with open(output_file, 'w') as f:
        f.write(dom.toprettyxml())
    
    dom.unlink() #Free up memory


def main():
    """Main function to handle command-line arguments and call modify_svg."""
    if len(sys.argv) != 3:
        print("Usage: python modify_svg.py <input_svg_file> <output_svg_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        modify_svg(input_file, output_file)
        print(f"SVG file '{input_file}' modified and saved to '{output_file}' successfully.")
    except (FileNotFoundError, Exception) as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
```
