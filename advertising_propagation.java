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

        System.err.println(nodes);

        System.out.println("1");
    }
}

// represent a node in the tree
class Node {

    public int value;                   // node number
    public boolean visited;             // true if this node has been cut
    public ArrayList<Node> parents;     // parents nodes
    public ArrayList<Node> children;    // children nodes

    /**
     * Constructor with the node number
     */
    public Node(int value) {
        this.value = value;
        this.visited = false;
        this.parents = new ArrayList<Node>();
        this.children = new ArrayList<Node>();
    }

    /**
     * Return String which describes a Node
     */
    public String toString() {
        String str = new String("--------------------------------\n");
        str += "Value : " + this.value + "\n";
        str += "Parents : ";
        for(int i = 0; i < this.parents.size(); i++) {
            str += this.parents.get(i).value + " ";
        }
        str += "\nChildren : ";
        for(int i = 0; i < this.children.size(); i++) {
            str += this.children.get(i).value + " ";
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
     * create a new Node in references[] and return the Node
     */
    public Node newNode(int value, int index) {
        Node newNode = new Node(value);
        this.references[index] = newNode;
        return this.references[index];
    }

    /**
     * get the references of the 2 Node and make the link
     */
    public void createLink(int parentValue, int childValue) {
        Node parent = this.getReference(parentValue);
        Node child = this.getReference(childValue);
        parent.children.add(child);
        child.parents.add(parent);
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
