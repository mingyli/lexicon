import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;

public class Trie {
    class Node {
        Map<Character, Node> children;
        String str;
        Set<String> complete; // memoize getByPrefix

        Node() {
            children = new HashMap<>();
            str = null;
            complete = new HashSet<>();
        }

        Node child(char ch) {
            return children.get(ch);
        }

        void addChild(char ch) {
            children.put(ch, new Node());
        }
    }

    private Node sentinel;

    public Trie() {
        this.sentinel = new Node();
    }

    public void insert(String s) {
        Node curr = sentinel;
        for (int i = 0; i < s.length(); i++) {
            curr.complete.add(s);
            char ch = s.charAt(i);
            if (curr.child(ch) == null) {
                curr.addChild(ch);
            }
            curr = curr.child(ch);
        }
        curr.str = s;
        curr.complete.add(s);
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
        list.addAll(curr.complete);
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
    }

}
