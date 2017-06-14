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
 * TrieCompressor uses a trie to determine
 * unique points of words. It is good
 * for compressing text with many 
 * long words.
 *
 * This usually performs very poorly.
 *
 *
 * How to use this utility:
 *
 * {@code java TrieCompressor <input_file>}
 *
 * @author Ming Li
 *
 */

public class TrieCompressor {
    private Trie trie;
    private String inputFile;

    /**
     * The constructor takes text from a file
     * and forms a trie with words from the text.
     * @param inputFile the name of the file
     */
    public TrieCompressor(String inputFile) {
        trie = new Trie();
        this.inputFile = inputFile;
        
        try {
            Scanner scanner = new Scanner(new File(inputFile));
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] tokens = line.split("\\b");
                for (String token : tokens) {
                    trie.insert(token);
                }
            }
            scanner.close();
        } catch (IOException e) {
            System.err.println(inputFile + " not found.");
        }
    }

    /**
     * This method writes the compressed contents of `inputFile`
     * to `outputFile`.
     * @param outputFile the name of the output file
     */
    private void compressToFile(String outputFile) {
        try {
            Scanner scanner = new Scanner(new File(inputFile));
            PrintWriter output = new PrintWriter(outputFile);
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] words = line.split("\\b");
                for (String word : words) {
                    String compressed = compress(word);
                    output.print(compressed);
                }
                output.println();
            }
            scanner.close();
            output.close();
        } catch (IOException e) {
            System.err.println(outputFile + " not found.");
        }
    }


    private String compress(String s) {
        // assert s in lexicon
        for (int i = 0; i < s.length(); i++) {
            String prefix = s.substring(0, i);
            List<String> completed = trie.getByPrefix(prefix);
            if (completed.size() == 1) {
                return prefix;
            }
        }
        return s;
    }

    public void serialize(String outputFile) {
        try {
            FileOutputStream fileOut = new FileOutputStream(outputFile);
            ObjectOutputStream objOut = new ObjectOutputStream(fileOut);
            objOut.writeObject(trie);
            objOut.close();
            fileOut.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            throw new IllegalArgumentException("provide <input_file>");
        }
        String[] tokens = args[0].split("\\.(?=[^\\.]+$)");
        TrieCompressor tc = new TrieCompressor(args[0]);
        System.out.println("Compressing " + args[0] + " to " + tokens[0] + ".short");
        tc.compressToFile(tokens[0] + ".short");
        System.out.println("Serializing trie to " + tokens[0] + ".trie");
        tc.serialize(tokens[0] + ".trie");

    }
}
