<?php
// To debug (equivalent to var_dump): error_log(var_export($var, true));

// Initial inputs
fscanf(STDIN, "%d %d %d",
    $width,
    $height,
    $myId
);

// Game loop
while (true)
{
    // turn variables
    $grid = [];
    $players = [];
    $bombs = [];

    // read the grid for this turn
    for ($i = 0; $i < $height; $i++)
    {
        array_push($grid, stream_get_line(STDIN, $width + 1, "\n"));
    }

    // read entities for this turn
    fscanf(STDIN, "%d",
        $entities
    );
    for ($i = 0; $i < $entities; $i++)
    {
        fscanf(STDIN, "%d %d %d %d %d %d",
            $entityType,
            $owner,
            $x,
            $y,
            $param1,
            $param2
        );

        $entity = array(
            'entityType' => $entityType,    // 0 for bomb, 1 for player
            'owner' => $owner,              // for a player : the id of the player / for a bomb : the id of the player who planted this bomb
            'x' => $x,
            'y' => $y,
            'param1' => $param1,            // for a player : the number of bomb he can still plant / for a bomb : the number of turns before it explode
            'param2' => $param2             // for a player : range of his bombs / for a bomb : range of the bomb
        );
    }

    echo("BOMB 6 5\n");
}
?>
