import java.util.List;
import java.util.Scanner;
import java.io.File;
import java.io.PrintWriter;
import java.io.IOException;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.io.FileInputStream;
import java.io.ObjectInputStream;

/**
 * TrieDecompressor uses a serialized 
 * trie and a compressed text file
 * to restore an original piece of text.
 *
 *
 * How to use this utility:
 *
 * {@code java TrieDecompressor <name.trie> <name.short>}
 *
 * @author Ming Li
 *
 */

public class TrieDecompressor {
    private Trie trie;

    public void deserialize(String trieFile) {
        try {
            FileInputStream fileIn = new FileInputStream(trieFile);
            ObjectInputStream objIn = new ObjectInputStream(fileIn);
            trie = (Trie) objIn.readObject();
            objIn.close();
            fileIn.close();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

    }

    public void decompressToFile(String shortFile, String outputFile) {
        try {
            Scanner scanner = new Scanner(new File(shortFile));
            PrintWriter output = new PrintWriter(outputFile);
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] words = line.split("\\b");
                for (String word : words) {
                    List<String> completes = trie.getByPrefix(word);
                    if (completes.size() == 1) {
                        output.print(completes.get(0));
                    } else {
                        output.print(word);
                    }
                }
                output.println();
            }
            scanner.close();
            output.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        if (args.length != 2)
            throw new IllegalArgumentException("provide .trie and .short files");

        String[] tokens = args[0].split("\\.(?=[^\\.]+$)");
        TrieDecompressor td = new TrieDecompressor();
        System.out.println("Deserializing " + args[0]);
        td.deserialize(args[0]);
        String decompressedFile = tokens[0] + "_dec.txt";
        System.out.println("Decompressing " + args[1] + " to " + decompressedFile);
        td.decompressToFile(args[1], decompressedFile);
    }
}
