package ex1.src;


import java.io.*;
import java.util.*;
import java.util.concurrent.LinkedBlockingQueue;

public class WGraph_Algo implements weighted_graph_algorithms
{

    private WGraph_DS currGraph;

    /**
     * Constructor to create a new graph and initializes it.
     */
    public WGraph_Algo()
    {
        init(new WGraph_DS());
    }

    /**
     * Init with graph g so this set of algorithms can operate on it.
     * Runtime: O(n)
     * @param g
     */
    public WGraph_Algo(weighted_graph g)
    {
        init(g);
    }

    /**
     * Init the graph on which this set of algorithms operates on.
     * Runtime: O(1)
     * @param g
     */
    @Override
    public void init(weighted_graph g)
    {
        if (g == null) throw new NullPointerException("The graph is null.");
        this.currGraph = (WGraph_DS) g;
    }

    /**
     * Return the underlying graph of which this class works.
     * Runtime: O(1)
     * @return
     */
    @Override
    public weighted_graph getGraph()
    {
        return this.currGraph;
    }

    /**
     * Compute a deep copy of this weighted graph.
     * Runtime: O(n)
     * @return
     */
    @Override
    public weighted_graph copy()
    {
        weighted_graph newGraph = new WGraph_DS(this.currGraph);
        return newGraph;
    }

    /**
     * Returns true if and only if (iff) there is a valid path from EVERY node to each
     * other node. NOTE: assume undirectional graph.
     * @return
     */
    @Override
    public boolean isConnected()
    {
        if (currGraph.nodeSize() == 0) return true;
        node_info node = currGraph.getV().iterator().next();
        return scoutGraph(node).size() == currGraph.nodeSize();
    }

    /**
     * returns the length of the shortest path between src to dest
     * Note: if no such path --> returns -1
     * @param src  - start node
     * @param dest - end (target) node
     * @return
     */
    @Override
    public double shortestPathDist(int src, int dest)
    {
        ArrayList<node_info> thePath = (ArrayList<node_info>) (shortestPath(src, dest));
        if (thePath == null) return -1;
        double shortestPathDistance = thePath.get(thePath.size() - 1).getTag();
        return shortestPathDistance;
    }


    /**
     * returns the the shortest path between src to dest - as an ordered List of nodes:
     * src--> n1-->n2-->...dest
     * see: https://en.wikipedia.org/wiki/Shortest_path_problem
     * Note if no such path --> returns null;
     * @param src  - start node
     * @param dest - end (target) node
     * @return
     */
    @Override
    public List<node_info> shortestPath(int src, int dest)
    {
        ArrayList<node_info> ans = dijkstra(currGraph.getNode(src), currGraph.getNode(dest));
        if (ans == null) return ans = null;
        return ans;
    }

    /**
     * Saves this weighted (undirected) graph to the given file name
     * @param file - the file name (may include a relative path).
     * @return true - iff the file was successfully saved
     */
    @Override
    public boolean save(String file)
    {
        try
        {
            FileOutputStream aFile = new FileOutputStream(file);
            ObjectOutputStream graphOutput = new ObjectOutputStream(aFile);
            graphOutput.writeObject(currGraph);
            graphOutput.flush();
            graphOutput.close();
        } catch (IOException e)
        {
            e.printStackTrace();
        }
        return true;
    }

    /**
     * This method load a graph to this graph algorithm.
     * if the file was successfully loaded - the underlying graph
     * of this class will be changed (to the loaded one), in case the
     * graph was not loaded the original graph should remain "as is".
     * @param file - file name
     * @return true - iff the graph was successfully loaded.
     */
    @Override
    public boolean load(String file)
    {
        try
        {
            FileInputStream incomingFile = new FileInputStream(file);
            ObjectInputStream aSavedGraph = new ObjectInputStream(incomingFile);
            currGraph = (WGraph_DS) (aSavedGraph.readObject());
            aSavedGraph.close();
        } catch (IOException | ClassNotFoundException e)
        {
            e.printStackTrace();
        }
        return true;
    }


    /**
     * This method encapsulates the 2 functions used to apply the Dijkstra, running them in order.
     * It receives a start node and end node, finds the connected nodes using the scoutGraph and
     * reconstructPath algorithms.
     * @param start
     * @param end
     * @return
     */
    private ArrayList<node_info> dijkstra(node_info start, node_info end)
    {
        if (start == null || end == null) return null;
        WGraph_DS graphBackup = (WGraph_DS) this.copy();
        node_info src = currGraph.getNode(start.getKey());
        node_info dest = currGraph.getNode(end.getKey());
        HashMap<Integer, node_info> parentList = scoutGraphStartAndEnd(start, end);
        ArrayList<node_info> thePath = reconstructPath(src, dest, parentList);
        currGraph = graphBackup;
        init(currGraph);
        return thePath;
    }


    /**
     * The first half of the dijkstra algorithm.
     * It receives a node to start the search and end node.
     * It stores it's key and a null node in a priority queue.
     * Then runs though the node's neighbours, if their key is in the map, skip.
     * else, store child key with his parent node.
     * Then return the map.
     * @param start
     * @return
     */
    private HashMap<Integer, node_info> scoutGraphStartAndEnd(node_info start, node_info end)
    {
        start.setTag(0);
        PriorityQueue<node_info> nodesInWait = new PriorityQueue<node_info>(Comparator.comparing(node_info::getTag));
        HashMap<Integer, node_info> parentList = new HashMap<Integer, node_info>();
        nodesInWait.add(start);
        while (!nodesInWait.isEmpty())
        {
            node_info currNode = nodesInWait.poll();
            if (!currNode.getInfo().equals("visited"))
            {
                currNode.setInfo("visited");
                if (currNode.equals(end)) return parentList;
            }
            for (node_info neighbourNode : currGraph.getV(currNode.getKey()))
            {
                if (!neighbourNode.getInfo().equals("visited"))
                {
                    if ((currGraph.getEdge(currNode.getKey(), neighbourNode.getKey()) + currNode.getTag()) < neighbourNode.getTag())
                    {
                        neighbourNode.setTag(currGraph.getEdge(currNode.getKey(), neighbourNode.getKey()) + currNode.getTag());
                        parentList.put(neighbourNode.getKey(), currNode);
                        nodesInWait.add(neighbourNode);
                    }
                }
            }
        }
        return parentList;
    }

    /**
     * It receives a node to start the search and stores it's key and a null node in a map.
     * Then runs though the node's neighbours, if their key is in the map, skip.
     * else, store child key with his parent node.
     * Then return the map.
     *
     * @param start
     * @return
     */
    private HashMap<Integer, node_info> scoutGraph(node_info start)
    {
        Queue<node_info> theQueue = new LinkedBlockingQueue<>();
        theQueue.add(start);
        HashMap<Integer, node_info> parentList = new HashMap<Integer, node_info>();
        parentList.put(start.getKey(), null);
        while (!theQueue.isEmpty())
        {
            node_info pullOut = theQueue.poll();
            Collection<node_info> neighbours = currGraph.getV(pullOut.getKey());
            for (node_info i : neighbours)
            {
                if (!parentList.containsKey(i.getKey()))
                {
                    theQueue.add(i);
                    parentList.put(i.getKey(), pullOut);
                }
            }
        }
        return parentList;
    }

    /**
     * The second half of the dijkstra algorithm.
     * It receives the map from the first half of the dijkstra algorithm, the start node and end node and uses them to
     * reconstructs the path, by starting at the end node and running through the map (every key will show who his
     * parent is) and storing the parent nodes in order.
     * At the end, reverse the order and you have the path from start to finish.
     *
     * @param start
     * @param end
     * @param parentList
     * @return
     */
    private ArrayList<node_info> reconstructPath(node_info start, node_info end, HashMap<Integer, node_info> parentList)
    {
        ArrayList<node_info> thePath = new ArrayList<node_info>();
        thePath.add(end);
        int i = end.getKey();
        while (parentList.get(i) != null)
        {
            thePath.add(parentList.get(i));
            i = parentList.get(i).getKey();
        }
        Collections.reverse(thePath);
        if (thePath.get(0).getKey() == start.getKey())
            return thePath;
        else
            return null;
    }

}
