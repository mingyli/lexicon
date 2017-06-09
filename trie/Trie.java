import java.util.List;
import java.util.ArrayList;

public class Trie {
    class Node {
        Node[] children;
        String str;

        Node() {
            children = new Node[256];
            str = null;
        }

        void getByPrefix(String prefix, List<String> list) {
            if (str != null) {
                list.add(str);
            }
            if (prefix.length() == 0) {
                for (char ch = 0; ch < 256; ch++) {
                    if (children[ch] != null)
                        children[ch].getByPrefix(prefix, list);
                }
            } else if (children[prefix.charAt(0)] != null) {
                children[prefix.charAt(0)].getByPrefix(prefix.substring(1), list);
            }
        }
    }

    Node sentinel;

    public Trie() {
        this.sentinel = new Node();
    }

    public void insert(String s) {
        Node curr = sentinel;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (curr.children[ch] == null) {
                curr.children[ch] = new Node();
            }
            curr = curr.children[ch];
        }
        curr.str = new String(s);
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
    }

}
