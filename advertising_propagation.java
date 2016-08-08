import java.util.*;
import java.io.*;
import java.math.*;

class Solution {

    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);

        int n = in.nextInt();           // the number of links

        Nodes nodes = new Nodes(n);     // will contains all tree
        ArrayList<int[]> tempLinks = new ArrayList<int[]>();    // will contains all the links we cant put for the moment

        for (int i = 0; i < n; i++) {
            int xi = in.nextInt();      // the ID of a Node
            int yi = in.nextInt();      // the ID of a Node
            nodes.createLink(xi, yi);
        }

        // System.err.println(nodes);

        System.out.println(minPropagation(nodes));
    }

    private static int minPropagation(Nodes nodes) {
        int minSteps = 1;
        while(nodes.hasLeaves()) {                                      // while there are leaves to cut
            for(int i = 0; i < nodes.references.length; i++) {          // go throught the Nodes
                if(nodes.references[i] != null) {                       // if the node has not been already cut
                    if(nodes.references[i].linkedNodes.size() == 1) {   // 1 link = a leave, so cut it
                        System.err.println("cut : " + nodes.references[i].value);
                        nodes.cutLeave(i);
                    }
                }
            }
            minSteps++;
        }
        return minSteps;
    }

}

// represent a node in the tree
class Node {

    public int value;                   // node number
    public ArrayList<Node> linkedNodes;  // nodes linked to this node

    /**
     * Constructor with the node number
     */
    public Node(int value) {
        this.value = value;
        this.linkedNodes = new ArrayList<Node>();
    }

    /**
     * Return String which describes a Node
     */
    public String toString() {
        String str = new String("--------------------------------\n");
        str += "Value : " + this.value + "\n";
        str += "Links : ";
        for(int i = 0; i < this.linkedNodes.size(); i++) {
            str += this.linkedNodes.get(i).value + " ";
        }
        str += "\n";
        return str;
    }

}

// represent all the Node of the tree
class Nodes {

    public Node[] references;                   // will contains all the Node of the tree

    /**
     * Constructor with the number of relations
     */
    public Nodes(int nbRel) {
        nbRel++;                                // n relations, so n+1 Node
        this.references = new Node[nbRel];
        this.initReferences(nbRel);
    }

    /**
     * return true if the number of node is > 1
     */
    public boolean hasLeaves() {
        int countNodes = 0;
        for(int i = 0; i < this.references.length; i++) {
            if(this.references[i] != null) {
                countNodes++;
            }
        }
        return countNodes > 1 ? true : false;
    }

    /**
     * cut a node from the tree
     */
    public void cutLeave(int index) {
        // first, remove it from the linkedNodes of the node connected with it
        Node connected = this.references[index].linkedNodes.get(0);
        //System.err.println(connected.linkedNodes.get(0));
        for(int i = 0; i < connected.linkedNodes.size(); i++) {
            if(connected.linkedNodes.get(i) != null && this.references[i] != null) {
                if(connected.linkedNodes.get(i).value == this.references[i].value) {
                    connected.linkedNodes.remove(i);
                    break;
                }
            }
        }
        // then, remove it from the references
        this.references[index] = null;
    }

    /**
     * Search the Node with the value or create a new Node if does'nt exists. Return the Node.
     */
    public Node getReference(int value) {
        // seach the Node
        int i = 0;
        while((this.references[i] != null) && (i < this.references.length)) {
            if(this.references[i].value == value) {
                return this.references[i];
            }
            i++;
        }
        // if the Node does'nt exists, create it
        return newNode(value, i);
    }

    /**
     * get the references of the 2 Node and make the link
     */
    public void createLink(int parentValue, int childValue) {
        Node parent = this.getReference(parentValue);
        Node child = this.getReference(childValue);
        parent.linkedNodes.add(child);
        child.linkedNodes.add(parent);
    }

    /**
     * create a new Node in references[] and return the Node
     */
    public Node newNode(int value, int index) {
        Node newNode = new Node(value);
        this.references[index] = newNode;
        return this.references[index];
    }

    /**
     * Return String which describes a Nodes
     */
    public String toString() {
        String str = new String("");
        for(int i = 0; i < this.references.length; i++) {
            str += this.references[i];
        }
        return str;
    }

    /**
     * init the references
     */
    private void initReferences(int nbNodes) {
        for(int i = 0; i < nbNodes; i++) {
            this.references[i] = null;
        }
    }

}
