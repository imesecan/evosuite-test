package com.dependence;

import java.util.Scanner;
import com.dependence.Dependence;

public class Main
{
	public static void main(String args[])
	{
		Scanner inp = new Scanner(System.in);
		int x = inp.nextInt();
		int y = inp.nextInt();
		long res = Dependence.SumCubes(x, y);
		System.out.println(res);
	}
}
