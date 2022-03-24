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
    draw.drawmenu()


if __name__ == "__main__":
    main()
