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
    $me = null;
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

        // build an entity key => value array
        $entity = array(
            'entityType' => $entityType,    // 0 for bomb, 1 for player
            'owner' => $owner,              // for a player : the id of the player / for a bomb : the id of the player who planted this bomb
            'x' => $x,
            'y' => $y,
            'param1' => $param1,            // for a player : the number of bomb he can still plant / for a bomb : the number of turns before it explode
            'param2' => $param2             // for a player : range of his bombs / for a bomb : range of the bomb
        );

        // save this entity
        if ($entity['entityType'] == 1) {
            array_push($bombs, $entity);
            $grid[$entity['y']][$entity['x']] == 'b';   // draw the bomb on the grid
        } else {
            if ($entity['owner'] == $myId) {
                $me = $entity;
            } else {
                array_push($players, $entity);
            }
        }
    }

    // update the grid => remove all the boxes that are in the range of a bomb
    $grid = cleanWillExplode($grid, $bombs, $height, $width);
    $targets = findWhereToPlant($height, $width, $me, $grid);   // find all the places where I can plant a bomb (sorted by score)
    $targets = calculateDistances($targets, $me['x'], $me['y']);
    $closests = sortByDistance($targets);                       // targets sorted by distance from me
    $target = findBestTarget($targets, $closests,  $me);        // find the best target for me

    // if the target is where I am and i can plant a bomb, plant
    // else, go to the target
    if ($target['x'] == $me['x'] && $target['y'] == $me['y'] && $me['param1']) {
        echo("BOMB ".$me['x']." ".$me['y']."\n");
    } else {
        echo("MOVE ".$target['x']." ".$target['y']."\n");
    }

}

function calculateDistances($targets, $mx, $my)
{
    for ($i = 0; $i < sizeof($targets); $i++) {
        $dx = ($mx > $targets[$i]['x']) ? $mx - $targets[$i]['x'] : $targets[$i]['x'] - $mx;
        $dy = ($my > $targets[$i]['y']) ? $my - $targets[$i]['y'] : $targets[$i]['y'] - $my;
        $targets[$i]['distance'] = $dx + $dy;
    }
    return $targets;
}


/**
 * Return the targets sorted by distance
 * @param $targets : the targets
 * @return $targets
 */
function sortByDistance($targets)
{
    for ($i = 1; $i < sizeof($targets); $i++) {
        for ($j = 1; $j < (sizeof($targets) - $i); $j++) {
            if ($targets[$j-1]['distance'] > $targets[$j]['distance']) {
                $temp = $targets[$j-1];
                $targets[$j-1] = $targets[$j];
                $targets[$j] = $temp;
            }
        }
    }

    return $targets;
}

/**
 * Remove the $bombs in $grid
 * @param $grid : the game grid
 * @param $bombs : the bombs planted on the grid
 * @param $height : the grid height
 * @param $width : the grid width
 * @return $grid : the grid updated
 */
function cleanWillExplode($grid, $bombs, $height, $width)
{
    for ($i = 0; $i < sizeof($bombs); $i++) {
        // foreach bomb, get his targets
        $bombTargets = targetedBoxes($bombs[$i]['x'], $bombs[$i]['y'], $bombs[$i]['param2'], $grid, $height, $width);
        // then , remove this targets to the grid
        for ($j = 0; $j < sizeof($bombTargets); $j++) {
            $grid[$bombTargets[$j]['y']][$bombTargets[$j]['x']] = '.';
        }
    }
    return $grid;
}

/**
 * Find the best place for me to plant a bomb.
 * If I can plant, then find a good place close to me
 * Else, go to the closest place where the score I get get with my bomb is max
 */
function findBestTarget($targets, $closests, $me)
{
    // if the closest target his top ranked, then this is where I have to plant my bomb
    // else, look at top ranked target to find the closest
    if ($closests[0]['nbBoxes'] == $targets[0]['nbBoxes']) {
        return $closests[0];
    } else {
        // if we can plant, plant
        // else, look the best target before we can plant the next bomb
        if ($me['param1']) {
            return $closests[0];
        } else {
            $i = 0;
            $max = 0;
            while ($closests[$i]['distance'] <= $me['param1'] && $closests[$max]['nbBoxes'] < $targets[0]['nbBoxes'] && $i < sizeof($closests)) {
                if ($closests[$i]['nbBoxes'] > $closests[$max]['nbBoxes']) {
                    $max = $i;
                }
                $i++;
            }
            return $closests[$max];
        }
    }
}

/**
 * Return the boxes which will explode by the bomb
 * @param $x : bomb x coordinate
 * @param $y : bomb y coodinate
 * @param $range : the bomb range
 * @param $grid : the game grid
 * @param $height : the grid height (y axis)
 * @param $width : the grid width (x axis)
 * @return Array
 */
function targetedBoxes($x, $y, $range, $grid, $height, $width)
{
    $boxes = [];

    // look at the top
    for ($ty = $y; ($ty >= ($y-$range) && $ty >= 0); $ty--) {
        // error_log(var_export($grid[$ty][$x], true));
        if ($grid[$ty][$x] == '0') {
            array_push($boxes, array(
                'x' => $x,
                'y' => $ty
            ));
            break;
        }
    }
    // look at the bottom
    for ($ty = $y; ($ty <= ($y+$range) && $ty < $height); $ty++) {
        // error_log(var_export($grid[$ty][$x], true));
        if ($grid[$ty][$x] == '0') {
            array_push($boxes, array(
                'x' => $x,
                'y' => $ty
            ));
            break;
        }
    }
    // look at the left
    for ($tx = $x; ($tx >= ($x-$range) && $tx >= 0); $tx--) {
        // error_log(var_export($grid[$y][$tx], true));
        if ($grid[$y][$tx] == '0') {
            array_push($boxes, array(
                'x' => $tx,
                'y' => $y
            ));
            break;
        }
    }
    // look at the right
    for ($tx = $x; ($tx <= ($x+$range) && $tx < $width); $tx++) {
        // error_log(var_export($grid[$y][$tx], true));
        if ($grid[$y][$tx] == '0') {
            array_push($boxes, array(
                'x' => $tx,
                'y' => $y
            ));
            break;
        }
    }

    return $boxes;
}

/**
 * For each square in the grid, put in an array the squares where if i plant a bomb here, i can brake a box.
 * Then sort this array by number of boxes i can brake.
 * @return Array
 */
function findWhereToPlant($height, $width, $me, $grid)
{
    $targets = [];
    for ($y = 0; $y < $height; $y++) {
        for ($x = 0; $x < $width; $x++) {
            // I can't go where the is a box, so test if this is floor
            if ($grid[$y][$x] == '.') {
                // the boxes which will explode if the bomb is planted here
                $boxes = targetedBoxes($x, $y, $me['param2']-1, $grid, $height, $width);
                // if there are boxes, write it in the $targets array
                if (sizeof($boxes)) {
                    array_push($targets, array(
                        'x' => $x,
                        'y' => $y,
                        'boxes' => $boxes,
                        'nbBoxes' => sizeof($boxes)
                    ));
                }
            }
        }
    }
    // sort the targets to have a priority order of attack
    return sortTargets($targets);
}

/**
 * Sort the targets by score
 * @param $targets
 * @return $targets
 */
function sortTargets($targets)
{
    for ($i = 1; $i < sizeof($targets); $i++) {
        for ($j = 1; $j < (sizeof($targets) - $i); $j++) {
            if ($targets[$j-1]['nbBoxes'] > $targets[$j]['nbBoxes']) {
                $temp = $targets[$j-1]['nbBoxes'];
                $targets[$j-1]['nbBoxes'] = $targets[$j]['nbBoxes'];
                $targets[$j]['nbBoxes'] = $temp;
            }
        }
    }

    return $targets;
}

?>
