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

    $targets = findWhereToPlant($height, $width, $me, $grid);   // find all the places where I can plant a bomb
    $target = findBestTarget($targets, $me);                    // find the best target for me

    // if the target is where I am and i can plant a bomb, plant
    // else, go to the target
    if ($targets[$target]['x'] == $me['x'] && $targets[$target]['y'] == $me['y']) {
        echo("BOMB ".$me['x']." ".$me['y']."\n");
    } else {
        echo("MOVE ".$targets[$target]['x']." ".$targets[$target]['y']."\n");
    }

}

/**
 * Find the best place for me to plant a bomb.
 * If I can plant, then find a good place close to me
 * Else, go to the closest place where the score I get get with my bomb is max
 */
function findBestTarget($targets, $me)
{
    $closest = 0;
    $closestDx = ($me['x'] > $targets[0]['x']) ? $me['x'] - $targets[0]['x'] : $targets[0]['x'] - $me['x'];
    $closestDy = ($me['y'] > $targets[0]['y']) ? $me['y'] - $targets[0]['y'] : $targets[0]['y'] - $me['y'];
    // find the closest target from me
    for ($i = 1; $i < sizeof($targets); $i++) {
        // calculate the distance between me and this target
        $dx = ($me['x'] > $targets[$i]['x']) ? $me['x'] - $targets[$i]['x'] : $targets[$i]['x'] - $me['x'];
        $dy = ($me['y'] > $targets[$i]['y']) ? $me['y'] - $targets[$i]['y'] : $targets[$i]['y'] - $me['y'];
        // check if this distance is closer than the current closest (to replace the old by the new if it is)
        if (($closestDx + $closestDy) > ($dx + $dy)) {
            $closest = $i;
            $closestDx = $dx;
            $closestDy = $dy;
        }
        // if distance is 0 (because im on this target), break : we found it
        if (!$dx && !$dy) {
            break;
        }
    }
    // if the closest target his top ranked, then this is where I have to plant my bomb
    // else, look at top ranked target to find the closest
    if ($targets[$closest]['boxes'] == $targets[0]['boxes']) {
        return $closest;
    } else {
        // return the same (testing if it works for the moment)
        return $closest;
    }
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
                $countBoxes = 0;
                // look at the top
                for ($ty = $y-1; ($ty >= ($y-$me['param1']) && $ty >= 0); $ty--) {
                    if ($grid[$ty][$x] == '0') {
                        $countBoxes++;
                        break;
                    }
                }
                // look at the bottom
                for ($ty = $y+1; ($ty <= ($y+$me['param1']) && $ty < $height); $ty++) {
                    if ($grid[$ty][$x] == '0') {
                        $countBoxes++;
                        break;
                    }
                }
                // look at the left
                for ($tx = $x-1; ($tx >= ($x-$me['param1']) && $tx >= 0); $tx--) {
                    if ($grid[$y][$tx] == '0') {
                        $countBoxes++;
                        break;
                    }
                }
                // look at the right
                for ($tx = $x+1; ($tx <= ($x+$me['param1']) && $tx < $width); $tx++) {
                    if ($grid[$y][$tx] == '0') {
                        $countBoxes++;
                        break;
                    }
                }
                // if there are boxes, write it in the $targets array
                if ($countBoxes) {
                    error_log(var_export("ok", true));
                    array_push($targets, array(
                        'x' => $x,
                        'y' => $y,
                        'boxes' => $countBoxes
                    ));
                }
            }
        }
    }
    // sort the targets to have a priority order of attack
    return sortTargets($targets);
}

function sortTargets($targets)
{
    for ($i = 1; $i < sizeof($targets); $i++) {
        for ($j = 1; $j < (sizeof($targets) - $i); $j++) {
            if ($targets[$i-1]['boxes'] > $targets[$i]['boxes']) {
                $temp = $targets[$i-1]['boxes'];
                $targets[$i-1]['boxes'] = $targets[$i]['boxes'];
                $targets[$i]['boxes'] = $temp;
            }
        }
    }

    return $targets;
}

?>
