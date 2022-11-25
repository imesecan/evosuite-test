package com.dependence;

import com.Point;

public class Dependence
{
	public static double distance(Point p1, Point p2)
	{
		int xdiff = p1.x - p2.x;
		int ydiff = p1.y - p2.y;

		return Math.sqrt(xdiff * xdiff + ydiff * ydiff);
	}
}
