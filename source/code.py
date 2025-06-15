import board
import digitalio
import displayio
from displayio import OnDiskBitmap
import json
import time
import terminalio
from adafruit_display_text import label


# function: change the currently dispalyed image
def display_bmp(filename, alt_text):
    global tile_grid

    if tile_grid is not None:
        main_group.pop()  # Remove previous tilegrid
    try:
        bitmap = OnDiskBitmap(open(filename, "rb"))
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        main_group.append(tile_grid)
    except Exception as e:
        screen_width = 240  # dispaly width in pixels
        char_width = 6  # character width in pixels (estimated)
        text_pixel_length = (len(alt_text) * char_width) + left_margin
        scale_factor = screen_width // text_pixel_length
        scale_factor = max(1, scale_factor) # Ensure scale is at least 1
        text_area = label.Label(terminalio.FONT, text=alt_text,color=text_color,scale=scale_factor)
        text_area.x = left_margin
        text_area.y = top_margin
        main_group.append(text_area)


# function: Load A game from the specified index
def select_game(game_index):
    global loaded_game
    loaded_game = current_index  # set the current indexed game as the loaded game
    display_bmp(loading_image, "Loading...")  # display loading
    reset_out.value = False  # hold game in reset

    # set dips
    dip_val_bin = dip_hex_to_bin(game_list[loaded_game]["dip_val"])
    for i, bit in enumerate(dip_val_bin):
        gpio_pins[i].value = True if bit == dip_on else False

    time.sleep(reset_time)  # wait for reset timer
    reset_out.value = True  # release reset
    display_bmp(game_list[loaded_game]["image"], game_list[loaded_game]["title"])  # replace loading image with game image
    save_selection(loaded_game)  # save the selection for use on reboot


# converts the hex dip val in the json to binary string
def dip_hex_to_bin(dip_val_hex):
    dip_val_int = int(dip_val_hex, 16)
    dip_val_bin = f'{dip_val_int:0{dip_bits}b}'
    return dip_val_bin


# function save the selected game index for use on reboot
# TODO: Fix this, this function doesn't currently work (permissions/write enabled?)
def save_selection(index):
    try:  # this will fail when USB is connected, so we will try and ignore if fail
        with open("/saved_index.txt", "w") as f:
            f.write(str(index))
    except Exception:
        pass

# configure reset GPIO (do this first so we can hold in reset during rest of the load
reset_out = digitalio.DigitalInOut(board.D13)
reset_out.switch_to_output(
    value=False,  # start LOW (reset on boot)
    #drive_mode=digitalio.DriveMode.OPEN_DRAIN #this is added on optionally later once config is parsed
)

# configure selector GPIOs
gpio_pins = []
gpio_pins.append(digitalio.DigitalInOut(board.D11))  # SEL1
gpio_pins.append(digitalio.DigitalInOut(board.D10))  # SEL2
gpio_pins.append(digitalio.DigitalInOut(board.D9))  # SEL3
gpio_pins.append(digitalio.DigitalInOut(board.D6))  # SEL4
gpio_pins.append(digitalio.DigitalInOut(board.D5))  # SEL5
gpio_pins.append(digitalio.DigitalInOut(board.D4))  # SEL6
gpio_pins.append(digitalio.DigitalInOut(board.D3))  # SEL7
for pin in gpio_pins:  # loop through the selection pins
    pin.direction = digitalio.Direction.OUTPUT  # configure them as outputs


# configure buttons
button_up = digitalio.DigitalInOut(board.D0)
button_up.switch_to_input(pull=digitalio.Pull.UP)
button_down = digitalio.DigitalInOut(board.D2)
button_down.switch_to_input(pull=digitalio.Pull.DOWN)
button_select = digitalio.DigitalInOut(board.D1)
button_select.switch_to_input(pull=digitalio.Pull.DOWN)


# load multi_config.json
try:
    with open("/multi_config.json", "r") as f:
        multi_config = json.load(f)
    dip_on = multi_config["dip_on"]  # determines if a dip_on position is high (1) or low (0)
    dip_bits = multi_config["dip_bits"]  # determines the number of dip swiches that the multi supports
    reset_time = multi_config["reset_time"]  # How long to hold in reset when loading new game
    if multi_config["reset_open_drain"]:
        #reconfigure reset pin
        reset_out.switch_to_output(
          value=False,  # start LOW (reset on boot)
          drive_mode=digitalio.DriveMode.OPEN_DRAIN #add open drain
        )
    
except Exception:
    print("Error Loading multi_config.json")
    while True:
        pass  # stop here


# load menu_config.json
game_list = []
try:
    with open("/menu_config.json", "r") as f:
        menu_config = json.load(f)
    debounce_delay = menu_config["debounce_delay"]
    idle_timeout = menu_config["idle_timeout"]  # How long before reset? (seconds)
    loading_image = menu_config["loading_image"]  # the image file for the loading screen
    text_color = int(menu_config["text_color"], 16)  # color of the alt_text
    left_margin = menu_config["left_margin"]  # offset from the left edge of the alt_text
    top_margin = menu_config["top_margin"]  # offset from the top edge of the alt_text
    for game in menu_config["game_order"]:
        game_list.append(menu_config["gamedefs"][game])
        if game == menu_config["default_game"]:  # initial game loaded
            loaded_game = len(game_list)-1
    for game in game_list:
        dip_val_bin = dip_hex_to_bin(game["dip_val"])
        if len(dip_val_bin) > dip_bits:
            raise Exception(f"dip_val {game['dip_val']} out of range")
        if not game["image"]:
            raise Exception("image property missing from gamedef")
        if not game["title"]:
            raise Exception("title property missing from gamedef")
except Exception as e:
    print("Error Loading menu_config.json")
    print(f"Exception: {e}")
    while True:
        pass  # stop here


# load_last_selected_game
try:
    if menu_config["retain_selection"]:  # if the option to retain the last loaded game is set
        with open("/current_image.txt", "r") as f:  # open the saved index file
            content = f.read().strip()  # clean it up
            saved_index = loaded_game  # set defailt if the following checks fail
            if content.isdigit():  # only allow positive integers
                saved_index = int(content)  # convert the text to int
            if saved_index < len(game_list):  # make sure the index is inbounds
                loaded_game = saved_index  # set the loaded game
except Exception:
    pass  # do nothing

# configure the display handling, we do this after loading json so we can display errors on console
display = board.DISPLAY  # setup built-in display
tile_grid = None
main_group = displayio.Group()
display.root_group = main_group

# first run executions
current_index = loaded_game  # set the default menu selection to the current loaded_game
select_game(loaded_game)  # sets the initial game
last_interaction_time = time.monotonic()  # Track time of last button interaction


# main program loop
while True:
    now = time.monotonic()  # capture the current time of this loop

    if button_down.value:  # NEXT Game Button
        current_index = (current_index + 1) % len(game_list)
        display_bmp(game_list[current_index]["image"], game_list[current_index]["title"])
        last_interaction_time = now  # reset idle timer
        time.sleep(debounce_delay)  # debounce delay

    if not button_up.value:  # PREVIOUS Game Button
        current_index = (current_index - 1) % len(game_list)
        display_bmp(game_list[current_index]["image"], game_list[current_index]["title"])
        last_interaction_time = now  # reset idle timer
        time.sleep(debounce_delay)  # button debounce

    if button_select.value:  # SELECT Game Button
        select_game(current_index)  # load the selected game
        time.sleep(debounce_delay)  # button debounce

    # Check for idle timeout
    if now - last_interaction_time > idle_timeout:
        if current_index != loaded_game:
            current_index = loaded_game
            display_bmp(game_list[current_index]["image"], game_list[current_index]["title"])

