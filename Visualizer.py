import os
import subprocess

class Visualizer:

    @staticmethod
    def svg(graphFile):
        if not os.path.isfile(graphFile):
            raise FileNotFoundError(f"File not found: {graphFile}")

        svgFile = graphFile.replace(".d2", ".svg")

        try:
            subprocess.run(
                ["d2", graphFile, svgFile],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"SVG generated successfully: {svgFile}")
        except FileNotFoundError:
            raise RuntimeError("d2 utility not installed")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error generating SVG:\n{e.stderr}"
            )


    @staticmethod
    def ascii(graphFile):
        if not os.path.isfile(graphFile):
            raise FileNotFoundError(f"File not found: {graphFile}")

        try:
            result = subprocess.run(
                ["d2", graphFile, "--stdout-format=ascii", "-"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(result.stdout)
        except FileNotFoundError:
            raise RuntimeError("d2 utility not installed")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip()
            raise RuntimeError(f"Error rendering ASCII: {error_msg}")
