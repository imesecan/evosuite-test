/**
    @author Benjamin Livshits <livshits@cs.stanford.edu>
    $Id: Sanitizers1.java,v 1.9 2006/04/21 17:14:27 livshits Exp $
 */
package securibench.micro.sanitizers;

import java.util.Scanner;
import java.io.IOException;
import java.io.PrintWriter;
import com.dependence.Dependence;
import securibench.micro.MicroTestCase;
import securibench.micro.BasicTestCase;

/**
 *  @servlet description="simple sanitization check"
 *  @servlet vuln_count = "1"
 *  */
public class Sanitizers1 extends BasicTestCase implements MicroTestCase
{
    private static final String FIELD_NAME = "name";

    protected static long calculate(int x, int y)
    {
        long res = Dependence.SumCubes(x, y);

        return res;
    }

    public String getDescription() {
        return "simple sanitization check";
    }

    public int getVulnerabilityCount() {
        return 1;
    }

    public static void main(String args[])
    {
        Scanner inp = new Scanner(System.in);
        int v1 = inp.nextInt();
        int v2 = inp.nextInt();

        long res = calculate(v1, v2);

        System.out.println(res);
    }
}
