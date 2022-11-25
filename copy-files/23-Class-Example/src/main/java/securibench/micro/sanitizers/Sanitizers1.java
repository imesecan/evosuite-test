/**
    @author Benjamin Livshits <livshits@cs.stanford.edu>
    $Id: Sanitizers1.java,v 1.9 2006/04/21 17:14:27 livshits Exp $
 */
package securibench.micro.sanitizers;

import com.dependence.Dependence;
import com.Point;
import securibench.micro.MicroTestCase;
import securibench.micro.BasicTestCase;

/**
 *  @servlet description="simple sanitization check"
 *  @servlet vuln_count = "1"
 *  */
public class Sanitizers1 extends BasicTestCase implements MicroTestCase
{
    protected static double calculate(Point p1, Point p2)
    {
        double res = Dependence.distance(p1, p2);

        return res;
    }

    public String getDescription() {
        return "simple sanitization check";
    }

    public int getVulnerabilityCount() {
        return 1;
    }
}
