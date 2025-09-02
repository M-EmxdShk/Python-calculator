import tkinter as tk
from math import sin, cos, tan, sqrt, log, pi, e

# -------------------- Functions --------------------
def click(value):
    if value == "=":
        try:
            expr = screen.get().replace("×", "*").replace("÷", "/").replace("^", "**")
            expr = expr.replace("√", "sqrt").replace("ln", "log").replace("π", str(pi)).replace("e", str(e))
            result = str(eval(expr))
            screen.set(result)
        except:
            screen.set("Error")
    elif value == "AC":
        screen.set("")
    elif value == "±":
        try:
            value_num = float(screen.get())
            screen.set(str(-value_num))
        except:
            screen.set("Error")
    elif value == "%":
        try:
            value_num = float(screen.get())
            screen.set(str(value_num / 100))
        except:
            screen.set("Error")
    elif value == "Sci":
        toggle_scientific()
    else:
        screen.set(screen.get() + value)

def toggle_scientific():
    global sci_mode
    sci_mode = not sci_mode
    for b in sci_buttons:
        if sci_mode:
            b.place()  # show
        else:
            b.place_forget()  # hide

def key_press(event):
    if event.char in "0123456789+-*/().":
        screen.set(screen.get() + event.char)
    elif event.keysym == "Return":
        click("=")
    elif event.keysym == "BackSpace":
        screen.set(screen.get()[:-1])

# Button press animation
def on_press(event, btn):
    btn.config(bg=darken(btn.cget("bg"), 0.8))

def on_release(event, value, btn):
    btn.config(bg=btn.original_color)
    click(value)

def darken(color, factor):
    color = color.lstrip('#')
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f'#{r:02x}{g:02x}{b:02x}'

# -------------------- GUI Setup --------------------
root = tk.Tk()
root.title("iPhone Round Calculator")
root.geometry("400x650")
root.config(bg="black")
root.bind("<Key>", key_press)

sci_mode = False

# Display
screen = tk.StringVar()
entry = tk.Entry(root, textvar=screen, font=("Helvetica", 36), bd=0, bg="black", fg="white",
                 justify="right", insertbackground="white")
entry.pack(fill="both", ipadx=8, ipady=25, padx=10, pady=10)

# -------------------- Buttons --------------------
button_colors = {
    "numbers": "#333333",
    "operators": "#ff9500",
    "functions": "#a5a5a5",
}

basic_buttons = [
    ["AC", "±", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", "Sci"]
]

button_width = 70
button_height = 70
padding = 10
button_widgets = []
sci_buttons = []

def create_button(text, x, y, color):
    btn = tk.Button(root, text=text, font=("Helvetica", 24), bg=color, fg="white", bd=0,
                    relief="flat", highlightthickness=0)
    btn.place(x=x, y=y, width=button_width, height=button_height)
    btn.original_color = color
    btn.bind("<Button-1>", lambda e, b=btn: on_press(e, b))
    btn.bind("<ButtonRelease-1>", lambda e, val=text, b=btn: on_release(e, val, b))
    return btn

# Place basic buttons
start_x = 10
start_y = 200
for r, row in enumerate(basic_buttons):
    for c, char in enumerate(row):
        if char == "0":
            btn = create_button(char, start_x + c* (button_width + padding), start_y + r*(button_height+padding), button_colors["numbers"])
            btn.place_configure(width=button_width*2 + padding)
        elif char in ["+", "−", "×", "÷", "="]:
            btn = create_button(char, start_x + c*(button_width+padding), start_y + r*(button_height+padding), button_colors["operators"])
        elif char in ["AC", "±", "%", "Sci"]:
            btn = create_button(char, start_x + c*(button_width+padding), start_y + r*(button_height+padding), button_colors["functions"])
        else:
            btn = create_button(char, start_x + c*(button_width+padding), start_y + r*(button_height+padding), button_colors["numbers"])
        button_widgets.append(btn)

# Scientific buttons
sci_layout = [
    ["sin", "cos", "tan", "π"],
    ["√", "^", "ln", "e"]
]

for r, row in enumerate(sci_layout):
    for c, char in enumerate(row):
        btn = create_button(char, start_x + 4*button_width + c*(button_width+padding), start_y + r*(button_height+padding), "#505050")
        btn.place_forget()
        sci_buttons.append(btn)

root.mainloop()
