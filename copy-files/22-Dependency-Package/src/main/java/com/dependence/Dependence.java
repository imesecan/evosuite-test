package com.dependence;

public class Dependence
{
	private static long Cube(int x)
	{
		return x * x * x;
	}

	public static long SumCubes(int x, int y)
	{
		long res = Cube(x) + Cube(y);

		return res;
	}
}
