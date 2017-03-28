#Riley Kunkel
#2143 OOP
#Program 2 - Grid
#due 3-28-17

from graphics import *    # Zelle's simple OO graphics

with open("colors.json") as file: 
   colors = file.read()

colors = json.loads(colors)

for color in colors:
    print(color)

global win  # The window we are drawing the grid in
global cell_width, cell_height  # The size of a cell in the grid

global color_wheel
color_wheel = [  color_rgb(255,0,0), color_rgb(0,255,0), color_rgb(0,0,255),
                        color_rgb(255,255,0), color_rgb(255,0,255), color_rgb(0,255,255),
                        color_rgb(127,255,0), color_rgb(0,127,255), color_rgb(127,0,255),
                        color_rgb(255,127,0), color_rgb(0,255,127), color_rgb(255,0,127),
                        color_rgb(127,127,0), color_rgb(127,0,127), color_rgb(0,127,127),
                        color_rgb(255,255,127), color_rgb(255,127,255), color_rgb(127,255,255) ]
global cur_color
cur_color = 0
global black, white, red, green, blue
black = color_rgb(0,0,0)
white = color_rgb(255,255,255)
red = color_rgb(200,0,0)
green = color_rgb(0,200,0)
blue = color_rgb(0,0,200)
grey = color_rgb(100,100,100)
light_grey = color_rgb(200,200,200)
global nrows
nrows = 1

class ***Grid***(object):

    def __init__(self, rows, cols, width, height) :
        """Create the grid display, initially all white.
        rows, cols are the grid size in rows and columns.
        width, height are the window size in pixels.
        
        Args: 
            rows:  number of rows of cells in the grid (vertical divisions)
            cols:  number of columns of cells in the grid (horizontal divisions)
            width:  horizontal width of window in pixels
            height: vertical height of window in pixels
        Returns:  nothing
        """
        global win, cell_width, cell_height, nrows
        win = GraphWin("Grid", width, height )
        win.setCoords(0, 0, rows, cols)
        bkgrnd = Rectangle( Point(0,0), Point(width,height) )
        bkgrnd.setFill( color_rgb(255,255,255) ) # White background
        cell_width = width / cols
        cell_height = height / rows
        nrows = rows 

    def get_cur_color(self):
        """Return the currently chosen color in the color wheel.  
        
        The color wheel is a list of colors selected to be contrast with each other. 
        The first few entries are bright primary colors; as we cycle through the color
        wheel, contrast becomes less, but colors should remain distinct to those with 
        normal color vision until the color wheel cycles all the way around in 18 
        choices and starts recycling previously used colors.   The color wheel starts
        out in position 0, so get_cur_color() may be called before get_next_color() has 
        been called. 
        
        Args:  none
        Returns:  
            a 'color' that can be passed to fill_cell
            
        FIXME: The color wheel should produce colors of contrasting brightness
        as well as hue, to maximize distinctness for dichromats (people with 
        "color blindness".  Maybe generating a good color wheel can be part of a 
        project later in CIS 210.   (This is not a required or expected change 
        for the week 4 project.) 
        """
        return color_wheel[cur_color]

    def get_next_color(self):
        """Advance the color wheel, returning the next available color. 
        
        The color wheel is a list of colors selected to be contrast with each other. 
        The first few entries are bright primary colors; as we cycle through the color
        wheel, contrast becomes less, but colors should remain distinct to those with 
        normal color vision until the color wheel cycles all the way around in 18 
        choices and starts recycling previously used colors. 
        
        Args:  none
        Returns:  
            a 'color' that can be passed to fill_cell    
        """
        global cur_color
        cur_color += 1
        if cur_color >= len(color_wheel) :
            cur_color = 0
        return color_wheel[cur_color]

    def fill_cell(self, row, col, color):
        """Fill cell[row,col] with color.
        
        Args: 
            row:  which row the selected cell is in.  Row 0 is the top row, 
            row 1 is the next row down, etc.  Row should be between 0 
            and one less than the number of rows in the grid. 
            col:  which column the selected cell is in.  Column 0 is 
            the leftmost row, column 1 is the next row to the right, etc. 
            Col should be between 0 and one less than the number of columns
            in the grid. 
            color: What color to fill fill the selecte cell with.  Valid colors
            include grid.white, grid.black, and values returned by 
            grid.get_next_color() and grid.get_cur_color()
        """
        global nrows, win
        left = col
        right = col + 1
        top = nrows - (row + 1)
        bottom = nrows - row
        mark = Rectangle( Point(left,bottom), Point(right,top) )
        mark.setFill(color)
        mark.draw(win)
        
    def label_cell(self, row, col, text, color=black):
        """Place text label on cell[row,col].
        
        Args: 
            row:  which row the selected cell is in.  Row 0 is the top row, 
            row 1 is the next row down, etc.  Row should be between 0 
            and one less than the number of rows in the grid. 
            col:  which column the selected cell is in.  Column 0 is 
            the leftmost row, column 1 is the next row to the right, etc. 
            Col should be between 0 and one less than the number of columns
            in the grid. 
            text: string (usually one character) to label the cell with
            color: Color of text label
        """
        global nrows, win
        xcenter = col + 0.5
        ycenter = nrows - (row + 1) + 0.5
        label = Text( Point(xcenter, ycenter), text)
        label.setFace("helvetica")
        label.setSize(20)  ## Is there a better way to choose text size? 
        label.setFill(color)
        label.draw(win)

    def sub_grid_dim(self, rows, cols):
        """Divide each cell into rows x cols for sub-labeling
        (like "pencil marks" in Sudoku).
        Args:
        rows:  The number of rows of sub-cell in a cell.
        cols:  The number of columns of sub-cell in a cell.
        Returns: nothing
        Effects: Affects behavior of sub_label_cell
        """
        global n_sub_rows, n_sub_cols
        n_sub_rows = rows
        n_sub_cols = cols

    def sub_label_cell(self, row, col, sub_row, sub_col, text, color=black):
        """Place label in subrow, subcol of row, col.
        Args:
            row:  Row of major grid (counting 0 as top row)
            col:  Column of major grid (counting 0 as leftmost column)
            sub_row:  Row in minor (interior) grid of cell
            sub_col:  Column in minor (interior) grid of cell
            text: Label (usually one character) to place there
            color: color of text
        """
        global nrows, n_sub_rows, n_sub_cols, win
        xcenter = col + ((sub_col + 0.5) / n_sub_cols)
        ycenter = nrows - (row + 1) + ((sub_row + 0.5) / n_sub_rows)
        # print("Placing subgrid label at ({},{})".format(xcenter,ycenter))
        label = Text( Point(xcenter, ycenter), text)
        label.setFace("helvetica")
        label.setSize(10)  ## Is there a better way to choose text size? 
        label.setFill(color)
        label.draw(win)
        

    def close(self):
        """ Close the graphics window (shut down graphics). 
        
        Args: none
        Returns: nothing
        Effect:  the grid graphics window is closed. 
        """
        global win
        win.close()
        
    if __name__ == "__main__":
        print("How many colors? (Must be perfect square.)")
        num = input
        if (sqrt(num) % 1 != 0)
            print("Not a perfect square. Reverts to 9.")
            num = 9

        num2 = sqrt(num)
        make(num2,num2,500,500)
        sub_grid_dim(num2,num2)
        for row in range(num2):
            for col in range(num2):
                fill_cell(row, col, get_next_color())


        input("Press enter to exit")
        close()