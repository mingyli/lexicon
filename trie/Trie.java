import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;
import java.util.Arrays;
import java.util.Queue;
import java.util.LinkedList;
import java.io.Serializable;

public class Trie implements Serializable {
    class Node implements Serializable {
        Map<Character, Node> children;
        String str;
        private static final int serialVersionUID = 2;

        Node() {
            children = new HashMap<>();
            str = null;
        }

        Node child(char ch) {
            return children.get(ch);
        }

        void addChild(char ch) {
            children.put(ch, new Node());
        }

        @Override
        public String toString() {
            return toString(0);
        }

        private String toString(int indent) {
            String res = "";
            indent++;
            if (this.str != null) {
                char[] spaces = new char[indent];
                Arrays.fill(spaces, ' ');
                res = new String(spaces);
                res += str + "\n";
            }
            for (Node n : children.values()) {
                res += n.toString(indent);
            }
            return res;
        }
    }

    private Node sentinel;
    private static final int serialVersionUID = 0;

    public Trie() {
        this.sentinel = new Node();
    }

    public void insert(String s) {
        Node curr = sentinel;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (curr.child(ch) == null) {
                curr.addChild(ch);
            }
            curr = curr.child(ch);
        }
        curr.str = s;
    }
                
    public List<String> getByPrefix(String prefix) {
        List<String> list = new ArrayList<>();
        getByPrefix(prefix, list);
        return list;
    }

    private void getByPrefix(String prefix, List<String> list) {
        Node curr = sentinel;
        for (int i = 0; i < prefix.length(); i++) {
            char ch = prefix.charAt(i);
            if (curr.child(ch) == null) {
                return;
            }
            curr = curr.child(ch);
        }
        Queue<Node> q = new LinkedList<>();
        q.add(curr);
        while (!q.isEmpty()) {
            Node n = q.remove();
            if (n.str != null)
                list.add(n.str);
            for (Node c : n.children.values()) 
                q.add(c);
        }
    }

    @Override
    public String toString() {
        return sentinel.toString();
    }

    public static void main(String[] args) {
        Trie trie = new Trie();
        trie.insert("and");
        trie.insert("andy");
        trie.insert("bob");
        System.out.println(trie.getByPrefix("a"));
        System.out.println(trie.getByPrefix("b"));
        System.out.println(trie.getByPrefix(""));
        System.out.println(trie.getByPrefix("andy"));
        System.out.println(trie.getByPrefix("c"));
        System.out.println(trie);
    }

}
