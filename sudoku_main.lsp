

; sudoku map : (3x3x3x3) -> notation (x,y)*(x',y') s.t. \forall x,y,x',y' \in S s.t. S = {w|0<=w<=2}

; takes board(2d plane): 4D array (3x3x3x3)
;				try(point): (x,y,z,w,n) -> (x,y)*(z,w) = n
;				misc(list): contains general info includes
;										(# of failed_ans, # of turn, list of answer)
;										(list of answer - stack of point(x,y,z,f)
(defun solve (board ans misc)
	(let* ((x (first ans))
				 (y (second ans))
				 (z (third ans))
				 (w (fourth ans))
				 (n (fifth ans))
				 (failed_ans (first ans))
				 (turn (second ans))
				 (ans_list (third ans))
				 )
		(cond (((is_wrong_horizontal_num x y z w) (failed_solve board misc))
					 ((is_wrong_vertical_num x y z w) (failed_solve board misc))
					 ((is_wrong_square_num x y z w) (failed_solve board 
