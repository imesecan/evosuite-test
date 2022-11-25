package com.dependence;

import java.util.Scanner;
import com.dependence.Dependence;
import com.Point;

public class Main
{
	public static void main(String args[])
	{
		Scanner inp = new Scanner(System.in);
		int x = inp.nextInt();
		int y = inp.nextInt();
		Point n1 = new Point(x, y);
		
		x = inp.nextInt();
		y = inp.nextInt();
		Point n2 = new Point(x, y);

		double res = Dependence.distance(n1, n2);
		
		System.out.println(res);
	}
}
