import sys
import parser

def main():
    if len(sys.argv) <= 1:
        print("Provide a story to be played")
        sys.exit(1)

    storyboard = parser.parse_storyboard(sys.argv[1])
    storyboard.displayHeader()
    storyboard.play()
    storyboard.report_score()


if __name__ == '__main__':
    main()
