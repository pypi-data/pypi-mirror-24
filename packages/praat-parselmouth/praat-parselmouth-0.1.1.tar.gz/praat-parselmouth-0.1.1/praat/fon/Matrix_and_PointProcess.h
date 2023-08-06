/* Matrix_and_PointProcess.h
 *
 * Copyright (C) 1992-2011,2015 Paul Boersma
 *
 * This code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This code is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this work. If not, see <http://www.gnu.org/licenses/>.
 */

#include "Matrix.h"
#include "PointProcess.h"

autoMatrix PointProcess_to_Matrix (PointProcess me);
/*
	Function:
		create a Matrix from a PointProcess.
	Postconditions:
		thy xmin == 1;
		thy xmax == my numberOfEvents;
		thy nx == my numberOfEvents;
		thy dx == 1;
		thy x1 == 1;
		thy ymin ymax ny dy y1 == 1;
		for (ievent in 1..my numberOfEvents) thy z [1] [ievent] == my event [ievent];
*/

autoPointProcess Matrix_to_PointProcess (Matrix me);
/*
	Function:
		create a PointProcess from a Matrix.
	Postconditions:
		thy maximumNumberOfEvents == my nx;
		thy numberOfEvents == my nx;
		for (ix in 1..my nx) thy event [ix] == my z [1] [ix];
*/

/* End of file Matrix_and_PointProcess.h */
