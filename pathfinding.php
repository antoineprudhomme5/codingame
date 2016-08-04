<?php
	
// Write an action using echo(). DON'T FORGET THE TRAILING \n
// To debug (equivalent to var_dump): error_log(var_export($var, true));

// DEFINES

define("WIDTH", 16);
define("HEIGHT", 9);

// CLASSES

/**
 * Represent a Node in the grid
 */
class Node {

	var $x;			// x coordinate
	var $y;			// y coordinate
	var $type;		// string => wall, empty, end, start
	var $visited;	// boolean 
	var $path;		// array => path from start to this Node

	public function __construct($x, $y, $type) {

		$this->x = $x;
		$this->y = $y;
		$this->type = $type;
		$this->visited = false;
		$this->path = [];

	}

	public function __toString() {

		if($this->visited) {
			return "[V]";
		} else {
			switch($this->type) {
			case "wall":
				return "[X]";
				break;
			case "empty":
				return "[O]";
				break;
			case "start":
				return "[S]";
				break;
			case "end":
				return "[E]";
				break;
			}	
		}
	}

} 

/**
 * The challenge grid
 */
class Grid {

	var $grid; 		// 2D array of Node

	public function __construct() {

		$this->grid = [];
		for($i = 0; $i < HEIGHT; $i++) {

			$this->grid[$i] = [];
			for($j = 0; $j < WIDTH; $j++) {

				$this->grid[$i][$j] = new Node($j, $i, "empty");
			}
		}
	}

	public function __toString() {

		$str = "";

		for($i = 0; $i < HEIGHT; $i++) {

			for($j = 0; $j < WIDTH; $j++) {

				$str .= $this->grid[$i][$j];
			}
			$str .= '<br>';
		}

		return $str;
	}

}

// FUNCTIONS

function isNeighborValid($node) {
	if(($node->type != "wall") && (!$node->visited)) {
		$node->visited = true;
		return true;
	}
	return false;
}

function displayPath($path) {
	$str = "";
	for($i = 0; $i < sizeof($path) - 1; $i++) {
		$str.=$path[$i]." ";
	}
	$str.=$path[sizeof($path) - 1]."\n";
	echo $str;
}

function updatePath($node, $oldPath, $direction) {
	$node->path = $oldPath;
	array_push($node->path, $direction);
}

// MAIN CODE

// init grid
fscanf(STDIN, "%d %d %d %d",
    $startX, 	// x coordinate of your start position
    $startY, 	// y coordinate of your start position
    $exitX, 	// x coordinate of the exit
    $exitY 		// y coordinate of the exit
);
fscanf(STDIN, "%d",
    $nbWalls 	// number of walls
);

$grid = new Grid();
$grid->grid[$startY][$startX]->type = "start"; 
$grid->grid[$exitY][$exitX]->type = "end"; 

for ($i = 0; $i < $nbWalls; $i++)
{
    fscanf(STDIN, "%d %d",
        $posX, 	// x coordinate of a wall
        $posY 	// y coordinate of a wall
    );
    $grid->grid[$posY][$posX]->type = "wall"; 
}

// search path

$found = false; 								// found the end node
$stack = [[$grid->grid[$startY][$startX]]];		// stack the neighbors

while(!$found) {
	$topStack = $stack[sizeof($stack)-1];		// get the nodes at the top of the stack
	array_push($stack, []);
	// for each node of topStack
	for($i = 0; $i < sizeof($topStack); $i++) {
		$x = $topStack[$i]->x;					// x coordinate of the node
		$y = $topStack[$i]->y;					// y coordinate of the node
		// UP 
		if($y > 0) {
			if(isNeighborValid($grid->grid[$y-1][$x])) {
				updatePath($grid->grid[$y-1][$x], $topStack[$i]->path, "UP");
				if($grid->grid[$y-1][$x]->type == "end") {
					$found = true;
					displayPath($grid->grid[$y-1][$x]->path);
				} else {
					array_push($stack[sizeof($stack)-1], $grid->grid[$y-1][$x]);
				}
			}
		}
		// DOWN
		if($y < 8) {
			 if(isNeighborValid($grid->grid[$y+1][$x]) && !$found) {
	        	updatePath($grid->grid[$y+1][$x], $topStack[$i]->path, "DOWN");
	            if($grid->grid[$y+1][$x]->type == "end") {
					$found = true;
					displayPath($grid->grid[$y+1][$x]->path);
				} else {
					array_push($stack[sizeof($stack)-1], $grid->grid[$y+1][$x]);
				}
	        }
		}
        // RIGHT
        if($x < 15) {
        	if(isNeighborValid($grid->grid[$y][$x+1]) && !$found) {
	        	updatePath($grid->grid[$y][$x+1], $topStack[$i]->path, "RIGHT");
	            if($grid->grid[$y][$x+1]->type == "end") {
					$found = true;
					displayPath($grid->grid[$y][$x+1]->path);
				} else {
					array_push($stack[sizeof($stack)-1], $grid->grid[$y][$x+1]);
				}
	        }
        }
        // LEFT
        if($x > 0) {
        	if(isNeighborValid($grid->grid[$y][$x-1]) && !$found) {
	        	updatePath($grid->grid[$y][$x-1], $topStack[$i]->path, "LEFT");
	            if($grid->grid[$y][$x-1]->type == "end") {
					$found = true;
					displayPath($grid->grid[$y][$x-1]->path);
				} else {
					array_push($stack[sizeof($stack)-1], $grid->grid[$y][$x-1]);
				}
	        }
        }
	}
}

?>