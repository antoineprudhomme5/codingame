// Write an action using printf(). DON'T FORGET THE TRAILING \n
// To debug: fprintf(stderr, "Debug messages...\n");

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// VARIABLES

int     L;          // nombre de ligne
int     C;          // nombre de colonne
char    row[102];   // utilise pour lire une ligne de la grille

int     X;          // coordonnees de BENDER sur L
int     Y;          // coordonnees de BENDER sur C
int     last_x = -1;// remember the last x coordinate of bender
int     last_y = -1;// remember the last y coordinate of bender
int     tp1[2];     // coordonnees du TP1
int     tp2[2];     // coordonnees du TP2

char    directions[4];      // direction que prend Bender
int     bool_suicide = 0;   // il n'a pas encore trouve le $
int     bool_beer = 0;      // if true, bender can broke 'X'

char    reponse = 'S';      // default priority

// MAIN

int main()
{
    scanf("%d%d", &L, &C); fgetc(stdin);    // map size
    char map[L][C];                         // carte sur laquelle Bender se deplace

    for (int i = 0; i < L; i++) {
        fgets(row, 102, stdin);
        fill_map(map[i], row);              // put the line one the map array
    }

    display_map(map);                       // display the map on the console
    init_coordonnees(map);                  // init bender position

    while(!bool_suicide)
    {
        //affiche_coordonnees_blender();
        prochaine_direction(map);
        if(!bool_suicide) // sinon il fait un deplacement en trop
        {
            switch(reponse)
            {
                case 'N' :
                    printf("NORTH\n");
                    break;
                case 'E' :
                    printf("EAST\n");
                    break;
                case 'S' :
                    printf("SOUTH\n");
                    break;
                case 'O' :
                    printf("WEST\n");
            }
        }
    }

    return 0;
}

// FUNCTIONS

/**
 * calcule le deplacement de bender en fonction de sa position actuelle
 */
void prochaine_direction(char map[L][C])
{
    switch(map[X][Y]) {
        case '$' : // end
            bool_suicide = 1;
            break;
        case 'B' : // beer
            bool_beer = !bool_beer;
            normal_move(map);
            break;
        default : // if empty
            normal_move(map);
            break;
    }
}

/**
 * Move bender
 */
void normal_move(char map[L][C])
{
    priorities();

    int i = 0, trouve = 0;

    while(i < 4 && !trouve) // 4 directions to test
    {
        int temp_x = X;
        int temp_y = Y;

        switch(directions[i])
        {
            case 'N' :
                temp_x--;
                break;
            case 'E' :
                temp_y++;
                break;
            case 'S' :
                temp_x++;
                break;
            case 'O' :
                temp_y--;
                break;
        }

        // test if the temp coordinates are ok
        if(map[temp_x][temp_y] != '#' && check_last_position(temp_x, temp_y))
        {
            if(map[temp_x][temp_y] != 'X')
            {
                trouve = 1;
                mise_a_jour_blender(map, directions[i]);
            }
            else
            {
                if(bool_beer)
                {
                    trouve = 1;
                    mise_a_jour_blender(map, directions[i]);
                }
            }
        }

        i++;
    }
}

/**
 * check if next direction is not the same as before (=> loop)
 */
int check_last_position(int tx, int ty)
{
    if(last_x == tx && last_y == ty)
    {
        return 0;
    }

    return 1;
}

/**
 * calculate the move priorities
 */
void priorities()
{
    strcpy(directions, "SENO");
}

/**
 * Update bender coordinates and the response
 */
void mise_a_jour_blender(char map[L][C], char direction)
{
    last_x = X;
    last_y = Y;
    reponse = direction;
    switch(direction)
    {
        case 'N' :
            X--;
            break;
        case 'E' :
            Y++;
            break;
        case 'S' :
            X++;
            break;
        case 'O' :
            Y--;
            break;
    }
}

/**
 * Init bender coordinates
 */
void init_coordonnees(char map[L][C])
{
    int bool_tp1 = 0;

    for(int i = 0; i < L; i++)
    {
        for(int j = 0; j < C; j++)
        {
            if(map[i][j] == '@') // bender coordinates
            {
                X = i;
                Y = j;
                map[i][j] = ' ';
            }
            else if(map[i][j] == 'T') // TP found
            {
                if(bool_tp1)
                {
                    tp2[0] = i;
                    tp2[1] = j;
                }
                else
                {
                    bool_tp1 = 1;
                    tp1[0] = i;
                    tp1[1] = j;
                }
            }
        }
    }

    if(bool_tp1)
    {
        fprintf(stderr, "TP1 :: X = %d // Y = %d\n", tp1[0], tp1[1]);
        fprintf(stderr, "TP2 :: X = %d // Y = %d\n", tp2[0], tp2[1]);
    }
}

/**
 * display the coordinates of bender
 */
void affiche_coordonnees_blender()
{
    fprintf(stderr, "X = %d // Y = %d\n", X, Y);
}

/**
 * Display the map on the debug console
 */
void display_map(char map[L][C])
{
    for(int i = 0; i < L; i++)
    {
        for(int j = 0; j < C; j++)
        {
            fprintf(stderr, "%c", map[i][j]);
        }

        fprintf(stderr, "\n");
    }

    fprintf(stderr, "\n");
}

/**
 * Fill a row of a map
 */
void fill_map(char map[C], char row[])
{
    for(int i = 0; i < C; i++)
    {
        map[i] = row[i];
    }
}
