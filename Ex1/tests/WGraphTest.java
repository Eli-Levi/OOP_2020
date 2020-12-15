package ex1.tests;


import ex1.src.WGraph_DS;
import ex1.src.node_info;
import org.junit.jupiter.api.*;

import java.util.ArrayList;

public class WGraphTest
{
    WGraph_DS graph;

    @BeforeEach
    public void init()
    {
        graph = new WGraph_DS();
        graph.addNode(0);
        graph.addNode(1);
        graph.addNode(2);
    }

    @Test
    public void proper_Graph_Init()
    {
        int actualMC = graph.getMC();
        int actualEdgeCounter = graph.edgeSize();
        int expectedMC = 3;
        int expectedEdgeCounter = 0;
        assert actualEdgeCounter == expectedEdgeCounter : "expected Edge Counter = " + expectedEdgeCounter
                + ", actual Edge Counter = " + actualEdgeCounter;
        assert actualMC == expectedMC : "expected Mode Counter = " + expectedMC
                + ", actual Mode Counter = " + actualMC;
    }

    @Test
    public void valid_Add_Node()
    {
        int actualNodeSize = graph.nodeSize();
        int expectedNodeSize = 3;
        assert actualNodeSize == expectedNodeSize;
    }


    @Test
    public void invalid_Get_Node()
    {
        node_info expectedNode = null;
        node_info actualNode = graph.getNode(7);
        assert expectedNode == actualNode;
    }


    @Test
    public void valid_MC()
    {
        graph.connect(0, 1, 10);
        graph.connect(1, 2, 20);
        graph.connect(2, 0, 30);
        int actualMC = graph.getMC();
        int expectedMC = 6;
        assert actualMC == expectedMC;
    }

    @Test
    public void valid_Edge_Counter()
    {
        graph.connect(0, 1, 10);
        graph.connect(1, 2, 20);
        graph.connect(2, 0, 30);
        int actualEdgeCounter = graph.edgeSize();
        int expectedEdgeCounter = 3;
        assert actualEdgeCounter == expectedEdgeCounter;
    }

    @Test
    public void valid_Node_Counter()
    {
        graph.addNode(3);
        graph.addNode(4);
        graph.addNode(5);
        int actualNodeSize = graph.nodeSize();
        int expectedNodeSize = 6;
        assert actualNodeSize == expectedNodeSize;
    }

    @Test
    public void valid_Has_Edge()
    {
        graph.connect(1, 2, 20);
        boolean actualRes = graph.hasEdge(1, 2);
        assert actualRes;
    }

    @Test
    public void has_Edge_To_One_Non_Existing_Node()
    {
        graph.connect(1, 10, 100);
        boolean actualRes = graph.hasEdge(1, 10);
        assert !actualRes;
    }

    @Test
    public void has_Edge_Two_Non_Existing_Nodes()
    {
        graph.connect(20, 10, 100);
        boolean actualRes = graph.hasEdge(1, 10);
        assert !actualRes;
    }

    @Test
    public void valid_Get_Edge()
    {
        graph.connect(1, 2, 10);
        double actualWeight = graph.getEdge(1, 2);
        double expectedWeight = 10;
        assert actualWeight == expectedWeight;
    }

    @Test
    public void invalid_Get_Edge_To_One_Non_Existing_Node()
    {
        graph.connect(1, 10, 100);
        double actualWeight = graph.getEdge(1, 10);
        double expectedWeight = -1;
        assert actualWeight == expectedWeight;
    }

    @Test
    public void valid_Get_All_Graph_Nodes()
    {
        graph.connect(0, 1, 10);
        graph.connect(0, 2, 20);
        ArrayList<node_info> actual_Neighbours_Of_Given_Node = (ArrayList<node_info>) (graph.getV(0));
        ArrayList<node_info> expected_Neighbours_Of_Given_Node = new ArrayList<node_info>();
        expected_Neighbours_Of_Given_Node.add(graph.getNode(1));
        expected_Neighbours_Of_Given_Node.add(graph.getNode(2));
        assert actual_Neighbours_Of_Given_Node.equals(expected_Neighbours_Of_Given_Node);
    }

    @Test
    public void invalid_Get_All_Graph_Nodes()
    {
        graph.connect(0, 1, 10);
        graph.connect(0, 2, 20);
        ArrayList<node_info> actual_Neighbours_Of_Given_Node = (ArrayList<node_info>) (graph.getV(0));
        ArrayList<node_info> expected_Neighbours_Of_Given_Node = new ArrayList<node_info>();
        expected_Neighbours_Of_Given_Node.add(graph.getNode(1));
        assert !actual_Neighbours_Of_Given_Node.equals(expected_Neighbours_Of_Given_Node);
    }

    @Test
    public void valid_Remove_Existing_Node()
    {
        graph.connect(0, 1, 10);
        graph.connect(0, 2, 20);
        node_info expectedNode = graph.getNode(0);
        node_info actualNode = graph.removeNode(0);
        ArrayList<node_info> actual_Neighbours_Of_Node_1 = (ArrayList<node_info>) (graph.getV(1));
        ArrayList<node_info> actual_Neighbours_Of_Node_2 = (ArrayList<node_info>) (graph.getV(2));
        ArrayList<node_info> expected_Neighbours_Of_Node_1 = new ArrayList<node_info>();
        ArrayList<node_info> expected_Neighbours_Of_Node_2 = new ArrayList<node_info>();
        assert actualNode.equals(expectedNode);
        assert actual_Neighbours_Of_Node_1.equals(expected_Neighbours_Of_Node_1);
        assert actual_Neighbours_Of_Node_2.equals(expected_Neighbours_Of_Node_2);
    }

    @Test
    public void remove_Non_Existing_Node()
    {
        node_info actualNode = graph.removeNode(10);
        node_info expectedNode = null;
        assert actualNode == expectedNode;
    }

    @Test
    public void Are_Graphs_Equal()
    {
        WGraph_DS secondGraph = new WGraph_DS(graph);
        System.out.println(graph);
        secondGraph.connect(1, 2, 10);
        secondGraph.removeEdge(1, 2);
        System.out.println(secondGraph);
        assert secondGraph.equals(graph);
    }

    @Test
    public void valid_Specific_Node_Neighbours()
    {
        graph.connect(0, 1, 12);
        graph.connect(1, 2, 10);
        ArrayList<node_info> actualNeighbours = new ArrayList<>();
        actualNeighbours = (ArrayList<node_info>) graph.getV(1);
        ArrayList<node_info> expectedNeighbours = new ArrayList<>();
        expectedNeighbours.add(graph.getNode(0));
        expectedNeighbours.add(graph.getNode(2));
        assert actualNeighbours.size() == expectedNeighbours.size();
    }

}
