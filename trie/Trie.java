import java.util.List;
import java.util.ArrayList;

public class Trie {
    public Node sentinel;

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
        sentinel.getByPrefix(prefix, list);
        return list;
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
    }

}
