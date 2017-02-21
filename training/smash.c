// Write an action using printf(). DON'T FORGET THE TRAILING \n
// To debug: fprintf(stderr, "Debug messages...\n");

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// DEFINE

#define HEIGHT  12  // map height
#define WIDTH   6   // map width
#define NEXTB   8   // number of next blocks

// GLOBAL VAR

int     my_score;                       // my score
int     opponent_score;                 // opponent score

char    row[7];                         // used to read a grid row  
int     next_blocks[NEXTB][2];          // 8 next blocks    

char    my_grid[HEIGHT][WIDTH];         // my grid
char    opponent_grid[HEIGHT][WIDTH];   // opponent grid
char    top_colors[WIDTH];              // contains the colors at the top of each grid column

int		response[2];					// [0] => column; [1] => rotation;

// MAIN

int main()
{
    // GAME LOOP
    
    while (1) {
        
        for (int i = 0; i < NEXTB; i++) {   					   	// 8 next blocks group 
            scanf("%d%d", &next_blocks[i][0], &next_blocks[i][1]); 	// main color, second color
        }
        
        scanf("%d", &my_score);             // read my current score
        
        for (int i = 0; i < HEIGHT; i++) {  // my grid
            scanf("%s", row);
            fill_grid(my_grid, row, i);     // put the row on my_grid
        }

        scanf("%d", &opponent_score);       // read the current score of the opponent 
        
        for (int i = 0; i < HEIGHT; i++) {  // opponent grid
            scanf("%s", row);
            fill_grid(opponent_grid, row, i);     // put the row on my_grid
        }
        
        display_grid(my_grid);
        
        find_top_colors();
        display_top_colors();
        
		drop_position();								// update the response array
        printf("%d %d\n", response[0], response[1]);	// the column in which to drop the blocks
    }

    return 0;
}

// FUNCTIONS

/**
 * Calculate the best position to drop the blocks
 */ 
void drop_position()
{
	// next_blocks[0][0] & next_blocks[0][1]
	int sbs_color_empty[2] = {-1, -1};					// side by side : color and empty ( [0] => column; [1] => rotation; )
	int sbs_empty[2] = {-1, -1};						// two empty location side by side
    int color1_pos = -1;								// position of a location which correspond to the 1 color
	int color2_pos = -1;								// position of a location which correspond to the 2 color
    int pos_empty = -1;									// position of an empty location
    int i = 0;
    int found = 0;
	
    while(i < WIDTH && !found)
    {
	
		if(i > 0) 
		{
			// color [0] at i-1 and color[1] at i 
			if(top_colors[i-1] == next_blocks[0][0] && top_colors[i] == next_blocks[0][1])
			{
				 response[0] = i-1;
				 response[1] = 0;
				 found = 1;
			}
			// color [1] at i-1 and color[0] at i
			else if(top_colors[i-1] == next_blocks[0][1] && top_colors[i] == next_blocks[0][0])
			{
				 response[0] = i;
				 response[1] = 2;
				 found = 1;
			} 
			// color [0] at i-1, empty at i
			else if((top_colors[i-1] == next_blocks[0][0] && top_colors[i] == '.') || (top_colors[i-1] == next_blocks[0][0] && top_colors[i] == '0'))
			{
				sbs_color_empty[0] = i-1;
				sbs_color_empty[1] = 0;
			}
			// color [1] at i-1, empty at i
			else if((top_colors[i-1] == next_blocks[0][1] && top_colors[i] == '.') || (top_colors[i-1] == next_blocks[0][1] && top_colors[i] == '0'))
			{
				sbs_color_empty[0] = i-1;
				sbs_color_empty[1] = 0;
			}
			// empty at i-1 and color[0] at i
			else if((top_colors[i] == next_blocks[0][0] && top_colors[i-1] == '.') || (top_colors[i] == next_blocks[0][0] && top_colors[i-1] == '0'))
			{
				sbs_color_empty[0] = i;
				sbs_color_empty[1] = 2;
			}
			// empty at i-1 and color[1] at i 
			else if((top_colors[i] == next_blocks[0][1] && top_colors[i-1] == '.') || (top_colors[i] == next_blocks[0][1] && top_colors[i-1] == '0'))
			{
				sbs_color_empty[0] = i;
				sbs_color_empty[1] = 2;
			}
			// empty at i and empty at i-1
			else if(top_colors[i] == '.' || top_colors[i] == '0')
			{
				if(top_colors[i-1] == '.' || top_colors[i-1] == '0')
				{
					sbs_empty[0] = i;
					sbs_empty[1] = 2;
				}
			}
		}
		
		if(!found) 
		{
			if(top_colors[i] == '.' || top_colors[i] == '0')
			{
				pos_empty = i;
			}
			else if(top_colors[i] == next_blocks[0][0])
			{
				color1_pos = i;
			}
			else if(top_colors[i] == next_blocks[0][1])
			{
				color2_pos = i;
			}
		
			i++;
		}
    }
    
    // if no perfect response
	if(!found)
	{
		// check if there is a empty location next to a color of next_blocks[0]
		if(sbs_color_empty[0] > -1 && sbs_color_empty[1] > -1)
		{
			response[0] = sbs_color_empty[0];
			response[1] = sbs_color_empty[1];
		} 
		// check if there is two empty location side by side
		else if(sbs_empty[0] > -1 && sbs_empty[1] > -1)
		{
			response[0] = sbs_empty[0];
			response[1] = sbs_empty[1];
		}
		else if(pos_empty > -1)
		{
			response[0] = pos_empty;
			response[1] = 1;			// next step => look to the next_blocks color ( to write 1 or 3 by looking to the next colors )
		}
		else if(color1_pos > -1)
		{
			response[0] = color1_pos;
			response[1] = 1;
		}
		else if(color2_pos > -1)
		{
			response[0] = color2_pos;
			response[1] = 3;
		}
		else
		{
			response[0] = 0;
			response[1] = 1;
		}
	}
}

/**
 * Find the color at the top of each grid column
 */
void find_top_colors()
{
    for(int j = 0; j < WIDTH; j++)
    {
        int end = 0;
        int i = 0;
        
        while(!end && i < HEIGHT)
        {
            if(my_grid[i][j] == '.')
            {
                end = 1;
            }
            else 
            {
                top_colors[j] = my_grid[i][j];
            }
            i++;
        }
        
        if(i == 1 && end == 1)
        {
            top_colors[j] = '.';
        }
    }
}

/**
 * Display the top color array
 */
void display_top_colors()
{
    for(int i = 0; i < WIDTH; i++)
    {
        fprintf(stderr, "%c", top_colors[i]);
    }
    
    fprintf(stderr, "\n\n");
}

/**
 * Display a grid on the debug console
 */ 
void display_grid(char grid[HEIGHT][WIDTH])
{
    for(int i = HEIGHT-1; i > -1; i--)
    {
        for(int j = 0; j < WIDTH; j++)
        {
            fprintf(stderr, "%c", grid[i][j]);
        }
        
        fprintf(stderr, "\n");
    }
    
    fprintf(stderr, "\n\n");
}

/**
 * Fill a row of a grid
 */
void fill_grid(char grid[HEIGHT][WIDTH], char row[7], int row_number)
{
    for(int i = 0; i < WIDTH; i++)
    {
        grid[(HEIGHT-1)-row_number][i] = row[i];
    }
}
