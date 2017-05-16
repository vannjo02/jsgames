var board = [];
var gap_position = -1;
var scrambling = false;
var num_moves = 0;
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var doc_moves = document.querySelector('#num_moves');

var Tile = function (number) {
	this.number = number;
}

create_game = function() {
	board = [];
	gap_position = 15;
	for (i=0; i<16; i++) {
		var t = new Tile(i);
		board.push(t);
	}
	for (i=0; i<board.length; i++) {
		drawTile(i);
	}
	scramble();
	num_moves = 0;
	doc_moves.value = num_moves;
}

move_tile = function(tile_position) {
	if (is_adjacent_to_gap(tile_position)) {
		var temp = board[tile_position];
		board[tile_position] = board[gap_position];
		board[gap_position] = temp;
		drawTile(gap_position);
		gap_position = tile_position;
		drawTile(tile_position);
		
		num_moves += 1;

		doc_moves.value = num_moves;
			
		if (gap_position == 15 && tile_position == board[tile_position].number && scrambling != true) {
			end_game_check();
		}
	}
	
	else if (double_move_allowed(tile_position)) {
		if (is_adjacent_to_gap(tile_position + 1)) {
			move_tile(tile_position + 1);
			move_tile(tile_position);
		}
		
		else if (is_adjacent_to_gap(tile_position - 1)) {
			move_tile(tile_position - 1);
			move_tile(tile_position);
		}
		
		else if (is_adjacent_to_gap(tile_position + 4)) {
			move_tile(tile_position + 4);
			move_tile(tile_position);
		}
		
		else if (is_adjacent_to_gap(tile_position - 4)) {
			move_tile(tile_position - 4);
			move_tile(tile_position);
		}
	}

	/*else if (triple_move_allowed(tile_position)) {
		if (is_adjacent_to_gap(tile_position + 3)) {
			move_tile(tile_position + 2);
			move_tile(tile_position + 1);
			move_tile(tile_position);
		}
		
		else if (is_adjacent_to_gap(tile_position - 3)) {
			move_tile(tile_position - 2);
			move_tile(tile_position - 1);
			move_tile(tile_position);
		}
		
		else if (is_adjacent_to_gap(tile_position + 12)) {
			move_tile(tile_position + 8);
			move_tile(tile_position + 4);
			move_tile(tile_position);
		}
		
		else if (is_adjacent_to_gap(tile_position - 12)) {
			move_tile(tile_position - 8);
			move_tile(tile_position - 4);
			move_tile(tile_position);
		}
	}*/
}

click_listen = function() {
	if (gap_position >= 0) {
		var mouseX = event.clientX - canvas.offsetLeft;
		var mouseY = event.clientY - canvas.offsetTop;
		//alert ("Coordinates: " + mouseX + " " + mouseY);
			
		var click_pos = get_position(mouseX, mouseY);
		//alert ("Position: " + click_pos);
		move_tile(click_pos);
	}
}

get_position = function(x, y) {
	
	var col;
	var row;
	
	if (y < 126)
		row = 0;
	else if (y < 251)
		row = 4;
	else if (y < 376)
		row = 8;
	else 
		row = 12;

	if (x < 126)
		col = 1;
	else if (x < 251)
		col = 2;
	else if (x < 376)
		col = 3;
	else
		col = 4;

	return row + col - 1;				
}

drawTile = function(pos) {

//alert ("Render into position " + pos + " tile number: " + board[pos].number + "gap pos: " + gap_position);

	var x;
	var y;
		
	if (pos < 4)
		y = 1;
	else if (pos < 8)
		y = 126;
	else if (pos < 12)
		y = 251;
	else
		y = 376;
		
	if (pos === 0 || pos == 4 || pos == 8 || pos == 12)
		x = 1;
	else if (pos == 1 || pos == 5 || pos == 9 || pos == 13)
		x = 126;
	else if (pos == 2 || pos == 6 || pos == 10 || pos == 14)
		x = 251;
	else
		x = 376;
			
	ctx.beginPath();

	if (board[pos].number == 15){
		ctx.fillStyle="silver";
		ctx.rect(x, y, 125, 125);
		ctx.fill();

	}
	else if (board[pos].number % 2 == 0){
		ctx.lineWidth="1";
		ctx.strokeStyle="black";
		ctx.fillStyle="red";
		ctx.rect(x,y,124,124); 

		ctx.stroke();
		ctx.fill();
		ctx.font="36px times";
		ctx.fillStyle="black";
		ctx.fillText(board[pos].number + 1, x+45, y+70);
	}
	
	else {
		ctx.lineWidth="1";
		ctx.strokeStyle="black";
		ctx.fillStyle="#F5E08E";
		ctx.rect(x,y,124,124); 

		ctx.stroke();
		ctx.fill();
		ctx.font="36px times";
		ctx.fillStyle="black";
		ctx.fillText(board[pos].number + 1, x+45, y+70);
	}
}

is_adjacent_to_gap = function(tile_position) {
	var move = false;
	switch(tile_position) {
		case 0:
			if (gap_position == 1 || gap_position == 4) {
				move = true;
			}
			break;
		case 1:
			if (gap_position == 0 || gap_position == 2 || gap_position == 5) {
				move = true;
			}
			break;
		case 2:
			if (gap_position == 1 || gap_position == 3 || gap_position == 6) {
				move = true;
			}
			break;
		case 3:
			if (gap_position == 2 || gap_position == 7) {
				move = true;
			}
			break;
		case 4:
			if (gap_position == 0 || gap_position == 5 || gap_position == 8) {
				move = true;
			}
			break;
		case 5:
			if (gap_position == 1 || gap_position == 4 || gap_position == 6 || gap_position == 9) {
				move = true;
			}
			break;
		case 6:
			if (gap_position == 2 || gap_position == 5 || gap_position == 7 || gap_position == 10) {
				move = true;
			}
			break;
		case 7:
			if (gap_position == 3 || gap_position == 6 || gap_position == 11) {
				move = true;
			}
			break;
		case 8:
			if (gap_position == 4 || gap_position == 9 || gap_position == 12) {
				move = true;
			}
			break;
		case 9:
			if (gap_position == 5 || gap_position == 8 || gap_position == 10 || gap_position == 13) {
				move = true;
			}
			break;
		case 10:
			if (gap_position == 6 || gap_position == 9 || gap_position == 11 || gap_position == 14) {
				move = true;
			}
			break;
		case 11:
			if (gap_position == 7 || gap_position == 10 || gap_position == 15) {
				move = true;
			}
			break;
		case 12:
			if (gap_position == 8 || gap_position == 13) {
				move = true;
			}
			break;
		case 13:
			if (gap_position == 9 || gap_position == 12 || gap_position == 14) {
				move = true;
			}
			break;
		case 14:
			if (gap_position == 10 || gap_position == 13 || gap_position == 15) {
				move = true;
			}
			break;
		case 15:
			if (gap_position == 11 || gap_position == 14) {
				move = true;
			}
			break;
	}
	return move;
}

double_move_allowed = function(tile_position) {
	var move = false;
	switch(tile_position) {
		case 0:
			if (gap_position == 2 || gap_position == 8) {
				move = true;
			}
			break;
		case 1:
			if (gap_position == 3 || gap_position == 9) {
				move = true;
			}
			break;
		case 2:
			if (gap_position == 0 || gap_position == 10) {
				move = true;
			}
			break;
		case 3:
			if (gap_position == 1 || gap_position == 11) {
				move = true;
			}
			break;
		case 4:
			if (gap_position == 6 || gap_position == 12) {
				move = true;
			}
			break;
		case 5:
			if (gap_position == 7 || gap_position == 13) {
				move = true;
			}
			break;
		case 6:
			if (gap_position == 4 || gap_position == 14) {
				move = true;
			}
			break;
		case 7:
			if (gap_position == 5 || gap_position == 15) {
				move = true;
			}
			break;
		case 8:
			if (gap_position == 0 || gap_position == 10) {
				move = true;
			}
			break;
		case 9:
			if (gap_position == 1 || gap_position == 11) {
				move = true;
			}
			break;
		case 10:
			if (gap_position == 2 || gap_position == 8) {
				move = true;
			}
			break;
		case 11:
			if (gap_position == 9 || gap_position == 3) {
				move = true;
			}
			break;
		case 12:
			if (gap_position == 4 || gap_position == 14) {
				move = true;
			}
			break;
		case 13:
			if (gap_position == 5 || gap_position == 15) {
				move = true;
			}
			break;
		case 14:
			if (gap_position == 6 || gap_position == 12) {
				move = true;
			}
			break;
		case 15:
			if (gap_position == 7 || gap_position == 13) {
				move = true;
			}
			break;
	}
	return move;
}

triple_move_allowed = function(tile_position) {
	var move = false;
	switch(tile_position) {
		case 0:
			if (gap_position == 3 || gap_position == 12) {
				move = true;
			}
			break;
		case 1:
			if (gap_position == 13) {
				move = true;
			}
			break;
		case 2:
			if (gap_position == 14) {
				move = true;
			}
			break;
		case 3:
			if (gap_position = 0 || gap_position == 15) {
				move = true;
			}
			break;
		case 4:
			if (gap_position == 7) {
				move = true;
			}
			break;
		case 7:
			if (gap_position == 4) {
				move = true;
			}
			break;
		case 8:
			if (gap_position == 11) {
				move = true;
			}
			break;
		case 11:
			if (gap_position == 8) {
				move = true;
			}
			break;
		case 12:
			if (gap_position == 0 || gap_position == 15) {
				move = true;
			}
			break;
		case 13:
			if (gap_position == 1) {
				move = true;
			}
			break;
		case 14:
			if (gap_position == 2) {
				move = true;
			}
			break;
		case 15:
			if (gap_position == 3 || gap_position == 12) {
				move = true;
			}
			break;
	}
	return move;
}

scramble = function() {
	scrambling = true;
	for (i=0;i<10000; i++) {
		var random_position = get_random_int(0,15);
		if (random_position != gap_position) {
			move_tile(random_position);
		}
	}
	scrambling = false;
}

get_random_int= function(min, max) {
	min = Math.ceil(min);
	max = Math.floor(max);
	return Math.floor(Math.random() * (max - min)) + min;
}

end_game_check = function() {
	var loop = true;
	var index = 0;
	var win = false;
	
	while (loop) {
		if (index == 16) {
			loop = false;
			win = true;
		}
		
		else if (board[index].number == index) {
			index += 1;
		}
		
		else {
			loop = false;
		}
	}
	
	if (win) {
		alert("Wait for it...");
		gap_position = -1;
		$.ajax({
            url: '/fifteen',
            data: JSON.stringify(num_moves),
            type: 'POST',
			contentType: 'application/json;charset=UTF-8',
            success: function(response) {
				console.log(response)
				$('#scores tr').remove();
				$('#p_scores tr').remove();
				for (table in response){
				var lst = []
				for (var score in response[table]) {
    			lst.push([score, response[table][score]]);
				}
				lst.sort(function(a, b){
					return b[1] - a[1];
				});
				var id = (table == "global_top" ? "scores" : "p_scores")
				var table = document.getElementById(id);
				console.log(lst[0]);
				
				if (id == "p_scores"){
					if (lst[0][1] == "Anonymous user"){
					var row = table.insertRow(0);
    				var cell1 = row.insertCell(0);
					cell1.innerHTML = "Anonymous user"
					} else {
						for (var i = 0; i < lst.length; i++) {
    					var row = table.insertRow(0);
    					var cell1 = row.insertCell(0);
    					cell1.innerHTML = lst[i][1];
				}
						}
				} else {
			for (var i = 0; i < lst.length; i++) {
    			var row = table.insertRow(0);
    			var cell1 = row.insertCell(0);
    			var cell2 = row.insertCell(1);
    			cell1.innerHTML = lst[i][0];
    			cell2.innerHTML = lst[i][1];
				}
				}
				}
            },
            error: function(error) {
                console.log(error);
            }
        });
	}
}
