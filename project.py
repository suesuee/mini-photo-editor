"""
This program takes an image and lets the users manipulate the image.
The program is named Mini Photo Editor.
"""
import random
from PIL import Image, ImageFont, ImageDraw
from simpleimage import SimpleImage

DEFAULT_FILE = 'images/marnie.jpg'

def main():

    # Get file and load image
    filename = get_file()

    original = SimpleImage(filename)
    my_image = Image.open(filename)

    # Show the original image
    original.show()

    # Ask the user what he want to do with the file. We have 6 options.
    print_explaination()

    # Manipulate the image
    while True:
        # Get user input
        user_input = get_user_input()
        # Decide what to do
        if user_input == 0:
            print()
            print("Thanks for playing!!! See you next time.")
            print("Have a great day~")
            break
        else:
            edit_image(original, my_image, user_input)


def edit_image(original, my_image, user_input):
    """
        Edit the image according to the numbers user has entered.

        Inputs:
            :param original: the original image to process from SimpleImage Library.
            :param my_image: the original image to process from Pillow Library.

        Returns:
            rotated images.
    """

    if user_input == 1:
        border_size = int(input("Enter border size: "))
        bordered_image = add_border(original, border_size)
        bordered_image.show()

    elif user_input == 2:
        threshold = int(input("Enter the threshold amount between 0 and 255: "))
        while threshold < 0 or threshold > 255:
            print("Invalid input.")
            threshold = int(input("Enter the threshold amount between 0 and 255: "))
        filtered_image = add_filter(original, threshold)
        filtered_image.show()

    elif user_input == 3:
        text = input("Enter the text you want to display on the image: ")
        text_image = add_texts(my_image, text)
        text_image.show()

    elif user_input == 4:
        reflected_image = add_reflection(original)
        reflected_image.show()

    elif user_input == 5:
        image_collage = repeat(original)
        image_collage.show()

    elif user_input == 6:
        rotated_image = rotate(my_image)
        rotated_image.show()

def rotate(image):
    """
        Rotate the image by the user's desired degrees input from 0 to 360 degrees.

        Inputs:
            :param image: the original image to process.

        Returns:
            rotated images.
    """
    # Load the original image, and get its size and color mode.
    width, height = image.size
    mode = image.mode

    # Load all pixels from the image.
    orig_pixel_map = image.load()

    # Create a new image matching the original image's color mode, and size.
    #   Load all the pixels from this new image as well.
    rotated_image = Image.new(mode, (width, height))
    new_pixel_map = rotated_image.load()

    # Modify each pixel in the new image.
    for x in range(width):
        for y in range(height):
            # Copy the original pixel to the new pixel map.
            new_pixel_map[x, y] = orig_pixel_map[x, y]

    # Ask for the rotation degrees
    rotate = int(input("Enter the degrees you want to rotate (0-360): "))
    # Rotate it by 45 degrees
    rotated_image = rotated_image.rotate(rotate)
    # Display the Image rotated by 45 degrees
    return rotated_image

def repeat(original):
    """
        Main function. Asks for rows, cols and patch size from the user.
        Create a blank image which to be used in define_start_pt function.

        Inputs:
            :param original: the original image to process.

        Returns:
            repeated images.
    """
    rows = int(input("Enter rows: "))
    cols = int(input("Enter cols: "))
    patch_size = 333
    width = cols * patch_size
    height = rows * patch_size
    # create a blank image
    final_image = SimpleImage.blank(width, height)
    # define start point x and y
    define_start_pt(final_image, rows, cols, patch_size, original)
    # show the result
    return final_image

def get_rgb_scales():
    """
    Get RGB values randomly

    Returns:
         list containing the random RGB values.
    """
    random_red = random.uniform(0, 2)
    random_green = random.uniform(0, 2)
    random_blue = random.uniform(0, 2)
    return random_red, random_green, random_blue

def define_start_pt(final_image, rows, cols, patch_size, original):
    """
        Define the start x and y and color each patch using the value from get_rgb_scales().
        Had an another function to put the patch in each row and col at the end.

        Inputs:
            :param final_image: the blank image which we will copy the patch into.
            :param start_x: the starting point of each patch horizontally.
            :param start_y: the starting point of each pathch vertically.
            :param patch_size: the size of the patch.
            :param original: the original image without random colors.

        Returns:
            No return
    """
    ask_user = input("Do you want to add colors randomly? (Y/N): ")
    for i in range(rows):
        for j in range(cols):
            if ask_user == "Y":
                random_red, random_green, random_blue = get_rgb_scales()
                patch = make_recolored_patch(random_red, random_green, random_blue)
                start_x = j * patch.width
                start_y = i * patch.height
                put_patch_with_colors(final_image, start_x, start_y, patch, patch_size)
            elif ask_user == "N":
                start_x = j * original.width
                start_y = i * original.height
                put_patch(final_image, start_x, start_y, original, patch_size)

def put_patch(final_image, start_x, start_y, original, patch_size):
    """
        Copying from final_image into each patch.

        Inputs:
            :param final_image: the blank image which we will copy the patch into.
            :param start_x: the starting point of each patch horizontally.
            :param start_y: the starting point of each pathch vertically.
            :param original: the original image without random colors.
            :param patch_size: the size of the patch.

        Returns:
            No return
    """
    for y in range(patch_size):
        for x in range(patch_size):
            pixel = original.get_pixel(x, y)
            final_image.set_pixel(start_x + x, start_y + y, pixel)

def put_patch_with_colors(final_image, start_x, start_y, patch, patch_size):
    """
        Copying from final_image into each patch.

        Inputs:
            :param final_image: the blank image which we will copy the patch into.
            :param start_x: the starting point of each patch horizontally.
            :param start_y: the starting point of each pathch vertically.
            :param patch: the original image with random colors.
            :param patch_size: the size of the patch.

        Returns:
            No return
    """
    for y in range(patch_size):
        for x in range(patch_size):
            pixel = patch.get_pixel(x, y)
            final_image.set_pixel(start_x + x, start_y + y, pixel)

def make_recolored_patch(red_scale, green_scale, blue_scale):
    """
        Implement this function to make a patch for the Warhol Filter.
        It loads the patch image and recolors it.

        Inputs:
            :param red_scale: A number to multiply each pixel's red component by
            :param green_scale: A number to multiply each pixel's green component by
            :param blue_scale: A number to multiply each pixel's blue component by

        Returns:
               Returns the newly generated patch.
    """
    patch = SimpleImage(DEFAULT_FILE)
    for pixel in patch:
        pixel.red *= red_scale
        pixel.green *= green_scale
        pixel.blue *= blue_scale
    return patch

def add_reflection(image):
    """
        This function returns a new reflected image.

        Inputs:
            - image: The original image to process

        Returns:
            A new reflected image.
    """
    width = image.width
    height = image.height
    # create a new image to contain mirror reflection
    mirror = SimpleImage.blank(width, height * 2)

    for y in range(height):
        for x in range(width):
            pixel = image.get_pixel(x, y)
            mirror.set_pixel(x, y, pixel)
            mirror.set_pixel(x, (height * 2) - (y + 1), pixel)
    return mirror

def add_texts(image, text):
    """
        This function returns a new image which is the same as
        original image except with the text added on the top left of the picture.

        Inputs:
            - image: The original image to process
            - text: The text to display on the image.

        Returns:
            A new image with the text added on the top left of the picture.
    """
    size = int(input("Enter the text size: "))
    title_font = ImageFont.truetype('AmalfiCoast.ttf', size)
    title_text = text

    # Load the original image, and get its size and color mode.
    width, height = image.size
    mode = image.mode

    # Load all pixels from the image.
    orig_pixel_map = image.load()

    # Create a new image matching the original image's color mode, and size.
    #   Load all the pixels from this new image as well.
    text_image = Image.new(mode, (width, height))
    new_pixel_map = text_image.load()

    # Modify each pixel in the new image.
    for x in range(width):
        for y in range(height):
            # Copy the original pixel to the new pixel map.
            new_pixel_map[x, y] = orig_pixel_map[x, y]

    # text_image.show()
    image_editable = ImageDraw.Draw(text_image)
    image_editable.text((10, 10), title_text, (237, 230, 211), font=title_font)

    return text_image

def add_border(original_img, border_size):
    """
    This function returns a new SimpleImage which is the same as
    original image except with a black border added around it. The
    border should be border_size many pixels thick.

    Inputs:
        - original_img: The original image to process
        - border_size: The thickness of the border to add around the image

    Returns:
        A new SimpleImage with the border added around original image
    """
    # calculate width and height of new image from the original image + border size
    new_width = original_img.width + ( 2 * border_size )
    new_height = original_img.height + ( 2 * border_size )

    # create a blank new image, bigger because it includes borders
    bordered_img = SimpleImage.blank(new_width, new_height)

    # loop through each pixel
    for y in range(new_height):
        for x in range(new_width):
            # check to see if each pixel should color black
            if put_border(x, y, bordered_img, border_size):
                # if so, get the pixel from (0,0)
                pixel = bordered_img.get_pixel(x, y)
                pixel.red = 0
                pixel.blue = 0
                pixel.green = 0
            else:
                # if not copy from original image into bordered image
                # need to subtract because x will start only after adding borders
                original_x = x - border_size
                original_y = y - border_size
                original_pixel = original_img.get_pixel(original_x, original_y)
                bordered_img.set_pixel(x, y, original_pixel)
    return bordered_img

def put_border(x, y, bordered_img, border_size):
    # for left border
    if x < border_size:
        return True
    # for right border
    if x >= bordered_img.width - border_size:
        return True
    # for top border
    if y < border_size:
        return True
    # for bottom border
    if y >= bordered_img.height - border_size:
        return True
    return False

def add_filter(image,threshold):
    """
        This function returns a new SimpleImage which is the same as
        original image except with a filter.

        Inputs:
            - image: The original image to process
            - threshold: To create a desirable filter

        Returns:
            A new SimpleImage with filter added
    """
    filtered_image = image.blank(image.width, image.height)

    for y in range(image.height):
        for x in range(image.width):
            original_pixel = image.get_pixel(x, y)
            filtered_image.set_pixel(x, y, original_pixel)

    for pixel in filtered_image:
        pixel_avg = (pixel.red + pixel.blue + pixel.green) // 3
        if pixel_avg > threshold:
            pixel.red = pixel_avg
            pixel.blue = pixel_avg
            pixel.green = pixel_avg

    return filtered_image

def print_explaination():
    print("Hi, there are 6 options to edit the image.")
    print("They are adding borders, filters, text and reflection.")
    print("Besides, you can make the image collage and change the color of it randomly.")
    print("You can also rotate the image to your desired degrees.")
    print("Enter one of these numbers to edit your image!")

def get_user_input():
    """
        This function gets the user's input from 1 to 6. Enter 0 to stop.

        No input

        Returns:
            User's input number
    """
    while True:
        try:
            print("1 for border")
            print("2 for filters")
            print("3 for text")
            print("4 for reflection")
            print("5 for pic collage")
            print("6 for rotation")
            print("0 for stopping the program")
            user_input = input("Enter a number: ")
            user_input = int(user_input)
            break
        except:
            print("That's not a valid option!")


    return user_input

def get_file():
    # Read image file path from user, or use the default file
    filename = input('Enter image file (or press enter for default): ')
    if filename == '':
        filename = DEFAULT_FILE
    return filename

if __name__ == '__main__':
    main()