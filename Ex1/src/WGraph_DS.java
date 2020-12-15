package ex1.src;


import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Set;

public class WGraph_DS implements weighted_graph , Serializable
{
    private int modeCounter;
    private int edgeCounter;
    private HashMap<Integer, node_info> graph;


    /**
     * A constructor to create a new graph.
     */
    public WGraph_DS()
    {
        modeCounter = 0;
        edgeCounter = 0;
        graph = new HashMap<Integer, node_info>();
    }

    /**
     * A constructor to create a deep copy of the given graph.
     * Runtime: O(n)
     * @param g
     */
    public WGraph_DS(weighted_graph g)
    {
        this.modeCounter = g.getMC();
        this.edgeCounter = g.edgeSize();
        graph = new HashMap<Integer, node_info>();
        for (node_info node : g.getV())
        {
            graph.put(node.getKey(), new NodeData(node));
        }
    }



    /**
     * return the node_info by the node_id.
     * @param key - the node_id
     * @return the node_info by the node_id, null if none.
     */
    @Override
    public node_info getNode(int key)
    {
        return graph.get(key);
    }


    /**
     * return true iff (if and only if) there is an edge between node1 and node2
     * Runtime: O(1).
     * @param node1
     * @param node2
     * @return
     */
    @Override
    public boolean hasEdge(int node1, int node2)
    {
        if (graph.get(node1) != null && graph.get(node2) != null && node1 != node2)
        {
            NodeData firstNode = (NodeData) graph.get(node1);
            return firstNode.hasNi(node2);
        }
        return false;
    }

    /**
     * return the weight of the edge (node1, node2).
     * In case there is no such edge - returns -1
     * Runtime: O(1).
     * @param node1
     * @param node2
     * @return
     */
    @Override
    public double getEdge(int node1, int node2)
    {
        if (graph.containsKey(node1) && graph.containsKey(node2))
        {
            if (node1 == node2) return 0; // boaz wrote the distance from node to itself is 0.
            NodeData firstNode = (NodeData) (graph.get(node1));
            if (firstNode.hasNi(node2))
                return firstNode.neighbourWeight.get(node2);
        }
        return -1;
    }

    /**
     * add a new node to the graph with the given key.
     * Note: if there is already a node with such a key -> no action is performed.
     * Runtime: O(1).
     * @param key
     */
    @Override
    public void addNode(int key)
    {
        if (!graph.containsKey(key))
        {
            graph.put(key, new NodeData(key));
            modeCounter++;
        }
    }

    /**
     * Connect an edge between node1 and node2, with an edge with weight >=0.
     * Note: if the edge node1-node2 already exists - the method simply updates the weight of the edge.
     * Runtime: O(1).
     * @param node1
     * @param node2
     * @param w
     */
    @Override
    public void connect(int node1, int node2, double w)
    {
        if (node1 != node2 && graph.containsKey(node1) && graph.containsKey(node2) && w >= 0)
        {
            if (!hasEdge(node1, node2))
            {
                NodeData firstNode = (NodeData) (graph.get(node1));
                NodeData secondNode = (NodeData) (graph.get(node2));
                firstNode.addNi(secondNode, w);
                secondNode.addNi(firstNode, w);
                edgeCounter++;
                modeCounter++;
            }
            else
            {
                NodeData firstNode = (NodeData) (graph.get(node1));
                NodeData secondNode = (NodeData) (graph.get(node2));
                firstNode.addNi(secondNode, w);
                secondNode.addNi(firstNode, w);
                modeCounter++;
            }
        }
    }

    /**
     * This method returns a pointer (shallow copy) for a
     * Collection representing all the nodes in the graph.
     * Runtime: O(1).
     * @return Collection<node_info>
     */
    @Override
    public Collection<node_info> getV()
    {
        if (graph == null) return null;
        return graph.values();
    }

    /**
     * This method returns a Collection containing all the
     * nodes connected to node_id
     * Runtime: O(k), k - being the degree of node_id.
     * @param node_id
     * @return Collection<node_info>
     */
    @Override
    public Collection<node_info> getV(int node_id)
    {
        if (graph.get(node_id) == null)
            return null;
        return getNi(node_id);
    }

    /**
     * Returns the collection of neighbours of this node
     * Runtime: O(k). where k is the number of neighbours this node has.
     * @return Collection <node_info> neighbours.
     */
    private Collection<node_info> getNi(int node_id)
    {
        ArrayList<node_info> givenNodeNeighbours = new ArrayList<>();
        if (graph.containsKey(node_id))
        {
            NodeData givenNode = (NodeData) (graph.get(node_id));
            Set<Integer> neighboursKeys = givenNode.neighbourWeight.keySet();
            for (int i : neighboursKeys)
            {
                givenNodeNeighbours.add(graph.get(i));
            }
        }
        return givenNodeNeighbours;
    }

    /**
     * Delete the node (with the given ID) from the graph -
     * and removes all edges which starts or ends at this node.
     * Runtime: O(n), |V|=n, as all the edges should be removed.
     * @param key
     * @return the data of the removed node (null if none).
     */
    @Override
    public node_info removeNode(int key)
    {
        if (graph.get(key) != null)
        {
            ArrayList<node_info> deletedNodeNeighbours = new ArrayList<>((ArrayList<node_info>) (getNi(key)));
            for (int i = 0; i < deletedNodeNeighbours.size(); i++)
            {
                removeEdge(key, deletedNodeNeighbours.get(i).getKey());
            }
            modeCounter++;
            return graph.remove(key);
        }
        else
            return null;
    }

    /**
     * Deletes the edge from the graph,
     * Runtime: O(1).
     * @param node1
     * @param node2
     */
    @Override
    public void removeEdge(int node1, int node2)
    {
        if (graph.get(node1) != null && graph.get(node2) != null && hasEdge(node1, node2))
        {
            NodeData firstNode = (NodeData) (graph.get(node1));
            firstNode.neighbourWeight.remove(node2);
            NodeData secondNode = (NodeData) (graph.get(node2));
            secondNode.neighbourWeight.remove(node1);
            modeCounter++;
            edgeCounter--;
        }
    }

    /**
     * return the number of vertices (nodes) in the graph.
     * Runtime: O(1).
     * @return
     */
    @Override
    public int nodeSize()
    {
        return graph.size();
    }


    /**
     * return the number of edges (undirectional graph).
     * Runtime: O(1).
     * @return
     */
    @Override
    public int edgeSize()
    {
        return edgeCounter;
    }


    /**
     * return the Mode Count - for testing changes in the graph.
     * Any change in the inner state of the graph should cause an increment in the ModeCount
     * Runtime: O(1).
     * @return
     */
    @Override
    public int getMC()
    {
        return modeCounter;
    }

    @Override
    public String toString()
    {
        return "WGraph_DS {" +
                ", edgeCounter = " + edgeCounter +
                ", graph = " + graph +
                '}';
    }


    @Override
    public boolean equals(Object obj)
    {
        if (obj.getClass() == this.getClass() )
            return this.toString().equals(obj.toString());
        else
            return false;
    }





    /**
     * This private class implements the interface node_info allowing to create nodes, get and set information (such as
     * color, key, tag etc) in nodes on an undirectional and weighted graph.
     */
    private class NodeData implements node_info ,Serializable
    {
        private final int key;
        private String info;
        private double tag;
        private HashMap<Integer, Double> neighbourWeight; // neighbour node key and weight


        /**
         * A constructor to create new nodes
         */
        public NodeData(int key)
        {
            this.key = key;
            info = "not visited";
            tag = Double.POSITIVE_INFINITY;
            neighbourWeight = new HashMap<Integer, Double>();
        }

        /**
         * a deep copy constructor for node
         * @param node
         */
        public NodeData(node_info node)
        {
            NodeData other = (NodeData) node;
            this.key = node.getKey();
            info = node.getInfo();
            tag = node.getTag();
            neighbourWeight = new HashMap<Integer, Double>();
            for(int key : other.neighbourWeight.keySet() )
            {
                this.neighbourWeight.put(key,other.neighbourWeight.get(key));
            }
        }


        /**
         * Adds node_data t and the weight to this node collection of neighbours.
         * Runtime: O(1).
         * @param t
         */
        public void addNi(node_info t, double weight)
        {
            if (!t.equals(this))
            {
                neighbourWeight.put(t.getKey(), weight);
            }
        }


        /**
         * Returns true iff the key appears in this node's neighbour collection.
         * Else returns false.
         * Runtime: O(n).
         * @param key
         * @return
         */
        public boolean hasNi(int key)
        {
            if (neighbourWeight.containsKey(key))
                return true;
            return false;
        }


        /**
         * Remove the given node from this node's collection of neighbours.
         * Runtime: O(1)
         * @param node
         */
        public void removeNode(node_info node)
        {
            neighbourWeight.remove(node);
        }


        /**
         * Return the key (id) associated with this node.
         * Note: each node_data should have a unique key.
         * Runtime: O(1).
         * @return
         */
        @Override
        public int getKey()
        {
            return this.key;
        }


        /**
         * return the remark (meta data) associated with this node.
         * Runtime: O(1).
         * @return
         */
        @Override
        public String getInfo()
        {
            return this.info;
        }


        /**
         * Allows changing the remark (meta data) associated with this node.
         * Runtime: O(1).
         * @param s
         */
        @Override
        public void setInfo(String s)
        {
            this.info = s;
        }


        /**
         * Temporal data (aka distance, color, or state)
         * which can be used be algorithms
         * Runtime: O(1).
         * @return
         */
        @Override
        public double getTag()
        {
            return this.tag;
        }


        /**
         * Allow setting the "tag" value for temporal marking an node - common
         * practice for marking by algorithms.
         * Runtime: O(1).
         * @param t - the new value of the tag
         */
        @Override
        public void setTag(double t)
        {
            this.tag = t;
        }


        @Override
        public String toString()
        {
            return "NodeData {" +
                    " key = " + key +
                    ", info = '" + info + '\'' +
                    ", tag = " + tag +
                    ", neighbours = " + neighbourWeight.keySet() +
                    ", dist from neighbours = " + neighbourWeight.values()
                    +'}';
        }
    }
}
