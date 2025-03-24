import curses
from curses import wrapper
from curses.textpad import rectangle
import time
import random

CENTER_ROW = 0
CENTER_COL = 0

def start_screen(stdscr):
    stdscr.clear()
    
    ascii_art = [
        "████████╗██╗   ██╗██████╗ ███████╗██████╗    ████████╗██╗   ██╗██╗",
        "╚══██╔══╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗   ╚══██╔══╝██║   ██║██║",
        "   ██║    ╚████╔╝ ██████╔╝█████╗  ██████╔╝█████╗██║   ██║   ██║██║",
        "   ██║     ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗╚════╝██║   ██║   ██║██║",
        "   ██║      ██║   ██║     ███████╗██║  ██║      ██║   ╚██████╔╝██║",
        "   ╚═╝      ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝      ╚═╝    ╚═════╝ ╚═╝",
    ]
    
    for i, line in enumerate(ascii_art):
        stdscr.addstr(CENTER_ROW - len(ascii_art)//2 + i - 2, CENTER_COL - len(line)//2, line)
    
    stdscr.addstr(CENTER_ROW + 5, CENTER_COL - len("Press any key to begin...") // 2, "Press any key to begin...")
    stdscr.addstr(CENTER_ROW + 6, CENTER_COL - len("Ctrl+C to exit | Esc for new paragraph") // 2, "Ctrl+C to exit | Esc for new paragraph")
    
    stdscr.refresh()
    stdscr.getkey()


def generate_random_sentence(word_list):
    random_words = random.sample(word_list, 10)
    sentence = ' '.join(random_words)
    return sentence

def load_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.readlines()
    words = [word.strip() for word in words]
    return words

def display_completion_screen(stdscr, wpm, time_taken):
    stdscr.clear()

    box_height = 7
    box_width = 40
    box_row_start = CENTER_ROW - box_height // 2
    box_col_start = CENTER_COL - box_width // 2
    box_row_end = box_row_start + box_height
    box_col_end = box_col_start + box_width

    rectangle(stdscr, box_row_start, box_col_start, box_row_end, box_col_end)

    stdscr.addstr(box_row_start + 1, box_col_start + (box_width // 2) - len("TEXT COMPLETED") // 2, "TEXT COMPLETED", curses.A_BOLD)
    stdscr.addstr(box_row_start + 3, box_col_start + 4, f"Time Taken: {time_taken:.2f} seconds")
    stdscr.addstr(box_row_start + 4, box_col_start + 4, f"Words Per Minute: {wpm}")
    stdscr.addstr(box_row_start + 5, box_col_start + 4, "Press any key to continue...")

    stdscr.refresh()
    stdscr.getkey()

def wpm_test(stdscr):
    stdscr.clear()
    word_list = load_words_from_file('word_list.txt')
    target_text = generate_random_sentence(word_list)
    current_text = []
    start_time = time.time()
    stdscr.nodelay(True)

    row = CENTER_ROW - 1
    col = CENTER_COL - len(target_text) // 2
    
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.addstr(row, col, target_text)
        stdscr.addstr(CENTER_ROW + 1, CENTER_COL - len(" WPM: 99 ") // 2, f" WPM: {wpm} ", curses.A_REVERSE)

        for i, char in enumerate(current_text):
            correct_char = target_text[i]
            color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
            stdscr.addstr(row, col + i, char, color)

        stdscr.move(row, col + len(current_text))

        stdscr.refresh()
        
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            time_taken = time.time() - start_time
            display_completion_screen(stdscr, wpm, time_taken)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if key == "\x1b":
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    global CENTER_ROW, CENTER_COL
    CENTER_ROW = curses.LINES // 2
    CENTER_COL = curses.COLS // 2

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)

if __name__ == "__main__":
    try:
        wrapper(main)
    except KeyboardInterrupt:
        print("\nProgram exited Goodbye!")

