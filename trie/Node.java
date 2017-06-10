import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class Node {
    Map<Character, Node> children;
    String str;

    public Node() {
        children = new HashMap<>();
        str = null;
    }

    void getByPrefix(String prefix, List<String> list) {
        if (prefix.length() == 0) {
            if (str != null) {
                list.add(str);
            }
            for (char ch = 0; ch < 256; ch++) {
                if (child(ch) != null)
                    child(ch).getByPrefix(prefix, list);
            }
        } else if (child(prefix.charAt(0)) != null) {
            child(prefix.charAt(0)).getByPrefix(prefix.substring(1), list);
        }
    }

    Node child(char ch) {
        return children.get(ch);
    }

    void addChild(char ch) {
        children.put(ch, new Node());
    }
}

