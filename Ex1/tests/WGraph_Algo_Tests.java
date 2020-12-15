package ex1.tests;

import ex1.src.WGraph_Algo;
import ex1.src.WGraph_DS;
import ex1.src.node_info;
import ex1.src.weighted_graph;
import org.junit.jupiter.api.*;

import java.util.ArrayList;
import java.util.Random;

import static org.junit.jupiter.api.Assertions.*;

public class WGraph_Algo_Tests
{
    private WGraph_Algo tester;
    private weighted_graph graph;

    @BeforeEach
    public void init()
    {
        tester = new WGraph_Algo();
        graph = new WGraph_DS();
        for (int i = 0; i < 10; i++)
        {
            graph.addNode(i);
        }
        graph.connect(0, 1, 5);   // 0 -> 1 w:5
        graph.connect(1, 2, 10);  // 1 -> 2 w:10
        graph.connect(9, 1, 7);   // 9 -> 1 w:7
        graph.connect(2, 3, 15);  // 2 -> 3 w:15
        graph.connect(3, 4, 20);  // 3 -> 4 w:20
        graph.connect(4, 5, 25);  // 4 -> 5 w:25
        graph.connect(5, 6, 30);  // 5 -> 6 w:30
        graph.connect(6, 7, 35);  // 6 -> 7 w:35
        graph.connect(7, 8, 40);  // 7 -> 8 w:40
        graph.connect(8, 9, 45);  // 8 -> 9 w:45
        graph.connect(5, 8, 2);   // 5 -> 8 w:2
        graph.connect(4, 7, 6);   // 4 -> 3 w:6
        graph.connect(6, 2, 17);  // 6 -> 2 w:17
        graph.connect(2, 8, 13);  // 2 -> 8 w:13
        tester.init(graph);
    }

    @Test
    public void successfulFileSave()
    {
        String fileName = "successful_file_save_test.txt";
        boolean didItWork = tester.save(fileName);
        assert didItWork;
    }

    @Test
    public void successfulFileLoad()
    {

        String fileName = "successful_file_save_test.txt";
        weighted_graph oldGraph = tester.copy();
        boolean didItWork = tester.load(fileName);
        if (oldGraph.equals(tester.getGraph()))
            assert didItWork;
        else
            fail();
    }

    @Test
    public void is_Saved_Graph_Identical_To_Loaded_Graph()
    {
        String fileName = "successful file save test.txt";
        tester.load(fileName);
        WGraph_DS loadedGraph = (WGraph_DS) tester.getGraph();
        assert loadedGraph.toString().equals(graph.toString()) : "loaded graph is " + loadedGraph.toString() +
                " and " + "graph is " + graph.toString();
    }

    @Test
    public void proper_Deep_Copy()
    {
        weighted_graph copyOfOrgGraph = tester.copy();
        copyOfOrgGraph.removeNode(0);
        assert !copyOfOrgGraph.equals(this) : "copy of graph contains: " + copyOfOrgGraph.getV() + ", original graph " +
                "contains: " + this.graph.getV();
    }

    @Test
    public void getGraph()
    {
        WGraph_DS secondGraph = new WGraph_DS();
        secondGraph.connect(0, 1, 5);
        secondGraph.connect(1, 2, 10);
        secondGraph.connect(2, 3, 15);
        tester.init(secondGraph);
        assert tester.getGraph() == secondGraph;
    }


    @Test
    public void valid_Is_Connected()
    {
        boolean expectedAns = true;
        boolean actualAns = tester.isConnected();
        assertTrue(expectedAns == actualAns);
    }

    @Test
    public void invalid_Is_Connected()
    {
        graph.removeEdge(0, 1);
        boolean expectedAns = false;
        boolean actualAns = tester.isConnected();
        assert actualAns == expectedAns;
    }


    @Test
    public void valid_Shortest_Path_Distance()
    {
        double expectedAns = 15;
        double actualAns = tester.shortestPathDist(0, 2);
        assert actualAns == expectedAns;
    }

    @Test
    public void invalid_Shortest_Path_Distance_Non_Existing_Node()
    {
        double expectedAns = -1;
        double actualAns = tester.shortestPathDist(0, 50);
        assert actualAns == expectedAns;
    }

    @Test
    public void invalid_Shortest_Path_Distance_Disconnected_Graph()
    {
        graph.removeEdge(0, 1);
        double expectedAns = -1;
        double actualAns = tester.shortestPathDist(1, 0);
        assert actualAns == expectedAns;
    }

    @Test
    public void invalid_Shortest_Path_Distance_Two_Non_Existing_Nodes()
    {
        double expectedAns = -1;
        double actualAns = tester.shortestPathDist(100, 50);
        assert actualAns == expectedAns;
    }

    @Test
    public void valid_Shortest_Path()
    {
        ArrayList<node_info> expectedList = new ArrayList<node_info>();
        expectedList.add(graph.getNode(0));
        expectedList.add(graph.getNode(1));
        expectedList.add(graph.getNode(2));
        expectedList.add(graph.getNode(3));
        expectedList.add(graph.getNode(4));
        expectedList.add(graph.getNode(7));
        ArrayList<node_info> actualList = (ArrayList<node_info>) (tester.shortestPath(0, 7));
        assert actualList.equals(expectedList);
    }

    @Test
    public void invalid_Shortest_Path_Disconnected_Graph()
    {
        graph.removeEdge(0, 1);
        ArrayList<node_info> actualList = (ArrayList<node_info>) (tester.shortestPath(0, 7));
        assertNull(actualList);
    }

    @Test
    public void invalid_Shortest_Path_One_Non_Existing_Node()
    {
        ArrayList<node_info> actualList = (ArrayList<node_info>) (tester.shortestPath(0, 500));
        assertNull(actualList);
    }

    @Test
    public void invalid_Shortest_Path_Two_Non_Existing_Node()
    {
        ArrayList<node_info> actualList = (ArrayList<node_info>) (tester.shortestPath(10000, 500));
        assertNull(actualList);
    }

    @Test
    // Using your code to create that graph.
    public void are_Million_Vertices_Connected_Properly()
    {
        weighted_graph hugeGraph = graphCreator(1000000, 10000000, 1);
        tester.init(hugeGraph);
        boolean actualAns = tester.isConnected();
        assert actualAns;
    }


    @Test
    // My test to create the graph only using your random function.
    public void are_Million_Vertices_Connected_Properly_V2()
    {
        int numOfNodes = 1_000_000;
        int numOfEdges = 10_000_000;
        int numOfConnectedEdges = 0;
        _rnd = new Random(1);
        weighted_graph hugeGraph = new WGraph_DS();
        tester.init(hugeGraph);
        hugeGraph.addNode(0);
        for (int i = 1; i < numOfNodes; i++)
        {
            hugeGraph.addNode(i);
            hugeGraph.connect(i - 1, i, nextRnd(0, numOfNodes));
            numOfConnectedEdges++;
        }
        while (hugeGraph.edgeSize() < numOfEdges - numOfConnectedEdges)
        {
            int node1 = nextRnd(0, numOfNodes);
            int node2 = nextRnd(0, numOfNodes);
            hugeGraph.connect(node1, node2, nextRnd(0, numOfNodes));
        }
        boolean actualAns = tester.isConnected();
        assert actualAns;
    }

    private static Random _rnd = null;

    public static weighted_graph graphCreator(int v_size, int e_size, int seed)
    {
        weighted_graph g = new WGraph_DS();
        _rnd = new Random(seed);
        for (int i = 0; i < v_size; i++)
        {
            g.addNode(i);
        }
        // Iterator<node_data> itr = V.iterator(); // Iterator is a more elegant and generic way, but KIS is more important
        while (g.edgeSize() < e_size)
        {
            int node1 = nextRnd(0, v_size);
            int node2 = nextRnd(0, v_size);
            if (node1 != node2)
                g.connect(node1, node2, nextRnd(0, v_size));
        }
        return g;
    }


    private static int nextRnd(int min, int max)
    {
        double v = nextRnd(0.0 + min, (double) max);
        int ans = (int) v;
        return ans;
    }

    private static double nextRnd(double min, double max)
    {
        double d = _rnd.nextDouble();
        double dx = max - min;
        double ans = d * dx + min;
        return ans;
    }

}
