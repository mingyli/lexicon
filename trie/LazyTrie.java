import java.util.List;
import java.util.ArrayList;


/**
 * LazyTrie is a trie that inserts words lazily.
 * A newly inserted word is inserted only to the 
 * point where its uniqueness can be determined.
 * Words are pushed downward as needed to their 
 * unique locations.
 */
class LazyTrie extends Trie {

    @Override
    public void insert(String s) {
        Node curr = sentinel;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (curr.children[ch] == null) {
                curr.children[ch] = new Node();
                curr.children[ch].str = new String(s);
                return;
            }
            if (curr.children[ch].str != null) {
                // sink these strings 
        }
    }

}
