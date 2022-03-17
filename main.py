"""
# mainfile
"""
import sys
from draw import Draw
sys.path.append(".")


def main():
    """
    # the main function
    """
    draw = Draw(playercount=1, npccount=1)
    draw.drawgame()


if __name__ == "__main__":
    main()
