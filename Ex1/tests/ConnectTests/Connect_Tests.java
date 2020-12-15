package ex1.tests.ConnectTests;

import ex1.src.WGraph_DS;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class Connect_Tests
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
    public void valid_Connect()
    {
        graph.connect(0,1,10);
        graph.connect(1,2,20);
        graph.connect(2,0,30);
        boolean zeroConnectToOne = graph.hasEdge(0,1);
        boolean oneConnectToTwo = graph.hasEdge(1,2);
        boolean twoConnectToZero = graph.hasEdge(2,0);
        assert zeroConnectToOne;
        assert oneConnectToTwo;
        assert twoConnectToZero;
    }

    @Test
    public void invalid_Connect_Same_Node()
    {
        graph.connect(1,1,20);
        int actualEdgeCounter = graph.edgeSize();
        int expectedEdgeCounter = 0;
        assert actualEdgeCounter == expectedEdgeCounter;
    }

    @Test
    public void invalid_Connect_Negative_Weight()
    {
        graph.connect(0,1,-8);
        boolean zeroConnectToOne = graph.hasEdge(0,1);
        assert !zeroConnectToOne;
    }

    @Test
    public void invalid_Connect_With_NonExisting_Node()
    {
        graph.connect(0,8,12);
        boolean actualBoolean = graph.hasEdge(0,8);
        assert !actualBoolean;
    }

    @Test
    public void connect_Updates_New_Weight()
    {
        graph.connect(1,2,10);
        graph.connect(1,2,50);
        double actualWeight = graph.getEdge(1,2);
        double expectedWeight = 50;
        assert actualWeight == expectedWeight;
    }
}
