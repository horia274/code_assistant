import javax.swing.tree.TreeNode;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.NoSuchElementException;
import java.util.Scanner;
import java.util.Stack;

class BinarySearchTree {

    // Folosesc design Pattern SingleTon pentru arbore
    private static BinarySearchTree binarySearchTree = null;
    private TreeNode root;

    private BinarySearchTree() {}

    public static BinarySearchTree getInstance(){
        if (binarySearchTree == null)
            binarySearchTree = new BinarySearchTree();
        return binarySearchTree;
    }
    static class TreeNode {
        String key, next;
        TreeNode left, right;

        public String getKey() {
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
    class PreorderIterator {
        Stack<TreeNode> nodes = new Stack<>();

        public PreorderIterator() {
            if (root != null) {
                nodes.push(root);
            }
        }

        public TreeNode next() {
            if (!hasNext()) {
                throw new NoSuchElementException("No more elements");
            }
            TreeNode node = nodes.pop();
            if (node.right != null)
                nodes.push(node.right);
            if (node.left != null)
                nodes.push(node.left);
            return node;
        }

        public boolean hasNext() {
            return !nodes.isEmpty();
        }
    }

    public PreorderIterator getPreorderIterator() {
        return new PreorderIterator();
    }

    public void insert(String value) {
        root = insertRec(root, value);
    }

    private TreeNode insertRec(TreeNode root, String value) {
        if (root == null) {
            root = new TreeNode(value);
            return root;
        }
        if (value.compareTo(root.key) < 0)
            root.left = insertRec(root.left, value);
        else if (value.compareTo(root.key) > 0)
            root.right = insertRec(root.right, value);
        return root;
    }
}

class BinarySearchTreeFactory {
    public static BinarySearchTree readTree(Scanner scanner) throws UnexpectedInputException {
        BinarySearchTree tree = BinarySearchTree.getInstance();
        while (scanner.hasNext()) {
            String value = scanner.next();
            if (value == null || value.trim().isEmpty()) {
                throw new UnexpectedInputException();
            }
            tree.insert(value);
        }
        return tree;
    }
}

class UnexpectedInputException extends Exception {
    public UnexpectedInputException() {
        super("Unexpected input format");
    }
}

public class Main {

    public static void main(String[] args) {
        try {
            Scanner inpFile = new Scanner(new File("in3.txt"));
            BinarySearchTree t = BinarySearchTreeFactory.readTree(inpFile);
            BinarySearchTree.PreorderIterator it = t.getPreorderIterator();
            while (it.hasNext()) {
                BinarySearchTree.TreeNode node = it.next();
                System.out.println(node.getKey());
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