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

// MAIN

int main()
{
    // GAME LOOP
    
    while (1) {
        
        for (int i = 0; i < NEXTB; i++) {   // 8 next blocks group 
            scanf("%d%d", &next_blocks[i][0], &next_blocks[i][1]); // main color, second color
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
        
        printf("%d\n", drop_position());                      // the column in which to drop the blocks
    }

    return 0;
}

// FUNCTIONS

/**
 * Calculate the best position to drop the blocks
 */ 
int drop_position()
{
    char color[1];
    sprintf(color, "%d", next_blocks[0][0]);
    int find = 0;
    int position = 0;
    int pos_empty = 0;
    int i = 0;
    
    while(i < WIDTH && !find)
    {
        if(top_colors[i] == '.' || top_colors[i] == '0')
        {
            pos_empty = i;
        }
        else if(top_colors[i] == color[0])
        {
            find = 1;
            position = i;
        }
        i++;
    }
    
    if(find == 1)
    {
        return position;   
    }
    else
    {
        return pos_empty;
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
