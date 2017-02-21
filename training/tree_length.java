import java.util.*;
import java.io.*;
import java.math.*;

// used to pass boolean by reference to a function
class BoolRef {

    public boolean bool;

    public BoolRef() {
        this.bool = false;
    }

}

class Node {

    public int value;
    public ArrayList<Node> children = new ArrayList<Node>();

    public Node(int value) {
        this.value = value;
    }

    public String toString() {
        return "Node " + this.value;
    }

}

// contains all the nodes
class Nodes {

    Node[] references;

    public Nodes(int n) {
        this.references = new Node[n+1];
        for(int i = 0; i < n; i++) {
            references[i] = null;
        }
    }

    public Node newNode(int value) {
        int i = 0;
        while(references[i] != null) {
            i++;
        }
        references[i] = new Node(value);
        return references[i];
    }

    public Node getReference(int val) {
        int i = 0;
        while((references[i] != null)) {
            if(references[i].value == val) {
                return references[i];
            }
            i++;
        }
        return newNode(val);
    }

}

class Solution {

    public static Nodes nodes;  // nodes references (to avoid duplicates, use only the nodes in references)

    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);

        int n = in.nextInt();       // the number of relationships of influence

        nodes = new Nodes(n);                                   // will contains all the nodes references
        ArrayList<Node> roots = new ArrayList<Node>();          // the tree can have many start nodes

        ArrayList<int[]> tempLinks = new ArrayList<int[]>();    // when the 2 nodes doesn't exists in the tree, put them in this list

        // links
        for (int i = 0; i < n; i++) {
            int x = in.nextInt();
            int y = in.nextInt();
            // set first node
            if(i == 0) {
                roots.add(nodes.newNode(x));
            }

            // for each root, try to put the link
            int rootIndex = 0;
            boolean found = false;

            while(rootIndex < roots.size() && !found) {
                BoolRef inTree = new BoolRef();
                Node root = roots.get(rootIndex);

                isInTree(root, x, inTree);
                if(inTree.bool) { // then insert a child
                    addChild(root, x, y);
                    found = true;
                } else {
                    isInTree(root, y, inTree);
                    if((inTree.bool) && (root.value == y)) {   // then insert a parent to the current root
                        roots.set(rootIndex, addParent(root, x, y));
                        found = true;
                    } else if((inTree.bool)) {
                        System.err.println("root : " + root);
                        System.err.println("X : " + x + " / y : " + y);
                        roots.add(rootIndex, newRoot(x, y));
                        found = true;
                    }
                }
                rootIndex++;
            }

            // cant put the link in the tree for the moment
            if(!found) {
                tempLinks.add(new int[]{x, y});
            }
        }

        // tempLinks
        for(int i = 0; i < tempLinks.size(); i++) {

            int rootIndex = 0;
            boolean found = false;

            while(rootIndex < roots.size() && !found) {
                BoolRef inTree = new BoolRef();
                Node root = roots.get(rootIndex);

                int x = tempLinks.get(i)[0];
                int y = tempLinks.get(i)[1];

                isInTree(root, x, inTree);
                if(inTree.bool) {   // then insert a child
                    addChild(root, x, y);
                    found = true;
                } else {            // the insert a parent if of on the node if y is on three
                    isInTree(root, y, inTree);
                    if(inTree.bool && (root.value == y)) {
                        root = addParent(root, x, y);
                        found = true;
                    } else if((inTree.bool)) {
                        System.err.println("root : " + root);
                        System.err.println("X : " + x + " / y : " + y);
                        roots.add(rootIndex, newRoot(x, y));
                        found = true;
                    }
                }
                rootIndex++;
            }

        }

        // calculate height
        int maxHeigth = 0;
        for(int i = 0; i < roots.size(); i++) {
            int tempHeight = height(roots.get(i));
            maxHeigth = tempHeight > maxHeigth ? tempHeight : maxHeigth;
        }
        System.out.println(maxHeigth);
    }

    // FUNCTIONS

    /**
     * create a new Node with x as parent and y as child
     */
    public static Node newRoot(int x, int y) {
        Node newNode = nodes.newNode(x);
        (newNode.children).add(nodes.getReference(y));
        return newNode;
    }

    /**
     * return the height of the tree
     */
    public static int height(Node root) {

        System.err.println(root);

        ArrayList<ArrayList<Node>> stack = new ArrayList<ArrayList<Node>>();
        ArrayList<Node> firstStack = new ArrayList<Node>();
        firstStack.add(root);
        stack.add(firstStack);

        int stackSize = 0;
        // while there is node in the last level
        while(stack.get(stackSize).size() > 0) {
            // create a new level in the stack
            stack.add(new ArrayList<Node>());
            stackSize++;
            // for each Node in the last level, add children to the new level
            ArrayList<Node> lastLevel = stack.get(stackSize - 1);
            for(int i = 0; i < lastLevel.size(); i++) {
                for(int j = 0; j < (lastLevel.get(i)).children.size(); j++) {
                    stack.get(stackSize).add(((lastLevel.get(i)).children).get(j));
                    System.err.println("SIZE : " + stackSize + " -- add " + ((lastLevel.get(i)).children).get(j).value + " -- " + ((lastLevel.get(i)).children).get(j).children);
                }
            }
        }

        return stackSize;
    }

    /**
     * add a child in the tree (added is for recursive call)
     */
    public static void addChild(Node n, int parent, int child) {

        if(n.value == parent) {
            (n.children).add(nodes.getReference(child));
        } else {
            int i = 0;
            while((i < (n.children).size())) {
                addChild((n.children).get(i), parent, child);
                i++;
            }
        }

    }

    /**
     *  add a parent in the tree
     */
    public static Node addParent(Node n, int parent, int child) {

        Node newRoot = nodes.newNode(parent);
        (newRoot.children).add(n);

        return newRoot;

    }

    /**
     * look if a value is already in the tree
     */
    public static void isInTree(Node n, int value, BoolRef inTree) {

       if(n.value == value) {
           inTree.bool = true;
       } else {
           int i = 0;
           while(!inTree.bool && (i < (n.children).size())) {
               isInTree((n.children).get(i), value, inTree);
               i++;
           }
       }

    }
}
