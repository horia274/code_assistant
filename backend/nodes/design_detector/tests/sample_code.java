import javax.swing.tree.TreeNode;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.NoSuchElementException;
import java.util.Scanner;
import java.util.Stack;

class BinarySearchTree {

    // Folosesc design Pattern SingleTon pentru arbore
    private static BinarySearchTree binarySearchTree = null;
    private BinarySearchTree(){}
    public static BinarySearchTree getInstance(){
        if (binarySearchTree == null)
            binarySearchTree = new BinarySearchTree();
        return binarySearchTree;
    }
    static class TreeNode {
        String key, next;
        TreeNode left, right;
        TreeNode root;

        public String key() {
            return key;
        }

        public void setKey(String key) {
            this.key = key;
        }

        public String getNext() {
            return next;
        }

        public void setNext(String next) {
            this.next = next;
        }

        //Constructor pentru nod
        public TreeNode(String value) {
            this.key = value;
            left = right = null;
        }
    }
    class PreorderIterator extends TreeNode {
        String data;
        Stack<TreeNode> nodes = new Stack<>();
        PreorderIterator(String data) {
            this.data = data;
        }
        // Parcurgerea in preordine
        public void getPreorderIterator() {
            nodes.push(root);

            while(!nodes.isEmpty()){
                TreeNode node = nodes.pop();
                if(node.right != null)
                    nodes.push(node.right);
                if(node.left != null)
                    nodes.push(node.left);
            }
        }
        public boolean hasNext() {
            if (!nodes.isEmpty()) {
                return true;
            }
            return false;
        }
    }

}

class BinarySearchTreeFactory extends BinarySearchTree{
    public BinarySearchTreeFactory(){}
    public void readTree(Scanner scanner){
        BinarySearchTree binarySearchTree = new BinarySearchTree();
    }
}

class UnexpectedInputException extends Exception{}

public class Main {

    public static void main(String[] args) {
        try {
            Scanner inpFile = new Scanner(new File("in3.txt"));
            BinarySearchTree<?> t = BinarySearchTreeFactory.readTree(inpFile);
            BinarySearchTree.PreorderIterator it = t.getPreorderIterator();
            while (it.hasNext()) {
                TreeNode node = it.next();
                System.out.println(node.key);
            }
            it.next(); // one more next(), to trigger the NoSuchElement exception
        } catch (FileNotFoundException e) {
            System.out.println("eroare citire fisier"); // this will never happen on LambdaChecker
        } catch (UnexpectedInputException e) {
            System.out.println("Unexpected input: "+e);
        } catch (NoSuchElementException e) {
            System.out.println("Iterator exception: "+e.getMessage());
        }
    }
}