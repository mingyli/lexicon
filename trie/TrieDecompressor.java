import java.io.IOException;
import java.io.FileInputStream;
import java.io.ObjectInputStream;

public class TrieDecompressor {
    public static void main(String[] args) {
        if (args.length != 2)
            throw new IllegalArgumentException("provide .trie and .ser files");
        try {
            FileInputStream fileIn = new FileInputStream(args[1]);
            ObjectInputStream objIn = new ObjectInputStream(fileIn);
            Trie trie = (Trie) objIn.readObject();
            objIn.close();
            fileIn.close();
            System.out.println(trie);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
